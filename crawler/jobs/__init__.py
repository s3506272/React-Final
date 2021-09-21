# **************************************************************
# MAINTENANCE BOX
# 27.09: James Collins setup api to return jobs using Flask and requests
# 03.10: James Collins reconfigured api as Azure function app
# 05.10: James Collins Fixed bugs with import
# 13.10: JC - Convert function app to upload JSON file to blob storage
#             and return file name to requester
# 13.10: JC - Add Azure connection string as configuration setting
# 13.10: JC - Update to use Azure Function tmp storage folder
# 19.10: JC - Update to use Github actions workflow for push to server 2
# **************************************************************

# **************************************************************
# Function App Info
# Configured to run as an Azure (serverless) Function that is started
# by http requests
#
# requirements.txt = include any additional packages required here
# functions.json  = configuration settings for Azure function
# funcignore      = files not to be included in Azure function
# **************************************************************

import logging
import json
import tempfile
import azure.functions as func
from jobs.main import Runtime
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


# Processes http request through parameters in the url
# http://...:{port}/api/jobs/?job={title}&location={location}
#     
# Passes these as arguments to the runtime class in main
# and returns these to the calling ip as json for processing as
# {"results": [{"title","salary","website"}]}
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # gets parameters from the url
    job = req.params.get('job')
    location = req.params.get('location')
    if not job and not location:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            job = req_body.get('job')
            location = req_body.get('location')

    if job and location:

        # calls the job search function in main and saves the resulting tuples
        # jobs = json array to return
        # end = time search took
        # total saved = jobs processed
        try:
            #create instance of Runtime class from main file
            rt = Runtime()
            jobs, end, total_saved = rt.search(job,location)
            
            print(jobs, ' ', end, ' ', total_saved )

            if job and location:
                return func.HttpResponse(json.dumps(jobs), mimetype="application/json", status_code=200)
            else:
                # Function triggered but something went wrong
                return func.HttpResponse(
                    "HTTP trigger not successful",
                    status_code=404
                )
        except Exception as ex:
            print('Exception:')
            print(ex)
