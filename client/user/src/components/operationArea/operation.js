import {React, useState} from "react";
import './operation.css';

const OperationArea = () =>{
    const [file, setFile] = useState();
    const [filePicked, setFilePicked] = useState(false);
    const [searchProt, setSearchProt] = useState("");

    /* 
    const sendFilePath = event =>{
        event.preventDefault();
        console.log(filePath)
        if(filePath === ""){
            console.log("ERROR: FILEPATH EMPTY")
        }
        else{
            try{
                fetch('http://localhost:5000/ProcessData', {
                    method: "POST",
                    headers: {
                        'Content-type': 'application/json'
                      },
                      body: JSON.stringify(filePath)
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
    }
    */

    /* Displays uploaded file information to user */
    const fileChangeHandler = (event) => {
        setFile(event.target.files[0]);
        setFilePicked(true);
    };

    /* Handles file submission to server */
    const fileSubmitHandler = (event) => {
        //TODO:
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
                <input className="upload" type = 'file' onChange={fileChangeHandler}></input>

                {/* Render conditionally if file is chosen or not chosen */}
                {filePicked ? (
                    <div className="fileinfo">
                        <p>Name: {file.name}</p>
                        <p>Type: {file.type}</p>
                        <p>Size: {parseInt(file.size / 100000)}kb</p>
                    </div>
                ): (
                    <p></p>
                )}

                <button className="button" type="submit" >Upload Patient Data</button>
            </form>
            
           <form className="proteinsearch" placeholder="Enter protein" onSubmit = {SearchProtein}>
                <input className="textfield" type = 'text' onChange={(e)=>setSearchProt(e.target.value) }></input>
                <button className="button" type="submit">Search Protein</button>
           </form> 
           
            {/* <h3>OperationArea</h3> */}
        </div>
    )
}

export default OperationArea;