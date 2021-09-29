import './App.css';
import SearchForm from '../SearchForm/SearchForm.js';
import Results from '../Results/Results.js';
import Hero from '../Hero/Hero.js';
import Header from '../Header/Header.js';
import Footer from '../Footer/Footer.js';
import Filters from '../Filters/Filters.js';

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

        <Route path={["/search", "/favourites"]} >
          <Filters />
        </Route>

        <Switch>
          <Route exact path="/" >
          </Route>

          <Route exact path={["/search", "/favourites"]} >
            <Results />
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
