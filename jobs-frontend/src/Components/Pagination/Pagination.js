import React from 'react';
import { HashLink } from 'react-router-hash-link';
import './Pagination.css';
import { JOB_PAGINATION, FAV_PAGINATION, NUMPAGES } from '../../Lib.js';

// Generate a pagination section with hops of 20 based on the current page number
// Might want to update to keep in lie with slideshow at some stage
// maybe add in a manual page entry and ability to control the number of pages shown
const Pagination = ({ currentPage, pages: totalPages, job, location, pageType }) => {
    let BASELINKURL;
    pageType === "search" ?
        BASELINKURL = JOB_PAGINATION :
        BASELINKURL = FAV_PAGINATION
        ;


    // Round the start down to the nearest NUMPAGES e.g. 99 will display 1-100 with NUMPAGES = 100
    // Return 1 if starting at 0 since one makes more sense as a first page
    const getPaginationStart = () => {

        let paginationStart = Math.floor(currentPage / NUMPAGES) * NUMPAGES;
        return paginationStart === 0 ? 1 : paginationStart;
    }

    const generatePagination = () => {

        let pageLinks = [];

        let pageStart = getPaginationStart();;

        let pageEnd = pageStart === 1 ? NUMPAGES : pageStart + NUMPAGES;

        // Handle under NUMPAGES of results returned
        if (totalPages <= pageEnd) {
            pageEnd = Math.ceil(totalPages);
        }

        // Update this to HashNavLink and use active class instead
        for (let page = pageStart; page <= pageEnd; page++) {

            pageLinks.push(
                <HashLink key={"pagina-" + page} to={BASELINKURL({ pageType, job, location, page })} className={Number(currentPage) === page ? "current" : ''}>{page}</HashLink>
            )
        }

        // Add arrow to return to start of pagination when above 20 
        // Add first arrow to start of pageLinks to return to previous 20
        if (pageEnd > NUMPAGES) {
            pageLinks.unshift(
                (pageStart !== NUMPAGES) && <HashLink key={"pagina-start"} to={BASELINKURL({ pageType, job, location, page: 1 })} className="state">&lt;&lt;</HashLink>,
                <HashLink key={"pagina-previous"} to={BASELINKURL({ pageType, job, location, page: pageStart - (pageStart === NUMPAGES ? NUMPAGES - 1 : NUMPAGES) })} className="page-prev">&lt;</HashLink>
            )
        }

        // Add end arrow to end of PageLinks
        if (pageEnd >= NUMPAGES && pageEnd < (totalPages - NUMPAGES)) {
            pageLinks.push(
                <HashLink key={"pagina-next"} to={BASELINKURL({ pageType, job, location, page: pageEnd })} className="page-next">&gt;</HashLink>,
                <HashLink key={"pagina-end"} to={BASELINKURL({ pageType, job, location, totalPages })} className="end">&gt;&gt;</HashLink>

            )
        }

        return pageLinks;
    }


    return <div className="pagination mt-5">{generatePagination()}</div>;

}

export default Pagination;