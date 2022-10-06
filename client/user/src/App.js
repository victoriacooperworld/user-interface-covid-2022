import './App.css';
import OperationArea from './components/operationArea/operation';
import TetramerGet from './components/TetramerGet';
import Navbar from './components/navbar/Navbar';
import Footer from './components/footer/Footer';
import DropdownMenu from './components/operationArea/SignificantTet/Dropdown';
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
