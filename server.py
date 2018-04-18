# System imports
import os
import datetime
import sys
from os import path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/jitendra_gtbit05/MajorProject/web_server/key/key.json"
lib_path = os.path.abspath(os.path.join('../'))
sys.path.append(lib_path)



from flask import Flask, render_template
from gevent.wsgi import WSGIServer
from flask.json import jsonify
from flask_cors import CORS
# from werkzeug.utils import secure_filename

from flask_ext import *
from TTS import speech_to_text
from TTS import text_to_speech
from TTS import fetch_from_file
from TTS import translate_from_file
from TTS import transliterate_from_file

from transliterate import evaluate


static_assets_path = path.join(path.dirname(__file__), "dist")

app = Flask(__name__, static_folder= static_assets_path ,template_folder="./")
CORS(app)

ALLOWED_EXTENSIONS = set(['wav', 'WAV'])

# ----- Routes ----------

@app.route("/")
def index():
    
    return render_template('index.html')

@app.route("/audio/<path:audio_path>")
def send_audio(audio_path):
    return send_file(path.join(app.config["UPLOAD_FOLDER"], audio_path), as_attachment=True)


@app.route('/text_uploader', methods = ['GET', 'POST'])
def text_file():
    if request.method == 'POST':
        text = request.form['text'].strip()
        if text != "":
            filename = datetime.datetime.now()
            filename = 'upload/{}.txt'.format(str(filename).replace(":", ""))
            with open(filename, 'w+') as file:
                word = text.split(" ")
                file.write("\n".join(word))
            result_file_name = '{}_result.{}'.format(filename.rsplit('.',1)[0],filename.rsplit('.',1)[1])
            transliterate_from_file(filename, result_file_name)
            #evaluate(train_dir = r"..\\model1",  transliterate_file_dir = ""  , data_dir =r"..\\vocab1" ,input_file=filename , output_file=result_file_name ,  )
            translate = fetch_from_file(result_file_name)
            translate = translate_from_file(translate)
            print(translate)
            loc = text_to_speech(translate['translatedText'])
            #yield send_file(loc , as_attachment=True)
            #return translate['translatedText']
            return jsonify({"data":translate['translatedText'] , "loc":loc})
        else:
            return 'text not present'
    else:
        return 'POST request required'





@app.route('/voice_uploader', methods = ['GET', 'POST'])
def upload_file():
    def is_allowed(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        
    if request.method == 'POST':
        file = request.files['file']
        # print(file)
        print(file.filename)
        if file and is_allowed(file.filename):
            filename = file.filename
            file_path = path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            print(file_path)
            filename = speech_to_text(file_path)
            result_file_name = '{}_result{}'.format(filename.rsplit('.',1)[0],filename.rsplit('.',1)[1])
            transliterate_from_file(filename,result_file_name)
            # evaluate(train_dir=r"..\model" , transliterate_file_dir = ""  , data_dir =r"..\vocab",  input_file=filename , output_file=result_file_name )
            result = fetch_from_file(result_file_name)
            translate = translate_from_file(result)
            # return translate
            print(translate)
            loc = text_to_speech(translate['translatedText'])
            return send_file(loc , as_attachment=True)
            #return "Done. elapsed time:{}s".format(diff.seconds)
        else:
            return 'file format is not correct'
    else:
        return 'POST request required'





def bad_request(reason):
    response = jsonify({"error" : reason})
    response.status_code = 400
    return response





if __name__ == "__main__":
    # Start the server
    app.config.update(
        DEBUG = True,
        SECRET_KEY = "asassdfs",
        CORS_HEADERS = "Content-Type",
        UPLOAD_FOLDER = "upload",
        # MODEL = os.path.join("model", "berlin_net_iter_10000.caffemodel"),
        # PROTOTXT = os.path.join("model", "net_mel_2lang_bn_deploy.prototxt")
    )

    # Make sure all frontend assets are compiled
    # subprocess.Popen("webpack")

    # Start the Flask app
    app.run(host='0.0.0.0', port=9000, threaded=True )
    #http_server = WSGIServer(('0.0.0.0', 9000), app)
    #http_server.serve_forever()

