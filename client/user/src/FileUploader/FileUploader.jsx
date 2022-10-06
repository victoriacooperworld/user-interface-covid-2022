/**
 * @author
 * @function FileUploader
 **/
import React from 'react';
import { HiArrowSmUp } from "react-icons/hi";
import './FileUploader.css'


export const FileUploader = ({buttonText, callBack}) => {
    const hiddenFileInput = React.useRef(null);
    const handleClick = event => {
        hiddenFileInput.current.click();
      };
  return(
  <div className='button-container'>
    <button onClick={handleClick} className='upload-button'>
      <HiArrowSmUp/>
      {buttonText}
    </button>
    <input
      type="file"
      ref={hiddenFileInput}
      onChange={callBack}
      style={{display: 'none'}} 
      accept = '.fna, .txt'
      webkitdirectory = "" 
      directory = ""
    />
  </div>
   )

 }