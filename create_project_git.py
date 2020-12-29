

##########################
##########################
######## Imports #########
##########################
##########################

import os
import re
import sys
import base64
import shutil
import getopt
from github import Github
from github import GithubException

##################################
##################################
######## Project Details #########
##################################
##################################

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
            dir_name = dir_name.casefold()
            dir_name = re.sub('[;!,*)@#%(&$?.^\'"+<>/\\{}]', '', dir_name)
            dir_name = dir_name.replace(" ", "_")
            return dir_name
        else:  
            print("Invalid Directory Name!")
            print("Please enter a valid directory name!")

# Prompt user 
projectName = str(project())
dir_name = str(dirName(projectName))

########################################
########################################
######## Make Base Directories #########
########################################
########################################
os.system('mkdir "' + dir_name +'"')

#######################################
#######################################
######## Install Requirements #########
#######################################
#######################################

os.system('pip install PyGithub')
os.system('pip install virtualenv')

#######################################
#######################################
######## Download GitHub Repo #########
#######################################
#######################################

def get_sha_for_tag(repository, tag):
    """
    Returns a commit PyGithub object for the specified repository and tag.
    """
    branches = repository.get_branches()
    matched_branches = [match for match in branches if match.name == tag]
    if matched_branches:
        return matched_branches[0].commit.sha

    tags = repository.get_tags()
    matched_tags = [match for match in tags if match.name == tag]
    if not matched_tags:
        raise ValueError('No Tag or Branch exists with that name')
    return matched_tags[0].commit.sha

def download_directory(repository, sha, server_path):
    """
    Download all contents at server_path with commit tag sha in
    the repository.
    """
    contents = repository.get_contents(server_path, ref=sha)

    for content in contents:
        print ("Processing %s" % content.path)
        if content.type == 'dir':
            os.system('mkdir "' + dir_name + '/' + content.path + '"')
            download_directory(repository, sha, content.path)
        else:
            try:
                path = content.path
                file_content = repository.get_contents(path, ref=sha)
                file_data = base64.b64decode(file_content.content)
                file_out = open(dir_name + '/' + content.path , "wb")
                file_out.write(file_data)
                file_out.close()
            except (GithubException, IOError) as exc:
                logging.error('Error processing %s: %s', content.path, exc)

gitToken = '976ff91676ee45f4f32073328e920494b3f8e1e1'

g = Github(gitToken)

owner = "RyanJulyan"
repo = "BDA"
full_repo = "{}/{}".format(owner,repo)

repository = g.get_repo(full_repo)

branch_or_tag_to_download = 'main'
sha = get_sha_for_tag(repository, branch_or_tag_to_download)

directory_to_download = 'template'
download_directory(repository, sha, directory_to_download)

#######################################
#######################################
######### Install virtualenv ##########
#######################################
#######################################

os.system('cd "' + dir_name + '" && virtualenv env')

