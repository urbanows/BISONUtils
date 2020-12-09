#!/usr/bin/python

import sys
import os
import os.path
import getpass
from urllib.request import urlretrieve
import requests
import errno
import json
import zipfile
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=10, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

pageid=sys.argv[1]

#need to build from user input
user=input('AD Username: ')
passwd = getpass.getpass(prompt='Password: ')

def download(url,filename):
    response = session.get(url, auth=(user, passwd), stream=True)
    if response.status_code == 200:
        if response.headers.get('Content-Disposition'):
            print(response.headers.get('Content-Length'))
            #check content-length != 118 (empty zip)
            if response.headers.get('Content-Length') != '118':
              open(filename, 'wb').write(response.content)
            else:
              print('Empty zipfile encountered: '+filename)

def buildPath(pageid):
    #fullPath="./"
    fullPath=""
    #https://my.usgs.gov/confluence/rest/api/content/544051479?expand=ancestors
    ancestorUrl='https://my.usgs.gov/confluence/rest/api/content/'+pageid+'?expand=ancestors'
    response = session.get(ancestorUrl, auth=(user, passwd))
    jsonResp=response.json()
    for item in jsonResp["ancestors"]:
      #use OS path seperastors
      fullPath+="".join([x if x.isalnum() else "_" for x in item["title"]])+os.path.sep
    print(fullPath)
    return fullPath

def processPage(pageid,pageName):
    cleanPageName="".join([x if x.isalnum() else "_" for x in pageName])
    pagePath=buildPath(pageid)
    if not os.path.exists(pagePath):
      try:
        os.makedirs(pagePath)
      except OSError as e:
        if e.errno != errno.EEXIST:
          raise

    #Export a page as a Word doc:
    wordUrl='https://my.usgs.gov/confluence/exportword?pageId='+pageid
    output_filename = pagePath+cleanPageName+'.doc'
    download(wordUrl,output_filename)

    #Download zip of all page attachments:
    attachmentsUrl='https://my.usgs.gov/confluence/pages/downloadallattachments.action?pageId='+pageid
    output_filename = pagePath+'/'+cleanPageName+'_attachments.zip'
    download(attachmentsUrl,output_filename)

    #Unzip attachments
    if os.path.isfile(output_filename):
        with zipfile.ZipFile(output_filename, 'r') as zip_ref:
            zip_ref.extractall(pagePath+'/'+cleanPageName+'_attachments')
        #Delete zip file
        os.remove(output_filename)

    #This will return all children, need to call recursivly:
    childrenUrl='https://my.usgs.gov/confluence/rest/api/content/search?cql=parent='+pageid
    response = session.get(childrenUrl, auth=(user, passwd))
    jsonResp=response.json()
    for item in jsonResp["results"]:
      print(item["id"])
      buildPath(pageid)
      processPage(item["id"], item["title"])
    #https://my.usgs.gov/confluence/rest/api/content/489357375/child/page

initPageUrl='https://my.usgs.gov/confluence/rest/api/content/'+pageid
response = requests.get(initPageUrl, auth=(user, passwd))
jsonResp=response.json()
processPage(pageid,"".join([x if x.isalnum() else "_" for x in jsonResp["title"]]))
