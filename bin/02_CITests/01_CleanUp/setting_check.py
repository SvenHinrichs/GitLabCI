import sys
import configparser
import os
import argparse

class Check_Settings(object):

    def __init__(self, setting):
        self.setting = setting

    def _get_setting(self):
        set_file_list = []
        set_dir_list = []
        var_list = []
        for set in self.setting:
            if set.find("__") > -1:
                continue
            if set.find("file") > -1 :
                set_file_list.append(set)
            if set.find("dir") > -1:
                set_dir_list.append(set)
        return set_file_list, set_dir_list


        
def _check_dir(path_list):
    for path in path_list:
        if os.path.exists(path) is False:
            print(f'Path {path} does not exist and will be created')
            os.makedirs(path)
        else:
            continue

def _check_file(file_list):
    for file in file_list:
        if os.path.isfile(file) is False:
            print(f'File {file} does not exist.')
            file_in = open(file, "w")
            file_in.close()
        else:
            continue


def _check_variables(variable_main_list, github_token, github_private_key, GL_Token):
    for var in variable_main_list:
        if var is None:
            print(f'Please set variable {var}.')
        else:
            print(f'variable {var} is set in file .gitlab-ci.yml.')
    if github_token is None:
        print(f'Please set variable GITHUB_API_TOKEN in your gitlab ci repo under CI/Variables.')
    if github_private_key is None:
        print(f'Please set variable GITHUB_PRIVATE_KEY in your gitlab ci repo under CI/Variables.')
    if GL_Token is None:
        print(f'Please set variable GL_TOKEN in your gitlab ci repo under CI/Variables.')




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Set Github Environment Variables")  # Configure the argument parser
    check_test_group = parser.add_argument_group("Arguments to set Environment Variables")
    check_test_group.add_argument('-GT', "--github-token", help="Your Set GITHUB Token")
    check_test_group.add_argument("-GR", "--github-private-key",
                                  help="Environment Variable owner/RepositoryName")
    check_test_group.add_argument('-GP', "--GL-Token",  help="Set your gitlab page url")
    args = parser.parse_args()
    sys.path.append('bin/02_CITests')

    from setting_check import Check_Settings
    from _config import *
    file_list = [ch_file, exit_file, eof_file, new_ref_file, ref_file, wh_file, ref_whitelist_file, html_wh_file, show_ref_file, update_ref_file, reg_temp_file, write_temp_file, sim_temp_file, page_temp_file, ibpsa_temp_file,
                 style_check_temp_file, html_temp_file, main_temp_file, main_yml_file, chart_temp_file, index_temp_file, layout_temp_file, setting_file]
    path_list = [artifacts_dir, temp_dir, chart_dir, ref_file_dir, resource_dir]
    _check_dir(path_list)
    _check_file(file_list)
    gitlab_ci_variables = [args.github_token, args.github_private_key, args.GL_Token]
    _check_variables(variable_main_list, github_token=args.github_token, github_private_key=args.github_private_key, GL_Token=args.GL_Token)

