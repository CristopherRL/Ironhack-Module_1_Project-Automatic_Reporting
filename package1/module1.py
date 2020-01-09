# Importing libraries
import pandas as pd
from sqlalchemy import create_engine
import re

######################################### IMPORTING DATA #################################################

# Using sqlalchemy to connect with the file which contains the  messy dataset Forbes Billionaires 2018
file_name = "CristopherRL.db"
data_location = "sqlite:///../data/raw/"
engine = create_engine(f'{data_location}{file_name}')

# Creating a query to incorporate all 3 tables in one with all the necessary information
query = """ 
SELECT 
personal_info.id, 
position, 
lastName, 
rank_info.name, 
age, 
personal_info."Unnamed: 0", 
gender, 
country, 
image, 
business_info.Source,
business_info.worth,
business_info.worthChange,
business_info.realTimeWorth
FROM personal_info
LEFT JOIN rank_info     ON personal_info.id = rank_info.id
LEFT JOIN business_info ON personal_info.id = business_info.id
ORDER BY position
;
"""

# Importing data from db file to dataframe
raw_data = pd.read_sql_query(query, engine)

#proc_data DataFrame will be the clean dataset
proc_data = raw_data

############################################## CHANGING DATA ###########################################

###### AGE
def real_age(x):
    
    if x is None:
        return 999 #to identify which doesnt have age informatio
    
    else:
        y = re.findall('[\d]+',x) # extracting y from "y years". The last on is '99 years'
        if int(y[0])<100:
            return int(y[0])
        else:
            return 2019-int(y[0]) #there are some people with year of birth
        
#applying function in every value and changing to int format
proc_data['age'] = proc_data['age'].apply(real_age).astype('int64')

##### GENDER
#when there is no information, it is filled with 'Unknown'
proc_data['gender'] = proc_data['gender'].fillna("Unknown")
#There are some None as string
proc_data.loc[proc_data['gender']=='None', 'gender'] = "Unknown"
#Replacin M for Male, and F for Female
proc_data.loc[proc_data['gender']=='M', 'gender'] = "Male"
proc_data.loc[proc_data['gender']=='F', 'gender'] = "Female"

#### NAME
proc_data['name'] = proc_data['name'].str.upper()
proc_data.rename(columns = {'name':'FullName'})

#### SOURCE
def ind(x):
    y = x.split(' ==> ')
    return y[0] #taking first element of the list

def comp(x):
    y = x.split(' ==> ')
    return y[1] #taking second element of the list

#applying function in every value and changing to int format
proc_data['Industry'] = proc_data['Source'].apply(ind)
proc_data['Company']  = proc_data['Source'].apply(comp)

############################################## DELETING DATA ###########################################

proc_data.drop(columns=['dif','lastName','name','country','Source','Unnamed: 0','worth','worthChange','realTimeWorth'], inplace=True)

############################################## CHANGING DATA TYPE ######################################

#Changing every column to the correct type
proc_data['id']       = proc_data['id'].astype('object') 
proc_data['position'] = proc_data['position'].astype('int64')
proc_data['worth_BUSD'] = proc_data['worth_BUSD'].astype('float64')
proc_data['worthChange_MUSD'] = proc_data['worthChange_MUSD'].astype('float64')

##################  DATA TYPES ##################
#Changing every column to the correct type
proc_data['id']       = proc_data['id'].astype('object') 
proc_data['position'] = proc_data['position'].astype('int64')
proc_data['worth_BUSD'] = proc_data['worth_BUSD'].astype('float64')
proc_data['worthChange_MUSD'] = proc_data['worthChange_MUSD'].astype('float64')

############################################## CHANGING DATAFRAME #######################################
new_order = ['position','id','FullName','worth_BUSD','worthChange_MUSD','Industry','Company','age','gender','image']
proc_data = proc_data[new_order]

#Exporting clean data to csv
proc_data.to_csv('../data/processed/CristopherRL_processed_data.csv', sep='|', index=False)
