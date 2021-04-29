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
    logger = setup_custom_logger("B003_Permits_New_Houses")
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


# Dataset 83668NED
dataset_id = "83668NED"

# Table definitions
# Woningen_1 = Bouwvergunningen_woonruimten_Woningen
# Wooneenheden_2 = Bouwvergunningen_woonruimten_Wooneenheden
# Recreatiewoningen_3 = Bouwvergunningen_woonruimten_Recreatiewoningen


# In[ ]:


try:
    logger.info(f"Retrieve data from dataset {dataset_id}")
    data = pd.DataFrame(
        cbsodata.get_data(
            f"{dataset_id}",
            filters=f"substring(Perioden,0,4) ge '{yearMin}'",
            select=["Perioden", "Woningen_1", "Wooneenheden_2", "Recreatiewoningen_3"],
        )
    )
except:
    logger.exception("error loading data from CBS Statline")
    raise


# In[ ]:


# Rename columns
try:
    data = data.rename(
        columns={
            "Woningen_1": "Bouwvergunningen_woonruimten_Woningen",
            "Wooneenheden_2": "Bouwvergunningen_woonruimten_Wooneenheden",
            "Recreatiewoningen_3": "Bouwvergunningen_woonruimten_Recreatiewoningen",
        }
    )

except:
    logger.exeption("Columns could not be renamed")
    raise


# In[ ]:


# Date formatting and quarter format
try:
    data["Perioden"] = data["Perioden"].str.replace(" januari", "-01")
    data["Perioden"] = data["Perioden"].str.replace(" februari", "-02")
    data["Perioden"] = data["Perioden"].str.replace(" maart", "-03")
    data["Perioden"] = data["Perioden"].str.replace(" april", "-04")
    data["Perioden"] = data["Perioden"].str.replace(" mei", "-05")
    data["Perioden"] = data["Perioden"].str.replace(" juni", "-06")
    data["Perioden"] = data["Perioden"].str.replace(" juli", "-07")
    data["Perioden"] = data["Perioden"].str.replace(" augustus", "-08")
    data["Perioden"] = data["Perioden"].str.replace(" september", "-09")
    data["Perioden"] = data["Perioden"].str.replace(" oktober", "-10")
    data["Perioden"] = data["Perioden"].str.replace(" november", "-11")
    data["Perioden"] = data["Perioden"].str.replace(" december", "-12")
    data["Perioden"] = pd.to_datetime(data["Perioden"]).dt.date
except:
    logger.exception(
        "Columns could not be changed to monthly numbers or formatted to different date"
    )
    raise


# In[ ]:


# Export dataFrame to Excel file
try:
    file_writer(data, "B003_Permits_New_Houses")
except:
    logger.exception("dataFrame could not be exported to output folder")
