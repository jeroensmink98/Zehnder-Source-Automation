###############################################
# author:  Jeroen Smink
# date:    30-03-2021  
# email:   jeroen.smink@sminkware.com
##############################################
# Realisation of Zehnders KPI E001 according to the KPI_Overview Document.


# Import Modules
import time
import redis
import pandas as pd
import cbsodata
import datetime
from logger import setup_custom_logger

# Setup of logger
try:
    logger = setup_custom_logger("E001")
    logger.info('Intializing logger')
except:
    logger.exception('Could not initialize logger')
    raise


## Get current year
try:
    # Get current datetime info
    now = datetime.datetime.now()

    # We want results from the last 4 years
    yearMin = now.year-8
    yearMax = now.year
except:
    yearMin = 2010
    yearMax = 2030
    raise

# Select a dataset
dataset_id = '84106NED'

# Table definitions

# SoortMutaties: A045299 = Volume, t.o.v. zelfde periode vorig jaar
# BrutoBinnenlandsProduct_2: waarde BBP


try:
    logger.info(f'Retrieve data from dataset {dataset_id}')
    data = pd.DataFrame(cbsodata.get_data(
    f'{dataset_id}',
    filters=f"substring(Perioden,0,4) ge '{yearMin}' and SoortMutaties eq 'A045299'",
    select=["Perioden", "BrutoBinnenlandsProduct_2"]))
except:
    logger.exception('error loading data from CBS Statline')
    raise

# Remove quaterly and yearly data
try:
    data = data[data["Perioden"].str.contains("kwartaal")==True]
    data = data[data['Perioden'].map(len) > 4 ]
except:
    logger.exception('Perioden filter could not be applied')
    raise

# Rename columns
try:
    data = data.rename(columns={
    "BrutoBinnenlandsProduct_2": "BBP_Percentage",
})

except:
    logger.exeption('Columns could not be renamed')
    raise


# Date formatting and quarter format
try:
    data["Perioden"] = data["Perioden"].str.replace(" 1e kwartaal", "-03-01")
    data["Perioden"] = data["Perioden"].str.replace(" 2e kwartaal", "-06-01")
    data["Perioden"] = data["Perioden"].str.replace(" 3e kwartaal", "-09-01")
    data["Perioden"] = data["Perioden"].str.replace(" 4e kwartaal", "-12-01")
    data['Perioden'] = pd.to_datetime(data["Perioden"]).dt.date
except:
    logger.exception('Columns could not be changed to monthly numbers or formatted to different date')
    raise


# Export dataFrame to Excel file
try:
     data.to_csv("E001_BBP.csv")  
except:
    logger.exception('dataFrame could not be exported to output folder')