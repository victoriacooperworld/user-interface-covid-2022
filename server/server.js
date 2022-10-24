const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')

require('dotenv').config()

const app = express()
const port = process.env.PORT || 5000;

app.use(cors())
app.use(bodyParser.json())

TetramerList = {"SSSS": "(0,1)", "SSSL": "(2,5)"}


app.get('/TetramerID/GetEntry/:Tetramer', async (request, response) =>{
    const Tetramer = request.params.Tetramer
    try{
        TetEntries = "Hah"
        response.json(TetEntries)
        //END PROTOTYPE CODE
    }
    catch (err){
        console.error(err.message)
    }

});

app.get('/data', async(request, response) =>{
    Members = ["1","2","3"]
    response.json(Members)
})




app.listen(port, () => {
    console.log(`Server is running on port: ${port}`);
});

