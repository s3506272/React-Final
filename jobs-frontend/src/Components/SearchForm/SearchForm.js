import { useHistory, useLocation } from 'react-router-dom';
import { useForm } from "react-hook-form";
import { useSelector } from 'react-redux'
import './SearchForm.css';
import { Search, GeoAlt } from 'react-bootstrap-icons';

function SearchForm(props) {

    const location = useLocation();
    const history = useHistory();
    const loading = useSelector(state => state.search.loading); // Update the search button to a loading state when api call triggered

    const { register, handleSubmit, formState: { errors } } = useForm();


    // Push to the history path
    const onSubmit = data => {

        history.push({
            pathname: "/search",
            search: `?job=${data.searchJob}&location=${data.searchLocation}&page=1`
        });


    }

    return (
        <section className={`${location.pathname === "/" ? "pb-5 px-5 home-form" : "bg-form pt-3 pb-4"}`}>
            <div className={`container px-5 main-form`}>
                <form className="row" onSubmit={handleSubmit(onSubmit)}>
                    <div className="col-sm-5">
                        <div>
                            <label htmlFor="searchJob">What
                                <div>
                                    <input
                                        id="searchJob"
                                        type="text"
                                        aria-invalid={errors.searchJob ? "true" : "false"}
                                        placeholder="e.g. Web Developer"
                                        {...register("searchJob", { required: true, maxLength: 20 })}
                                    />
                                    <Search className="icon" />
                                </div>
                            </label>
                        </div>
                        {errors.searchJob?.type === 'required' && <p className="warning-text">Job is required</p>}

                    </div>
                    <div className="col-sm-5">
                        <div>
                            <label htmlFor="searchLocation">Where
                                <div>
                                    <input
                                        id="searchLocation"
                                        type="text"
                                        placeholder="Country, city, postcode"
                                        aria-invalid={errors.searchLocation ? "true" : "false"}
                                        {...register("searchLocation", { required: true, maxLength: 20 })}
                                    />
                                    <GeoAlt className="icon" />
                                </div>
                            </label>
                        </div>
                        {errors.searchLocation?.type === 'required' && <p className="warning-text">Location is required</p>}

                    </div>
                    <div className="col-sm-2 btn-search align-self-end">
                        <button className="btn btn-primary">{loading ? <><span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Search</> : "Search"}</button>
                    </div>
                </form>
            </div>
        </section>
    );
}

export default SearchForm;
