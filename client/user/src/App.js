import './App.css';
import OperationArea from './components/operationArea/operation';
import TetramerGet from './components/TetramerGet';
import Header from './components/header/header';
import Footer from './components/footer/Footer';
// import NavBar from './components/navbar/navbar.js'
import ColorSchemesExample from './components/navbar/navbar.js'
import FAQ from './components/FAQ/index.js'
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import PageNotFound from './components/PageNotFound';
import ContactUs from './components/ContactUs'

function App() {
  return (


      <BrowserRouter>
          <div className="App">
      <Header/>
        <ColorSchemesExample/>
        <Routes>
          <Route exact path = '/' element = {<OperationArea/>}> </Route>
          <Route exact path = 'FAQ' element = {<FAQ></FAQ>}></Route>
          <Route exact path = 'ContactUs' element = {<ContactUs></ContactUs>}></Route>
          <Route exact path = '*' component = {<PageNotFound/>}></Route>
        </Routes>
        
        
        <Footer/>
        </div>
      </BrowserRouter>



  );
}

export default App;
