# **************************************************************
# MAINTENANCE BOX
# 04.10: Ben O'Brien structured the functions into the Functions file / structure
# 11.10: Ben O'Brien updated JSON to include the Job URL
# 11.10: JC - Update source-website -> source (hyphen caused error on frontend)
# 14.11: Ben O'Brien included posting date as a field to be returned in the JSON
# 14.11: Ben O'Brien added function to format the post date from '3d ago' to '3 days ago'
# **************************************************************

# function to format a string from '1 of 100 jobs' to '100'
# used when returning the number of jobs in a search
def format_job_count(tmp_str):

    # remove whitespace
    tmp_str = tmp_str.strip()
    # remove chars on left of number
    tmp_str = tmp_str[tmp_str.find('of ') + 3: len(tmp_str)]
    # remove chars on right of number
    tmp_str = tmp_str[0: tmp_str.find(' ')]
    return tmp_str


# function to create a dictionary of job titles and corresponding salaries
def create_title_salary_dict(title, salary, source, post_date, job_url):


    # determine the number of jobs
    max_val = len(title)
    # create the collection
    salary_dict = []
    # loop through all jobs
    for i in range(max_val):
        salary_dict.append({
            'title': title[i],
            'salary': salary[i],
            'post-date' : post_date[i],
            'job-url': job_url[i],
            'source': source,
        })
    return salary_dict


# function to deal with none results for salaries
def format_salary_list(salaries):

    # determine the length of the list
    max_val = len(salaries)
    # loop through the list and update each entry as required
    for i in range(max_val):
        if salaries[i] is None:
            salaries[i] = "None available"
        else:
            salaries[i] = salaries[i].get_text().strip()
    return salaries

# function to format the number of jobs string for career one
def career_one_format_str(num):

    # 0 results
    if num[8] == '0':
        num = '0'

    # exactly 1 job
    elif num[8] == '1' and len(num) == 13:
        num = '1'

    # greater than 20 jobs
    elif '1 -' in num:
        pos = num.find('of ')
        num = num[pos + 3:]
        pos = num.find(' jobs')
        num = num[:pos]

    # less than 20 jobs
    else:
        pos = num.find(' jobs')
        num = num[8:pos]

    return int(num)

# function to generate JSON file
def export_json(seek, indeed, career_one, job_search):

    # create a tuple with all of the job websites
    websites = (seek, indeed, career_one, job_search)

    # create the dictionary for JSON output
    output = {'results': []}

    # loop through all jobs from all websites and add to dictionary
    for website in websites:
        for job in website:
            output['results'].append({
                'title': job['title'],
                'salary': job['salary'],
                'post-date': job['post-date'],
                'job-url': job['job-url'],
                'source': job['source'],
            })

    # export JSON
    return output

# function to format job post date from 1d ago to 1 day ago
def format_post_date(post_date):

    # for 1 day ago replace '1d' with '1 day ago'
    # check the first char is '1' and the second char is 'd' to prevent capturing 16
    if post_date[0] == '1' and post_date[1] == 'd':
        new_date = post_date.replace('d', ' day')

    # for greater than 1 day ago, replace 'd' with ' days ago' e.g. 5d ago becomes 5 days ago
    else:
        new_date = post_date.replace('d', ' days')


    return new_date
