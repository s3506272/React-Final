
const initialState = {
    jobResults: [],
    jobPage: 1,
    jobName: '',
    jobLocation: "",
    loading: false
};

// A reducer takes the current state, an action to perform on that state,
// optionally a payload within the action (which is like arguments for the action),
// and returns the new state after that action has been applied
export default function SearchReducer(state = initialState, action) {

    console.log("dsadsa", action.type)
    // The average reducer will use a switch block to examine the action
    // type and decide how to change state for that action
    // It must return the new value of state, and it should also be careful
    // not to lose any existing state
    switch (action.type) {

        case "search/set_jobs":
            console.log("resutls")
            return {
                ...state,
                jobResults: action.jobResults,
                loading: !state.loading
            };

        case "search/set_loading":
            console.log("loading")
            return {
                ...state,
                loading: true
            };

        case "search/job_added":
            console.log("added")
            return {
                ...state,
                jobName: action.jobName
            };

        case "search/location_added":

            return {
                ...state,
                jobLocation: action.jobLocation
            };

        default:

            return state;
    } // switch

} // reducer()
