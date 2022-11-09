from distutils.command import upload
import os
from src.GenerateDB import HumanDB 
from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS, cross_origin
import shutil, os
app = Flask(__name__)
cors = CORS(app)


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





def ProcessPatientData(uploads_dir1, uploads_dir2, file_list_1, file_list_2):
    ###PLACEHOLDER TEST CODE
    
    return ""
    ###


def ProcessTetramerData(uploaded_file1_Path, heapSize, positionsDifference, selectedDB, returnPearson = False):

    ###PLACEHOLDER TEST CODE
    print(uploaded_file1_Path)
    filePath1 = uploaded_file1_Path
    print("Filepath 1 is", filePath1)

    ret1 = HumanDB.check(filePath1, heapSize, positionsDifference, selectedDB)
    print('Ret is', ret1)
    return ret1
    

@app.route("/Uploads", methods=['POST'])
@cross_origin()
def uploadPatients():
    print("Using Patient Upload")
    # uploads_dir1 = '/Users/keanewong/Desktop/User-interface-covid2022/Uploads/Patient/Pos'
    # uploads_dir2 = '/Users/keanewong/Desktop/User-interface-covid2022/Uploads/Patient/Neg'
    uploads_dir1 = r"C:\Users\User\Desktop\PosNegTest\UploadFiles\PosOutput"
    uploads_dir2 = r"C:\Users\User\Desktop\PosNegTest\UploadFiles\NegOutput"
    ClrDirectory(uploads_dir1)
    ClrDirectory(uploads_dir2)
    uploaded_files1 = request.files.getlist('filePos')
    uploaded_files2 = request.files.getlist('fileNeg')
    if 'filePos' not in request.files:
        print("No file1 sent")
    if 'fileNeg' not in request.files:
        print("No file sent")
    print("Upload function called, uploading ", len(uploaded_files1), " positive to server")
    print("Upload function called, uploading ", len(uploaded_files2), " negative to server")
    print("Saving in ", uploads_dir1)
    print("Saving in ", uploads_dir2)
    
    for file in uploaded_files1:
        # print("Going to ", os.path.join(uploads_dir1, file.filename.split('/')[1]))
        file.save(os.path.join(uploads_dir1, file.filename.split('/')[1]))
    for file in uploaded_files2:
        file.save(os.path.join(uploads_dir2, file.filename.split('/')[1]))
    
    returnFile = ProcessPatientData(uploads_dir1, uploads_dir2, uploaded_files1, uploaded_files2) #a path
    returnResponse = make_response(send_file(returnFile))
    return returnResponse

@app.route("/UploadsTet", methods=['POST'])
@cross_origin()
def uploadTet():
    print("Using Tetramer Upload")
    returnPearson = bool(int(request.form.get('ReturnPearson')))
    print("Return pearson is ",returnPearson)
    selectedDB = request.form.get("DB")
    print("DB to use", selectedDB)
    uploads_dir1 = r"C:\Users\User\Desktop\PosNegTest\UploadFiles\PosOutput"
    ClrDirectory(uploads_dir1)
    uploaded_file1 = request.files.get('filePos')

    if 'filePos' not in request.files:
        print("No filePos sent")
    else:
        print(request.files['filePos'])
    print("Upload function called, uploading ", len(request.files), " file to server")
    print("Saving in ", uploads_dir1)
    positionDiff = int(request.form.get("PositionDifference"))
    heapSize = int(request.form.get('HeapSize'))

    print("Position difference is ", positionDiff)
    print("Heap size is ", heapSize)
    print("Saving at ",os.path.join(uploads_dir1, uploaded_file1.filename))
    uploaded_file1.save(os.path.join(uploads_dir1, uploaded_file1.filename))
    uploaded_file1_Path = os.path.join(uploads_dir1, uploaded_file1.filename)
    returnFile = ProcessTetramerData(uploaded_file1_Path,  heapSize, positionDiff, selectedDB, returnPearson)
    returnResponse = make_response(send_file(returnFile))

    return returnResponse
    

if(__name__) == "__main__":
    app.run(debug=True)