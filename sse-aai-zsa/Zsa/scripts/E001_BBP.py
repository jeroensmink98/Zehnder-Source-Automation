#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import modules
from logger import setup_custom_logger
from file_writer import file_writer
import sys
import pandas as pd
import cbsodata
import datetime


# In[ ]:


# Setup of logger
try:
    logger = setup_custom_logger("E001_BBP")
    logger.info("starting")
except:
    logger.exception("logger could not be loaded")
    raise


# In[ ]:


try:
    # Get current date information
    now = datetime.datetime.now()

    logger.info("datetime loaded")
    yearMin = now.year - 4
    yearMax = now.year

    # Values you can load
    # now.year
    # now.month
    # now.day
    # now.hour
    # now.minute
except:
    logger.exception("datetime could not be loaded")
    logger.info("set yearmin to a default value")
    # Set default values for fallback
    yearMin = 2010
    yearMax = 2030
    raise


# In[ ]:


# Dataset 84106NED
dataset_id = "84106NED"

# Table definitions

# SoortMutaties: A045299 = Volume, t.o.v. zelfde periode vorig jaar
# BrutoBinnenlandsProduct_2: waarde BBP


# In[ ]:


try:
    logger.info(f"Retrieve data from dataset {dataset_id}")
    data = pd.DataFrame(
        cbsodata.get_data(
            f"{dataset_id}",
            filters=f"substring(Perioden,0,4) ge '{yearMin}'",
            select=["Perioden", "SoortMutaties", "BrutoBinnenlandsProduct_2"],
        )
    )
except:
    logger.exception("error loading data from CBS Statline")
    raise


# In[ ]:


# Remove quaterly and yearly data
try:
    data = data[data["Perioden"].str.contains("kwartaal") == True]
    data = data[data["Perioden"].map(len) > 4]
except:
    logger.exception("Perioden filter could not be applied")
    raise


# In[ ]:


# Rename columns
try:
    data = data.rename(
        columns={
            "BrutoBinnenlandsProduct_2": "BBP_Percentage",
        }
    )

except:
    logger.exeption("Columns could not be renamed")
    raise


# In[ ]:


# Date formatting and quarter format
try:
    data["Perioden"] = data["Perioden"].str.replace(" 1e kwartaal", "-03-01")
    data["Perioden"] = data["Perioden"].str.replace(" 2e kwartaal", "-06-01")
    data["Perioden"] = data["Perioden"].str.replace(" 3e kwartaal", "-09-01")
    data["Perioden"] = data["Perioden"].str.replace(" 4e kwartaal", "-12-01")
    data["Perioden"] = pd.to_datetime(data["Perioden"]).dt.date
except:
    logger.exception(
        "Columns could not be changed to monthly numbers or formatted to different date"
    )
    raise


# In[ ]:


# Export dataFrame to Excel file
try:
    file_writer(data, "E001_BBP")
except:
    logger.exception("dataFrame could not be exported to output folder")
