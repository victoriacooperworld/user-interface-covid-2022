import {React, useState} from "react";
import * as ReactDOM from 'react-dom';
import { FileUploader } from "../../../FileUploader/FileUploader";
import '../operation.css';
import { Button } from "@mui/material";
import Select from 'react-select'
import 'react-dropdown/style.css';
import DropdownMenu from "../SignificantTet/Dropdown";
import HelpIcon from '@mui/icons-material/Help';
import CheckPCC from '../SignificantTet/CheckBox.js'
const ProcessPatient = () =>{
    const [filePos,setfilePos] = useState();
    const [fileNeg,setfileNeg] = useState();
    const [filePicked1, setFilePicked1] = useState(false);
    const [filePicked2, setFilePicked2] = useState(false);
    const [patientDatasPos, setpatientDatasPos] = useState([]);
    const [patientDatasNeg, setpatientDatasNeg] = useState([]);
    const [loadingPatient, setLoadingPatient] = useState(false);
    var tetramerHeapSize = 0;
    var positionDifference = 0;
    var cutoffValue = 2;
    var qCutoffValue = 0.01;
    var numTopHits = 20;
    const [checked, setChecked] = useState(false);
    const [DB, setDB] = useState("")
    const [showAdvanced, setShowAdvanced] = useState(false)

    /* Caches files locally to be sent */
    const handleDB = (childData) =>{
        setDB(childData)
        console.log("Parent Sidde: ", childData)
    };
    const fileChangeHandlerPos = (event) => {

        setfilePos(event.target.files[0]);
        console.log(event.target.files[0]);
        
        setFilePicked1(true);
        let newPatientData = []
        for (let i = 0; i < event.target.files.length; i++) 
        {
            setpatientDatasPos(result => result.concat(event.target.files[i]))
        }
       
    };
    const fileChangeHandlerNeg = (event) => {
        setfileNeg(event.target.files[0]);
        setFilePicked2(true);
        let newPatientData = []
        for (let i = 0; i < event.target.files.length; i++) {
            setpatientDatasNeg(result => result.concat(event.target.files[i]))
        }

    };
    /* Handles file submission to server */
    const fileSubmitHandler = (event) => {
        event.preventDefault();
        positionDifference  = event.target.PositionDifference.value;
        tetramerHeapSize    = event.target.HeapSize.value;
        cutoffValue         = event.target.CutoffValue.value;
        qCutoffValue        = event.target.QCutoffValue.value;
        numTopHits          = event.target.TopHitNum.value;


        positionDifference = positionDifference == "" ? 100 : positionDifference;
        tetramerHeapSize = tetramerHeapSize == "" ? 25 : tetramerHeapSize;
        cutoffValue = cutoffValue == "" ? 2 : cutoffValue;
        qCutoffValue = qCutoffValue == "" ? 0.01 : qCutoffValue;
        // if (qCutoffValue.startsWith(".")){
        //     qCutoffValue =  qCutoffValue.replace(".","0.")
        // }
        numTopHits = numTopHits == "" ? 20 : numTopHits;

        if (positionDifference <1 || tetramerHeapSize < 1 || cutoffValue <0 || qCutoffValue <=0 || numTopHits < 1){
            console.log("ERROR: One of the arguments are invalid")
            return
        }
        console.log(positionDifference, tetramerHeapSize, cutoffValue, qCutoffValue, numTopHits)
        if(!filePicked1 || !filePicked2){
            console.log("ERROR: One of the files were not set")
            return
        }
        setLoadingPatient(true)
        let data = new FormData()
        for (let i =0; i < patientDatasPos.length;i++){
            data.append("filePos",patientDatasPos[i])
        }
        for (let i =0; i < patientDatasNeg.length;i++){
            data.append("fileNeg",patientDatasNeg[i])
        }
        data.append("PositionDifference", positionDifference)
        data.append("HeapSize", tetramerHeapSize)
        data.append("ReturnPearson", checked ? 1:0)
        data.append("DB", DB)
        data.append("CutoffValue", cutoffValue)
        data.append("QCutoffValue", qCutoffValue)
        data.append("NumTopHits", numTopHits)

        try{
            fetch('http://localhost:5000/Uploads',{
                method: "POST",
                body: data

            }).then((response) =>
                response.blob()
            ).then((res)=>{
                console.log(res)
                const url = URL.createObjectURL(res)
                const filename = 'Downloadd.zip'
                let a = document.createElement("a");
                document.body.appendChild(a)
                a.style = "display: none"
                a.href = url
                a.download = filename
                a.click()
                setLoadingPatient(false)
            }
            )
        }
        catch(err){
            console.log(err)
        }
    };
    return(
        <form className="fileupload" onSubmit = {fileSubmitHandler}>
            {/* <input className="upload" directory="" webkitdirectory="" type="file" onChange={fileChangeHandlerPos} accept = '.fna, .txt'></input> */}
            <FileUploader buttonText = "Upload Positive Patient Data" callBack = {fileChangeHandlerPos} multipleFiles="multiple" />
            {/* Render conditionally if file is chosen or not chosen */}
            {filePicked1 ? (
                <div className="fileinfo">
                    <p>Name: {filePos.name}</p>
                    <p>Type: {filePos.type}</p>
                    <p>Size: {parseInt(filePos.size / 100000)}kb</p>
                </div>
            ): (
                <p></p>
            )}

            <FileUploader buttonText = "Upload Negative Patient Data" callBack = {fileChangeHandlerNeg} multipleFiles="multiple"/>
            {/* Render conditionally if file is chosen or not chosen */}
            {filePicked2 ? (
                <div className="fileinfo">
                    <p>Name: {fileNeg.name}</p>
                    <p>Type: {fileNeg.type}</p>
                    <p>Size: {parseInt(fileNeg.size / 100000)}kb</p>
                </div>
            ): (
                <p></p>
            )}
            <div className = 'textFieldWrap'> 
                <input className="textfield" name = "HeapSize" placeholder="Output Heap Size" type = 'text' onKeyPress={(event) => {
                    if (!/[0-9]/.test(event.key)) {
                        event.preventDefault();
                    }
                    else{
                        // tetramerHeapSize = event.target.value
                    }
                }}></input>
      
                <div className="textFieldHelp" data-hover="This is the maximum heap size for the output tetramers">
                    <HelpIcon ></HelpIcon>
                </div>       
            </div>
         
            <div className = 'textFieldWrap'>
                <input className="textfield" name = "PositionDifference" placeholder="Position Difference" type = 'text' onKeyPress={(event) => {
                    if (!/[0-9]/.test(event.key)) {
                        event.preventDefault();
                    }
                    else{
                        // positionDifference = event.target.value
                    }
                }}>
                </input>
                <div className="textFieldHelp" data-hover="This is the maximum position difference allowed between two tetramers in a protein where it can still be called significantly correlated.">
                    <HelpIcon ></HelpIcon>
                </div>
            </div>
           
            <div className = 'pearsonCheckWrap'>
                <h5 className="pearsonCheck"></h5>
                <CheckPCC onClickBox = {setChecked}/>
                <div className = "pearsonCBWrapper">
                    <div className="textFieldHelp" data-hover="Relates significant tetramers to one another on a -1 to 1 scale">
                        <HelpIcon ></HelpIcon>
                    </div>
                    {/* <span className="textFieldHelp pearsonCheckBox" data-hover="Relates significant tetramers to one another on a -1 to 1 scale"> Hint </span> */}
                </div>
            </div>
            <DropdownMenu parentCallback = {handleDB}/>

            
            <Button className="buttonSubmit" type="submit" disabled = {loadingPatient}>Process Patient Data</Button>


            <div style = {{display : showAdvanced ? 'block' : 'none'}}>
                <div className = 'textFieldWrap'>
                    <input className="textfield" name = "CutoffValue" placeholder="Cutoff Value" type = 'text' onKeyPress={(event) => {
                        if (!/[0-9]/.test(event.key)) {
                            event.preventDefault();
                        }
                        else{
                            // cutoffValue = event.target.value
                        }
                    }}>
                    </input>
                    <div className="textFieldHelp" data-hover="Sequences with frequency less than or equal to this number are dropped (Default: 2)">
                        <HelpIcon></HelpIcon>
                    </div>
                </div>
                <div className = 'textFieldWrap'>
                    <input className="textfield" name = "QCutoffValue" placeholder="Q Cutoff Value" type = 'text' onKeyPress={(event) => {
                        if (!/[0-9]/.test(event.key)  && !/./.test(event.key)) {
                            event.preventDefault();
                        }
                        else{
                            // qCutoffValue = event.target.value
                        }
                    }}>
                    </input>
                    <div className="textFieldHelp" data-hover="Q values greater than this are discarded (Default: 0.01)">
                        <HelpIcon></HelpIcon>
                    </div>
                </div>
                <div className = 'textFieldWrap'>
                    <input className="textfield" name = "TopHitNum" placeholder="Number of top hits" type = 'text' onKeyPress={(event) => {
                        if (!/[0-9]/.test(event.key)) {
                            event.preventDefault();
                        }
                        else{
                            // numTopHits = event.target.value
                        }
                    }}>
                    </input>
                    <div className="textFieldHelp" data-hover="Number of the most significant tetramers to analyze (Default: 20)">
                        <HelpIcon></HelpIcon>
                    </div>
                </div>
                </div>
              


            <div>
                <a href = "" onClick = {(event) => {event.preventDefault(); setShowAdvanced(!showAdvanced); }}>Advanced Settings</a>
            </div>
        </form>
        
    )
}

export default ProcessPatient;