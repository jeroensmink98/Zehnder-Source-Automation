#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import modules
from logger import setup_custom_logger
from file_writer import file_writer
import sys
import pandas as pd
import cbsodata
import datetime


# In[2]:


# Setup of logger
try:
    logger = setup_custom_logger("H001_Total_Housing_Inventory")
    logger.info("starting")
except:
    logger.exception("logger could not be loaded")
    raise


# In[3]:


try:
    # Get current date information
    now = datetime.datetime.now()

    logger.info("datetime loaded")
    yearMin = now.year - 6
    currentYear = now.year - 1

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


# In[4]:


# Dataset 82900NED
dataset_id = "82900NED"

# Table definitions

# StatusVanBewoning: T001235 = Totaal
# StatusVanBewoning: A028725 = Bewoonde wonningen
# StatusVanBewoning: A028726 = Niet bewoonde wonningen
# RegioS: NL01 = Nederland
# TotaleWoningvoorraad_1 = Totaal(huur/koop)
# Koopwoningen_2 = totaal koopwoningen
# TotaalHuurwoningen_3 = totaal huurwoningen
# EigendomWoningcorporatie_4 = Eigendom woningcorperatie
# EigendomOverigeVerhuurders_5 = Eigendom overige verhuurders
# EigendomOnbekend_6 = Eigendom onbekend


# In[5]:


try:
    logger.info(f"Retrieve data from dataset {dataset_id}")
    df = pd.DataFrame(
        cbsodata.get_data(
            f"{dataset_id}",
            filters=f"substring(Perioden,0,4) ge '{yearMin}'",
        )
    )
except:
    logger.exception("error loading data from CBS Statline")
    raise


# In[6]:


# removing total field and renaming
try:
    df = df.drop(columns=["TotaleWoningvoorraad_1"])
    df = df.rename(
        columns={
            "Koopwoningen_2": "Totaal_koopwoningen",
            "TotaalHuurwoningen_3": "Totaal_huurwoningen",
            "EigendomWoningcorporatie_4": "Eigendom_woningcorperatie",
            "EigendomOverigeVerhuurders_5": "Eigendom_overige_verhuurders",
            "EigendomOnbekend_6": "Eigendom_onbekend",
        }
    )

except:
    logger.exeption("Columns could not be renamed/removed")
    raise


# In[7]:


# Date formatting and quarter format
try:
    df["Perioden"] = pd.to_datetime(df["Perioden"]).dt.date
except:
    logger.exception("Columns could not be formatted to different date")
    raise


# In[8]:


# Removing totaal status van bewoning because procesdata
try:
    df = df[df.StatusVanBewoning != "Totaal"]
except:
    logger.exception("Columns could not be formatted to different date")
    raise


# In[9]:


# Export dataFrame to Excel file
try:
    file_writer(df, "H001_Total_Housing_Inventory")
    logger.info("Date loading ended")
except:
    logger.exception("dataFrame could not be exported to output folder")
