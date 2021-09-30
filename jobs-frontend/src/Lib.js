const API_SEARCH_URL = 'https://jobsseach.azurewebsites.net/api/jobs?';


const JOB_PAGINATION = $ => `/${$.pageType}?job=${$.job}&location=${$.location}&page=${$.page}#top`;
const FAV_PAGINATION = $ => `/${$.pageType}?page=${$.page}#top`;

// Control number of paginations and jobs on each page
const NUMPAGES = 20;

export function getJobResults(search, location) {
    return fetch(API_SEARCH_URL + `job=${search}&location=${location}`)
        .then(res => res.json())
}

export { NUMPAGES, JOB_PAGINATION, FAV_PAGINATION };