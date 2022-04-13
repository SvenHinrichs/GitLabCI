import argparse
import os


def create_branch_name(issue_title):
    branch_list = issue_title.split(" ")
    file = open(f'bin{os.sep}Configfiles{os.sep}ci_branch_name.txt', "w")
    print(len(branch_list))
    if len(branch_list) > 2:
        branch_name = f'{branch_list[0]}_{branch_list[1]}_{branch_list[2]}'
    elif len(branch_list) > 1:
        branch_name = f'{branch_list[0]}_{branch_list[1]}'
    else:
        branch_name = f'{issue_title}'
    print(f'Branchname is {branch_name}')
    file.write(branch_name)
    file.close()

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Create a branchname')
    check_test_group = parser.add_argument_group("arguments to run check tests")
    check_test_group.add_argument('-s', "--issue-title", metavar="AixLib.Package",
                                  help="Test only the Modelica package AixLib.Package")
    args = parser.parse_args()  # Parse the arguments
    create_branch_name(args.issue_title)

