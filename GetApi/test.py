from fastapi import FastAPI, HTTPException, Depends
import subprocess


app = FastAPI()


@app.get('/')
def get_all():
    result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
    return {
        "code":result.returncode,
        "result":result.stdout
    }
