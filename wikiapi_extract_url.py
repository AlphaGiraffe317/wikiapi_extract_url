
# -*- coding: utf-8 -*-
# =============================================================================
"""
 Created on Thu Jul 22 12:58:08 2021
 
 @author: sssav
"""
"""
 Ronald Savage
 GTD 598 Summer 2021
 
"""
# =============================================================================



# =============================================================================
# """
# ******************************** READ FIRST ********************************
# 
# Before running this, you need to import wikipedia api package for python. In 
# the command prompt type:
#     "pip install wikipediaapi"
# this allows us to interact with wikipedia. Next, the list of articles should
# be a single column of article names with a header labeled "Article_Name". This
# file should also be saved as a .csv file. The name of this file needs to be:
#     "article_list"
# Therefor, the file should appear as "article_list.csv" for this code to run.
# 
# 
# There are some special characters that are not handled well in this code, so 
# people's names do not always work if they contain special characters. 
# 
# This code is slow, since it accesses wikipedia for each article. If the
# article list is short (100 article) it could take a minute to complete. If 
# the article list is long (2000 articles) it could take more than 10 minutes.
# Be patient if the list is long. My suggestion is to make a short test list.
# 
# There can also be errors when encoding the data to a new file (final_list.csv).
# Sometimes special characters cannot be written over. In this case the special
# character is replaced with the name of the character or just a question mark.
# 
# The final results should be checked for accuracy.
#
# For more detials on how to properly set up for this code, see the How_To.docx 
# document.
#
# 
# """
# =============================================================================


import wikipediaapi
# this is the new wikipedia package

import pandas as pd
# pandas package to handle our data

import urllib.parse
# this is supposed to convert the strange special characters back 

import requests
# this will allow us to search for the closest match if the article does not
    # have an exact match

wiki_wiki = wikipediaapi.Wikipedia('en')
# we are working with english wikipedia

url_list = []
# just a list to hold the urls pulled from each page

articles = pd.read_csv("article_list.csv", encoding='UTF-8')
# Math_Article_List.csv is just a single column with all of
    # the article names in the first column with a header 
    # labelled 'Article_Name'
    
approx = [0] * len(articles)
# this is the last column which will tell us if an entry has been approximated

"How to get the wikipedia Page URL"


for i in range(len(articles)):
    
    current_page = articles.at[i, 'Article_Name']
    
    wiki_page = wiki_wiki.page(current_page)
    
    try:
        page_url = wiki_page.fullurl
        
    except:
        exsisting = "Page - Exists: %s" %     wiki_page.exists()
        
        if exsisting == 'Page - Exists: False':
            # if the specified page does not exist, then there might not be
                # an exact match for the article. Below is an attempt at 
                # searching for the closest match to the desired article.
            try:
                S = requests.Session()
                # starts the request session
        
                URL = "https://en.wikipedia.org/w/api.php"
                # the URL for the wiki api
                
                PARAMS = {
                    "action": "opensearch",
                    "namespace": "0",
                    "search": current_page,
                    "limit": "1",
                    "format": "json"
                }
                # these are the parameters for the search. the action is to do
                    # an open search. search: is the string that we are searching
                    # for. limit: is the number of results that we want. You can
                    # have more results, but I have it so that only the top result
                    # will be used. This is not a good technique for people's names
                    # where their may be multiple results and special care should
                    # be taken with common names. format: is just the default 
                    # output type.
                
                R = S.get(url=URL, params=PARAMS)
                # runs the search
                
                new_page = R.json()
                
                wiki_page = wiki_wiki.page(new_page[1][0])
                # assigns the wikipedia page of the top result
                
                page_url = wiki_page.fullurl
                
                approx[i] = 'URL and Kiwix strings are approximated'
            except:
                page_url = 'ERROR'
        else:
            page_url = 'ERROR'
            # if all that has failed then the result will be ERROR so that we
                # can handle this manually
    
    url_list.append(page_url)
    # add this url onto the list

"Kiwix Format"

kiwix_link = []
# this will be the list we have our kiwix formatted strings

for k in range(len(url_list)):
    # for each page link we have
    
    k_str = url_list[k].rsplit('/', 1)[-1]
    # split the url on the last / and return everything to the right
        # of that marker.
        
    kiwix_link.append(k_str) 
    # now that we have the kiwix formatted text, add it to the list



kiwix_formatted = []
for item in kiwix_link:
    kiwix_formatted.append(urllib.parse.unquote(item))
    # this decodes the HTTP special characters from the URL

"final stuff - add it all together"

final = articles
# making a new array for the changes coming up
final['HyperLink'] = url_list
# add a new column for the hyperlinks, which will be filled by page_link
final['Kiwix'] = kiwix_formatted
# add another column for the kiwix links, same as above
final['Warnings'] = approx
# a final column that adds a warning if the results have been approximated
final.to_csv("final_list.csv", index = False, header = True\
             , encoding='UTF-8', errors = "namereplace")
# write all this new data to a csv file so we can use it