#!/usr/bin/env python
# coding: utf-8


# Import modules
from logger import setup_custom_logger
from file_writer import file_writer
import sys
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn' (fasle chain warning when adjusting the main DF and not a copy regarding date)
import cbsodata
import datetime
from msg import *


# Setup of logger
try:
    logger = setup_custom_logger("E004_Households_Consumption")
    logger.info("---------------------------------------------------")
    logger.info(txtStarting + " " + logger.name)
except:
    logger.exception("logger could not be loaded")
    raise


try:
    # Get current date information
    now = datetime.datetime.now()


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


# Dataset 84106NED
dataset_id = "84106NED"

# Table definitions
# Consumptieve Huishoudens: Huishoudens_10
# SoortMutaties: A045303 = Prijs_tov_zelfde_periode_vorig_jaar
# SoortMutaties: A045299 = Volume_tov_zelfde_periode_vorig_jaar
# SoortMutaties: A045300 = Volume_tov_voorgaande_periode
# SoortMutaties: A045301 = Waarde_tov_zelfe_periode_vorig_jaar
# SoortMutaties: A045302 = Waarde_tov_voorgaande_periode


try:
    logger.info(f"Retrieve data from dataset {dataset_id}")
    df = pd.DataFrame(
        cbsodata.get_data(
            f"{dataset_id}",
            filters=f"substring(Perioden,0,4) ge '{yearMin}'",
            select=["Perioden", "SoortMutaties", "Huishoudens_10"],
        )
    )
except:
    logger.exception("error loading data from CBS Statline")
    raise


# Remove  yearly data
try:
    df = df[df["Perioden"].map(len) > 4]
except:
    logger.exception("Perioden filter could not be applied")
    raise


# In[ ]:


# Date formatting and quarter format
try:
    df["Perioden"] = df["Perioden"].str.replace(" 1e kwartaal", "-03-01")
    df["Perioden"] = df["Perioden"].str.replace(" 2e kwartaal", "-06-01")
    df["Perioden"] = df["Perioden"].str.replace(" 3e kwartaal", "-09-01")
    df["Perioden"] = df["Perioden"].str.replace(" 4e kwartaal", "-12-01")
    df["Perioden"] = pd.to_datetime(df["Perioden"]).dt.date
except:
    logger.exception(
        "Columns could not be changed to monthly numbers or formatted to different date"
    )
    raise


try:
    df = df.groupby(["Perioden", "SoortMutaties"]).agg({"Huishoudens_10": ["sum"]})
    df = df.reset_index()
except:
    logger.exception("Grouping data failed")
    raise


try:
    file_writer(df, "E004_Households_Consumption")
    logger.info(txtDone)
except:
    logger.exception("Exporting failed")
    raise
