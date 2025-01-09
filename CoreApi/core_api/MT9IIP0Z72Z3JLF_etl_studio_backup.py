import os
import subprocess
from datetime import datetime
def custom_api(db, data):
# Variables
    current_date = datetime.now().strftime("%d-%m-%Y-%H-%M %p")
    backup_dir = f"/Backup/ETLSTUDIO/{current_date}"
    backup_log = "/Backup/ETLSTUDIO/LOG"
    destination_dir = "/SK/CLOUDSERVER BACKUP/CENTOS/ETLSTUDIO/"

    # Ensure backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    # Ensure log directory exists
    os.makedirs(backup_log, exist_ok=True)

    # Backup command
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M%p")
    backup_file = f"""{backup_dir}/ETLSTDUIO-{timestamp}.sql"""
    dump_command = f"""PGPASSWORD='{db["db_password"]}' pg_dump -U '{db["db_user"]}' -d '{db["db_name"]}' --schema=etlstudio > '{backup_file}' --verbose 2> '{backup_log}'/ETLSTUDIO-'{timestamp}'.log"""
    subprocess.run(dump_command, shell=True, check=True)


    # Move the backup directory to the destination directory
    subprocess.run(["mv", backup_dir, destination_dir], check=True)
    
    return {"message": "Successfully completed"}
