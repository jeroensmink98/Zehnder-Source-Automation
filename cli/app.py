# Import Modules
import time
import redis
import pandas as pd
import cbsodata
import datetime
from logger import setup_custom_logger
from flask import Flask

# Python configuration
app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# Setup logger configuration
try:
    logger = setup_custom_logger('app')
    logger.info('Intializing logger')
except:
    logger.exeception('Could not initialize logger')
    raise

# Application routes
@app.route('/')
def route():
    return "Hello World"


@app.route('/kpi/<kpi_id>')
def return_kpi_id(kpi_id):
    # Capitalize the strings since URL's dont give a damn about capitalization.
    kpi_id = kpi_id.upper()
  
    # Try to execute a script
    try:
        logger.info(f'running script {kpi_id}')
        exec(open(f'kpi/{kpi_id}.py').read())
        return(kpi_id)
    except:
        logger.exception('cannot run script')
        return('canot run script')
        raise


    
    