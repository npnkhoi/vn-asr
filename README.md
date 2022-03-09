# Vietnamese ASR
A joint project in CS398, supervised by Dr. Nanette Veilleux. This repo currently contains only utility scripts.

## Features
- Generate textgrid from the CSV transcript
- Adjust textgrid length to be equal to the audio file

## Installation
You must have Python and a terminal. If you don't know what a terminal is, install [Git Bash](https://git-scm.com/downloads).

Clone this repository to your comuputer. This is usually done by entering the following command to Git Bash:
```
git clone https://github.com/npnkhoi/vn-asr.git
```
## Usage

First, prepare two files:
- Put your audio file (e.g., `example.wav`) into `logs/` folder. This folder will also contains the textgrid output.
- Put your transcription (e.g., `24nums.csv`) into the `transcriptions/` folder. This transciption can be used for all files with the same script.

Then, open terminal inside this project folder (usually `vn-asr/`). Run this command (replace the filenames appropriately):
```
python gen_textgrid.py example.wav 24nums.csv
```

Done! You should see a new file called `example.textgrid` in the `logs/` folder. Open that in Praat and start annotating.