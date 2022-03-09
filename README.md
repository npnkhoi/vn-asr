# Vietnamese ASR
A joint project in CS398, supervised by Dr. Nanette Veilleux.

## Features
- Generate textgrid from the CSV transcript
- Adjust textgrid length to be equal to the audio file

## Installation
You must have Python and should have Git Bash in your computer.

Clone this repository to your comuputer. This is usually done by entering the following command to Git Bash:
```
git clone https://github.com/npnkhoi/vn-asr.git
```

## Usage
2. `cd` into the folder of this project
```
cd vn-asr
```
3. Put the audio file (e.g., `quynh.wav`) in the `logs/` folder.
4. Run this command (replace `quynh.wav` with your filename):
```
python gen_textgrid.py quynh.wav
```
If you have your own CSV transcription (say, `trans.csv`), put it in the top folder then run:
```
python gen_textgrid.py quynh.wav --csv_filename trans.csv
```
By now, you should see a new file called `quynh.wav` in the `logs/` folder. That is the textgrid.