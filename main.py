import subprocess
import os
# index scanners 
subdir_path = os.path.join(os.path.dirname(__file__), "scanners")
# verify and check environment
# establish db connection
# index scanners
# ask user which scanners to run
# run scans
for f in os.listdir(subdir_path):
    if f.endswith('.py'):
        script = os.path.join(subdir_path, f)
        subprocess.run(['python', script])
# run db maintenance
subdir_path = os.path.join(os.path.dirname(__file__), "db")
for f in os. listdir(subdir_path):
    if f.endswith('.py'):
        script = os.path.join(subdir_path, f)
        subprocess.run(['python', script])
# build reports
