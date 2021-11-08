import os
import codecs
import sys
import shutil
import argparse


class Deploy_Artifacts(object):

    def __init__(self, library):
        self.library = library
        self.folder = 'Referencefiles'

        self.green = '\033[0;32m'
        self.CRED = '\033[91m'
        self.CEND = '\033[0m'

        sys.path.append('bin/02_CITests')
        from _config import ch_file
        self.ch_file = ch_file

    def _get_changed_ref(self):  # list all changed reference results to a list
        changed_file = codecs.open(self.ch_file, "r", encoding='utf8')
        lines = changed_file.readlines()
        changed_ref = []
        for line in lines:
            if line.find("txt") > -1 and line.find("ReferenceResults") > -1 and line.find("Resources") > -1:
                line = line.strip()
                ref = line[line.find(self.library):line.rfind("txt") + 3]
                changed_ref.append(ref)
                continue
            else:
                continue
        changed_file.close()
        return changed_ref

    def copy_txt(self, changed_ref):  # Copy reference results from AixLib\Resources\ReferenceResults\Dymola\* to Referencefiles\\*
        if os.path.exists(self.folder) is False:
            os.mkdir(self.folder)
        for ref in changed_ref:
            destination = self.folder + os.sep + ref[ref.rfind(os.sep):]
            try:
                shutil.copy(ref, destination)
                continue
            except FileNotFoundError:
                print(f'{self.CRED}Cannot find folder:{self.CEND} {destination}')



if __name__ == '__main__':
    #  python bin/02_CITests/CleanUpSkripts/deploy_artifacts.py --library AixLib --ref
    parser = argparse.ArgumentParser(description='deploy artifacts')
    unit_test_group = parser.add_argument_group("arguments to run deploy artifacts")
    unit_test_group.add_argument("-L", "--library", default="AixLib", help="Library to test")
    unit_test_group.add_argument("--ref", help='Deploy new reference files', action="store_true")
    args = parser.parse_args()

    from deploy_artifacts import Deploy_Artifacts

    if args.ref is True:
        ref_artifact = Deploy_Artifacts(library=args.library)
        changed_ref = ref_artifact._get_changed_ref()
        ref_artifact.copy_txt(changed_ref)
