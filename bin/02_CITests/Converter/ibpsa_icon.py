import os
from pathlib import Path

class Lock_model(object):

    def __init__(self, path):
        self.path = path
        sys.path.append('bin/02_CITests')

        from _config import html_wh_file
        self.html_wh_file = html_wh_file

    def _read_wh(self):  # Read whitelist and return a list
        wh = open(self.html_wh_file, "r")
        wl_lines = wh.readlines()
        wh.close()
        return wl_lines

    def _sort_list(self, wl_lines):  # Sort List of models
        list = []
        for line in wl_lines:
            if len(line) == 1:
                continue
            if line.find("package.mo") > -1 :
                continue
            if line.find("package.order") > -1 :
                continue
            if line.find("UsersGuide") > -1:
                continue
            else:
                line = line.replace("IBPSA","AixLib")
                numb = line.count(".")
                mo = line.replace(".", os.sep, numb-1)
                mo = mo.lstrip()
                mo = mo.strip()
                list.append(mo)
        return list

    def _add_icon(self, mo_li): # Add ibpsa icon and search a suitable line
        entry = "  extends AixLib.Icons.ibpsa;"
        for i in mo_li:
            if (exist_file(i)) == True:
                print(i)
                f = open(i,"r+")
                lines = f.readlines()
                f.close()
                mo = i[i.rfind(os.sep)+1:i.rfind(".mo")]
                y = []
                c = 0
                num = 0
                semi = 0
                ano = 0
                for t in lines:
                    c = c + 1
                    if t.find(mo) > -1:  #ModelName == Zeile Mit Modelname
                        if len(y) == 0:
                            if t.find("type ") > -1:
                                y = []
                                break
                            if t.find("function ") > -1:
                                y = []
                                break
                            if t.find("record ") > -1:
                                y = []
                                break
                            if t.find("package ") > -1:
                                y = []
                                break
                            if t.find("=") > -1:
                                y = []
                                break
                            else:
                                if t.count('"') == 2:
                                    y.append(c)
                                    continue
                                else:
                                    ano = 1
                                    y.append(c)
                                    continue
                    if len(y) == 1 and ano == 1:
                            if t.count('"') == 2:
                                y.append(c)
                                continue
                    if t.find(";")> -1 and semi == 1:
                        y.append(c)
                        semi = 0
                        continue
                    if t.find("parameter") > -1:
                        break
                    if t.find("annotation")> -1 :
                        break
                    if t.find("extends") > -1:
                        num = 1
                        if t.find("extends AixLib.Icons.ibpsa;") == -1:
                            if t.find(";") > -1:
                                y.append(c)
                                continue
                            else:
                                semi = 1
                                y.append(c)

                    if t.find("extends AixLib.Icons.ibpsa;") > -1:
                            y = []
                            break
                    if num == 1:
                        if len(t) == 0:
                            y.append(c)
                            break
                if len(y)==0:
                    continue
                else:
                    lines.insert(y[len(y)-1] , "\n" + entry +  "\n")
                    f = open(i, "w")
                    f.writelines(lines)
                    f.close()
            else:
                print("\n************************************")
                print(i)
                print("File does not exist.")

    def _exist_file(self, file):  # File exist
        f = Path(file)
        if f.is_file():
            return True
        else:
            return False

    def _lock_model(self, mo_li):  # lock ibpsa models
        entry = '   __Dymola_LockedEditing="ibpsa");'
        old_text = '</html>"));'
        new_text = '</html>"), ' +"\n" + entry
        replacements = {old_text : new_text}
        lines = []
        for model in mo_li:

            if exist_file(model) == True:
                print("lock object: "+model)
                infile = open(model).read()
                outfile = open(model, 'w')

                for i in replacements.keys():
                    infile = infile.replace(i, replacements[i])
                outfile.write(infile)
                outfile.close

            else:
                print("\n************************************")
                print(model)
                print("File does not exist.")
                continue

if __name__ == '__main__':

    from ibpsa_icon import Lock_model
    lock = Lock_model()
    wl_lines = lock._read_wh()
    mo_li = lock._sort_list(wl_lines)
    lock._lock_model(mo_li)
