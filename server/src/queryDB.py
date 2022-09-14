from GenerateDB.DatabaseInit import databaseInit
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
def getTetramer():
    pass
    # TODO: use api to get the wanted tetramer from express

@app.route("/query/<input>")
@cross_origin()
def query(input):
    #input: SSSS
    
    #1. query it from the db and get all the entries
    db = databaseInit()
    db.useDB("ProteinDB")
    entries = db.search('entries','tetramerid','sequence',input)
    a = str(entries[0])[2:-2]
    entriesList = a.split("),(")
    relatedProteins = []
    for entry in entriesList:
        proteinId = entry[1:].split(',')[0]
        relatedProteins.append(proteinId)
    jsonifiedReturn = jsonify(Length = len(relatedProteins))
    print(len(relatedProteins))
    return(jsonifiedReturn)


if __name__ == '__main__':
    app.run(debug = True)