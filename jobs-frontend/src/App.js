import logo from './logo.svg';
import './App.css';
import SearchForm from './Components/SearchForm/SearchForm.js';
import JobResults from './Components/JobResults/JobResults.js';
import Hero from './Components/Hero/Hero.js';
import Header from './Components/Header/Header.js';
import Footer from './Components/Footer/Footer';

import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';


function App() {

  const NotFound = () => {
    return (<div className="Container p-5"><h2>Something went wrong and we couldnt find what you want try making a search!</h2></div>)
  }

  // TODO re-arrange switch block
  return (
    <div className="App d-flex flex-column min-vh-100">

      <Router>

        <Header />
        <Route exact path="/" >
          <Hero />

        </Route>

        <SearchForm />

        <Switch>
          <Route exact path="/" >
          </Route>

          <Route exact path="/search">
            <JobResults />
          </Route >

          <Route component={NotFound} >
            <NotFound />
          </Route>


        </Switch>

        <Footer />
      </Router>


    </div >
  );
}

export default App;
