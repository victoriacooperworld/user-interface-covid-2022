import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)


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

@app.route("/Uploads", methods=['POST'])
@cross_origin()
def upload():
    
    uploads_dir = '/Users/keanewong/Desktop/User-interface-covid2022/Uploads'
    uploaded_files = request.files.getlist('file')
    # uploaded_files = request.files['file']
    # print(uploaded_files)
    if 'file' not in request.files:
        print("No file sent")
    print("Upload function called, uploading ", len(uploaded_files), " to server")
    print("Saving in ", uploads_dir)
    for file in uploaded_files:
        file.save(os.path.join(uploads_dir, file.filename.split('/')[1]))
    return jsonify("Uploads completed")

if(__name__) == "__main__":
    app.run(debug=True)