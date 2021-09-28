import './ResultInfo.css';

const ResultsInfo = (props) => {
    const { job, location, start, end, total } = props;
    return (

        <div className="row justify-content-between my-3 result-info">
            <div className="col-6">{job} in {location}</div>
            <div className="col-6 text-end">Displaying {start} - {end >= total ? total : end} of {total}</div>
        </div>

    );
}

export default ResultsInfo;
