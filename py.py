from flask import Flask, request, send_file
import os
import pickle as pk
import time
import tensorflow as tf
from tensorflow.keras.models import load_model
import subprocess
import pandas as pd
app = Flask(__name__)

def change_feature_name(dataset):
  array = [i for i in range(len(dataset.columns))]
  for i in range(len(dataset.columns.values)):
    array[i] = dataset.columns.values[i]
    array[i] = array[i].replace("_", " ")
    array[i] = array[i].replace("src", "Source")
    array[i] = array[i].replace("dst", "Destination")
    array[i] = array[i].replace("ip", "IP")
    array[i] = array[i].replace("tot", "Total")
    array[i] = array[i].replace("pkts", "Packets")
    array[i] = array[i].replace("pkt", "Packet")
    array[i] = array[i].replace("cnt", "Count")
    array[i] = array[i].replace("seg", "Segment")
    array[i] = array[i].replace("var", "Variance")
    array[i] = array[i].replace("len", "length")
    array[i] = array[i].replace("byts", "Bytes")
    array[i] = array[i].title()
    array[i] = array[i].replace("Ip", "IP")
    array[i] = array[i].replace("Iat", "IAT")
    array[i] = array[i].replace("Fin", "FIN")
    array[i] = array[i].replace("Ack", "ACK")
    array[i] = array[i].replace("Syn", "SYN")
    array[i] = array[i].replace("Psh", "PSH")
    array[i] = array[i].replace("Rst", "RST")
    array[i] = array[i].replace("Ece", "ECE")
    array[i] = array[i].replace("Cwe", "CWE")
    array[i] = array[i].replace("Urg", "URG")
    array[i] = array[i].replace(" B ", " Bulk ")
    array[i] = array[i].replace("s S", "s/s")
    array[i] = array[i].replace("Blk", "Bulk")
    array[i] = array[i].replace("Totallength", "Total Length of")
    array[i] = array[i].replace("Down Up Ratio", "Down/Up Ratio")
    array[i] = array[i].replace("Total Bwd Packets", "Total Backward Packets")
    array[i] = array[i].replace("Packet Length Max", "Max Packet Length")
    array[i] = array[i].replace("Packet Length Min", "Min Packet Length")
    array[i] = array[i].replace("Fwd Max Packet Length", "Fwd Packet Length Max")
    array[i] = array[i].replace("Fwd Min Packet Length", "Fwd Packet Length Min")
    array[i] = array[i].replace("Bwd Max Packet Length", "Bwd Packet Length Max")
    array[i] = array[i].replace("Bwd Min Packet Length", "Bwd Packet Length Min")
    array[i] = array[i].replace("Fwd Segment Size Min", "min_seg_size_forward")
    array[i] = array[i].replace("Fwd Act Data Packets", "act_data_pkt_fwd")
    array[i] = array[i].replace("Packet Size Avg", "Average Packet Size")
    array[i] = array[i].replace("Init Fwd Win Bytes", "Init_Win_bytes_forward")
    array[i] = array[i].replace("Init Bwd Win Bytes", "Init_Win_bytes_backward")
    array[i] = array[i].replace("Fwd Segment Size Avg", "Avg Fwd Segment Size")
    array[i] = array[i].replace("Bwd Segment Size Avg", "Avg Bwd Segment Size")
    array[i] = array[i].replace("Fwd Bulk Rate Avg", "Fwd Avg Bulk Rate")
    array[i] = array[i].replace("Bwd Bulk Rate Avg", "Bwd Avg Bulk Rate")
    array[i] = array[i].replace("Fwd Bytes Bulk Avg", "Fwd Avg Bytes/Bulk")
    array[i] = array[i].replace("Fwd Packets Bulk Avg", "Fwd Avg Packets/Bulk")
    array[i] = array[i].replace("Bwd Bytes Bulk Avg", "Bwd Avg Bytes/Bulk")
    array[i] = array[i].replace("Bwd Packets Bulk Avg", "Bwd Avg Packets/Bulk")
  print(len(array))
  return array
feature_list = ['Destination Port', 'Flow Duration', 'Total Fwd Packets','Total Backward Packets', 'Total Length of Fwd Packets', 'Total Length of Bwd Packets', 'Fwd Packet Length Max',
       'Fwd Packet Length Min', 'Fwd Packet Length Mean',
       'Fwd Packet Length Std', 'Bwd Packet Length Max',
       'Bwd Packet Length Min', 'Bwd Packet Length Mean',
       'Bwd Packet Length Std', 'Flow IAT Mean', 'Flow IAT Std',
       'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean',
       'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total',
       'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min',
       'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags',
       'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s',
       'Bwd Packets/s', 'Min Packet Length', 'Max Packet Length',
       'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance',
       'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count',
       'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count',
       'Down/Up Ratio', 'Average Packet Size', 'Avg Fwd Segment Size',
       'Avg Bwd Segment Size', 'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk',
       'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk',
       'Bwd Avg Bulk Rate', 'Subflow Fwd Packets', 'Subflow Fwd Bytes',
       'Subflow Bwd Packets', 'Subflow Bwd Bytes', 'Init_Win_bytes_forward',
       'Init_Win_bytes_backward', 'act_data_pkt_fwd', 'min_seg_size_forward',
       'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Mean',
       'Idle Std', 'Idle Max', 'Idle Min']

def drop_feature(dataset):
  dataset.drop("Flow Bytes/s", axis=1, inplace=True)
  dataset.drop("Flow Packets/s", axis=1, inplace=True)
  cols = dataset.columns.values
  for col in cols:
    if col not in feature_list:
      dataset.drop(col, axis=1, inplace=True)


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
            time.sleep(5)
            X = pd.read_csv("./uploads/" + newname + '.csv')
            X.columns = change_feature_name(X)
            drop_feature(X)
            X = X.reindex(columns=feature_list)
            pca_reload = pk.load(open("pca.pkl",'rb'))
            result_new = pca_reload.transform(X)
            #pca_reload = pk.load(open("pca.pkl",'rb'))
            #result_new = pca_reload .transform(X)
            a = model1.predict(result_new)
            time.sleep(3)
            a = a.flatten().tolist()
            num1 = sum(a)
            num0 = len(a) - num1
            if num1 > num0:
                return "safe"
            return "can be dos ed"
            return send_file(os.path.join(app.config['UPLOAD_FOLDER'], newname + '.csv'), as_attachment=True)

        except Exception as e:
            print(e)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)