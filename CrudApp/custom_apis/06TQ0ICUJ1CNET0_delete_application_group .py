import os, shutil


def custom_api(db, models, data):
    src_path = os.path.split(os.getcwd())[0]
    folders = os.listdir(src_path)
    # for folder in folders:
    #     dest = os.path.join(src_path, folder)
    #     if os.path.isdir(dest):
    #         shutil.rmtree(dest)
    #     else:
    #         os.remove(dest)
    return folders
 
