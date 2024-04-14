from flask import Flask, request, send_file
import os
import pickle as pk
import time
import tensorflow as tf
from tensorflow.keras.models import load_model
import subprocess
app = Flask(__name__)



model1 = load_model('cnn.h5')

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        try:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            newname = filename.replace(".pcap", "")
            

            statement = ['cicflowmeter', '-f' , "./uploads/" + filename, '-c', "./uploads/" + newname + '.csv']
            subprocess.run(statement, check=True)
            a = model.predict("./uploads/" + newname + '.csv')
            time.sleep(1)
            return a
            return send_file(os.path.join(app.config['UPLOAD_FOLDER'], newname + '.csv'), as_attachment=True)
        
        except Exception:
            return "Error"
            

        