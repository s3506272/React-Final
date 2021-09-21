# **************************************************************
# MAINTENANCE BOX
# 26.09: Ben O'Brien created the basic crawler functionality to search Seek.com.au and return job titles
# 27.09: Ben O'Brien updated Daniel's work to extend the search by job and location to indeed, career one and job search
# 27.09: Ben O'Brien added feature to extract the number of jobs returned in a search
# 27.09: Ben O'Brien added feature to extract the salary of jobs from indeed
# 03.10: Ben O'Brien added ability to search the top x pages of search results from Seek
# 03.10: Ben O'Brien added a timer to measure performance of the query
# 04.10: Ben O'Brien added ability to search the top x pages of search results from Indeed
# 04.10: Ben O'Brien added ability to export results for indeed to JSON
# 05.10: Ben O'Brien included salary in the search for SEEK
# 05.10: Ben O'Brien included SEEK results in the exported JSON file
# 07.10: JC - Restructed to Azure Function App
# 07.10: JC - Updated returned jobs to a function returning JSON
# 10.10: JC - Remove uneeded git merge files
# 10.10: Ben O'Brien added ability to extract the title of jobs from the first page of Job Search
# 11.10: JC - Uncomment CareerOne options until Azure Function Selenium integration is figured out
# 17.10: Ben O'Brien updated the main function so that it can run in non-server mode to support testing
# 17.10: Ben O'Brien added a timer for each individual web page performance
# 18.10: Ben O'Brien added the capability to search Neuvoo
# 31.10: Ben O'Brien added a class structure to the main file
# 31.10: Ben O'Brien added multi threading to the main file to allow all job searches to complete concurrently
# 22.11: Ben O'Brien added exception handling such that the crawler will return blank results if the naming conventions
# in one of the websites changes and an error exception thrown. Previously this errored out.
# **************************************************************


import time
import concurrent.futures

# imports are defined differently if this file is being run locally as opposed to on the server
# the file will be run locally for testing so both versions are supported
if __name__ == "__main__":

    from jobs.JobSearchClasses import SeekSearch
    from jobs.JobSearchClasses import IndeedSearch
    from jobs.JobSearchClasses import CareerOneSearch
    from jobs.JobSearchClasses import NeuvooSearch
    from jobs.Functions import *

else:

    from .JobSearchClasses import SeekSearch
    from .JobSearchClasses import IndeedSearch
    from .JobSearchClasses import CareerOneSearch
    from .JobSearchClasses import NeuvooSearch
    from .Functions import *


