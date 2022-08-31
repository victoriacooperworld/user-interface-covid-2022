import {React, useState} from "react";

const OperationArea = () =>{
    const [filePath, setFilePath] = useState("")
    const [searchProt, setSearchProt] = useState("")

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
        <div>
            <form onSubmit = {sendFilePath}>
                <input type = 'text' onChange={(e) => setFilePath(e.target.value)}></input>
                <button type="submit" >Upload Patient Data</button>
            </form>
            
           <form onSubmit = {SearchProtein}>
                <input type = 'text' onChange={(e)=>setSearchProt(e.target.value) }></input>
                <button type="submit">Search Protein</button>
           </form> 
           
            {/* <h3>OperationArea</h3> */}
        </div>
    )
}

export default OperationArea;