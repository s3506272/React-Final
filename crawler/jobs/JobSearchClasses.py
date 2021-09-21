# **************************************************************
# MAINTENANCE BOX
# 04.10: Ben O'Brien structured the job searches into the JobSearchClasses file / structure
# 05.10: Ben O'Brien structured the classes into an Abstract Base Class and concrete implementation
# 05.10: Ben O'Brien added the functions for Career One to search the first page
# 10.10: Ben O'Brien updated the Career One class to integrate with Selenium class and search X pages of results
# 11.10: Ben O'Brien included Job Search number of results
# 11.10: Ben O'Brien included Job Search results from additional pages
# 11.10: Ben O'Brien included the ability for each website to include the job url in results
# 17.10: Ben O'Brien removed Selenium search from Career One and updated the new solution to use /page_x
# 17.10: Ben O'Brien identified and fixed bug where career one was not handling exactly 10 results correctly
# 17.10: Ben O'Brien updated career one to replace '~' with 'est.' for roles where the salary is estimated
# 18.10: Ben O'Brien created the Neuvoo class
# 31.10: Ben O'Brien improved the performance of Neuvoo class using multithreading
# 14.11: Ben O'Brien included posting date as a field to be returned in the JSON
# **************************************************************

import concurrent.futures
import requests
from . import Functions
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import logging
# re supports string searching as used in neuvoo search
import re

# set constant for the ADDITIONAL number of pages to be searched
MAX_PAGES = 2

# **********************************************************************************
# ABSTRACT BASE CLASS FOR JOB SEARCHES
# **********************************************************************************


class AbstractSearch(ABC):
    # constructor
    def __init__(self, url):

        # instance variables
        self._url = url
        self._num_results = 0
        self._num_jobs = 0
        self._job_dict = {}

        # establish a request session to avoid having to re-establish TLS connection on each page search
        self._requests_session = requests.Session()

        # specify soup variables, collection of soups required for Neuvoo
        self._soup = None
        self._soups = []

        # abstract constructor call
        super(AbstractSearch, self).__init__()

    # calculate the number of jobs
    @abstractmethod
    def calc_num_jobs(self):
        pass

    # getter to return the number of jobs
    @abstractmethod
    def get_num_jobs(self):
        pass

    # getter to return the jobs dictionary
    @abstractmethod
    def get_jobs(self):
        pass

    # complete the job search and update the jobs dictionary
    @abstractmethod
    def calc_jobs(self):
        pass

    # helper method to complete the jobs search
    @abstractmethod
    def job_search(self):
        pass


# **********************************************************************************
# SEEK CLASS
# **********************************************************************************
class SeekSearch(AbstractSearch):
    print("in seek")
    # calculate and return the number of jobs
    def calc_num_jobs(self):
        print("in seek 1")
        print("in seek 1: ", self._url)
        # create the soup for the first page
        _page = self._requests_session.get(self._url)
        self._soup = BeautifulSoup(_page.content, 'html.parser')

        # determine the number of results
        self._num_jobs = self._soup.find(attrs={"data-automation": "totalJobsCount"}).get_text()
        print("in seek 1: ", self._num_jobs)

    # getter to return the number of jobs
    def get_num_jobs(self):
        print("in seek 2: ", self._num_jobs)
        return self._num_jobs

    # getter to return the jobs dictionary
    def get_jobs(self):
        return self._job_dict

    # complete the job search and update the jobs dictionary
    def calc_jobs(self):
        print("in seek 3 : ", self._url)
        # start by calculating the number of jobs which is required to determine if there are any jobs to search
        self.calc_num_jobs()

        # only complete the search if there are results, otherwise update values for 0 results
        if self._num_jobs != '0':
            print("in seek 4")
            # create a collection of all links to the job pages
            all_pages = self._soup.find(class_='_1YM701W')
            list_pages = [item.get('href') for item in all_pages.find_all('a')]
            print('list_pages: ', list_pages )
            # if there are more than 1 links the last link will be 'next'
            # remove the next link
            if len(list_pages) > 1:
                list_pages.pop()

            # complete the search on the first page and update the _job_dict
            self._job_dict = self.job_search()

            # add to the collection of jobs from the next x pages
            max_pages = MAX_PAGES
            if len(list_pages) < max_pages:
                max_pages = len(list_pages)

            # loop through collection of URLs
            for i in range(max_pages):
                # update web page for the search
                next_url = 'http://seek.com.au' + list_pages[i]
                page = self._requests_session.get(next_url)
                self._soup = BeautifulSoup(page.content, 'html.parser')

                # create a collection of all the jobs from the current page
                temp_jobs_dict = self.job_search()

                # update the _job_dict with this page's results
                for item in temp_jobs_dict:
                    self._job_dict.append(item)

        else:
            self._job_dict = {}

        return self._job_dict

    # helper method to complete the jobs search
    def job_search(self):

        # specify the element which contains the results
        seek_jobs = self._soup.find(class_='_1UfdD4q')
        job_items = (seek_jobs.find_all('article', attrs={'data-automation': 'normalJob'}))

        # create collection of job titles from job_items
        titles = [item.get('aria-label') for item in job_items]

        # create a collection of salaries from job_items
        salaries = [item.find('span', attrs={'data-automation': 'jobSalary'}) for item in job_items]
        salaries = Functions.format_salary_list(salaries)

        # create a collection of posting dates, if there is no posting date append 'Not available'
        dates = []
        for item in job_items:
            value = item.find('span', attrs={'data-automation': 'jobListingDate'})
            if value is not None:
                # format the result to change '1d ago' to '1 day ago' etc.
                value = Functions.format_post_date(value.get_text().strip())
            else:
                value = 'Not available'
            dates.append(value)

        # create a collection of urls from job_items
        job_urls = []
        for item in job_items:

            link = item.find('a')
            # append link from h1 to the default seek url
            url = 'https://www.seek.com.au' + link['href']
            job_urls.append(url)

        # return a dictionary of job titles and salaries
        return Functions.create_title_salary_dict(titles, salaries, 'seek', dates, job_urls)


