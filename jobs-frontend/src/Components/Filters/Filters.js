import { useHistory, useLocation } from 'react-router-dom';
import './Filter.css';

const Filters = () => {

    const history = useHistory();
    const location = useLocation();
    let page = location.pathname;


    const handleSearch = () => {

        history.push({
            pathname: "/search"
        });
    }

    const handleFave = () => {

        history.push({
            pathname: "/favourites",
            search: `?page=1`
        });
    }

    return (
        <>
            <section className="container-fluid filter-big">
                <div className="container">
                    <div className="row px-5">
                        <button
                            className={`col-6 filter-button ${page === "/search" && "filter-active"} `}
                            disabled={page === "/search" ? "disabled" : ''}
                            onClick={handleSearch}>{page === "/search" ? "Viewing search results" : "View Search Results"}
                        </button>
                        <button
                            className={`col-6 filter-button 
                            ${page === "/favourites" && "filter-active"} `}
                            disabled={page === "/favourites" ? "disabled" : ''}
                            onClick={handleFave}>{page === "/favourites" ? "Viewing favourites" : "View favourites"}
                        </button>
                    </div>
                </div>
            </section>
        </>
    )

}

export default Filters;