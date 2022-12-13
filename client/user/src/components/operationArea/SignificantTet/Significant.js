import {React, useState} from "react";
import * as ReactDOM from 'react-dom';
import { FileUploader } from "../../../FileUploader/FileUploader";
import '../operation.css';
import Select from 'react-select'
import 'react-dropdown/style.css';
import DropdownMenu from "./Dropdown";
import {Button} from '@mui/material';
import HelpIcon from '@mui/icons-material/Help';
import CheckPCC from './CheckBox.js'
const SignificantTetramers = () =>{
    const [tetFilePos,settetfilePos] = useState();
    const [tetFilePicked1, setTetFilePicked1] = useState(false);
    const [tetramerDatasPos,setTetramerDatasPos] = useState([]);
    var tetramerHeapSize = 0;
    var positionDifference = 0;

    const [loadingTet, setLoadingTet] = useState(false);
    const [checked, setChecked] = useState(false);
    const [DB, setDB] = useState("")
    const [showAdvanced, setShowAdvanced] = useState(false)

    const handleDB = (childData) =>{
        setDB(childData)
        console.log("Parent Side: ", childData)
    }
    
    const TetChangeHandlerPos = (event) => {
        settetfilePos(event.target.files[0]);
        console.log(event.target.files[0]);
        setTetFilePicked1(true);
        for (let i = 0; i < event.target.files.length; i++) {
            setTetramerDatasPos(result => result.concat(event.target.files[i]))
        }

    };


    /* Handles file submission to server */
    const TetSubmitHandler = (event) => {
        event.preventDefault();
        positionDifference  = event.target.PositionDifference.value;
        tetramerHeapSize    = event.target.HeapSize.value;

        // checked = event.target.CheckPCC
        positionDifference = positionDifference == "" ? 100 : positionDifference;
        tetramerHeapSize = tetramerHeapSize == "" ? 25 : tetramerHeapSize;


        if(!tetFilePicked1 ){
            //PSUEDO CODE: NEED TO THROW VISIBLE ERROR
            console.log("ERROR: File was not set")
            return
        }
        if(tetramerHeapSize <= 0 || positionDifference <= 0){
            //PSEUDO CODE: NEED TO THROW A VISIBLE ERROR
            console.log("Heap size or position difference invalid")
            console.log(positionDifference, tetramerHeapSize)
            return
        }

        setLoadingTet(true)
        let data = new FormData()
        for (let i =0; i < tetramerDatasPos.length;i++){
            data.append("filePos",tetramerDatasPos[i])
        }
        // setChecked(!checked)
        data.append("PositionDifference", positionDifference)
        data.append("HeapSize", tetramerHeapSize)
        data.append("ReturnPearson", checked ? 1 : 0)
        data.append("DB", DB);
        console.log(positionDifference, tetramerHeapSize, checked, DB)
        try{
            fetch('http://localhost:5000/UploadsTet',{
                method: "POST",
                body: data

            }).then((response) =>
                response.blob()
            ).then((res)=>{
                console.log(res)
                const url = URL.createObjectURL(res)
                const filename = 'Downloadd.csv'
                let a = document.createElement("a");
                document.body.appendChild(a)
                a.style = "display: none"
                a.href = url
                a.download = filename
                a.click()
                setLoadingTet(false)
            })
        }
        catch(err){
            console.log(err)
        }
    };

    return(
        <form className="fileupload" onSubmit = {TetSubmitHandler} >
           
            <FileUploader buttonText = "Upload Significant Sample Tetramer Data" callBack = {TetChangeHandlerPos}/>

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
            <Button className="buttonSubmit" type="submit" disabled = {loadingTet} >Process Tetramer Data</Button>

        </form>
    );
}

export default SignificantTetramers;