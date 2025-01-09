REM Set the path to your virtual environment
set VENV_PATH=D:\B2E_DjanoProjects\API_STUDIO\ApiStudio\venv
 
REM Activate the virtual environment
call %VENV_PATH%\Scripts\activate.bat
 
cd /d D:\B2E_DjanoProjects\API_STUDIO\ApiStudio
 
REM Run the Python service command and log the output
python manage.py runserver 127.0.0.1:8005 > D:\B2E_DjanoProjects\API_STUDIO\ApiStudio\apistudio.log 2>&1 