import React from 'react';
import Select from 'react-select';


const databaseOptions = [
  { label: "Human", value: 1 },
  { label: "Viral", value: 2 },
  { label: "Non-redundant", value: 3 },
];

const DropdownMenu = (props) => {
    
    const onTrigger = (selected) =>{
        console.log(selected.label)
        props.parentCallback(selected.label)
        
    }
    return (

        <Select options = {databaseOptions} onChange = {onTrigger}></Select>
    )
};

export default DropdownMenu;