
## CI commands and CI list

These lists should create a link between the CI and the user. If certain models are displayed graphically or certain reference files are created or updated, these are to be written into the files "show_ref.txt" or "update_ref.txt" line by line. 

show_ref : Lists all mentioned reference results graphically.  
update_ref : Updates the model and the whole package in which the model is located.

## Command list
- update_ref_commit = "ci_update_ref" # Update referencefiles for all models in file  bin/08_interact_CI/update_ref.txt
- show_ref_commit = "ci_show_ref"	# plot all referencifiles in file bin/08_interact_CI/show_ref.txt
- dif_ref_commit = "ci_dif_ref"
- html_commit = "ci_correct_html" 
- create_wh_commit = "ci_create_whitelist" y
- create_html_wh_commit = "ci_create_html_whitelist"  y
- simulate_commit = "ci_simulate" y
- check_commit = "ci_check" y
- regression_test_commit = "ci_regression_test"
- ci_html_commit = "ci_html"