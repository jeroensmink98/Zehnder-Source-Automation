#!/usr/bin/env python
# coding: utf-8


# Import Modules
from logger import setup_custom_logger
from file_writer import file_writer
import pandas as pd
import requests
import cbsodata
import datetime
from msg import *


# Setup Logger
try:
    logger = setup_custom_logger("E008_Producer_Confidence")
    logger.info("---------------------------------------------------")
    logger.info(txtStarting + " " + logger.name)
except:
    logger.exception("logger could not be loaded")
    raise


# In[3]:


try:
    # Get current date information
    now = datetime.datetime.now()

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


# Dataset 81234ned
dataset_id = "81234NED"
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


try:
    logger.info(f"Retrieve data from dataset {dataset_id}")
    data = pd.DataFrame(
        cbsodata.get_data(
            f"{dataset_id}", filters=f"substring(Perioden,0,4) ge '{yearMin}'"
        )
    )  # These spaces need to be there, they are part of the value..
except:
    logger.exception("error loading data from CBS Statline")
    raise


# Remove quaterly and yearly data
try:
    data = data[data["Perioden"].str.contains("kwartaal") == False]
    data = data[data["Perioden"].map(len) > 4]
except:
    logger.exception("Perioden filter could not be applied")
    raise


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


# Export dataFrame to Excel file
try:
    file_writer(data, "E008_Producer_Confidence")
    logger.info(txtDone)
except:
    logger.exception("dataFrame could not be exported to output folder")
