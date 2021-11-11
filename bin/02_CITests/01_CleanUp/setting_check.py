import sys
import configparser
import os

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


        
def _check_dir(set_dir_list):
    for dir in set_dir_list:
        if  os.path.exists(dir) is False:
            os.makedirs(dir)
            print(f'Create path {dir}')
    
def _check_file(set_file_list):
    for file in set_file_list:
        if os.path.isfile(file) is False:
            print(f'File {file} does not exist.')



if __name__ == '__main__':
    sys.path.append('bin/02_CITests')
    import _config
    setting = dir(_config)

    from setting_check import Check_Settings
    check = Check_Settings(setting)
    result = check._get_setting()
    from _config import *


    _check_dir(result[1])
    _check_file(result[0])