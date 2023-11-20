#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


# In[2]:


# define url
url = 'https://www.jobberman.com/jobs/software-data?sort=featured'


# In[3]:


#headers for request
HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0', 'Accept-Language':'en-US, en;q=0.5'})


# In[4]:


#http request
webpage = requests.get(url, headers=HEADERS)


# In[5]:


webpage


# In[6]:


type(webpage.content)


# In[7]:


#soup objects containing all data
soup = BeautifulSoup(webpage.content, "html.parser")


# In[8]:


soup


# In[9]:


#fetch links as list of tag objects
links = soup.find_all("a", attrs={'class':'relative mb-3 text-lg font-medium break-words focus:outline-none metrics-apply-now text-link-500 text-loading-animate'})


# In[10]:


#check if you get proper links
links


# In[11]:


# extract the specific link
link = links[0].get('href')


# In[12]:


link


# In[13]:


#http request
new_webpage = requests.get(link, headers=HEADERS)


# In[14]:


new_webpage


# In[15]:


#soup objects containing all data
new_soup = BeautifulSoup(new_webpage.content, "html.parser")


# In[16]:


new_soup


# In[62]:


#get jobtitle
job_title = new_soup.find("h1", attrs={"class":'mt-6 mb-3 text-lg font-medium text-gray-700 md:mb-4 md:mt-0'}).text
print(job_title)


# In[61]:


#get job description
job_description = new_soup.find("p", attrs={"class":'mb-4 text-sm text-gray-500'}).text.strip()
print(job_description)


# In[38]:


#get job requirement
new_soup.find("li", attrs={"style":'word-break: break-word;'})

for li in new_soup.find_all("li", attrs={"style":'word-break: break-word;'}):
    if 'experience' in li.text:
        print(li.text)


# In[60]:


#Job type
#get job type
job_type = new_soup.find("a", attrs={"class":'text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block'}).text.strip()
print(job_type)


# In[55]:


#Industry
# Find all elements with the same class
sector = new_soup.find_all("a", attrs={"class":'text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block'})

# Check if there are at least two elements
if len(sector) >= 2:
    # Get the second element
    industry = sector[1].text
    print(industry)
else:
    print("no industry")


# In[59]:


#Salary
# Find all elements with the same class
pay = new_soup.find_all("span", attrs={"class":'text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block'})

# Check if there are at least two elements
if len(pay) >= 2:
    # Get the second element
    salary = pay[1].text.strip()
    print(salary)
else:
    print("no salary")


# In[68]:


# Function to extract Job Title
def get_title(soup):
    try:
        title = soup.find("h1", attrs={"class":'mt-6 mb-3 text-lg font-medium text-gray-700 md:mb-4 md:mt-0'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

# Function to extract Job Description
def get_description(soup):
    try:
        description = soup.find("p", attrs={"class":'mb-4 text-sm text-gray-500'}).text.strip()
    except AttributeError:
        description = ""
    return description

# Function to extract Job Requirement
def get_requirement(soup):
    requirement = ""
    try:
        for li in soup.find_all("li", attrs={"style":'word-break: break-word;'}):
            if 'experience' in li.text:
                requirement = li.text
    except AttributeError:
        requirement = ""
    return requirement

# Function to extract Job_type
def get_job_type(soup):
    try:
        job_type = soup.find("a", attrs={"class":'text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block'}).text.strip()
    except AttributeError:
        job_type = ""	
    return job_type

# Function to extract industry
def get_industry(soup):
    industry = ""
    try:
        sector = soup.find_all("a", attrs={"class":'text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block'})
        if len(sector) >= 2:
            industry = sector[1].text.strip()
    except AttributeError:
        industry = "no industry"
    return industry

# Function to extract salary
def get_salary(soup):
    salary = ""
    try:
        pay = soup.find_all("span", attrs={"class":'text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block'})
        if len(pay) >= 2:
            salary = pay[1].text.strip()
    except AttributeError:
        salary = "no salary"
    return salary


# In[72]:


if __name__ == '__main__':
    
    #add your user agent
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0', 'Accept-Language':'en-US, en;q=0.5'})
    
    # The  webpage url
    URL = "https://www.jobberman.com/jobs/software-data?sort=featured"
    
    #http request
    webpage = requests.get(URL, headers=HEADERS)
    
    #soup object containinng
    soup = BeautifulSoup(webpage.content, "html.parser")
    
    #Fetch links 
    links = soup.find_all("a", attrs={'class':'relative mb-3 text-lg font-medium break-words focus:outline-none metrics-apply-now text-link-500 text-loading-animate'})
    
    links_list = []
    
    #Loop for extracting links from link list
    for link in links:
        links_list.append(link.get('href'))
    
    d = {"title":[], "description":[], "requirement":[], "job_type":[], "industry":[], "salary":[]}
    
    #Loop for extracting all job details from each link
    for link in links_list:
        new_webpage = requests.get(link, headers=HEADERS)
        
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        
        
        #Functions to dislay all job details
        d['title'].append(get_title(new_soup))
        d['description'].append(get_description(new_soup))
        d['requirement'].append(get_requirement(new_soup))
        d['job_type'].append(get_job_type(new_soup))
        d['industry'].append(get_industry(new_soup))
        d['salary'].append(get_salary(new_soup))
    
    df = pd.DataFrame.from_dict(d)
    df['title'].replace('', np.nan, inplace=True)
    df = df.dropna(subset=['title'])
    df.to_csv("jobberman_data.csv", header=True, index=False)


# In[65]:


df


# In[76]:


# Scraping through different pages
# Function to extract Product Title
# ... (your function definitions go here) ...

if __name__ == '__main__':
    
    #add your headers
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0', 'Accept-Language':'en-US, en;q=0.5'})
    
    #define your url
    URL = "https://www.jobberman.com/jobs/software-data?sort=featured&page="
    
    #create an empty dataframe to store details
    d = {"title":[], "description":[], "requirement":[], "job_type":[], "industry":[], "salary":[]}

    # Loop over the pages
    for page in range(1, 17):
        webpage = requests.get(URL + str(page), headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        links = soup.find_all("a", attrs={'class':'relative mb-3 text-lg font-medium break-words focus:outline-none metrics-apply-now text-link-500 text-loading-animate'})
        links_list = []
        
        #Loop for extracting links from link list
        for link in links:
            links_list.append(link.get('href'))

        
        #Loop for extracting all job details from each link
        for link in links_list:
            new_webpage = requests.get(link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")
            
            #Functions to dislay all job details
            d['title'].append(get_title(new_soup))
            d['description'].append(get_description(new_soup))
            d['requirement'].append(get_requirement(new_soup))
            d['job_type'].append(get_job_type(new_soup))
            d['industry'].append(get_industry(new_soup))
            d['salary'].append(get_salary(new_soup))

    df = pd.DataFrame.from_dict(d)
    df['title'].replace('', np.nan, inplace=True)
    df = df.dropna(subset=['title'])
    df.to_csv("jobberman_data.csv", header=True, index=False)


# In[77]:


df


# In[85]:


df.to_csv(r"C:\Users\Olamilekan .A. David\Downloads\jobberman_data.csv", index=False)


# In[86]:


df.to_excel(r"C:\Users\Olamilekan .A. David\Downloads\jobberman_data.xlsx", index=False)


# In[ ]:




