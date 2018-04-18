import os
import datetime
from gtts import gTTS
import requests
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import translate

import json
# Instantiates a client
client = speech.SpeechClient()
translate_client = translate.Client()

def speech_to_text(audio_filename):
	# The name of the audio file to transcribe
	print("speech to text ",audio_filename)
	file_name = os.path.join(
		os.path.dirname(__file__),
		audio_filename)
	
	# r'K:\Python\env\NLTK\voiceTotext\sample01.wav')
	
	# Loads the audio into memory
	with open(file_name, 'rb') as audio_file:
		content = audio_file.read()
		audio = types.RecognitionAudio(content=content)
	
	config = types.RecognitionConfig(
		encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
		sample_rate_hertz=16000,
		language_code='en-IN')
	
	# Detects speech in the audio file
	response = client.recognize(config, audio)
	filename = datetime.datetime.now()
	filename = 'upload/{}.txt'.format(str(filename).replace(":",""))
	# print(type('upload\{}.txt'.format(str(filename).replace(":",""))))
	with open(filename , 'w+') as file:
		for result in response.results:
			word = result.alternatives[0].transcript.split(" ")
			file.write("\n".join(word))
	return filename

def translate_from_file(str):
	print("translate")
	trans = translate_client.translate(str, target_language='en', source_language='hi')
	return trans

def transliterate_from_file(input_file, result_file):
	print("transliteration")
	text=[]
	with open(input_file , 'r') as file:
		lines = file.readlines()
		for line in lines:
			text.append(line.strip())
		text = " ".join(text)
		dictToSend = {'message': '{}'.format(text)}
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		data = requests.post(r"https://majortranslitrate.herokuapp.com/transl", data=json.dumps(dictToSend) ,headers=headers )
	words = data.text.replace("\"" , "")
	with open(result_file , 'w' , encoding='utf-8') as file:
		for word in words:
			file.write("\n".join(word))
	return result_file



def text_to_speech(text):
    tts = gTTS(text, lang='en', slow=False)
    filename = s = datetime.datetime.now()
    filename = 'upload/{}.wav'.format(str(filename).replace(":", ""))
    tts.save(filename)
    print("text to speech" ,filename)
    return filename

def fetch_from_file(result_file):
	print("fetching from file")
	translate = []
	with open(result_file , 'r',encoding='utf-8') as file:
		lines = file.readlines()
		for line in lines:
			translate.append(line.strip())
	return " ".join(translate)