import pandas as pd
import os
from mako.template import Template
import sys


class CI_yml_templates(object):

    def __init__(self, library, package_list, dymolaversion, wh_library, git_url, wh_path):
        self.library = library
        self.package_list = package_list
        self.dymolaversion = dymolaversion
        self.wh_library = wh_library
        self.git_url = git_url
        self.wh_path = wh_path

        # except commits
        self.update_ref_commit = "^ci_update_ref_.*$"
        self.dif_ref_commit = "ci_dif_ref"
        self.html_commit = "ci_correct_html"
        self.create_wh_commit = "ci_create_whitelist"

        self.bot_merge_commit = "Update WhiteList_CheckModel.txt and HTML_IBPSA_WhiteList.txt"
        self.bot_push_commit = "Automatic push of CI with new regression reference files. Please pull the new files before push again."
        self.bot_update_wh_commit = "Update or created new whitelist [skip ci]. Please pull the new whitelist before push again."
        # - $CI_COMMIT_MESSAGE =~ /CI - Create IBPSA Merge/
        # - $CI_COMMIT_MESSAGE =~ /fix errors manually/
        # - $CI_COMMIT_MESSAGE =~/Trigger CI - give different reference results/
        # - $CI_COMMIT_MESSAGE  =~ /Trigger CI - Update reference results/

        self.except_commit_list = [self.update_ref_commit, self.dif_ref_commit, self.html_commit, self.create_wh_commit, self.bot_merge_commit , self.bot_push_commit]

        # except branches
        self.merge_branch = wh_library + "_Merge"

        # files
        sys.path.append('bin/02_CITests')
        from _config import ch_file, wh_file, reg_temp, write_temp, sim_temp, page_temp, ibpsa_temp, main_temp, temp_dir, exitfile
        self.ch_file = ch_file
        self.wh_file = wh_file

        self.reg_temp = reg_temp
        self.write_temp = write_temp
        self.sim_temp = sim_temp
        self.page_temp = page_temp
        self.ibpsa_temp = ibpsa_temp
        self.main_temp = main_temp
        self.temp_dir = temp_dir
        self.exitfile = exitfile.replace(os.sep, "/")


    def _write_package(self):
        data = {'Package': self.package_list}
        df = pd.DataFrame(data, columns=['Package'])
        csv_file = f'bin{os.sep}02_CITests{os.sep}ci_templates{os.sep}templates{os.sep}UnitTests{os.sep}configuration.csv'
        df.to_csv(csv_file, index=False, header=True)

    def _write_conf_csv(self):
        data = {'Package': self.package_list}
        df = pd.DataFrame(data, columns=['Package'])
        csv_file = f'bin{os.sep}02_CITests{os.sep}ci_templates{os.sep}templates{os.sep}UnitTests{os.sep}configuration.csv'
        df.to_csv(csv_file, index=False, header=True)

    def _write_merge_template(self):
        mytemplate = Template(filename=self.ibpsa_temp)
        yml_text = mytemplate.render(git_url=self.git_url, merge_branch=self.merge_branch, dymolaversion=self.dymolaversion, except_commit_list=self.except_commit_list, GITLAB_USER_NAME="${GITLAB_USER_NAME}",
                                    GITLAB_USER_EMAIL="${GITLAB_USER_EMAIL}", CI_PROJECT_NAME="${CI_PROJECT_NAME}", Github_Repository="${Github_Repository}", Merge_Branch="${Merge_Branch}", IBPSA_Repo="${IBPSA_Repo}",
                                    GITHUB_PRIVATE_KEY="${GITHUB_PRIVATE_KEY}", library=self.library, Target_Branch="${Target_Branch}", GITHUB_API_TOKEN="${GITHUB_API_TOKEN}", bot_commit=self.bot_merge_commit)
        yml_tmp = open(self.ibpsa_temp.replace(".txt", ".gitlab-ci.yml"), "w")
        yml_tmp.write(yml_text.replace("\n", ""))
        yml_tmp.close()

    def _write_regression_template(self):
        mytemplate = Template(filename=self.reg_temp)
        yml_text = mytemplate.render(library=self.library, lib_package="${lib_package}", dymolaversion=self.dymolaversion, except_commit_list=self.except_commit_list, package_list=self.package_list,
                                    update_commit=self.update_ref_commit,  merge_branch=self.merge_branch, TARGET_BRANCH="${TARGET_BRANCH}", GITLAB_Page="${GITLAB_Page}",
                                    GITHUB_API_TOKEN="${GITHUB_API_TOKEN}", Github_Repository="${Github_Repository}", GITLAB_USER_NAME="${GITLAB_USER_NAME}", GITLAB_USER_EMAIL="${GITLAB_USER_EMAIL}",
                                    CI_PROJECT_NAME="${CI_PROJECT_NAME}", exitfile=self.exitfile, ch_file=self.ch_file)
        yml_tmp = open(self.reg_temp.replace(".txt", ".gitlab-ci.yml"), "w")
        yml_tmp.write(yml_text.replace("\n", ""))
        yml_tmp.close()
    #def _write_setting_template(self):

    def _write_check_template(self):
        if self.wh_library is not None:
            filterflag = "--filterwhitelist"
            wh_flag = "--wh-library " + self.wh_library
            if self.wh_path is not None:
                wh_path = "--wh-path " + self.wh_path
                git_url = ""
            elif self.git_url is not None:
                git_url = "--git-url " + self.git_url
                wh_path = ""
            else:
                wh_path = ""
                git_url = ""
        else:
            wh_flag = ""
            git_url = ""
            filterflag = ""
            wh_path = ""

        mytemplate = Template(filename=self.write_temp)
        yml_text = mytemplate.render(package_list=self.package_list, library=self.library, lib_package="${lib_package}",
                                     dymolaversion=self.dymolaversion, package_name="${package_name}", wh_flag=wh_flag,
                                     filterflag=filterflag, except_commit_list=self.except_commit_list,
                                     merge_branch=self.merge_branch, wh_commit=self.create_wh_commit,
                                     wh_library=self.wh_library, wh_path=wh_path, git_url=git_url, wh_file=self.wh_file.replace(os.sep, "/"), ch_file=self.ch_file.replace(os.sep, "/"), bot_update_wh_commit=self.bot_update_wh_commit, TARGET_BRANCH="$CI_COMMIT_REF_NAME",
                                     GITHUB_PRIVATE_KEY="${GITHUB_PRIVATE_KEY}", GITLAB_USER_NAME="${GITLAB_USER_NAME}", GITLAB_USER_EMAIL="${GITLAB_USER_EMAIL}", Github_Repository="${Github_Repository}", CI_PROJECT_NAME="${CI_PROJECT_NAME}",
                                     exitfile=self.exitfile)
        yml_tmp = open(self.write_temp.replace(".txt", ".gitlab-ci.yml"), "w")
        yml_tmp.write(yml_text.replace("\n", ""))
        yml_tmp.close()

    def _write_simulate_template(self):
        if self.wh_library is not None:
            filterflag = "--filterwhitelist"
            wh_flag = "--wh-library " + self.wh_library
        else:
            filterflag = ""
            wh_flag = ""
        mytemplate = Template(filename=self.sim_temp)
        yml_text = mytemplate.render(package_list=self.package_list, library=self.library, lib_package="${lib_package}",
                                     dymolaversion=self.dymolaversion, package_name="${package_name}", wh_flag=wh_flag,
                                     filterflag=filterflag, except_commit_list=self.except_commit_list,
                                     merge_branch=self.merge_branch, git_url=self.git_url,
                                     wh_commit=self.create_wh_commit, wh_library=self.wh_library, ch_file=self.ch_file)
        yml_tmp = open(self.sim_temp.replace(".txt", ".gitlab-ci.yml"), "w")
        yml_tmp.write(yml_text.replace("\n", ""))
        yml_tmp.close()

    def _write_main_yml(self, image_name, stage_list, variable_list, project, file_list):
        mytemplate = Template(filename=self.main_temp)
        yml_text = mytemplate.render(image_name=image_name, stage_list=stage_list, variable_list=variable_list, project=project, file_list=file_list)
        yml_tmp = open(self.main_temp.replace("gitlab-ci.txt", ".gitlab-ci.yml"), "w")
        yml_tmp.write(yml_text.replace("\n", ""))
        yml_tmp.close()

    def _get_variables(self):
        variable_list =['Praefix_Branch: "Correct_HTML_"', 'TARGET_BRANCH: $CI_COMMIT_REF_NAME', 'Newbranch: ${Praefix_Branch}${CI_COMMIT_REF_NAME}', 'Github_Repository: git SvenHinrichs/GitLabCI', 'GITLAB_Page: "https://svenhinrichs.pages.rwth-aachen.de/GitLabCI"']
        return variable_list

    def _get_image_name(self):
        image_name = 'registry.git.rwth-aachen.de/ebc/ebc_intern/dymola-docker:miniconda-latest'
        return image_name

    def _get_project_name(self):
        project_name = 'EBC/EBC_all/gitlab_ci/templates'
        return project_name

    def _get_yml_templates(self):

        file_list = []
        for subdir, dirs, files in os.walk(self.temp_dir):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".yml") and file != ".gitlab-ci.yml":
                    filepath = filepath.replace(os.sep, "/")
                    file_list.append(filepath)
        if len(file_list) == 0:
            print(f'No templates')
            exit(1)
        return file_list

    def _get_stages(self, file_list):
        stage_list = []
        for file in file_list:
            infile = open(file, "r")
            lines = infile.readlines()
            stage_content = False
            for line in lines:
                line = line.strip()
                if len(line.strip()) == 0:
                    continue
                elif line.find("stages:") > -1:
                    stage_content = True
                elif line.find(":") > -1 and line.find("stages:") == -1:
                    stage_content = False
                elif stage_content is True:
                    line = line.replace("-", "")
                    line = line.replace(" ", "")
                    print("stage: " + line)
                    stage_list.append(line)
                else:
                    continue
        if len(stage_list) == 0:
            print(f'No stages')
            exit(1)
        stage_list = list(set(stage_list))
        return stage_list

