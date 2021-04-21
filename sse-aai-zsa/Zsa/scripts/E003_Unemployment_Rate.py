#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import Modules
from logger import setup_custom_logger
from file_writer import file_writer
import pandas as pd
import requests
import cbsodata
import datetime


# In[ ]:


# Setup Logger
try:
    logger = setup_custom_logger("E002_Unemployment_Rate")
    logger.info("starting")
except:
    logger.exception("logger could not be loaded")
    raise


# In[ ]:


try:
    # Get current date information
    now = datetime.datetime.now()

    logger.info("datetime loaded")
    yearMin = now.year - 3
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


# Dataset 80590ned
dataset_id = "80590ned"

# Table definitions

# Geslacht: T001038 = Totaal (man/vrouw)
# Leeftijd: 52052   = 15 tot 75 jaar
# Perioden: YYYY%%MM
# Seizoengecorrigeerd_2 = x1000_Beroepsbevolking_Seizoengecorrigeerd
# Seizoengecorrigeerd_4 = x1000_Werkzame_Beroepsbevolking_Seizoengecorrigeerd
# Seizoengecorrigeerd_6 = x1000_Werkloze_Beroepsbevolking_Seizoengecorrigeerd
# Seizoengecorrigeerd_8 = Werkloosheidspeercentage_Seizoengecorrigeerd_procenten
# Seizoengecorrigeerd_12 = Bruto_Arbeitsparticipatie_Seizoengecorrigeerd_procenten
# Seizoengecorrigeerd_14 = Netto_Arbeitsparticipatie_Seizoengecorrigeerd_procenten


# In[ ]:


try:
    logger.info(f"Retrieve data from dataset {dataset_id}")
    data = pd.DataFrame(
        cbsodata.get_data(
            f"{dataset_id}",
            filters=f"substring(Perioden,0,4) ge '{yearMin}'",  # These spaces need to be there, they are part of the value..
            select=[
                "Geslacht",
                "Leeftijd",
                "Perioden",
                "Seizoengecorrigeerd_2",
                "Seizoengecorrigeerd_4",
                "Seizoengecorrigeerd_6",
                "Seizoengecorrigeerd_8",
                "Seizoengecorrigeerd_12",
                "Seizoengecorrigeerd_14",
            ],
        )
    )
except:
    logger.exception("error loading data from CBS Statline")
    raise


# In[ ]:


# Remove quaterly and yearly data
try:
    data = data[data["Perioden"].str.contains("kwartaal") == False]
    data = data[data["Perioden"].map(len) > 4]
except:
    logger.exception("Perioden filter could not be applied")
    raise


# In[ ]:


# Date formatting and quarter format
try:
    data["Seizoengecorrigeerd_2"] = data["Seizoengecorrigeerd_2"] * 1000
    data["Seizoengecorrigeerd_4"] = data["Seizoengecorrigeerd_4"] * 1000
    data["Seizoengecorrigeerd_6"] = data["Seizoengecorrigeerd_2"] * 1000
except:
    logger.exception("Values could not get multiplied")
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


# Rename columns
try:
    data = data.rename(
        columns={
            "Seizoengecorrigeerd_2": "Beroepsbevolking_Seizoengecorrigeerd",
            "Seizoengecorrigeerd_4": "Werkzame_Beroepsbevolking_Seizoengecorrigeerd",
            "Seizoengecorrigeerd_6": "Werkloze_Beroepsbevolking_Seizoengecorrigeerd",
            "Seizoengecorrigeerd_8": "Werkloosheidspeercentage_Seizoengecorrigeerd_procenten",
            "Seizoengecorrigeerd_12": "Bruto_Arbeitsparticipatie_Seizoengecorrigeerd_procenten",
            "Seizoengecorrigeerd_14": "Netto_Arbeitsparticipatie_Seizoengecorrigeerd_procenten",
        }
    )

except:
    logger.exeption("Columns could not be renamed")
    raise


# In[ ]:


# Export dataFrame to Excel file
try:
    file_writer(data, "E003_UnemploymentRate")
except:
    logger.exception("dataFrame could not be exported to output folder")
