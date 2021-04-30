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

    logger = setup_custom_logger("E005_Investments_Non_Current_Assets")
    logger.info("---------------------------------------------------")
    logger.info(txtStarting + " " + logger.name)
except:
    logger.exception("logger could not be loaded")
    raise


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


# Dataset 84106NED
dataset_id = "84106NED"

# Non-Current-Assets = Vaste Activa!

# Table definitions

# SoortMutaties: A045303 = Prijs_tov_zelfde_periode_vorig_jaar
# SoortMutaties: A045299 = Volume_tov_zelfde_periode_vorig_jaar
# SoortMutaties: A045300 = Volume_tov_voorgaande_periode
# SoortMutaties: A045301 = Waarde_tov_zelfe_periode_vorig_jaar
# SoortMutaties: A045302 = Waarde_tov_voorgaande_periode
# Totaal_12 = Totaal
# BedrijvenEnHuishoudens_13 = Bedrijven_en_huishoudens
# Overheid_14 = Overheid

# We could skip totaal since we can calculate that on or own (process gegeven)


try:
    logger.info(f"Retrieve data from dataset {dataset_id}")
    df = pd.DataFrame(
        cbsodata.get_data(
            f"{dataset_id}",
            filters=f"substring(Perioden,0,4) ge '{yearMin}'",
            select=[
                "Perioden",
                "SoortMutaties",
                "Totaal_12",
                "BedrijvenEnHuishoudens_13",
                "Overheid_14",
            ],
        )
    )
except:
    logger.exception("error loading data from CBS Statline")
    raise


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


# removing total field and renaming
try:
    df = df.rename(
        columns={
            "BedrijvenEnHuishoudens_13": "BedrijvenEnHuishoudens",
            "Totaal_12": "Totaal",
            "Overheid_14": "Overheid",
        }
    )

except:
    logger.exeption("Columns could not be renamed/removed")
    raise


# Export dataFrame to Excel file
try:
    file_writer(df, "E005_Investments_Non_Current_Assets")
    logger.info(txtDone)
except:
    logger.exception("dataFrame could not be exported to output folder")
