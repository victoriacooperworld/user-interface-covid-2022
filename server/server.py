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



if(__name__) == "__main__":
    app.run(debug=True)