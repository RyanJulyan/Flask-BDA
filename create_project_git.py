

###########
###########
# Imports #
###########
###########

import os
import platform
import subprocess
import re
import shutil
import zipfile
import secrets

###################
###################
# Project Details #
###################
###################


def project():
    print("Project Name:")
    while True:
        project_name = input()
        if(len(project_name) > 0):
            return project_name
        else:
            print("Invalid Project Name!")
            print("Please enter a valid project name!")


def dirName(projectName):
    while True:
        dir_name = projectName
        if(len(dir_name) > 0):
            dir_name = dir_name.lower()
            dir_name = re.sub('[;!,*)@#%(&$?.^\'"+<>/\\{}]', '', dir_name)
            dir_name = dir_name.replace(" ", "_")
            return dir_name
        else:
            print("Invalid Directory Name!")
            print("Please enter a valid directory name!")


# Prompt user
projectName = str(project())
dir_name = str(dirName(projectName))


CSRF_SESSION_KEY = secrets.token_urlsafe(256)
SECRET_KEY = secrets.token_urlsafe(256)
JWT_SECRET_KEY = secrets.token_urlsafe(256)

########################
########################
# Install Requirements #
########################
########################

os.system('pip install virtualenv')

########################
########################
# Download GitHub Repo #
########################
########################

owner = "RyanJulyan"
repo = "Flask-BDA"

os.system('curl -L https://codeload.github.com/{}/{}/zip/main --ssl-no-revok -o {}.zip'.format(owner, repo, repo))

with zipfile.ZipFile(repo+'.zip', 'r') as zip_ref:
    zip_ref.extractall('./')
zip_ref.close()


def copytree(src, dst, renameFrom='', renameTo='', symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst.replace(renameFrom, renameTo))
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst.replace(renameFrom, renameTo), item.replace(renameFrom, renameTo))
        if os.path.isdir(s):
            copytree(s, d, renameFrom, renameTo, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)


copytree(repo+'-main/template', dir_name, 'Flask BDA', projectName)

shutil.rmtree(repo+'-main')

os.remove(repo+'.zip')


#############################
#############################
# Update Config Secret Keys #
#############################
#############################

#########################################################
# Copy App config.py for manage source -> destination #
#########################################################

shutil.copy2(dir_name + '/config.py', dir_name + '/config.py~')

################################
# manage source -> destination #
################################

source = open(dir_name + '/config.py~', "r")
destination = open(dir_name + '/config.py~', "w")

for line in source:
    if "CSRF_SESSION_KEY = 'secret'" in line:
        destination.write("CSRF_SESSION_KEY = '" + CSRF_SESSION_KEY + "'" + "\n")
    elif "SECRET_KEY = 'secret'" in line:
        destination.write("SECRET_KEY = '" + SECRET_KEY + "'" + "\n")
    elif "JWT_SECRET_KEY = 'secret'" in line:
        destination.write("JWT_SECRET_KEY = '" + JWT_SECRET_KEY + "'" + "\n")
    else:
        destination.write(line)

source.close()
destination.close()

#################
# remove source #
#################

os.remove(dir_name + '/config.py~')

######################
######################
# Install virtualenv #
######################
######################

os.system('cd "' + dir_name + '" && virtualenv venv')
os.system('cd "' + dir_name + '" && venv/bin/activate && pip install --no-cache-dir -r requirements.txt && export FLASK_APP=app && export FLASK_ENV=development')
os.system('cd "' + dir_name + '" && venv\\Scripts\\activate && pip install --no-cache-dir -r requirements.txt && set FLASK_APP=app && set FLASK_ENV=development')

#####################################################
#####################################################
# Open Folder in Native Explorer to help people see #
#####################################################
#####################################################


def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


abs_folder_path = os.path.abspath(os.path.dirname(__file__)) + "/" + dir_name

open_file(abs_folder_path)
