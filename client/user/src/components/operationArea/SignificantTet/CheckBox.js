import React from "react";

import {Checkbox} from '@mui/material'
import { FormControlLabel } from "@mui/material";
const CheckPCC = (props) => {
  const [checked, setChecked] = React.useState(false);

  const handleChange = (event) => {
    setChecked(event.target.checked)
    console.log("Checked in child is ", event.target.checked)
    props.onClickBox(event.target.checked);
  };

  return (
    <FormControlLabel
      control={<Checkbox checked={checked} onChange={handleChange} />}
      label="Check for Pearson Correlation Coefficient"
    />
  );
}

export default CheckPCC