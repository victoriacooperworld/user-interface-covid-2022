/**
 * @author
 * @function FileUploader
 **/
import React from 'react';
import { HiArrowSmUp } from "react-icons/hi";
import './FileUploader.css'
import { Button } from '@mui/material';
import FileUploadIcon from '@mui/icons-material/FileUpload';
export const FileUploader = ({buttonText, callBack}) => {
    const hiddenFileInput = React.useRef(null);
    const handleClick = event => {
        hiddenFileInput.current.click();
      };
    return(
      <div className='button-container'>
        <Button variant="contained" onClick={handleClick} className='upload-button' >
          <FileUploadIcon/>
          {buttonText} 
        </Button>
        <input
          type="file"
          ref={hiddenFileInput}
          onChange={callBack}
          style={{display: 'none'}} 
          accept = '.fna, .txt'
        />
      </div>
    )

 }