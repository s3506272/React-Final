import { createStore } from 'redux'
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage' // defaults to localStorage for web

import rootReducer from './Reducer.js';

// Persist changes to redux state in local storage
// Whitelist favourite so that only it is syncd to local storage
const persistConfig = {
    key: 'root',
    storage,
    whitelist: ['favourite']
}

const persistedReducer = persistReducer(persistConfig, rootReducer)


export const store = createStore(persistedReducer,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
)
export const persistor = persistStore(store)
