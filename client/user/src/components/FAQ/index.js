
import './style.css'
import Faq from "react-faq-component";
import { useState } from 'react';
import exampleFormat from './Format_Example.png';
import exampleFormatPatient from './Format_Example_Patients.png'
function FAQ() {
    const [rows, setRowsOption] = useState(null);
    const data = {
      title: "FAQ (How it works)",
      rows: [
        {
          title: "What is the K-Mer Project?",
          content: ""
        },
        {
          title: "How do I use this tool?",
          content: 
                <div>
                    <img src = {exampleFormatPatient} alt = "Image Missing"></img>
                    <p>You can use the patient processing function to process raw patient data in the form of FASTA files.
                        Have a directory of patient files each containing a list significant 12-mers sorted by prevalance.
                        The fasta files should resemble the image above
                    </p>
                    <img src = {exampleFormat} alt = "Image Missing"></img>
                    <p>You can instead use the sample tetramer data if you already have a list of significant Tetramers.
                        Start by formatting your data. Have a plain text file containing a list of tetramers found to be 
                        statistically significant as well as a p value on the same line, separated by a tab. The format 
                        should resemble the image above
                    </p>
                </div>
        },
        {
          title: "What are each of the database options?",
          content: `Each database option refers the non-redundant proteome that the algorithm will query from. It is best to have an idea of what
          you may be looking for to help narrow relevant proteins, but for the broadest scope search, the Non-Redundant (NR) proteome
          option queries the entire catalogue of proteins known currently. `
        },
        {
            title: "What is heap size?",
            content: `Heap size is the size you expect to see for the output proteins.`
          },
        {
            title: "What is position difference?",
            content: `Position difference refers to the maximum number of amino acids between two significant tetramers in a given 
            protein. Any tetramers that have a distance less than this value is marked as correlated.  `
        },
        {
          title: "How can I contact help?",
          content: <p>You can email technical support at <a href = 'mailto: example@aol.com'>glabelab@uci.edu</a> and we will do our 
          best to help you in any way we can.</p>
        }
      ]
    };
    return (
        <div>
        <h2 className="section-title">Who We Are</h2>
        <p>The Glabe Lab is a research group dedicated to the study of disease correlated antibodies</p>
        <p>Headed by Professor Charles Glabe, the K-Mer Project....</p>
        <div className="faq-style-wrapper">
          <Faq data={data} getRowOptions={setRowsOption} />
        </div>
      </div>
  
    );
}
  
  export default FAQ;