import { useDispatch, useSelector } from 'react-redux'
import './Job.css';
import { Heart as OutLine, HeartFill as Full } from 'react-bootstrap-icons';
import React from 'react';

const Job = (props) => {

    const { "job-url": url, "post-date": date, salary, source, title } = props.job;

    const favouriteJobs = useSelector(state => state.favouriteJobs);
    const dispatch = useDispatch();

    const handleFaveToggle = (ev) => {

        const indexOf = favouriteJobs.indexOf(props.job);

        dispatch({
            type: `favourites/${indexOf === -1 ? "job_added" : "job_removed"}`,
            jobFav: props.job
        })

    }

    const isFav = () => {

        const indexOf = favouriteJobs.indexOf(props.job);

        const star = indexOf === -1 ? <React.Fragment>{"Save"} <OutLine /> </React.Fragment> : <React.Fragment>{"Saved "} <Full /> </React.Fragment>;
        return star;
    }

    return (
        <>
            <div className="col-sm-6">

                <article >
                    <div className="px-4 py-3 title">
                        <h2>
                            {title}

                        </h2>
                        {<span onClick={(ev) => handleFaveToggle(ev)}>{isFav()} </span>}
                    </div>

                    <div className="py-4 px-4">
                        <div className="row justify-space-between">
                            <div className="col-7">
                                <h3 >Salary: {salary}</h3>
                                <p className="">Posted: {date}</p>
                            </div>
                            <div className="col-5 text-end">
                                <a className="btn btn-primary" target="_blank" rel="noopener" href={url}>Apply on {source}</a>
                            </div>
                        </div>


                    </div>

                </article>
            </div >
        </>
    )

}

export default Job;