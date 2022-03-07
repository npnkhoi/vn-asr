import contextlib
import wave
import click

@click.command()
@click.argument('filename', type=str)
def main(filename):
    DEBUG = False
    IS_HEADER = True
    X_MIN = 0  # start at 0, the beginning of the file. May need to adjust
    audio_length = get_audio_length(filename)
    print(audio_length)

    # READ INPUT
    input_file = open("Number transcription - Wiki version - SyllableTrans.csv", "r", encoding="utf8")
    lines = input_file.readlines()
    input_file.close()

    # MODIFY INPUT
    if IS_HEADER:
        lines = lines[2:]  # remove header row
    SILENCE_LINE = 'sil,sil,'
    words = [SILENCE_LINE]
    for line in lines:
        words.append(line)
        words.append(SILENCE_LINE)
    xmax = audio_length
    num_words = len(words)
    word_time = audio_length / num_words


    fout = open("trans.TextGrid", "w", encoding="utf8")

    # NMV: question? add a silence between each word?
    # originally each word was 250 msec (0.25 sec). May need to adjust
    # from recordings: 25 "words" take about 58 seconds or about 2.3 seconds/word
    # adjust to accomodate silence (24 sil), which is included in the numIntervalsWords count
    # about 1.2 seconds/ word, silence


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
    timeStart = X_MIN
    for i in range(num_words):
        line = words[i].split(",")
        word = line[0]
        phones = fixPhoneList(line[1:]) # remove the first column
        numIntervalsPhones += len(phones)
        allPhones[timeStart] = phones
        
        if DEBUG:
            print("debug: " + str(i))
            print(len(phones))
            print(phones)
            print(allPhones)
            # wait = input("any key")
        fout.write("\t\tintervals[" + str(i + 1) + "]:\n")
        fout.write("\t\t\txmin = " + str(timeStart) + "\n")
        fout.write("\t\t\txmax = " + str(timeStart + word_time) + "\n")
        fout.write('\t\t\ttext = "' + word + '"\n')
        timeStart += word_time

    secondTierHeader = (
        '\titem [2]:\n\t\tclass = "IntervalTier"\n\t\tname = "Phones" \n\t\txmin = '
        + str(X_MIN)
        + "\n\t\txmax = "
        + str(xmax)
        + "\n"
    )
    fout.write("\n" + secondTierHeader)
    fout.write("\t\tintervals: size = " + str(numIntervalsPhones) + "\n")

    i = 0
    for (k, phones) in allPhones.items():
        timeStart = float(k)
        if len(phones) > 0:
            intervalTime = word_time / len(phones)
        else:
            intervalTime = word_time
            phones.append("no phones in this word")
        for p in phones:
            # wait = input(p + "\nany key")
            fout.write("\t\tintervals[" + str(i + 1) + "]:\n")
            fout.write("\t\t\txmin = " + str(timeStart) + "\n")
            fout.write("\t\t\txmax = " + str(timeStart + intervalTime) + "\n")
            fout.write('\t\t\ttext = "' + p + '"\n')
            i = i + 1
            timeStart += intervalTime

    fout.close()


def fixPhoneList(v):
    newV = []
    for item in v:
        item = item.strip()
        if not item.isspace() and len(item) > 0:
            newV.append(item)
    return newV

def get_audio_length(filename):
    with contextlib.closing(wave.open(filename, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


if __name__ == "__main__":
    main()