class Runtime:

    # constructor
    def __init__(self):
        # variables to store job results
        self._seek_job_results = None
        self._indeed_job_results = None
        self._career_one_job_results = None
        self._neuvoo_job_results = None

        # variables to store end time of searches
        self._end_seek = None
        self._end_indeed = None
        self._end_career_one = None
        self._end_neuvoo_time = None

        # variable to track any failures
        self._failure = []

    def search(self, job, location):

        # start the timer to measure performance of the query
        start = time.time()

        # create a collection of tuples to store url and source website
        # tuples allow one variable to be passed to the multi_threading func
        url = []
        search_job = job.replace(' ', '-')
        search_location = location.replace(' ', '-')

        # seek
        tup = ('seek', 'https://www.seek.com.au/' + search_job + '-jobs/in-' + search_location)
        url.append(tup)

        # indeed
        indeed_job = job.replace(' ', '+')
        indeed_location = location.replace(' ', '+')
        tup = ('indeed', 'https://au.indeed.com/jobs?q=' + indeed_job + '&l=' + indeed_location)
        url.append(tup)

        # career one
        tup = ('careerone', 'https://www.careerone.com.au/' + search_job + '-jobs/in-' + search_location)

        url.append(tup)

        # neuvoo
        tup = ('neuvoo', 'https://au.neuvoo.com/jobs/?k=' + search_job + '&l=' + search_location)
        url.append(tup)

        # display the urls
        print(url[0][1])
        print(url[1][1])
        print(url[2][1])
        print(url[3][1])

        # set the max number of threads
        threads = 4

        # complete the multi threading operation
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.multi_threading, url)

        # if any job search failed send an empty results dictionary
        if 'SEEK' in self._failure:
            seek_results = []
        else:
            seek_results = self._seek_job_results

        if 'INDEED' in self._failure:
            indeed_results = []
        else:
            indeed_results = self._indeed_job_results

        if 'CAREER' in self._failure:
            career_one_results = []
        else:
            career_one_results = self._career_one_job_results

        if 'NEUVOO' in self._failure:
            neuvoo_results = []
        else:
            neuvoo_results = self._neuvoo_job_results

        # generate JSON array for seek, indeed and jobsearch
        jobs = export_json(seek_results, indeed_results, career_one_results, neuvoo_results)

        # end timer for measuring overall performance
        end = time.time()

        # Count total processed jobs. Return zero results if there was an exception.

        len_seek = 0
        len_indeed = 0
        len_career_one = 0
        len_neuvoo = 0

        if self._seek_job_results is not None:
            len_seek = len(self._seek_job_results)

        if self._indeed_job_results is not None:
            len_indeed = len(self._indeed_job_results)

        if self._career_one_job_results is not None:
            len_career_one = len(self._career_one_job_results)

        if self._neuvoo_job_results is not None:
            len_neuvoo = len(self._neuvoo_job_results)

        total_saved = len_seek + len_indeed + len_career_one + len_neuvoo

        # display job results
        self.print_jobs(self._seek_job_results, 'Seek')
        self.print_jobs(self._indeed_job_results, 'Indeed')
        self.print_jobs(self._career_one_job_results, 'Career One')
        self.print_jobs(self._neuvoo_job_results, 'Neuvoo')

        # display time taken for searches
        seek_time = self._end_seek - start
        indeed_time = self._end_indeed - start
        career_one_time = self._end_career_one - start
        neuvoo_time = self._end_neuvoo - start

        print('\n')
        print(f'Overall time: {end - start} seconds')
        print(f'Seek time: {seek_time} seconds')
        print(f'Indeed time: {indeed_time} seconds')
        print(f'Career One time: {career_one_time} seconds')
        print(f'Neuvoo time: {neuvoo_time} seconds')

        # return the result for API consumption
        return jobs, (end - start), total_saved

    # helper function to support running job searches concurrently using multi threading
    def multi_threading(self, url):

        source, target_url = url

        if source == 'seek':
            self.seek(target_url)
        elif source == 'indeed':
            self.indeed(target_url)
        elif source == 'careerone':
            self.career_one(target_url)
        elif source == 'neuvoo':
            self.neuvoo(target_url)

    # SEEK
    def seek(self, url):

        try:

            # create instance of SeekSearch class and complete search
            seek = SeekSearch(url)
            seek.calc_jobs()
            seek_job_results = seek.get_jobs()

            # update results
            self._seek_job_results = seek_job_results

            # display the number of results
            print('\nJobs found on Seek:')
            print(f'{seek.get_num_jobs()} total jobs match your search ')
            num = len(seek_job_results)
            print(f'Number of jobs saved: {num}')
            print()


        # error message upon exceptions
        except:

            # if there is a failure update the failure collection
            self._failure.append('SEEK')
            print()
            print('SEEK search encountered unexpected error')

        # set end time of seek search
        self._end_seek = time.time()

    # INDEED
    def indeed(self, url):

        try:

            # instantiate the class and complete search
            indeed = IndeedSearch(url)
            indeed.calc_jobs()
            indeed_job_results = indeed.get_jobs()

            # update job results
            self._indeed_job_results = indeed_job_results

            # display the number of results
            print('Jobs found on Indeed: ')
            print(f'{indeed.get_num_jobs()} total jobs match your search ')
            num = len(indeed_job_results)
            print(f'Number of jobs saved: {num} ')
            print()

        # error message for any exceptions
        except:

            # if there is a failure update the failure collection
            self._failure.append('INDEED')

            print()
            print('INDEED search encountered unexpected error')

        # set end time of query
        self._end_indeed = time.time()

    # CAREER ONE
    def career_one(self, url):

        try:

            # instantiate the class and complete the search
            career_one = CareerOneSearch(url)
            career_one.calc_jobs()
            career_one_job_results = career_one.get_jobs()

            # update job results
            self._career_one_job_results = career_one_job_results

            # display the number of results
            print('Jobs found on Career One: ')
            print(f'{career_one.get_num_jobs()} total jobs match your search ')
            num = len(career_one_job_results)
            print(f'Number of jobs saved: {num} ')
            print()

        # error message for any exceptions
        except:

            # if there is a failure update the failure collection
            self._failure.append('CAREER')

            print()
            print('CAREER ONE search encountered unexpected error')

        # set end time of query
        self._end_career_one = time.time()

    # NEUVOO
    def neuvoo(self, url):

        try:
            # instantiate the class and complete the search
            neuvoo = NeuvooSearch(url)
            neuvoo.calc_jobs()
            neuvoo_job_results = neuvoo.get_jobs()

            # update job results
            self._neuvoo_job_results = neuvoo_job_results

            # display the number of results
            print('Jobs found on Neuvoo: ')
            print(f'{neuvoo.get_num_jobs()} total jobs match your search')
            num = len(neuvoo_job_results)
            print(f'Number of jobs saved: {num}')
            print()

        # error message for any exceptions
        except:

            # if there is a failure update the failure collection
            self._failure.append('NEUVOO')

            print()
            print("NEUVOO encountered unexpected error")

        # set end time of query
        self._end_neuvoo = time.time()

    # function to print results from any job_search_results
    def print_jobs(self, jobs, source):

        # display a message if no jobs are found, otherwise return the details of the jobs
        if jobs is None or len(jobs) == 0:
            print(f'No jobs found on {source}')
        else:
            print(f'\nJobs found on {source}:')
            for result in jobs:
                print(result['title'] + ' : ' + result['salary'] + ' : ' + result['source'])

# # TODO: used for testing - to be deleted
# def testModule(Job, Location):
#     # Generating and saving correct URLs with user input
#     url = []
#     SeekJob = Job.replace(' ', '-')
#     SeekLocation = Location.replace(' ', '-')
#     url.append('https://www.seek.com.au/' + SeekJob + '-jobs/in-' + SeekLocation)

#     IndeedJob = Job.replace(' ', '+')
#     IndeedLocation = Location.replace(' ', '+')
#     url.append('https://au.indeed.com/jobs?q=' + IndeedJob + '&l=' + IndeedLocation)

#     url.append('https://www.careerone.com.au/' + SeekJob + '-jobs/in-' + SeekLocation)
#     url.append('https://au.neuvoo.com/jobs/?k=' + SeekJob + '&l=' + SeekLocation)

#     # ######################################################################################
#     test_url = url[0]
#     tup = ('seek', test_url)
#     col = []
#     col.append(tup)
#     test_url = url[2]
#     tup = ('careerone', test_url)
#     col.append(tup)
#     rt = Runtime()
#     rt.multi_threading(col)
#     rt.print_jobs()


# def main():
#     # TODO: Delete testing code
#     Job = 'marketing'
#     Location = 'Sydney-nsw'
#     # testModule(Job,Location)
#     # exit()

#     rt = Runtime()
#     rt.search(Job, Location)


# if __name__ == "__main__":
#     main()