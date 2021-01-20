import librosa.display
import scipy.io.wavfile as wavfile
import numpy
import os.path
from os import walk
import librosa 
import numpy as np
import pickle
import matplotlib.pyplot as plt
# Import the libraries
from sklearn import svm
from pycm import *

def extractMelSpectrogram_features(folder):
    print('************extractMelSpectrogram_features*************')   
    hop_length = 512
    n_fft = 2048
    n_mels = 128
    types = ["disco", "jazz"]
    labels = {'blues': 0,'classical': 1, 'country': 2, 'disco': 3, 'hiphop': 4, 'jazz': 5, 'metal': 6, 'pop': 7, 'reggae': 8, 'rock': 9}
    a = []
    b = []
    for nametype in list(labels.keys()):
        _wavs = []
        wavs_duration = []
        for (_,_,filenames) in walk(folder+nametype+"/"):
            print(filenames)
            _wavs.extend(filenames)
            break
        Mel_Spectrogram = []
        for _wav in _wavs:
            # read audio samples
            if(".wav" in _wav): 
                file = folder +nametype+"/"+_wav
                print ("-"+file)
                signal, rate = librosa.load(file)  
                #The Mel Spectrogram
                S = librosa.feature.melspectrogram(signal, sr=rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
                S_DB = librosa.power_to_db(S, ref=np.max)
                #Mel_Spectrogram.append(S_DB)
                #print (S_DB)
                S_DB = S_DB.flatten()[:1200]
                a.append(S_DB)
                b.append(labels[nametype])
                
    return a, b



folder = "/app/data/genres_original/"
a, b = extractMelSpectrogram_features(folder)
print ("#Load mel features:")

print ("#SVM:")
clf = svm.SVC()
clf = svm.SVC(kernel="rbf")
clf.fit(a, b)

pickle.dump(clf, open('model.pkl','wb'))

value=input("Press OK to finish the program ...")


