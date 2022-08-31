import './App.css';
import Author from './components/author/author';
import OperationArea from './components/operationArea/operation';
import TetramerGet from './components/TetramerGet';
import Navbar from './components/navbar/Navbar';
import Footer from './components/footer/Footer';

function App() {
  return (

    <div className="App">
      <Navbar/>
      <Author/>
      <OperationArea/>
      <TetramerGet/>
      <Footer/>
    </div>


  );
}

export default App;
