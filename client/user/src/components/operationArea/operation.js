import {React, useState} from "react";
import ProcessPatient from "./ProcessPatientData/Process";
import SignificantTetramers from "./SignificantTet/Significant";

import './operation.css';

const OperationArea = () =>{




    return(
        <div className="operations">
            <ProcessPatient/>
            <SignificantTetramers/>
        </div>
    )
}

export default OperationArea;