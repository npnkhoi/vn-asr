"""
Generates textgrid files based on audio's length and CSV transcription.
The textgrid file will get the same name as the audio file.

Usage: `python csv_to_textgrid audio.wav trans.csv`
Author: Khoi + prof Nanette
"""

# TODO: fix bug rounding error

import contextlib
import os
import wave
import click

@click.command()
@click.argument('audio_filename', type=str) # Example: audio.wav
@click.option('--csv_filename', type=str, default="Number transcription - Wiki version - SyllableTrans.csv")
def main(audio_filename, csv_filename):
    X_MIN = 0  # start at 0, the beginning of the file. May need to adjust

    # READ INPUTS
    csv_file = open(csv_filename, "r", encoding="utf8")
    lines = csv_file.readlines()
    csv_file.close()

    assert audio_filename.endswith('.wav')
    audio_length = get_audio_length(os.path.join('logs', audio_filename))
    sample_name = audio_filename[:-4]

    # MODIFY INPUT
    lines = lines[2:]  # remove header row
    SILENCE_LINE = 'sil,sil,'
    words = [SILENCE_LINE]
    for row in lines:
        words.append(row)
        words.append(SILENCE_LINE)
    
    # DEFINE WORD TIME BASED ON AUDIO LENGTH
    xmax = audio_length
    num_words = len(words)
    word_time = audio_length / num_words

    # NMV: question? add a silence between each word?
    # originally each word was 250 msec (0.25 sec). May need to adjust
    # from recordings: 25 "words" take about 58 seconds or about 2.3 seconds/word
    # adjust to accomodate silence (24 sil), which is included in the numIntervalsWords count
    # about 1.2 seconds/ word, silence

    # WRITE INTO TEXTGRID FILE
    fout = open(os.path.join('logs', sample_name + '.textgrid'), "w", encoding="utf8")
    header = (
        'File type = "ooTextFile"\nObject class = "TextGrid"\n\nxmin = '
        + str(X_MIN)
        + "\nxmax = "
        + str(xmax)
        + "\ntiers? <exists> \nsize = 2"
    )
    firstTierHeader = (
        'item []: \n\titem [1]:\n\t\tclass = "IntervalTier"\n\t\tname = "Words" \n\t\txmin = 0 \n\t\txmax = '
        + str(xmax)
        + "\n"
    )

    fout.write(header + "\n" + firstTierHeader)
    fout.write("\t\tintervals: size = " + str(num_words) + "\n")

    allPhones = {}
    numIntervalsPhones = 0
    first_tier = []
    second_tier = []

    
    for word_id, row in enumerate(words):
        row = row.split(",")
        word = row[0]
        phones = fixPhoneList(row[1:]) # remove the first column and empty cells
        numIntervalsPhones += len(phones)
        word_start = X_MIN + word_time * word_id
        allPhones[word_start] = phones
        
        # try:
        #     phone_time = word_time / len(phones)
        # except:
        #     print(word_id, word, row)
        # first_tier.append((word_start, word_start + word_time, word))
        # for phone_id, phone in enumerate(phones):
        #     phone_start = word_start + phone_time * phone_id
        #     second_tier.append((phone_start, phone_time, phone))


        fout.write("\t\tintervals[" + str(word_id + 1) + "]:\n")
        fout.write("\t\t\txmin = " + str(word_start) + "\n")
        fout.write("\t\t\txmax = " + str(word_start + word_time) + "\n")
        fout.write('\t\t\ttext = "' + word + '"\n')
        word_start += word_time

    # print(len(first_tier), first_tier[:5])
    # print(len(second_tier), second_tier[:5])

    secondTierHeader = (
        '\titem [2]:\n\t\tclass = "IntervalTier"\n\t\tname = "Phones" \n\t\txmin = '
        + str(X_MIN)
        + "\n\t\txmax = "
        + str(xmax)
        + "\n"
    )
    fout.write("\n" + secondTierHeader)
    fout.write("\t\tintervals: size = " + str(numIntervalsPhones) + "\n")

    word_id = 0
    for (k, phones) in allPhones.items():
        word_start = float(k)
        if len(phones) > 0:
            intervalTime = word_time / len(phones)
        else:
            intervalTime = word_time
            phones.append("no phones in this word")
        for p in phones:
            fout.write("\t\tintervals[" + str(word_id + 1) + "]:\n")
            fout.write("\t\t\txmin = " + str(word_start) + "\n")
            fout.write("\t\t\txmax = " + str(word_start + intervalTime) + "\n")
            fout.write('\t\t\ttext = "' + p + '"\n')
            word_id = word_id + 1
            word_start += intervalTime
    fout.close()

def fixPhoneList(v):
    newV = []
    for item in v:
        item = item.strip()
        if not item.isspace() and len(item) > 0:
            newV.append(item)
    return newV

def get_audio_length(audio_filename):
    with contextlib.closing(wave.open(audio_filename, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


if __name__ == "__main__":
    main()
