# Job Search

:star: Star us on GitHub!

Job Search is a webcrawler job collation service, that will help you find and get the job of your dreams!

Job search sites such as Seek and Indeed often have different results. We live crawl these websites based on user requests and collate them in one place to 
reduce the number of sites you have to crawl through. 

    Contains the code required to run the job crawler and frontend react website that interfaces with the crawler.
    The crawler is a python application using the Beautiful Soup 4, Requests and Azure-Functions packages 
    to crawl a whitelist of websites based on user preferences.
    It is packaged as an Azure Function app and runs on the Azure Function Service responding to Http requests.
    
    The front end website is a React application that provided all the fronted display and filtering of the job results.


## Table of content

- [Features](#features)
    - [Crawler](#crawler)
    - [Website](#website)
- [How it Works](#how-it-works)
- [API](#API)
- [To be developed](#features-to-be-developed)
- [Links](#links)


## Features

### Crawler
* Scans job post websites such as seek.com to obtain job information
* Searches for jobs based on the job title and location
* Respons to HTTP API requests through url parameters
* Returns search results in JSON format with, title, salary, url, and source website

### Website
* Takes user input and submits this as an api request with jobname and location to the crawler
* Displays results to user with pagination
* Allows a user to favourite a job to come back to later
* Users can switch between results and favourites

## How it Works

### Search system

    When a user enters correct information into the search form it sends a HTTP request the Web Crawler Azure Function App.
    
    This then live crawls the relevant websites, turns results into JSON and returns the results to the frontend.
    
    The website gets the results, stores them in a redux store and displays the results to the user.
    
### Favourites

    A job result can be favourited by a user. When a job is favourited it is stored in a redux store and also syncd with 
    browser local storage using persis redux react so that a user can revisit them later.

### FrontEnd Website Implementation

    The website is currently hosted as an Azure App Service on the basic development plan
    Github actions are used to build and deploy to the app service on a push to the Master branch

## API

### Job searches

Get: https://jobsseach.azurewebsites.net/api/jobs?job={title}&location={location}

Parameters
* Job: Search websites for results based on the job title
* location: Search websites for results based on the location of jobs

## Features TO BE DEVELOPED

### Frontend
* Filtering of results: Filter results by Source, Salary, Date
* Application tracking: Tracking of application process through job favourites
* Accounts system: Using Azure ADB2C to handle login and credentials

### Crawler
* Crawl more information: Exact location, categories, Key selection criteria, etc
* Pagination: Crawling capped to top 3 pages to be a kind crawler and reduce results, add page field to api to start from there
* Crawl caching: Save crawls in database with hash of results and search keys so that a database of jobs can be served instead of live crawling

## Links
* Website: https://jobsearchproject.azurewebsites.net/

## Disclaimer
This project is being developed as part of a General Assembly React Bootcamp.
