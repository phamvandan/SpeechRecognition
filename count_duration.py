import sys, glob,os
import librosa
import datetime

if __name__ == '__main__':
    duration = 0
    audio_paths = glob.glob(os.path.join(sys.argv[1],"*.mp3"))
    print(audio_paths)
    for audio_path in audio_paths:
        print(audio_path)
        duration = duration + librosa.get_duration(filename=audio_path,sr=44100)
        print("Total duration",duration)
    print("Total time: ",str(datetime.timedelta(seconds=duration)))