import requests
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import librosa.display
import librosa 
import numpy as np
import pickle
import base64
import os

app = Flask(__name__)

clf=pickle.load(open('model.pkl','rb'))

def getPrediction(soundfile):
	hop_length = 512
	n_fft = 2048
	n_mels = 128

	types = {0: 'blues', 1: 'classical', 2: 'country', 3: 'disco', 4: 'hiphop', 5: 'jazz', 6: 'metal', 7: 'pop', 8: 'reggae', 9: 'rock'}   
	#sound_b64 = base64.b64decode(soundfile)
	
	signal, rate = librosa.load(soundfile)  
	
	#The Mel Spectrogram
	S = librosa.feature.melspectrogram(signal, sr=rate, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
	S_DB = librosa.power_to_db(S, ref=np.max)
	S_DB = S_DB.flatten()[:1200]
	y_pred = clf.predict([S_DB])[0]
	
	return types[y_pred]

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/get_message' , methods=['GET'])
def get_msg():
    print("f1",request.args.get('f1'))
    print("f2",request.args.get('f2'))
    payload = {'f1': request.args.get('f1'), 'f2': request.args.get('f2')}
    message = requests.get('http://172.17.0.3:5000/return_message',params=payload)
    print("message=",message)
    return message.text
@app.route('/uploader', methods=['POST'])
def upload_file():
	print("request.method=",request.method)
	if request.method == 'POST':
		f = request.files['file']
		print("filename=",f.filename)
		f.save(secure_filename(f.filename))
		#print('f.read()',f.read())
		with open(f.filename,"rb") as song_file:
			enc=base64.b64encode(song_file.read())
			#print("**enc=",enc)
			
			#base64_bytes = base64.b64encode(f.read())
			#base64_str = base64_bytes.decode("utf-8")
			
			#print("**base64_bytes=",base64_bytes)
			#print("**base64_str=",base64_str)
			y = getPrediction(f.filename)
			print("y=",y)
		
	return "<p>succes {{ y }} "+y+"</p>" 

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')


