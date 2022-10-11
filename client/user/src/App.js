import './App.css';
import OperationArea from './components/operationArea/operation';
import TetramerGet from './components/TetramerGet';
import Header from './components/header/header';
import Footer from './components/footer/Footer';
import Navbar from './components/navbar/navbar.js'

function App() {
  return (

    <div className="App">
      <Header/>
      <Navbar></Navbar>
      <OperationArea/>
      <Footer/>
      
    </div>


  );
}

export default App;
