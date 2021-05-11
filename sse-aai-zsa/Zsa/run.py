from configparser import ConfigParser
import subprocess
from logger import setup_custom_logger

# Create instance of configParser
config = ConfigParser()

# Create logger instance

logger = setup_custom_logger("MAIN_THREAD")
# Import ini file
config.read("config.ini")

bat = config.get("main", "bat_path") + "/run_all_scripts.bat"


# Create a subprocess based on the file in the filepath
run_all_scripts = subprocess.Popen(bat)


stdout, stderr = run_all_scripts.communicate()

logger.info("---------------------------------------------------")
logger.info("Finished")

# Return status code (if 0 its good)
print(run_all_scripts.returncode)