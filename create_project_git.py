

###########
###########
# Imports #
###########
###########

import sys


def check_installation(rv):
    current_version = sys.version_info
    if current_version[0] == rv[0] and current_version[1] >= rv[1]:
        pass
    else:
        sys.stderr.write( "[%s] - Error: Your Python interpreter must be %d.%d or greater (within major version %d)\n" % (sys.argv[0], rv[0], rv[1], rv[0]) )
        sys.exit(-1)
    return 0


required_version = (3,8)
check_installation(required_version)

import os  # noqa: E402
import platform  # noqa: E402
import subprocess  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import zipfile  # noqa: E402
import secrets  # noqa: E402
import click  # noqa: E402

###################
###################
# Project Details #
###################
###################

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

@click.command()
@click.option('--project', required=True, 
                    help='Name of project to create.')
@click.option('--owner', default='RyanJulyan',
                    help='Name of GitHub owner to use.')
@click.option('--repo', default='Flask-BDA',
                    help='Name of GitHub repository to use (must be linked to owner).')
@click.option('--branch', default='main',
                    help='Name of branch to use.')
@click.option('--create_venv', default='True',
                    help='Automatically Create venv and install requirements')
# @click.pass_context
def cmd_create_project(project, owner, repo, branch, create_venv):
    """Generate a new project"""

    create_venv = str2bool(create_venv)

    create_project(project, owner, repo, branch, create_venv)


def create_project(project_name, owner = "RyanJulyan", repo = "Flask-BDA", branch="main", create_venv=True):
    """Generate a new project"""

    while True:
        if(len(project_name) > 0):
            break
        else:
            print("Invalid Project Name!")
            print("Please enter a valid project name:")
            project_name = input()


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
    projectName = str(project_name)
    dir_name = str(dirName(projectName))


    CSRF_SESSION_KEY = secrets.token_urlsafe(256)
    SECRET_KEY = secrets.token_urlsafe(256)
    SECURITY_PASSWORD_SALT = secrets.token_urlsafe(256)
    JWT_SECRET_KEY = secrets.token_urlsafe(256)

    ########################
    ########################
    # Install Requirements #
    ########################
    ########################

    os.system('pip install --upgrade pip')
    os.system('pip install virtualenv')
    os.system('pip install click')
    os.system('pip install flaskwebgui')
    os.system('pip install tinyaes')
    os.system('pip install pyinstaller')

    ######################################################################################
    # Repeat for pip3 as symlinks do not seem to work with os.system (at least on MacOS) #
    ######################################################################################
    os.system('pip3 install --upgrade pip3')
    os.system('pip3 install virtualenv')
    os.system('pip3 install click')
    os.system('pip3 install flaskwebgui')
    os.system('pip3 install tinyaes')
    os.system('pip3 install pyinstaller')

    ########################
    ########################
    # Download GitHub Repo #
    ########################
    ########################

    os.system('curl -L https://codeload.github.com/{}/{}/zip/{} --ssl-no-revok -o {}.zip'.format(owner, repo, branch, repo))

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


    copytree(repo+'-'+branch+'/template', dir_name, 'Flask BDA', projectName)
    copytree(repo+'-'+branch+'/mobile_app', dir_name + "_mobile_app", 'Flask BDA', projectName)

    shutil.rmtree(repo+'-'+branch)

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
    destination = open(dir_name + '/config.py', "w")

    for line in source:
        if 'CSRF_SESSION_KEY = env("CSRF_SESSION_KEY", "secret")' in line:
            destination.write('CSRF_SESSION_KEY = env("CSRF_SESSION_KEY", "' + CSRF_SESSION_KEY + '")' + '\n')
        elif 'SECRET_KEY = env("SECRET_KEY", "secret")' in line:
            destination.write('SECRET_KEY = env("SECRET_KEY", "' + SECRET_KEY + '")' + "\n")
        elif 'JWT_SECRET_KEY = env("JWT_SECRET_KEY", "secret")' in line:
            destination.write('JWT_SECRET_KEY = env("JWT_SECRET_KEY", "' + JWT_SECRET_KEY + '")' + "\n")
        elif 'SECURITY_PASSWORD_SALT = env("SECURITY_PASSWORD_SALT", "secret")' in line:
            destination.write('SECURITY_PASSWORD_SALT = env("SECURITY_PASSWORD_SALT", "' + SECURITY_PASSWORD_SALT + '")' + "\n")
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
    if create_venv:
        os.system('cd "' + dir_name + '" && pip install --upgrade pip')
        os.system('cd "' + dir_name + '" && pip install --no-cache-dir -r requirements.txt')
        os.system('cd "' + dir_name + '" && virtualenv venv')
        os.system('cd "' + dir_name + '" && venv/bin/activate && pip install --no-cache-dir -r requirements.txt && export FLASK_APP=app && export FLASK_ENV=development')
        os.system('cd "' + dir_name + '" && venv\\Scripts\\activate && pip install --no-cache-dir -r requirements.txt && set FLASK_APP=app && set FLASK_ENV=development')

        ######################################################################################
        # Repeat for pip3 as symlinks do not seem to work with os.system (at least on MacOS) #
        ######################################################################################
        os.system('cd "' + dir_name + '" && pip3 install --upgrade pip3')
        os.system('cd "' + dir_name + '" && pip3 install --no-cache-dir -r requirements.txt')
        os.system('cd "' + dir_name + '" && virtualenv venv')
        os.system('cd "' + dir_name + '" && venv/bin/activate && pip3 install --no-cache-dir -r requirements.txt && export FLASK_APP=app && export FLASK_ENV=development')
        os.system('cd "' + dir_name + '" && venv\\Scripts\\activate && pip3 install --no-cache-dir -r requirements.txt && set FLASK_APP=app && set FLASK_ENV=development')

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

    def customizeFileVariables(src, renameFrom='', renameTo=''):

        # print("src: ",src)
        # print("renameFrom: ",renameFrom)
        # print("renameTo: ",renameTo)

        ignore_list = [
            ## Files
            'FLASK-BDA LICENSE',
            ## Folders
            '.github',
            '.vscode',
            '__pycache__',
            'app',
            'cli',
            'create_module_template',
            'databases',
        ]

        for item in os.listdir(src):
            s = os.path.join(src, item)
            if (any(map(s.__contains__, ignore_list))):
                pass
            elif os.path.isdir(s):
                customizeFileVariables(s, renameFrom, renameTo)
            else:
                ##############################################
                # Copy temp for manage source -> destination #
                ##############################################
                shutil.copy2(s, s+'~')
                ################################
                # manage source -> destination #
                ################################
                source = open(s+'~', "r")
                destination = open(s, "w")
                for line in source:
                    ####################
                    # Rename Variables #
                    ####################
                    if "def __init__" in line and 'models.py' in s:
                        pass
                    elif 'models.json' in s:
                        pass
                    else:
                        # print("line: ",line)
                        destination.write((line.replace(renameFrom, renameTo)).replace(renameFrom.capitalize(), renameTo.capitalize()))
                source.close()
                destination.close()

                #################
                # remove source #
                #################

                os.remove(s+'~')


    #############
    ## FAILING ##
    #############
    # customizeFileVariables(dir_name, 'Falsk BDA', project_name)
    # customizeFileVariables(dir_name, 'Falsk-BDA', project_name)

    abs_folder_path = os.path.abspath(os.path.dirname(__file__)) + "/" + dir_name
    open_file(abs_folder_path)


if __name__ == "__main__":
    cmd_create_project()