# **********************************************************************************
# INDEED CLASS
# **********************************************************************************
class IndeedSearch(AbstractSearch):

    # calculate and return the number of jobs
    def calc_num_jobs(self):

        # create the soup for the first page
        _page = self._requests_session.get(self._url)
        self._soup = BeautifulSoup(_page.content, 'html.parser')

        # only complete the search if there are results, otherwise update values for 0 results
        if self._soup.find(class_="bad_query") is None:
            # determine number of results
            results = self._soup.find(id='searchCountPages').get_text()
            # format the resulting string to isolate the number of jobs
            self._num_jobs = Functions.format_job_count(results)

        else:
            self._num_jobs = '0'

    # getter to return number of jobs
    def get_num_jobs(self):
        return self._num_jobs

    # getter to return the jobs dictionary
    def get_jobs(self):
        return self._job_dict

    # complete the job search and update the jobs dictionary
    def calc_jobs(self):

        # first calculate the number of jobs
        self.calc_num_jobs()

        # only complete the search if there are results, otherwise return an empty dictionary
        if self.get_num_jobs() != '0':

            # search the jobs on the first page
            self._job_dict = self.job_search()

            # review jobs on any subsequent pages

            # create a collection of all links to the job pages
            all_pages = self._soup.find(class_='pagination')

            # if there are multiple pages, create a collection of URLs
            if all_pages is not None:
                page_links = []

                for item in all_pages.find_all('li'):
                    page_links.append(item.get_text())

                # remove the first and 'next' page links
                page_links.pop(0)
                page_links.pop()

                # note URL structure to search other pages involves adding '&start=X'
                # create the list of URLs as per this structure
                list_pages = []
                for item in page_links:
                    temp_url = self._url
                    start_num = int(item)
                    start_num = (start_num - 1) * 10
                    additional_url = '&start=' + str(start_num)
                    list_pages.append(temp_url + additional_url)

                # iterate through the X next pages - note MAX_PAGES defined at top of file
                if len(list_pages) > 0:

                    max_pages = MAX_PAGES
                    if len(list_pages) < max_pages:
                        max_pages = len(list_pages)
                    counter = 0

                    while counter < max_pages:
                        # open next page
                        page = self._requests_session.get(list_pages[counter])
                        self._soup = BeautifulSoup(page.content, 'html.parser')

                        # create a dictionary of job titles and salaries
                        temp_indeed_dict = self.job_search()

                        # insert each new job / salary pair to the original indeedDict
                        for item in temp_indeed_dict:
                            self._job_dict.append(item)

                        counter += 1

        else:
            self._job_dict = {}

        return self._job_dict

    # helper method to complete the jobs search
    def job_search(self):

        # specify the element which contains the results
        jobs = self._soup.find(id='mosaic-provider-jobcards')

        # create a collection of all the jobs
        job_items = (jobs.find_all('a', recursive=False))


        # create a collection of all the title extracted from the job links
        titles = [item.find(class_='jobTitle').find('span', recursive=False).get_text() for item in job_items]

        # create a collection of all the salaries extracted from the job links
        salaries = [item.find(class_='salary-snippet') for item in job_items]

        salaries = Functions.format_salary_list(salaries)


        # create a collection of all the job posting dates, add 'not available' if date not found
        dates = []
        for item in job_items:
            value = item.find(class_="date")
            if value is not None:
                value = value.get_text()
            else:
                value = 'Not available'
            dates.append(value)


        # create a collection of all the job URLs extracted from the job links
        job_urls = []
        for item in job_items:

            link = item.attrs.get('data-jk')

            url = 'https://au.indeed.com/viewjob?jk=' + link
            job_urls.append(url)

        # return a dictionary of job titles and salaries
        return Functions.create_title_salary_dict(titles, salaries, 'indeed', dates, job_urls)


