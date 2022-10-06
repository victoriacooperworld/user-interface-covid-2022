import {React, useState} from "react";

import { FileUploader } from "../../FileUploader/FileUploader";
import './operation.css';

const OperationArea = () =>{
    const [filePos,setfilePos] = useState();
    const [fileNeg,setfileNeg] = useState();
    const [filePicked1, setFilePicked1] = useState(false);
    const [filePicked2, setFilePicked2] = useState(false);
    const [patientDatasPos, setpatientDatasPos] = useState([]);
    const [patientDatasNeg, setpatientDatasNeg] = useState([]);
    const [loadingPatient, setLoadingPatient] = useState(false);
    const [searchProt, setSearchProt] = useState("");
    const [tetFilePos,settetfilePos] = useState();
    const [tetFileNeg,settetfileNeg] = useState();
    const [tetFilePicked1, setTetFilePicked1] = useState(false);
    const [tetFilePicked2, setTetFilePicked2] = useState(false);
    const [tetramerDatasPos,setTetramerDatasPos] = useState([]);
    const [tetramerDatasNeg,setTetramerDatasNeg] = useState([]);
    var tetramerHeapSize = 0;
    var positionDifference = 0;
    const [loadingTet, setLoadingTet] = useState(false);

    const [checked, setChecked] = useState(false);

    /* Caches files locally to be sent */
    const fileChangeHandlerPos = (event) => {

        setfilePos(event.target.files[0]);
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
        for (let i = 0; i < event.target.files.length; i++) 
        {
            setpatientDatasNeg(result => result.concat(event.target.files[i]))
        }

    };
    /* Handles file submission to server */
    const fileSubmitHandler = (event) => {
        event.preventDefault();
        if(!filePicked1 || !filePicked2)
        {
            console.log("ERROR: One of the files were not set")
            return
        }
        setLoadingPatient(true)
        let data = new FormData()
        for (let i =0; i < patientDatasPos.length;i++)
        {
            data.append("filePos",patientDatasPos[i])
        }
        for (let i =0; i < patientDatasNeg.length;i++)
        {
            data.append("fileNeg",patientDatasNeg[i])
        }
        try
        {
            fetch('http://localhost:5000/Uploads',{
                method: "POST",
                
                body: data

            }).then((response) =>
                response.json()
            ).then((res)=>
            {
                console.log(res)
                setLoadingPatient(false)
            }
            )
        }
        catch(err)
        {
            console.log(err)
        }
    };

    const TetChangeHandlerPos = (event) => {
        
        settetfilePos(event.target.files[0]);
        setTetFilePicked1(true);
        let newPatientData = []
        for (let i = 0; i < event.target.files.length; i++) 
        {
            setTetramerDatasPos(result => result.concat(event.target.files[i]))
        }
       
    };
    const TetChangeHandlerNeg = (event) => {
        settetfileNeg(event.target.files[0]);
        setTetFilePicked2(true);
        let newPatientData = []
        for (let i = 0; i < event.target.files.length; i++) 
        {
            setTetramerDatasNeg(result => result.concat(event.target.files[i]))
        }

    };
    /* Handles file submission to server */
    const TetSubmitHandler = (event) => {
        event.preventDefault();
        tetramerHeapSize = event.target.HeapSize.value
        positionDifference = event.target.PositionDifference.value
        if(!tetFilePicked1 || !tetFilePicked2)
        {
            //PSUEDO CODE: NEED TO THROW VISIBLE ERROR
            console.log("ERROR: One of the files were not set")
            //
            return
        }
        if(tetramerHeapSize <= 0 || positionDifference <= 0){
            //PSEUDO CODE: NEED TO THROW A VISIBLE ERROR
            console.log("Heap size or position difference invalid")
            console.log(positionDifference, tetramerHeapSize)
            //
            return
        }

        setLoadingTet(true)
        let data = new FormData()
        for (let i =0; i < tetramerDatasPos.length;i++)
        {
            data.append("filePos",tetramerDatasPos[i])
        }
        for (let i =0; i < tetramerDatasNeg.length;i++)
        {
            data.append("fileNeg",tetramerDatasNeg[i])
        }
        data.append("PositionDifference", positionDifference)
        data.append("HeapSize", tetramerHeapSize)
        data.append("ReturnPearson", checked ? 1 : 0)
        console.log(positionDifference, tetramerHeapSize)
        try
        {
            fetch('http://localhost:5000/UploadsTet',{
                method: "POST",
                body: data
            }).then((response) =>
                response.blob()
            ).then((res)=>
                {
                    console.log(res)
                    const url = URL.createObjectURL(res)
                    const filename = 'Downloadd'
                    let a = document.createElement("a");
                    document.body.appendChild(a)
                    a.style = "display: none"
                    a.href = url
                    a.download = filename
                    a.click()
                    setLoadingTet(false)
                }
            )
        }
        catch(err)
        {
            console.log(err)
        }
    };



    return(
        <div className="operations">
            <form className="fileupload" onSubmit = {fileSubmitHandler}>
                {/* <input className="upload" directory="" webkitdirectory="" type="file" onChange={fileChangeHandlerPos} accept = '.fna, .txt'></input> */}
                <FileUploader buttonText = "Upload Positive Patient Data" callBack = {fileChangeHandlerPos} />
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

                <FileUploader buttonText = "Upload Negative Patient Data" callBack = {fileChangeHandlerNeg}/>
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
                <button className="buttonSubmit" type="submit" disabled = {loadingPatient}>Process Patient Data</button>
            </form>
            


           <form className="fileupload" onSubmit = {TetSubmitHandler} >
                <FileUploader buttonText = "Upload Positive Sample Tetramer Data" callBack = {TetChangeHandlerPos}/>

                {/* Render conditionally if file is chosen or not chosen */}
                {tetFilePicked1 ? (
                    <div className="fileinfo">
                        <p>Name: {tetFilePos.name}</p>
                        <p>Type: {tetFilePos.type}</p>
                        <p>Size: {parseInt(tetFilePos.size / 100000)}kb</p>
                    </div>
                ): (
                    <p></p>
                )}

                <FileUploader buttonText = "Upload Negative Sample Tetramer Data" callBack = {TetChangeHandlerNeg}/>
                {/* Render conditionally if file is chosen or not chosen */}
                {tetFilePicked2 ? (
                    <div className="fileinfo">
                        <p>Name: {tetFileNeg.name}</p>
                        <p>Type: {tetFileNeg.type}</p>
                        <p>Size: {parseInt(tetFileNeg.size / 100000)}kb</p>
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
                            tetramerHeapSize = event.target.value
                        }
                    }}></input>

                <span className="textFieldHelp" data-hover="This is the maximum heap size for the output tetramers">?</span>
                </div>
                <div className = 'textFieldWrap'>
                <input className="textfield" name = "PositionDifference" placeholder="Position Difference" type = 'text' onKeyPress={(event) => {
                    if (!/[0-9]/.test(event.key)) {
                        event.preventDefault();
                    }
                    else{
                        positionDifference = event.target.value
                    }
                }}></input>
                <span className="textFieldHelp" data-hover="This is the maximum position difference allowed between two tetramers in a protein where it can still be called significantly correlated.">?</span>
                </div>
                <div className = 'pearsonCheckWrap'>
                    <div className="pearsonCheck">Calculate Pearson Correlation Coefficients</div>
                    <div className = "pearsonCBWrapper">
                        <input className = "pearsonCheckBox" type="checkbox" checked = {checked} onChange={()=>{setChecked(!checked)}} />
                        <span  className="textFieldHelp pearsonCheckBox" data-hover="Relates significant tetramers to one another on a -1 to 1 scale">?</span>
                    </div>
                </div>
                <button className="buttonSubmit" type="submit" disabled = {loadingTet} >Process Tetramer Data</button>
                
            </form>

        </div>
    )
}

export default OperationArea;