def _get_package(library):
    for subdir, dirs, files in os.walk(library):
        return dirs


def _config_test():
    config_list = []
    response = input(f'Config template: check models? (y/n) ')
    if response == "y":
        print(f'Create check template')
        config_list.append("check")
    response = input(f'Config template: simulate examples? (y/n) ')
    if response == "y":
        print(f'Create simulate template')
        config_list.append("simulate")
    response = input(f'Config template: regression test? (y/n) ')
    if response == "y":
        print(f'Create regression template')
        config_list.append("regression")
    response = input(f'Config template: Merge Update? (y/n) ')
    if response == "y":
        print(f'Create merge template')
        config_list.append("Merge")
    return config_list


def _config_settings_check():
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

    response = input(
        f'Create whitelist? Useful if your own library has been assembled from other libraries. A whitelist is created, where faulty models from the foreign library are no longer tested in the future and are filtered out. (y/n)  ')
    if response == "y":
        wh_config = True
        while wh_config is True:
            wh_library = input(f'What library models should on whitelist: Give the name of the library: ')
            print(f'Setting whitelist library: {wh_library}')

            response = input(f'If the foreign library is local on the PC? (y/n) ')
            if response == "y":
                wh_path = input(f'Specify the local path of the library (eg. D:\..path..\AixLib) ')
                print(f'path of library: {wh_path}')
                git_url = None
            else:
                git_url = input(f'Give the url of the library repository: ')
                print(f'Setting git_url: {git_url}')
                wh_path = None

            response = input(f'Are settings okay(y/n)? ')
            if response == "y":
                wh_config = False
                return library, package_list_final, dymolaversion, wh_library, git_url, wh_path
    wh_library = None
    git_url = None
    wh_path = None
    return library, package_list_final, dymolaversion, wh_library, git_url, wh_path

