import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux'
import Pagination from '../Pagination/Pagination';
import Favourites from './FavouritesResults';
import JobsDisplay from './JobResults';

const SEARCH_URL = 'https://jobsseach.azurewebsites.net/api/jobs?';


const SearchResults = (props) => {

    const location = useLocation();
    let search = new URLSearchParams(location.search);

    const dispatch = useDispatch();

    const [jobPage, setjobPage] = useState(1);
    const [resultStart, setResultStart] = useState('');
    const [resultEnd, setResultEnd] = useState('');
    // const jobResults = [];
    const jobResults = useSelector(state => state.search.jobResults);
    const favouriteJobs = useSelector(state => state.favourite.favouriteJobs);

    const loading = useSelector(state => state.search.loading);
    const job = useSelector(state => state.search.jobName);
    const jobLocation = useSelector(state => state.search.jobLocation);


    // TODO update to trigger on page refresh or 
    useEffect(() => {

        // If stored job and location match url parameters do nothing as not a new search
        if (job === search.get("job") && jobLocation === search.get("location")) {
            return;
        }

        // Do nothing if on favourites page or if no url parameters for search
        if (location.pathname !== "/search" || (search.get("job") === null && search.get("location") === null)) {
            return
        }

        //
        dispatch({
            type: "search/job_added",
            jobName: search.get("job")
        })

        dispatch({
            type: "search/location_added",
            jobLocation: search.get("location")
        })


        // Clear old job results
        dispatch({
            type: 'search/set_jobs', jobResults: []
        })

        // Se loading to true
        dispatch({
            type: 'search/set_loading', loading: true
        })

        // Fetch job results based on user search
        fetch(SEARCH_URL + 'job=' + search.get("job") + '&location=' + search.get("location"))
            .then(res => res.json())
            .then(data => dispatch({

                type: 'search/set_jobs', jobResults: data,
            })
            )
            .catch(err => console.log('error loading results:', err));

    }, [location])

    // Update the pagination start and end information when page parameter is updated
    useEffect(() => {

        let newPage = search.get("page");
        if (newPage === null) {
            return
        }

        setjobPage(newPage);
        setResultStart(Number(newPage) === 1 ? 0 : (newPage - 1) * 20);
        setResultEnd((Number(newPage - 1) * 20 + 20));

    }, [search.get("page")])



    return (
        <>
            <div id="top" className="container p-5">

                {location.pathname === '/search' ?

                    jobResults && loading ?

                        // Information still loading - display spinnder
                        <div className="d-flex justify-content-center">
                            <div className="spinner-border" role="status">
                                <span className="visually-hidden">Loading...</span>
                            </div>
                        </div>
                        // Information loaded and path = search, display search results
                        : jobResults.results ?
                            <JobsDisplay
                                results={jobResults.results.slice(resultStart, resultEnd)}
                                job={job} jobLocation={jobLocation}
                                resultStart={resultStart}
                                resultEnd={resultEnd}
                                total={jobResults.total} />
                            :
                            <h2>Looks like you currently do not have any results</h2>
                    :
                    // Display favourites
                    favouriteJobs.length >= 1 ? <Favourites results={favouriteJobs.slice(resultStart, resultEnd)} />
                        :
                        <h2>Looks like you currently do not have any favourites</h2>
                }

                {
                    // Display pagination
                    jobResults.results && <Pagination
                        currentPage={jobPage}
                        pages={location.pathname === '/search' ? jobResults.total / 20 : favouriteJobs.length / 20}
                        job={job}
                        location={jobLocation}
                        pageType={location.pathname === '/search' ? "search" : "favourites"}
                    />
                }


            </div>
        </>
    )

}

export default SearchResults;