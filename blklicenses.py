# -*- coding: utf-8 -*-
"""
This is a Twitter bot that will tweet when a new business license is issued within a majority-black
ward within the City of Chicago.
"""

import string, usaddress, pandas as pd, urllib.parse, os, urllib.error, tweepy, logging
from datetime import datetime, timedelta, date
from config import config


def post_status(text):
    auth = tweepy.OAuthHandler(config['consumer_key'],config['consumer_secret'])
    auth.set_access_token(config['access_token_key'],config['access_token_secret'])
    api = tweepy.API(auth,wait_on_rate_limit=True,
                    wait_on_rate_limit_notify=True)
    status = api.update_status(text)

def test_api():
    logger = logging.getLogger()
    try:
        api.VerifyCredentials()
    except Exception as e:
        logger.error("Error creating API",exc_info=True)
        raise e
    logger.info("API created")
    return api

# Check if a license has already been tweeted by comparing against external file of ids
def duplicate_check(id,file):
    if not os.path.isfile(file):
        open(file, 'w+')
    found = 0
    with open(file, 'r') as idfile:
        for line in idfile:
            if id in line:
                found = 1
    return found

# Write id to external file
def add_id_to_file(id,file):
    with open(file, 'a') as file:
        file.write(str(id) + "\n")
        
def get_data(limit=1000,offset=0,days=1):
    days = int(days)
    endpoint = 'https://data.cityofchicago.org/resource/r5kz-chrr.csv?'
    
    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')
    today = date.today().strftime('%Y-%m-%dT%H:%M:%S')
    query = "$where=date_issued between '{}' and '{}'".format(yesterday, today)
    qquery = urllib.parse.quote(query, '=&?$')
    url = endpoint+qquery
    try:
        licenses = pd.read_csv(url)
        return licenses
    except urllib.error.HTTPError as error:
        print(error.read())

        
def find_black(days=1):
    licenses = get_data(days=days)
    black_wards = ['3','4','5','6','7','8','9','16','17','18','20','21','24','27','28','29','34','37']
    black_licenses = licenses[licenses['ward'].isin(black_wards)]
    new_black_licenses = black_licenses[black_licenses['application_type'] == 'ISSUE']  
    for ind in new_black_licenses.index:
        id = new_black_licenses['id'][ind]
        dupe = duplicate_check(id,'tweeted_license_ids.txt')
        if dupe == 0:
            business_acts = new_black_licenses['business_activity'][ind].split(' | ')
            address = usaddress.tag(string.capwords(new_black_licenses['address'][ind]))
            if 'StreetNamePostType' in address[0]:
                address_reformat = address[0]['AddressNumber'] + " " + address[0]['StreetNamePreDirectional'] + " " + address[0]['StreetName'] + " " + address[0]['StreetNamePostType']
            else:
                address_reformat = address[0]['AddressNumber'] + " " + address[0]['StreetNamePreDirectional'] + " " + address[0]['StreetName']

            text = "Hey! A new business in our community! " + new_black_licenses['doing_business_as_name'][ind].upper() + " was licensed for " + business_acts[0].lower() + " on " + datetime.strftime(datetime.fromisoformat(new_black_licenses['date_issued'][ind]),'%B %d') + " at " + address_reformat
            print(text)
            post_status(text)
            add_id_to_file(id,'tweeted_license_ids.txt')
            
find_black(days=1)