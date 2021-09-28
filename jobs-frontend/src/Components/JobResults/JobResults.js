import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux'
import Job from '../job/Job';
import Pagination from '../Pagination/Pagination';
import ResultInfo from '../ResultInfo/ResultInfo';

const SEARCH_URL = 'https://jobsseach.azurewebsites.net/api/jobs?';

const SearchResults = (props) => {

    const location = useLocation();
    let search = new URLSearchParams(location.search);
    const dispatch = useDispatch();

    const [jobPage, setjobPage] = useState(1);
    const [jobLocation, setJobLocation] = useState('');
    const [job, setJob] = useState('');
    const [resultStart, setResultStart] = useState('');
    const [resultEnd, setResultEnd] = useState('');

    const jobResults = useSelector(state => state.jobResults);
    let jobs = jobResults.results && jobResults.results.slice(resultStart, resultEnd);
    const favouriteJobs = useSelector(state => state.favouriteJobs);

    useEffect(() => {

        if ((job === search.get("job") && jobLocation === search.get("location")) || !location.search) {
            return;
        }

        dispatch({
            type: 'jobs/set_jobs', jobResults: []
        })

        dispatch({
            type: 'jobs/set_loading', loading: true
        })


        fetch(SEARCH_URL + 'job=' + search.get("job") + '&location=' + search.get("location"))
            .then(res => res.json())
            .then(data => dispatch({

                type: 'jobs/set_jobs', jobResults: data,
            }),
                setJob(search.get("job")),
                setJobLocation(search.get("location"))
            )
            .catch(err => console.log('error loading results:', err));

    }, [search.get("job"), search.get("location")])

    useEffect(() => {
        let newPage = search.get("page");
        setjobPage(newPage);
        setResultStart(Number(newPage) === 1 ? 0 : (newPage - 1) * 20);
        setResultEnd((Number(newPage - 1) * 20 + 20));

    }, [search.get("page")])


    return (
        <>

            <div id="top" className="container p-5">

                {jobResults.results && <ResultInfo job={job} location={jobLocation} start={resultStart} end={resultEnd} total={jobResults.total} />}

                <section className="row g-5">

                    {
                        !jobResults.results ?
                            <div className="d-flex justify-content-center">
                                <div className="spinner-border" role="status">
                                    <span className="visually-hidden">Loading...</span>
                                </div>
                            </div>
                            :
                            jobs.map((jobDetails, index) => <Job key={"job-" + index} job={jobDetails} id={index} />)
                    }
                </section>

                {
                    jobResults.results && <Pagination currentPage={jobPage} pages={jobResults.total / 20} job={job} location={jobLocation} />
                }


            </div>
        </>
    )

}

export default SearchResults;