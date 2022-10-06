import React from 'react';
import Select from 'react-select';


const databaseOptions = [
  { label: "Human", value: 1 },
  { label: "Viral", value: 2 },
  { label: "Non-redundant", value: 3 },
];

const DropdownMenu = () => (

    
  <div className="dropdown">
    <div className="row">
      <div className="col-md-4"></div>
      <div className="col-md-4">
      <Select options={databaseOptions} />
      </div>
      <div className="col-md-4"></div>
    </div>
  </div>
);

export default DropdownMenu;