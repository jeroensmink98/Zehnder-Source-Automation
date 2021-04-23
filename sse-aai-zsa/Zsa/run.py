from configparser import ConfigParser
import subprocess

# Create instance of configParser
config = ConfigParser()

# Import ini file
config.read("config.ini")

bat = config.get("main", "bat_path") + "/run_all_scripts.bat"


# Create a subprocess based on the file in the filepath
run_all_scripts = subprocess.Popen(bat)

stdout, stderr = run_all_scripts.communicate()

# Return status code (if 0 its good)
print(run_all_scripts.returncode)