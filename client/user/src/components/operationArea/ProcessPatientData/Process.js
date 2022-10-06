import {React, useState} from "react";

import { FileUploader } from "../../../FileUploader/FileUploader";
import '../operation.css';

const ProcessPatient = () =>{
    const [filePos,setfilePos] = useState();
    const [fileNeg,setfileNeg] = useState();
    const [filePicked1, setFilePicked1] = useState(false);
    const [filePicked2, setFilePicked2] = useState(false);
    const [patientDatasPos, setpatientDatasPos] = useState([]);
    const [patientDatasNeg, setpatientDatasNeg] = useState([]);
    const [loadingPatient, setLoadingPatient] = useState(false);

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
        for (let i = 0; i < event.target.files.length; i++) {
            setpatientDatasNeg(result => result.concat(event.target.files[i]))
        }

    };
    /* Handles file submission to server */
    const fileSubmitHandler = (event) => {
        event.preventDefault();
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
        try{
            fetch('http://localhost:5000/Uploads',{
                method: "POST",
                body: data

            }).then((response) =>
                response.json()
            ).then((res)=>{
                console.log(res)
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
    )
}

export default ProcessPatient;