if __name__ == '__main__':
    # python bin/02_CITests/ci_templates/ci_templates.py


    from ci_templates import CI_yml_templates

    config_list = _config_test()
    if len(config_list) == 0:
        exit(0)

    result = _config_settings_check()
    library = result[0]
    package_list = result[1]
    dymolaversion = result[2]
    wh_library = result[3]
    #git_url = result[4]
    wh_path = result[5]
    git_url = "https://github.com/ibpsa/modelica-ibpsa.git"
    CI_Class = CI_yml_templates(library, package_list, dymolaversion, wh_library, git_url, wh_path)
    for temp in config_list:
        if temp == "check":
            CI_Class._write_check_template()
        if temp == "simulate":
            CI_Class._write_simulate_template()
        if temp == "regression":
            CI_Class._write_regression_template()
        if temp == "Merge":
            CI_Class._write_merge_template()
    variable_list = CI_Class._get_variables()
    print(f'Setting variables: {variable_list}')
    image_name = CI_Class._get_image_name()
    print(f'Setting image: {image_name}')
    project = CI_Class._get_project_name()
    print(f'Setting project: {project}')
    file_list = CI_Class._get_yml_templates()
    print(f'Setting yml files: {file_list}')
    stage_list = CI_Class._get_stages(file_list)
    print(f'Setting stages: {stage_list}')
    CI_Class._write_main_yml(image_name, stage_list, variable_list, project, file_list)

