import pandas as pd
import os
from mako.template import Template
class CI_yml_templates(object):
    update_ref_commit: str

    def __init__(self, library, package_list, dymolaversion, wh_library):
        self.library = library
        self.package_list = package_list
        self.dymolaversion = dymolaversion
        self.wh_library = wh_library

        #except commits
        self.update_ref_commit = "ci_update_ref"
        self.dif_ref_commit = "ci_dif_ref"
        self.html_commit = "correct_html"
        self.except_commit_list = [self.update_ref_commit, self.dif_ref_commit, self.html_commit]

        #except branches
        self.merge_branch = wh_library+"_Merge"

    def _write_package(self):
        data = {'Package': self.package_list}
        df = pd.DataFrame(data, columns=['Package'])
        csv_file  = f'bin{os.sep}02_CITests{os.sep}ci_templates{os.sep}templates{os.sep}UnitTests{os.sep}configuration.csv'
        df.to_csv(csv_file, index=False, header=True)

    def _write_conf_csv(self):
        data = {'Package': self.package_list}
        df = pd.DataFrame(data, columns=['Package'])
        csv_file = f'bin{os.sep}02_CITests{os.sep}ci_templates{os.sep}templates{os.sep}UnitTests{os.sep}configuration.csv'
        df.to_csv(csv_file, index=False, header=True)

    def _write_check_template(self):
        temp = f'bin{os.sep}02_CITests{os.sep}ci_templates{os.sep}templates{os.sep}UnitTests{os.sep}check_model.txt'
        yml = f'bin{os.sep}02_CITests{os.sep}ci_templates{os.sep}templates{os.sep}UnitTests{os.sep}check_model.gitlab-ci.yml'

        if self.wh_library is not None:
            filterflag = "--filterwhitelist"
            wh_flag = "--wh-library " + wh_library
        else:
            filterflag = ""
            wh_flag = ""
        mytemplate = Template(filename=temp)
        yml_text = mytemplate.render(package_list=self.package_list, library=self.library, lib_package="${lib_package}", dymolaversion=self.dymolaversion, package_name="${package_name}", wh_library=wh_flag, filterflag=filterflag, except_commit_list=self.except_commit_list, merge_branch=self.merge_branch)
        yml_tmp = open(yml, "w")
        yml_tmp.write(yml_text.replace("\n",""))
        yml_tmp.close()

    def _write_simulate_template(self):
        temp = f'bin{os.sep}02_CITests{os.sep}ci_templates{os.sep}templates{os.sep}UnitTests{os.sep}simulate_model.txt'
        yml = f'bin{os.sep}02_CITests{os.sep}ci_templates{os.sep}templates{os.sep}UnitTests{os.sep}simulate_model.gitlab-ci.yml'
        mytemplate = Template(filename=temp)
        yml_text = mytemplate.render(package_list=self.package_list, library=self.library, lib_package="${lib_package}",
                                     dymolaversion=self.dymolaversion, package_name="${package_name}")
        yml_tmp = open(yml, "w")
        yml_tmp.write(yml_text.replace("\n", ""))
        yml_tmp.close()


    #def _write_whitelist_template(package_list,library,dymolaversion):

def _get_package(library):
    for subdir, dirs, files in os.walk(library):
        return dirs

def _config_settings():
    library = input(f'What library should test package? ')
    print(f'Setting library: {library}')

    package_list = _get_package(library)
    package_list_final = []
    for package in package_list:
        response = input(f'Test package {package}? (y/n) ')
        if response == "y":
            package_list_final.append(package)
            continue
    print(f'Setting packages: {package_list_final}')

    dymolaversion = input(f'Give the dymolaversion (e.g. 2020): ')
    print(f'Setting dymola version: {dymolaversion}')

    response = input(f'Create whitelist? Useful if your own library has been assembled from other libraries. A whitelist is created, where faulty models from the foreign library are no longer tested in the future and are filtered out. (y/n)  ')
    if response == "y":
        wh_config = True
        while wh_config is True:
            wh_library = input(f'What library models should on whitelist: Give the name of the library: ')
            print(f'Setting whitelist library: {wh_library}')

            response = input(f'If the foreign library is local on the PC? (y/n) ')
            if response == "y":
                path = input(f'Specify the local path of the library ')
                print(f'path of library: {path}')
            else:
                git_url = input(f'Give the url of the library repository: ')
                print(f'Setting git_url: {git_url}')

            response = input(f'Are settings okay(y/n)? ')
            if response == "y":
                wh_config = False
                return library, package_list_final, dymolaversion, wh_library, git_url
    wh_library = None
    git_url = None
    return library, package_list_final, dymolaversion, wh_library, git_url




# python bin\02_CITests\UnitTests\CheckPackages\validatetest.py -DS 2019 --single-package "Airflow" --library "AixLib"
# python bin\02_CITests\UnitTests\CheckPackages\validatetest.py -DS 2019 --single-package "Airflow" --library "AixLib" --SimulateExamples
# python bin\02_CITests\UnitTests\CheckPackages\validatetest.py -DS 2019 --single-package "Airflow" --library "AixLib" --wh-library "IBPSA" --filterwhitelist
# python bin\02_CITests\UnitTests\CheckPackages\validatetest.py -DS 2019 --repo-dir IBPSA --git-url https://github.com/ibpsa/modelica-ibpsa.git --library AixLib --wh-library IBPSA --whitelist

if __name__ == '__main__':
    # python bin/02_CITests/ci_templates/ci_templates.py
    from ci_templates import CI_yml_templates

    result = _config_settings()
    library = result[0]
    package_list = result[1]
    dymolaversion = result[2]
    wh_library = result[3]
    git_url = result[4]
    CI_Class = CI_yml_templates(library, package_list, dymolaversion, wh_library)
    CI_Class._write_check_template()

    #_write_conf_csv(package_list)
    #_write_check_template(package_list, library, dymolaversion, wh_library)
    #_write_check_template(package_list, library, dymolaversion)
    #_write_simulate_template(package_list, library, dymolaversion)
