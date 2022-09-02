import {React, useState, useEffect} from 'react'

/**
* @author
* @function TetramerGet
**/

function TetramerGet(){
    const[data,setData] = useState([{}])

    useEffect( () => {
        try{
            fetch('http://localhost:5000/members').then(
                (res)=>res.json()
            ).then(
                (data) =>{
                    setData(data)
                }
            )
        }
        catch(err){
            console.log(err)
        }

    },[])

  return(
      <div>
    {(typeof data.members === 'undefined') ? (
        <p>Loading....</p>
    ) : (
        data.members.map((member,i) => (
            <p key = {i}>{member}</p>
        ))
    )
    }
    </div>
  )
}
 export default TetramerGet;