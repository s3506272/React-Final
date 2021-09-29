
const initialState = {
    favouriteJobs: []

};

// A reducer takes the current state, an action to perform on that state,
// optionally a payload within the action (which is like arguments for the action),
// and returns the new state after that action has been applied
export default function FavouriteReducer(state = initialState, action) {

    console.log("dsadsa", action.type)
    // The average reducer will use a switch block to examine the action
    // type and decide how to change state for that action
    // It must return the new value of state, and it should also be careful
    // not to lose any existing state
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