# **********************************************************************************
# CAREER ONE CLASS
# **********************************************************************************
class CareerOneSearch(AbstractSearch):

    # calculate the number of jobs
    def calc_num_jobs(self):

        # create the soup for the first page
        _page = self._requests_session.get(self._url)
        self._soup = BeautifulSoup(_page.content, 'html.parser')

        # extract the number of jobs from webpage
        num = self._soup.find(class_='srh-page').get_text()
        num = num.strip()

        # no results
        if self.search_empty() is True:
            num = '0'

        # else format the string to return the number of jobs
        self._num_results = Functions.career_one_format_str(num)

    # getter to return the number of jobs
    def get_num_jobs(self):
        return self._num_results

    # getter to return the jobs dictionary
    def get_jobs(self):
        return self._job_dict

    # complete the job search and update the jobs dictionary
    def calc_jobs(self):

        # start by calculating the number of jobs which is required by this method
        self.calc_num_jobs()

        # only complete the search if there are results
        if self.search_empty() is False:

            # search the first page
            self._job_dict = self.job_search()

            # if there are more than 20 jobs search subsequent pages
            if self._num_results > 20:

                # count the number of additional pages
                all_pages = self._soup.find(class_='pagination')
                all_pages = all_pages.find_all('li')

                # remove all non-numbers from the collection and create a collection of page numbers
                page_links = []
                for item in all_pages:
                    if item.get_text().isnumeric():
                        page_links.append(item.get_text())

                # remove the first page from the collection as it has already been searched
                page_links.pop()

                # determine the number of pages to be searched
                num = len(page_links)
                num = int(num)
                if num > MAX_PAGES:
                    num = MAX_PAGES

                # loop through the pages and generate a new soup to pass to job search
                for i in range(2, num + 2):
                    url = self._url + "/page_" + str(i)
                    page = requests.get(url)
                    self._soup = BeautifulSoup(page.content, 'html.parser')
                    temp_dict = self.job_search()
                    for item in temp_dict:
                        self._job_dict.append(item)

        else:
            # return an empty dict if there are no results
            self._job_dict = {}

        return self._job_dict

    # helper method to complete the jobs search
    # if the search is being used on a subsequent page a selenium derived soup will be provided
    def job_search(self):

        # specify the element which contains the results
        jobs = self._soup.find(class_='SearchJobLoop')

        # create a collection of all the jobs
        items = (jobs.find_all(class_='job__right'))

        # create a collection of all the titles, salaries and URLs extracted from the job links
        titles = []
        salaries = []
        job_urls = []
        dates = []

        for item in items:

            # title
            title = item.find('a').get_text()
            # strip the whitespace which is returned from career one query
            title = title.strip()
            # append to collection
            titles.append(title)

            # salary
            # check for None values as some jobs return no data other than a title
            salary = item.find(class_='job-card-salary__figure')
            if salary is not None:
                salary = salary.get_text()
            else:
                salary = 'not available'

            # strip the whitespace which is returned from career one query
            salary = salary.strip()
            # if salary starts with ~ this means salary is estimated, change ~ to est.
            if salary[0] == '~':
                salary = 'est. ' + salary[2:]
            # append to collection
            salaries.append(salary)

            # create a collection of posting dates, update 'not availble' if date cannot be found
            # note job posted date is stored in a different tag depending on whether it is > or < 1 day old
            # check the job date class for < 1 day old
            value = item.find(class_='job__date job-date')
            # if there is no value, check the job date class for > 1 day old
            if value is None:
                value = item.find(class_='job__date job-date is-bold')

            if value is not None:
                # format the result to change '1d ago' to '1 day ago' etc.
                value = Functions.format_post_date(value.get_text().strip())
            else:
                value = 'Not available'
            dates.append(value)

            # url
            link = item.find('a')
            url = 'https://www.careerone.com.au' + link['href']
            job_urls.append(url)

        # return a dictionary of job titles and salaries
        return Functions.create_title_salary_dict(titles, salaries, 'career-one', dates, job_urls)

    # helper method to determine if there are no search results
    def search_empty(self):

        # find the element which contains the error message
        test = self._soup.find(class_='search-message')

        # if the span does not exist return false
        if test is None:
            return False

        # extract the text from the span element
        test = test.find('span')
        test = test.get_text().strip()
        # if the span text starts with "Sorry" return true
        if 'Sorry' in test:
            return True
        else:
            return False


