import os
import re
import argparse
import whisper
import torch

os.chdir('C:\\Users\\andre\\Dropbox\\dev\\sysadmin')

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", help="File to transcribe", type=str)

parser.add_argument("-m", "--model", help="Model size to use", type=str)

args = parser.parse_args()

current_device = torch.cuda.current_device()

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# load the WhisperAI transcription model
model = whisper.load_model(args.model, device=DEVICE)

# select the audio file to transcribe
# TODO - make this a command line argument sys.argv[1]
audio_file = os.path.join(os.getcwd(), 'transcribe', args.file)

# store the transcription result in a variable
result = model.transcribe(audio_file)

# create a text file with the same name as the audio file
audio_filename = args.file
text_filename = re.sub(pattern='mp3', repl='txt', string=audio_filename)

# put the text file in the same directory as the audio file
text_file = os.path.join(os.getcwd(), 'transcribe', text_filename)

# write the transcription result to the text file
with open(text_file, 'w') as f:
    f.write(result["text"])
