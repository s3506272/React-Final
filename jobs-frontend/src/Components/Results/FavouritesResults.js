
import Job from '../job/Job';

const Favourites = ({ results }) => {
    return (
        <section className="row g-5">
            {
                results.map((jobDetails, index) => <Job key={"fav-" + index} job={jobDetails} id={index} />)
            }

        </section>
    )
}

export default Favourites;