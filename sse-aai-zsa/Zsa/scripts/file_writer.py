# Import modules
from configparser import ConfigParser
import pandas as pd

# Create instance of configParser
config = ConfigParser()

# Import ini file
config.read("../config.ini")

output_path = config.get("main", "output_path")

# Output the dataFrame to the output location
def file_writer(dataFrame, fileName):
    dataFrame.to_csv(output_path + "/" + fileName + ".csv")
