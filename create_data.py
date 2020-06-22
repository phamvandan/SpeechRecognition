import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from scipy.io.wavfile import write
import sys,os,glob,shutil

## string have format: hh:mm:ss
def get_seconds_from_string(string):
  times = string.split(":")
  time = int(times[0])*3600 + int(times[1])*60 + float(times[2])
  return time

def get_time(time_string):
  time_string = time_string.replace("\n","").replace(" --> ","-").replace(",",".")
  time_strings = time_string.split("-")
  start_time = get_seconds_from_string(time_strings[0])
  end_time = get_seconds_from_string(time_strings[1])
  return start_time,end_time

def create_data(lines,audio_path,prefix = ""):
    signal, sample_rate = librosa.load(audio_path, sr=44100)
    i = 1
    chunck = 1
    length = len(lines)
    while i < length:
        time_string = lines[i]
        start_time, end_time = get_time(time_string)
        text  = ""
        i = i + 1
        while not lines[i].startswith("\n"):
            text =  text +" " + lines[i].replace("\n", "")
            i = i + 1
        splited_signal = signal[int(start_time * sample_rate):int(end_time * sample_rate)]
        write(prefix + "_" + str(chunck) + '.wav', sample_rate, splited_signal)
        f = open(prefix + "_" + str(chunck) + ".txt", "w+")
        f.write(text)
        chunck = chunck + 1
        i = i + 2
        print("saved ",prefix + "_" + str(chunck) + '.wav', " ",prefix + "_" + str(chunck) + ".txt")

if __name__ == '__main__':
    # src folder
    raw_folder = sys.argv[1]
    # folder to save
    dataset_folder = sys.argv[2]
    # use to remove invalid file from raw folder
    invalid_folder = sys.argv[3]
    # .mp3 or .mkv
    extension = sys.argv[4]

    substitudes = glob.glob(os.path.join(raw_folder,"*.srt"))
    for substitude in substitudes:
        prefix = substitude.split("/")[-1]
        prefix = prefix[:len(prefix)-4]
        name = prefix
        prefix = os.path.join(dataset_folder,prefix)
        os.mkdir(prefix)
        prefix = os.path.join(prefix,name)
        audio_path = substitude[:len(substitude)-4] + extension
        if os.path.exists(audio_path):
            f = open(substitude,"r")
            lines = f.readlines()
            create_data(lines,audio_path,prefix)
        else:
            shutil.move(substitude,os.path.join(invalid_folder,substitude.split("/")[-1]))
            print("Not exist: ",audio_path," for ",substitude, " MOVED")