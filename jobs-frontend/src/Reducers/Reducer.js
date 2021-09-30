import { combineReducers } from 'redux'
import FavouritesReducer from './FavouriteSlice.js'
import SearchReducer from './SearchSlice.js';

// TODO update project structure via feature folders 
// reducers stored in reducer folder for now

const rootReducer = combineReducers({
    // Define a top-level state field named search and favourite
    search: SearchReducer,
    favourite: FavouritesReducer
})

export default rootReducer
