const initialState = {
    favouriteJobs: []

};

export default function FavouriteReducer(state = initialState, action) {


    switch (action.type) {


        case "favourites/job_added":
            const newFav = [...state.favouriteJobs, action.jobFav];
            return {
                ...state,
                favouriteJobs: newFav
            };

        case "favourites/job_removed":

            const removeFaves = state.favouriteJobs.filter(job => job.id !== action.jobFav.id);

            return {
                ...state,
                favouriteJobs: removeFaves
            };

        default:

            return state;
    } // switch

} // reducer()
