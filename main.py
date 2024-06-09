import subprocess
import os
from datetime import datetime
import sys
import logging

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename="chickadee.log", level=logging.DEBUG)
    logger.info("App started: " + str(datetime.now()))
    MIN_PYTHON = (3,)
    if sys.version_info < MIN_PYTHON:
        sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)
    else:
        runScanners()
        runMaintenance()

def runScanners():
    # run scans
    logger.info("Starting scanners.")
    subdir_path = os.path.join(os.path.dirname(__file__), "scanners")
    for f in os.listdir(subdir_path):
        if f.endswith('.py'):
            script = os.path.join(subdir_path, f)
            logger.info("Starting scanner: " + script)
            exec(open(script).read(), {'logger': logger})

def runMaintenance():
    # run db maintenance
    logger.info("Starting maintenance.")
    subdir_path = os.path.join(os.path.dirname(__file__), "db")
    for f in os. listdir(subdir_path):
        if f.endswith('.py'):
            script = os.path.join(subdir_path, f)
            logger.info("Starting maintenance script: " + script)
            exec(open(script).read(), {'logger': logger})

# index scanners 
# verify and check environment
# establish db connection
# index scanners
# build reports

if __name__ == "__main__":
    main()