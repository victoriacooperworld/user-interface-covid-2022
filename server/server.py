import os
from aiohttp import ClientRequest
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import shutil, os
app = Flask(__name__)

def ClrDirectory(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if filename.endswith('.fna'):
                os.remove(file_path)
            else:
                continue
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

@app.route("/members")
@cross_origin()
def members():
    return {"members":["Member1","Member2", "Member3"]}

@app.route("/tetramer/<tetId>")
@cross_origin()
def getTetId(tetId):
    return tetId

@app.route("/ProcessData", methods = ['POST'])
@cross_origin()
def ProcessData():
    print("Using ProcessData()")
    filepath = request.json
    if not filepath:
        print("Filepath doesnt exist")
    else:
        print(filepath)

    
    return jsonify("Hi")

@app.route("/SearchProtein/<searchProt>", methods = ['GET'])
@cross_origin()
def SearchProtein(searchProt):
    print("Using SearchProtein()")
    if not searchProt:
        print("SearchProt doesnt exist")
    else:
        print(searchProt)
    
    return jsonify(searchProt + searchProt)



def ProcessPatientData(uploads_dir1, uploads_dir2):
    
    pass

@app.route("/Uploads", methods=['POST'])
@cross_origin()
def upload():
    print("Using Upload")
    uploads_dir1 = '/Users/keanewong/Desktop/User-interface-covid2022/Uploads/Pos'
    uploads_dir2 = '/Users/keanewong/Desktop/User-interface-covid2022/Uploads/Neg'
    ClrDirectory(uploads_dir1)
    ClrDirectory(uploads_dir2)
    uploaded_files1 = request.files.getlist('file1')
    uploaded_files2 = request.files.getlist('file2')
    if 'file1' not in request.files:
        print("No file1 sent")
    if 'file2' not in request.files:
        print("No file sent")
    print("Upload function called, uploading ", len(uploaded_files1), " positive to server")
    print("Upload function called, uploading ", len(uploaded_files2), " negative to server")
    print("Saving in ", uploads_dir1)
    print("Saving in ", uploads_dir2)
    for file in uploaded_files1:
        file.save(os.path.join(uploads_dir1, file.filename.split('/')[1]))
    for file in uploaded_files2:
        file.save(os.path.join(uploads_dir2, file.filename.split('/')[1]))
    return jsonify({"Message":"Uploads completed"})




if(__name__) == "__main__":
    app.run(debug=True)