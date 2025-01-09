import os
import subprocess
from datetime import datetime

# Variables
current_date = datetime.now().strftime("%d.%m.%Y-%H:%M")
backup_dir = f"/Backup/APISTUDIO/{current_date}"
backup_log = "/Backup/APISTUDIO/LOG"
db_user = "microapi"
db_name = "apicloud"
db_password = "M!cr0ap!*C$E*"
destination_dir = "/SK/CLOUDSERVER BACKUP/CENTOS/APISTUDIO/"

# Ensure backup directory exists
os.makedirs(backup_dir, exist_ok=True)

# Ensure log directory exists
os.makedirs(backup_log, exist_ok=True)

# Backup command
timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M%p")
backup_file = f"{backup_dir}/{db_user}-{timestamp}.sql"
dump_command = f"PGPASSWORD='{db_password}' pg_dump -U '{db_user}' -d '{db_name}' --schema=public > '{backup_file}' --verbose 2> '{backup_log}/{db_user}-$TIMESTAMP'"
subprocess.run(dump_command, shell=True, check=True)

# Move the backup directory to the destination directory
subprocess.run(["mv", backup_dir, destination_dir], check=True)
