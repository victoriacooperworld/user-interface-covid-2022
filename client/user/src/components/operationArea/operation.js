import {React, useState} from "react";
import './operation.css';

const OperationArea = () =>{
    const [file1,setFile1] = useState();
    const [file2,setFile2] = useState();
    const [filePicked1, setFilePicked1] = useState(false);
    const [filePicked2, setFilePicked2] = useState(false);
    const [patientDatasPos, setpatientDatasPos] = useState([])
    const [patientDatasNeg, setpatientDatasNeg] = useState([])

    const [searchProt, setSearchProt] = useState("");

    /* Displays uploaded file information to user */
    const fileChangeHandler1 = (event) => {
        setFile1(event.target.files[0]);
        setFilePicked1(true);
        let newPatientData = []
        for (let i = 0; i < event.target.files.length; i++) 
        {
            setpatientDatasPos(result => result.concat(event.target.files[i]))
        }
        console.log(patientDatasPos)
       
    };
    const fileChangeHandler2 = (event) => {
        setFile2(event.target.files[0]);
        setFilePicked2(true);
        let newPatientData = []
        for (let i = 0; i < event.target.files.length; i++) 
        {
            setpatientDatasNeg(result => result.concat(event.target.files[i]))
        }
        console.log(patientDatasNeg)

    };

    /* Handles file submission to server */
    const fileSubmitHandler = (event) => {
        event.preventDefault();
 
        if(!filePicked1 || !filePicked2){
            console.log("ERROR: One of the files were not set")
            return
        }
        let data = new FormData()
        for (let i =0; i < patientDatasPos.length;i++)
        {
            data.append("file1",patientDatasPos[i])
        }
        for (let i =0; i < patientDatasNeg.length;i++)
        {
            data.append("file2",patientDatasNeg[i])
        }
        try
        {
            fetch('http://localhost:5000/Uploads',{
                method: "POST",
                
                body: data

            }).then((response) =>
                response.json()
            ).then((res)=>
                console.log(res)
            )
        }
        catch(err)
        {
            console.log(err)
        }
    };

    /* Hanldes submission of text entered in protein search */
    const SearchProtein = event => {
        event.preventDefault();
        try{
            fetch('http://localhost:5000/SearchProtein/'+searchProt, {
                method: "GET",
                headers: {
                    'Content-type': 'application/json'
                  }
            }).then(
                res => 
                    res.json()
                
                //do something with the responnse
            ).then(
                jsonRet => console.log(jsonRet)
              //do sometjing with the response
            )
        }
        catch(err){
            console.log(err)
        }
    }


    return(
        <div className="operations">
            <form className="fileupload" onSubmit = {fileSubmitHandler}>
                <input className="upload" directory="" webkitdirectory="" type="file" onChange={fileChangeHandler1}></input>

                {/* Render conditionally if file is chosen or not chosen */}
                {filePicked1 ? (
                    <div className="fileinfo">
                        <p>Name: {file1.name}</p>
                        <p>Type: {file1.type}</p>
                        <p>Size: {parseInt(file1.size / 100000)}kb</p>
                    </div>
                ): (
                    <p></p>
                )}

                <input className="upload" directory="" webkitdirectory="" type="file" onChange={fileChangeHandler2}></input>
                {/* Render conditionally if file is chosen or not chosen */}
                {filePicked2 ? (
                    <div className="fileinfo">
                        <p>Name: {file2.name}</p>
                        <p>Type: {file2.type}</p>
                        <p>Size: {parseInt(file2.size / 100000)}kb</p>
                    </div>
                ): (
                    <p></p>
                )}
                <button className="button" type="submit" >Process Patient Data</button>
            </form>
            
           <form className="proteinsearch" onSubmit = {SearchProtein}>
                <input className="textfield" placeholder="Enter protein" type = 'text' onChange={(e)=>setSearchProt(e.target.value) }></input>
                <button className="button" type="submit">Search Protein</button>
           </form> 
           
            {/* <h3>OperationArea</h3> */}
        </div>
    )
}

export default OperationArea;