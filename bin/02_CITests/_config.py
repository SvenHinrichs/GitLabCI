import os

#[Whitelist files]
ch_file = f'bin{os.sep}06_Configfiles{os.sep}ci_changed_model_list.txt'
wh_file = f'bin{os.sep}03_ci_whitelist{os.sep}model_whitelist.txt'
exit_file = f'bin{os.sep}06_Configfiles{os.sep}exit.sh'
eof_file = f'bin{os.sep}06_Configfiles{os.sep}EOF.sh'
new_ref_file = f'bin{os.sep}06_Configfiles{os.sep}ci_new_created_reference.txt'
ref_file = f'bin{os.sep}06_Configfiles{os.sep}ci_reference_list.txt'
ref_whitelist_file = f'bin{os.sep}03_ci_whitelist{os.sep}reference_check_whitelist.txt'
html_wh_file = f'bin{os.sep}03_ci_whitelist{os.sep}html_whitelist.txt'
show_ref_file = f'bin{os.sep}08_interact_CI{os.sep}show_ref.txt'
update_ref_file = f'bin{os.sep}08_interact_CI{os.sep}update_ref.txt'

# Ci Templates
reg_temp_file = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}UnitTests{os.sep}regression_test.txt'
write_temp_file = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}UnitTests{os.sep}check_model.txt'
sim_temp_file = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}UnitTests{os.sep}simulate_model.txt'
page_temp_file = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}deploy{os.sep}gitlab_pages.txt'
ibpsa_temp_file = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}deploy{os.sep}IBPSA_Merge.txt'
style_check_temp_file = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}03_SyntaxTest{os.sep}style_check.txt'
html_temp_file = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}03_SyntaxTest{os.sep}html_check.txt'
main_temp_file = f'bin{os.sep}07_templates{os.sep}03_ci_templates{os.sep}gitlab-ci.txt'
main_yml_file = f'.gitlab-ci.yml'

temp_dir = f'bin{os.sep}07_templates{os.sep}03_ci_templates'

# Charts
chart_temp_file = f'bin{os.sep}07_templates{os.sep}01_google_templates{os.sep}google_chart.txt'
index_temp_file = f'bin{os.sep}07_templates{os.sep}01_google_templates{os.sep}index.txt'
layout_temp_file = f'bin{os.sep}07_templates{os.sep}01_google_templates{os.sep}layout_index.txt'

chart_dir = f'bin{os.sep}07_templates{os.sep}02_charts'

# Reference files
ref_file_dir = f'Resources{os.sep}ReferenceResults{os.sep}Dymola'
resource_dir = f'Resources{os.sep}Scripts{os.sep}Dymola'

# image_name
image_name = 'registry.git.rwth-aachen.de/ebc/ebc_intern/dymola-docker:miniconda-latest'
project_name = 'SvenHinrichs/GitLabCI'
variable_main_list = ['Praefix_Branch: "Correct_HTML_"', 'TARGET_BRANCH: $CI_COMMIT_REF_NAME', 'Newbranch: ${Praefix_Branch}${CI_COMMIT_REF_NAME}', 'Github_Repository: SvenHinrichs/GitLabCI', 'GITLAB_Page: "https://svenhinrichs.pages.rwth-aachen.de/GitLabCI"']
stage_list = ["Ref_Check", "build", "HTMLCheck", "StyleCheck", "check", "openMR", "post", "create_whitelist", "simulate", "RegressionTest", "Update_Ref", "plot_ref", "prepare", "deploy"]
# Pull Request Comment
#self.post_comment_message = f'Error in regression test.\\n Compare the results on the following page {self.page_url}'
