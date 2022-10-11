import React from "react";
import {Checkbox} from '@mui/material'
import { FormControlLabel } from "@mui/material";
const CheckPCC = (props) => {
  const [checked, setChecked] = React.useState(true);
  const handleChange = (event) => {
    setChecked(event.target.checked);
  };
  return (
    <FormControlLabel
      control={<Checkbox checked={checked} onChange={handleChange} />}
      label="Check for Pearson Correlation Coefficient"
    />
  );
}

export default CheckPCC