# **********************************************************************************
# NEUVOO CLASS
# NOTE: Neuvoo has a very slow return query, as such multi threading is used to
# create all three soups simultaneously
# this makes the structure of the Neuvoo class different to the other classes
# **********************************************************************************

class NeuvooSearch(AbstractSearch):

    # calculate the number of jobs
    def calc_num_jobs(self):

        # start by getting the soups for up to the first 3 pages
        self.get_soups()

        # extract the description string from the head which contains the number of jobs
        head = self._soup.find('head')
        content_tags = head.find_all('meta')
        content = content_tags[4].get('content')

        # strip all spaces as numbers greater than 999 include a space e.g. 1 250
        content = content.replace(' ', '')
        # extract the text between the first number and the first character
        start = re.search(r"\d", content)
        start = start.start()
        content = content[start:]
        end = re.search(r"\D", content)
        end = end.start()
        self._num_jobs = int(content[:end])

    # getter to return the number of jobs
    def get_num_jobs(self):
        return self._num_jobs

    # getter to return the jobs dictionary
    def get_jobs(self):
        return self._job_dict

    # complete the job search and update the jobs dictionary
    def calc_jobs(self):

        # calculate the number of jobs
        self.calc_num_jobs()

        # only complete the search if there are results, otherwise return an empty dictionary
        if self._num_jobs != '0':

            # add results from the first page
            self._job_dict = self.job_search()

            # add results from SECOND page if available using pre-defined soups
            if self._num_jobs > 26:
                self._soup = self._soups[1]
                _temp_dict = self.job_search()
                for item in _temp_dict:
                    self._job_dict.append(item)

            # add results from THIRD page if available using pre-defined soups
            if self._num_jobs > 52:
                self._soup = self._soups[2]
                _temp_dict = self.job_search()
                for item in _temp_dict:
                    self._job_dict.append(item)

        else:
            self._job_dict = {}

        return self._job_dict

    # method to update self._soups with all of the soups for the first three pages
    def get_soups(self):

        # page numbers
        page_nums = [1, 2, 3]

        threads = 3

        # use multi threading to create all of the soups simultaneously
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.get_soup, page_nums)

    # helper method to get each soup during multi threaded url request
    def get_soup(self, i):

        # format the first page without the page number
        if i == 1:
            url = self._url
        else:
            url = self._url + "p=" + str(i)

        # try block to return none if there is no additional pages
        try:
            # create the soup
            _page = self._requests_session.get(url)
            soup = BeautifulSoup(_page.content, 'html.parser')

            # if it is the first page being searched, set the soup for the class
            if i == 1:
                self._soup = soup

            self._soups.append(soup)

        except:
            return None

    # helper method to complete the jobs search
    def job_search(self):

        # specify the element which contains the results
        # note there can be multiple separated panels which contain job results
        jobs = self._soup.find(class_='joblist')
        jobs = jobs.find_all(class_='card card__job')

        # create a collection of all the title extracted from the job links
        titles = [item.find('a').get_text() for item in jobs]

        # create a collection of all the salaries extracted from the job links
        salaries = []
        for item in jobs:
            salary = item.find(class_='j-salary')
            if salary is None:
                salaries.append('None Available')
            else:
                salaries.append(salary.get_text())

        # create a collection of all the posting dates
        dates = []
        for item in jobs:
            dates.append('Not available')

        # create a collection of all the job URLs extracted from the job links
        job_urls = []
        for item in jobs:
            link = item.find('a')
            url = 'https://au.neuvoo.com' + link['href']
            job_urls.append(url)

        # return a dictionary of job titles and salaries
        return Functions.create_title_salary_dict(titles, salaries, 'neuvoo', dates, job_urls)

