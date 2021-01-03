# Black-Chicago-BusinessBot
Black Chicago BusinessBot is a Twitter bot that sends tweets whenever a new business license is issued within the City of Chicago for a location within a majority-Black ward. The tweet will contain the business name, what kind of service(s) it provides, when it received a license and at what location the license was issued. There are 18 wards within Chicago where the majority of the population is Black. Although the businesses themselves may not be Black-owned, they still provide one indicator of the level of economic development in Black communities in Chicago. 

Credit to Chris Hagan's PermitBot https://github.com/chagan/permitbot for the basis of this bot.

# Setup for the Bot
Create Twitter account
Obtain Twitter API keys/secrets
Clone this repo to obtain files

# Python packages used
USAddresses https://github.com/datamade/usaddress
Pandas
URLLib
Tweepy
Logging
OS
String
Datetime

# Functions
Post_status(text): Posts the text passed to it containing the new business license info
Test_api(): Tests connection to Twitter API
Duplicate_check(id,file): Checks the license ID against a running list of license IDs to confirm any duplicates prior to posting to Twitter
Add_id_to_file(id,file): Adds the license ID to a list after posting it to Twitter. Will create a text file if one does not already exist and append to it after each run, assuming any new licenses are found
Get_data(limit,offset,days): Downloads a CSV file of license data from the Chicago Open Data Portal from the past day and creates a Pandas dataframe. 
Find_black(days=1): Calls get_data to retrieve a dataframe, creates a new dataframe that contains only licenses that have a ward number matching any of the 18 wards in a list called black_wards, and concantenates the text that will be tweeted. The usaddress parser helps to format the address in a more readable format. 
