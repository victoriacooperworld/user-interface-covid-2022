import React from 'react'

/**
* @author
* @function FileUploader
**/
import './style.css'


export const FileUploader = (props) => {
    const hiddenFileInput = React.useRef(null);
    const handleClick = event => {
        hiddenFileInput.current.click();
      };
  return(
  <>
    <button onClick={handleClick} className = "FileUploader">
      {props.buttonText}
    </button>
    <input
      type="file"
      ref={hiddenFileInput}
      onChange={props.callBack}
      style={{display: 'none'}} 
      accept = '.fna, .txt'
      webkitdirectory = "" 
      directory = ""
    />
  </>
   )

 }