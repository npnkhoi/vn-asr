"""
Generates textgrid files based on audio's length and CSV transcription.
The textgrid file will get the same name as the audio file.

Usage: `python gen_textgrid.py [example].wav [trans].csv`
Author: Khoi + prof Nanette
"""

import os
import sys
from textgrid_utils import write_textgrid
from utils import fix_phone_list, get_audio_length
def main(audio_filename, csv_filename):
    X_MIN = 0  # start at 0, the beginning of the file. May need to adjust
    # READ INPUTS
    csv_file = open(os.path.join('transcriptions', csv_filename), "r", encoding="utf8")
    lines = csv_file.readlines()
    csv_file.close()

    assert audio_filename.endswith('.wav')
    sample_name = audio_filename[:-4]
    audio_length = get_audio_length(os.path.join('logs', audio_filename))

    # CROP CSV
    lines = lines[2:]  # remove header row
    SILENCE_LINE = 'sil,sil,'
    words = [SILENCE_LINE]
    for row in lines:
        words.append(row)
        words.append(SILENCE_LINE)
    
    # DEFINE WORD TIME BASED ON AUDIO LENGTH
    num_words = len(words)
    word_time = audio_length / num_words

    # WRITE INTO TEXTGRID FILE    
    first_tier = []
    second_tier = []
    for word_id, row in enumerate(words):
        row = row.split(",")
        word = row[0]
        phones = fix_phone_list(row[1:]) # remove the first column and empty cells
        word_start = X_MIN + word_time * word_id
        word_end = word_start + word_time
        
        try:
            phone_time = word_time / len(phones)
        except:
            print(f"WARNING: One word does not have phonemes")
        
        # Insert into the tiers
        first_tier.append((word_end, word))
        for phone_id, phone in enumerate(phones):
            phone_start = word_start + phone_time * phone_id
            phone_end = phone_start + phone_time
            
            if phone_id == len(phones) - 1:
                # Ensure the right boundary of the last phoneme must match the word's right boundary
                # This is to avoid confusion for Praat when reading non-identical boundaries
                EPS = 10**-6
                assert(abs(phone_end - word_end) < EPS)
                phone_end = word_end 
            second_tier.append((phone_start + phone_time, phone))
    
    write_textgrid(os.path.join('logs', sample_name + '.textgrid'), first_tier, second_tier, X_MIN, audio_length)

if __name__ == "__main__":
    _, audio_filename, csv_filename = sys.argv
    main(audio_filename, csv_filename)

# NMV: question? add a silence between each word?
# originally each word was 250 msec (0.25 sec). May need to adjust
# from recordings: 25 "words" take about 58 seconds or about 2.3 seconds/word
# adjust to accomodate silence (24 sil), which is included in the numIntervalsWords count
# about 1.2 seconds/ word, silence