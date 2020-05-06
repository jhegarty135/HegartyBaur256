#!/usr/bin/env python
# coding: utf-8

# In[16]:


pip install xmltodict


# In[ ]:


import xmltodict
import json
import requests
import pandas as pd
import numpy as np

key = "f935c022c103817c465fa3d33f64ed86"


# In[143]:


#Contributions to candidates from specific organizations

def candOrgs(key):
    cid = input('Enter the CID of the Candidate/Legislator whose Contributions from Organizations You Would Like To View: ')
    year = input("What cycle would you like to view? (2012, 2014, 2016, 2018, 2020): ")
    
    params = {'method' : 'candContrib', 'cid' : cid, 'cycle' : year, 'apikey' : key}

    url = "https://www.opensecrets.org/api"

    response = requests.get(url, params = params)
    response_string = response.content

    qwerty = xmltodict.parse(response_string)

    alob = qwerty['response']['contributors']['contributor']

    candOrgsTable = pd.DataFrame([])

    for alobs in alob:
        org = alobs['@org_name']
        indivs = alobs['@indivs']
        pacs = alobs['@pacs']
        total = alobs['@total']
        candOrgsTable = candOrgsTable.append(pd.DataFrame({'Org' : org, 'Indivs' : indivs, 'PACS' : pacs, 'Total' : total}, index=[0]))
    
    print("\n Showing organizations that contribute to", qwerty['response']['contributors']['@cand_name'])
    return candOrgsTable

candOrgs(key)


# In[142]:


#List of Legislators of a certain state purpose is to provide user with CID

def getLegislators(key, url):
    state = input("Enter an Abbreviated State (AL, AK, AZ, etc.): ")
    
    params = {'method' : 'getLegislators', 'id' : state, 'apikey' : key}

    url = "https://www.opensecrets.org/api"

    response = requests.get(url, params = params)
    response_string = response.content

    qwerty = xmltodict.parse(response_string)
    alob = qwerty['response']['legislator']

    getLegislatorsTable = pd.DataFrame([])

    for alobs in alob:
        name = alobs['@firstlast']
        cid = alobs['@cid']
        party = alobs['@party']
        getLegislatorsTable = getLegislatorsTable.append(pd.DataFrame({'Name' : name, 'CID' : cid, 'Party' : party}, index=[0]))
 
    print('\n Showing current Legislators for', state)
    return getLegislatorsTable

getLegislators(key)


# In[141]:


#Summary of specific info of a legislator based on CID obtained in previous step

def summLegislators(key):
    
    state = input("Enter a Candidates/Legislators CID: ")
    
    params = {'method' : 'getLegislators', 'id' : state, 'apikey' : key}

    url = "https://www.opensecrets.org/api"

    response = requests.get(url, params = params)
    response_string = response.content

    qwerty = xmltodict.parse(response_string)
    alob = qwerty['response']['legislator']
    
    summLegislatorsTable= pd.DataFrame([])

    name = alob['@firstlast']
    party = alob['@party']
    cid = alob['@cid']
    gender = alob['@gender']
    dob = alob['@birthdate']
    elected = alob['@first_elected']
    office = alob['@office']
    phone = alob['@phone']
    website = alob['@website']
    comments = alob['@comments']
    
    summLegislatorsTable = summLegislatorsTable.append(pd.DataFrame({'Name' : name, 'Party' : party, 'CID' : cid, 'Gender' : gender, 'DOB' : dob,
                                          'Elected in': elected, 'Office' : office, 'Phone Num' : phone,
                                          'Website' : website, 'Comments' : comments}, index=[0]))
    return summLegislatorsTable

summLegislators(key)


# In[140]:


#Contributions to a specific candidate based on industry

def candIndustry(key):
    
    cid = input("Enter Candidate/Legislator's CID: ")
    cycle = input("What cycle would you like to view? (2012, 2014, 2016, 2018, 2020): ")
    params = {'method' : 'candIndustry', 'cid' : cid, 'cycle' : cycle, 'apikey' : key}

    url = "https://www.opensecrets.org/api"

    response = requests.get(url, params = params)
    response_string = response.content

    qwerty = xmltodict.parse(response_string)
    alob = qwerty['response']['industries']['industry']
    cand_Ind_Table = pd.DataFrame([])

    for alobs in alob:
        name = alobs['@industry_name']
        code = alobs['@industry_code']
        indivs = alobs['@indivs']
        pacs = alobs['@pacs']
        total = alobs['@total']
        cand_Ind_Table = cand_Ind_Table.append(pd.DataFrame({'Industry' : name, 'Industry Code': code, 'Individuals' : indivs, 'PACS': pacs,
                                           'Total' : total}, index=[0]))
    print('\n Showing contributions by Industry for', qwerty['response']['industries']['@cand_name'])
    return cand_Ind_Table


candIndustry(key)


# In[ ]:





# In[160]:


#Final Program

import xmltodict
import json
import requests
import pandas as pd
import numpy as np

key = "f935c022c103817c465fa3d33f64ed86"

class color:
    BOLD = '\033[1m'
    END = '\033[0m'

while True:
    next_step = input("If you would like to see a list of Legislators and their CID (Candidate ID), type " + color.BOLD + "'State'" + color.END + ".\n"
    "\nIf you already have a CID, and you would like to view Summary data of a candidate, type " + color.BOLD + "'Summary'" + color.END + ".\n"
    "\nIf you already have a CID and you would like to view the top ten industries contributing to a specified candidate for a House or Senate seat or member of Congress, type " + color.BOLD + "'Industry'" + color.END + ". \n"
    "\nIf you already have a CID and you would like to view the leading contributing organizations for a  specified candidate for a House or Senate seat or member of Congress, type" + color.BOLD + " 'Orgs'" + color.END + ". \n"
    "\nIf you would like to exit, type 'Exit'. \n")
    
    if next_step == 'State':
        getLegis_df = getLegislators(key)
        display(getLegis_df)
    elif next_step == 'Summary':
        summ_df = summLegislators(key)
        display(summ_df)
    elif next_step == 'Industry':
        candInd_df = candIndustry(key)
        display(candInd_df)
    elif next_step == 'Orgs':
        candOrgs_df = candOrgs(key)
        display(candOrgs_df)
    elif next_step == 'Exit':
        print('Thank you for staying informed. Goodbye. :)')
        break


# In[ ]:




