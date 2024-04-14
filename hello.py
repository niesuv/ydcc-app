from flask import Flask, request, send_file
import os
app = Flask(__name__)



UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST'])
def upload_file():
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        newname = filename.replace(".pcap", "")
        with open("./uploads/" + newname + '.csv', 'w') as file:
            file.write("skdlsd")

        statement = ['cicflowmeter', '-f' , "./uploads/" + filename, '-c', "./uploads/" + newname + '.csv']
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], newname + '.csv'), as_attachment=True)

        