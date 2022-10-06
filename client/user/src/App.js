import './App.css';
import OperationArea from './components/operationArea/operation';
import TetramerGet from './components/TetramerGet';
import Navbar from './components/navbar/Navbar';
import Footer from './components/footer/Footer';

function App() {
  return (

    <div className="App">
      <Navbar/>
      <OperationArea/>
      <Footer/>
    </div>


  );
}

export default App;
