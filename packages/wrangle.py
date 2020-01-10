######################################### IMPORTING LIBRARIES #################################################
import re

def cleaning_data(raw_data):

    proc_data = raw_data

    #### AGE
    def real_age(x):

        if x is None:
            return 999  # to identify which doesnt have age information

        else:
            y = re.findall('[\d]+', x)  # extracting y from "y years". The last on is '99 years'

            if int(y[0]) < 100:
                return int(y[0])
            else:
                return 2019 - int(y[0])  # there are some people with year of birth

    # applying function in every value ...
    proc_data['age'] = proc_data['age'].apply(real_age)
    # ... and changing to int format
    proc_data['age'] = proc_data['age'].astype('int64')
    #### GENDER
    # When there is no information, it is filled with 'Unknown'
    proc_data['gender'] = proc_data['gender'].fillna("Unknown")
    # There are some None as string
    proc_data.loc[proc_data['gender'] == 'None', 'gender'] = "Unknown"
    # Replacing M for Male, and F for Female
    proc_data.loc[proc_data['gender'] == 'M', 'gender'] = "Male"
    proc_data.loc[proc_data['gender'] == 'F', 'gender'] = "Female"

    #### NAME
    proc_data['name'] = proc_data['name'].str.upper()
    proc_data.rename( columns = {'name':'FullName'}, inplace=True )

    #### SOURCE
    def ind(x):
        y = x.split(' ==> ')
        return y[0]  # taking first element of the list

    def comp(x):
        y = x.split(' ==> ')
        return y[1]  # taking second element of the list

    # applying function in every value and changing to int format
    proc_data['Industry'] = proc_data['Source'].apply(ind)
    proc_data['Company'] = proc_data['Source'].apply(comp)

    ### WORTH
    proc_data['worth_BUSD'] = proc_data['worth'].str.replace(' BUSD', '')

    ############################################## DELETING DATA ###########################################
    proc_data.drop(
        columns=['lastName', 'country', 'Source', 'Unnamed: 0', 'worth', 'worthChange', 'realTimeWorth'],
        inplace=True)

    ############################################## CHANGING DATA TYPE ######################################
    # Changing every column to the correct type
    proc_data['id'] = proc_data['id'].astype('object')
    proc_data['position'] = proc_data['position'].astype('int64')
    proc_data['worth_BUSD'] = proc_data['worth_BUSD'].astype('float64')

    ##################  DATA TYPES ##################
    # Changing every column to the correct type
    proc_data['id'] = proc_data['id'].astype('object')
    proc_data['position'] = proc_data['position'].astype('int64')
    proc_data['worth_BUSD'] = proc_data['worth_BUSD'].astype('float64')

    ############################################## CHANGING DATAFRAME #######################################
    new_order = ['position', 'id', 'FullName', 'worth_BUSD', 'Industry', 'Company', 'age', 'gender',
                 'image']
    proc_data = proc_data[new_order]

    # Exporting clean data to csv
    proc_data.to_csv('data/processed/proc_data.csv', sep=';', index=False)

    return proc_data