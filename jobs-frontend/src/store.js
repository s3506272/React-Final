import { createStore } from 'redux';

const initialState = {
    jobResults: [],
    favouriteJobs: [],
    jobPage: 1,
    loading: false
};

// A reducer takes the current state, an action to perform on that state,
// optionally a payload within the action (which is like arguments for the action),
// and returns the new state after that action has been applied
function reducer(state = initialState, action) {


    // The average reducer will use a switch block to examine the action
    // type and decide how to change state for that action
    // It must return the new value of state, and it should also be careful
    // not to lose any existing state
    switch (action.type) {

        case "jobs/set_jobs":

            return {
                ...state,
                jobResults: action.jobResults,
                loading: !state.loading
            };

        case "jobs/set_loading":

            return {
                ...state,
                loading: true
            };


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



// TODO: load saved state from localStorage here?


export const store = createStore(
    reducer,
    // 2nd optional arg: initial state provided by localStorage(), possible merge with initialState variable?
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);
// export store;

// // TODO: subscribe to changes to the store, for example to save to localStorage:
// store.subscribe(() => {
//     const state = store.getState();
//     console.log('store subscribe callback!', state);
//     // serialise state and save to localStorage here after every change?
// });