import Job from '../job/Job';
import ResultInfo from '../ResultInfo/ResultInfo';

const jobResults = ({ results, job, jobLocation, resultStart, resultEnd, total }) => {
    return (
        <>
            {results && <ResultInfo job={job} location={jobLocation} start={resultStart} end={resultEnd} total={total} />}

            <section className="row g-5">

                {
                    results && results.map((jobDetails, index) => <Job key={"job-" + index} job={jobDetails} id={index} />)
                }
            </section>
        </>
    )

}

export default jobResults;