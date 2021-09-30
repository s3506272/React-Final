import { createStore } from 'redux'
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage' // defaults to localStorage for web

import rootReducer from './Reducer.js';

// Persist changes to redux state in local storage
// Whitelist favouriteJobs so that only it is syncd to local storage
const persistConfig = {
    key: 'root',
    storage,
    whitelist: ['favouriteJobs']
}

const persistedReducer = persistReducer(persistConfig, rootReducer)

export default () => {
    let store = createStore(persistedReducer,
        window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
    )
    let persistor = persistStore(store)
    return { store, persistor }
}
