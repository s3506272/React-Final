const initialState = {
    jobResults: [],
    jobPage: 1,
    jobName: '',
    jobLocation: "",
    loading: false
};

export default function SearchReducer(state = initialState, action) {

    switch (action.type) {

        case "search/set_jobs":
            return {
                ...state,
                jobResults: action.jobResults,
                loading: !state.loading
            };

        case "search/set_loading":
            return {
                ...state,
                loading: true
            };

        case "search/job_added":
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
