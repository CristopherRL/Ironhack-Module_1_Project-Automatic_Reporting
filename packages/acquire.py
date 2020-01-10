######################################### IMPORTING LIBRARIES #################################################
import pandas as pd
from sqlalchemy import create_engine

######################################### IMPORTING DATA #################################################
#def get_data():
def getting_data(file_name):

    # Using sqlalchemy to connect with the downloaded file which contains the messy data of "Forbes"
    #file_name = 'CristopherRL'
    data_location = "../data/raw/"
    engine = create_engine(f'sqlite:///{data_location}{file_name}')

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

    # Importing data from db file to 'raw_data' dataframe
    raw_data = pd.read_sql_query(query, engine)

    ### ONLY UNTIL I CAN BE ABLE TO SOLVE THE ERROR
    raw_data.to_sql_query('../data/raw/raw_data.csv', sep='|', index=False)

    return raw_data