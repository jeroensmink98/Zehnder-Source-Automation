#!/usr/bin/env python
# coding: utf-8


from logger import setup_custom_logger
from file_writer import file_writer
import sys
import pandas as pd
import cbsodata
from msg import *


logger = setup_custom_logger("B009_New_Building_Permits")
logger.info("---------------------------------------------------")
logger.info(txtStarting + " " + logger.name)

dataset_id = "83671NED"
logger.info(f"Retrieve data from dataset {dataset_id}")
try:
    df = pd.DataFrame(
        cbsodata.get_data(
            "83671NED",
            filters="Perioden gt '2012' and Opdrachtgever ne 'T001209' and Eigendom ne'T001258'",
            select=[
                "RegioS",
                "Perioden",
                "Opdrachtgever",
                "Eigendom",
                "Woningen_2",
                "Wooneenheden_3",
                "Recreatiewoningen_4",
            ],
        )
    )
except:
    logger.exception("API incorrectly loaded")
    raise


try:
    df = df.groupby(["Perioden", "Opdrachtgever", "Eigendom"]).agg(
        {"Woningen_2": ["sum"], "Wooneenheden_3": sum, "Recreatiewoningen_4": sum}
    )
    df = df.reset_index()
except:
    logger.exception("Grouping data failed")
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


try:
    file_writer(df, "B009_New_Building_Permits")
    logger.info(txtDone)
except:
    logger.exception("Exporting failed")
    raise
