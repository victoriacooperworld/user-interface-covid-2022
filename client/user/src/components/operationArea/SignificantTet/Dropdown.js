import React, { useState } from 'react';
import {Select} from '@mui/material';
import {FormControl} from '@mui/material'
import {MenuItem} from '@mui/material'
import {InputLabel} from '@mui/material'


const DropdownMenu = (props) => {
    const [displaydb, setdisplaydb] = useState("Database")
    const handleChange = (event) =>{
        console.log("Ye",event.target.value)
        props.parentCallback( event.target.value)
        setdisplaydb(String(event.target.value))
        
    }
    return (
        <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">Database</InputLabel>
        <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value= {displaydb}
            label="Database"
            onChange={handleChange}
        >
            <MenuItem value={1}>Human</MenuItem>
            <MenuItem value={2}>Viral</MenuItem>
            <MenuItem value={3}>Non-redundant</MenuItem>
        </Select>
        </FormControl>
    )
};




export default DropdownMenu;