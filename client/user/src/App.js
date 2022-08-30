import './App.css';
import Author from './components/author/author';
import OperationArea from './components/operationArea/operation';
import TetramerGet from './components/TetramerGet';
import {BrowserRouter, Routes, Switch, Route} from 'react-router-dom'

function App() {
  return (

    <div className="App">

      <h1>Hello World</h1>
      <Author/>
      <OperationArea/>
      <TetramerGet/>
    </div>


  );
}

export default App;
