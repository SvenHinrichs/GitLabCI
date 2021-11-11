import os
import io
import argparse
import shutil
from git import Repo

# ! /usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""View errors in the HTML code of a Modelica .mo file

@author: Sven Hinrichs
The script will
* collect all the HTML code (<html>...</html>) in the Modelica file and
* print out the original code with line numbers as well as
* the tidy version of the code (with line numbers).
* tidylib will look for errors and present the respective line numbers.

You can then inspect the code and make corrections to your Modelica
file by hand. You might want to use the tidy version as produced by
tidylib.

Example
-------
You can use this script on the command line and point it
to your Modelica file::

	$ python html_tidy_errors.py <file> [file [...]]

Note:
-----
	* This script uses Python 3.6 for printing syntax and
	function parameter annotations.
	* The script assumes that you have installed pytidylib

	`$ pip install pytidylib`

	* You also need to install the necessary dll's and
	your python interpreter must be able to find the files.
	In case of trouble just put the dll in your working dir.

	[http://binaries.html-tidy.org/](http://binaries.html-tidy.org/)
"""


class HTML_Tidy(object):
    """Class to Check Packages and run CheckModel Tests"""
    """Import Python Libraries"""

    def __init__(self, package, rootDir, correct_overwrite, correct_backup, log, font, align, WhiteList, correct_view,
                 library, wh_library):
        self.package = package
        self.rootDir = rootDir
        self.correct_overwrite = correct_overwrite
        self.correct_backup = correct_backup
        self.log = log
        self.font = font
        self.align = align
        self.WhiteList = WhiteList
        self.correct_view = correct_view
        self.library = library
        self.wh_library = wh_library
        sys.path.append('../bin/02_CITests')
        from _config import html_wh_file
        self.html_wh_file = html_wh_file

        self.CRED = '\033[91m'
        self.CEND = '\033[0m'
        self.green = "\033[0;32m"

    def run_files(self):  # Make sure that the parameter rootDir points to a Modelica package.
        rootDir = self.package.replace(".", os.sep)
        topPackage = os.path.join(rootDir, "package.mo")
        errMsg = list()
        if not os.path.isfile(topPackage):
            raise ValueError("Argument rootDir=%s is not a Modelica package. Expected file '%s'." % (
                rootDir, topPackage))
        file_counter = 0
        model_list = HTML_Tidy._ListAixLibModel(self)
        for model in model_list:
            model = model.replace(".", os.sep)
            model = model.replace(os.sep + "mo", ".mo")
            results = HTML_Tidy._CheckFile(self, model)
            document_corr = results[0]
            err = results[1]
            if err is not "":  # write error to error message
                errMsg.append("[-- %s ]\n%s" % (model, err))
            if self.correct_backup:
                HTML_Tidy._backup_old_files(
                    self, model, document_corr, file_counter)
            if self.correct_overwrite:
                HTML_Tidy._correct_overwrite(self, model, document_corr)
                continue
            if self.correct_view:
                htmlList = HTML_Tidy.getInfoRevisionsHTML(self, model)
                htmlStr = HTML_Tidy.join_body(
                    self, htmlList=htmlList, substitutions_dict={'\\"': '"'})
                document_corr, errors = HTML_Tidy.htmlCorrection(self, htmlStr)
                docCorrStr = HTML_Tidy.number_print_List(self, document_corr.split('\n'), sep='\n')
                ErrWhite = "Warning: The summary attribute on the <table> element is obsolete in HTML5"
                if len(errors) > 0 and errors.find(ErrWhite) == -1:
                    print('\n' + "----" + model + "----")
                    print("\n-------- HTML Code --------")
                    print(f"\n{HTML_Tidy.number_print_List(self, htmlList)}")
                    print(self.green + "\n-------- Corrected Code --------" + self.CEND)
                    print(f"\n{docCorrStr}")
                    print(self.CRED + "\n-------- Errors --------" + self.CEND)
                    print(f"\n{errors}")
                    continue
                else:
                    continue

        if self.log:
            file = HTML_Tidy._return_logfile(self, errMsg)
            print("##########################################################")
            print("you can find your logfile under " +
                  rootDir + os.sep + "HTML-logfile.txt")
            var = HTML_Tidy.read_logFile(self, file)
            return var

    def number_print_List(self, htmlList: list, sep: str = '') -> None:
        """Print a list of strings with line numbers
		Should be extended by a feature to highlight a given set of line
		numbers. This can help the reader to quickly identify the lines
		with errors.

		Parameters
		----------
		htmlList : list of str
				The html code - each line a list entry.
		sep : str
				String that seperates the line number from the line text.
		"""
        return sep.join(['{0:>5d} {1}'.format(i, line) for i, line in enumerate(htmlList)])

    def join_body(self, htmlList: list, substitutions_dict: dict = {'\\"': '"'}) -> str:
        """Joins a list of strings into a single string and makes replacements
		Parameters
		----------
		htmlList : list of str
				The html code - each line a list entry.
		substitutions_dict : dict
				A dictionary with key:value pairs for old and new text.
				The html code is escaped in Modelica. To feed it to tidylib
				we need to remove the escape characters.
		Returns
		-------
		str
				The html code as one string, cleared from escape characters.
		"""
        body = ''.join(htmlList)  # just glue it together again
        body = HTML_Tidy.make_string_replacements(
            self, theString=body, substitutions_dict={'\\"': '"'})
        return body

    def make_string_replacements(self, theString: str,
                                 substitutions_dict: dict = {'\\"': '"'}) -> str:
        """Takes a string and replaces according to a given dictionary
		Parameters
		----------
		theString : str
				The string that contains replaceble text.
		substitutions_dict : dict
				A dictionary with key:value pairs for old and new text.
		Returns
		-------
		str
				The modified string. """
        for k, v in substitutions_dict.items():
            theString = theString.replace(k, v)
        return theString

    def getInfoRevisionsHTML(self, moFile):
        """Returns a list that contains the html code
		This function returns a list that contain the html code of the
		info and revision sections. Each element of the list
		is a string.
		Parameters
		----------
		moFile : str
				The name of a Modelica source file.
		Returns
		-------
		list
				The list of strings of the info and revisions section. """
        with open(moFile, mode="r", encoding="utf-8-sig") as f:
            lines = f.readlines()
        nLin = len(lines)
        isTagClosed = True
        entries = list()
        for i in range(nLin):
            if isTagClosed:  # search for opening tag
                idxO = lines[i].find("<html>")
                if idxO > -1:  # search for closing tag on same line as opening tag
                    idxC = lines[i].find("</html>")
                    if idxC > -1:
                        entries.append(lines[i][idxO + 6:idxC] + '\n')
                        isTagClosed = True
                    else:
                        entries.append(lines[i][idxO + 6:])
                        isTagClosed = False
            else:  # search for closing tag
                idxC = lines[i].find("</html>")
                if idxC == -1:  # closing tag not found, copy full line
                    entries.append(lines[i])
                else:  # search for opening tag on same line as closing tag
                    entries.append(lines[i][0:idxC] + '\n')  # found closing tag, copy beginning of line only
                    isTagClosed = True
                    idxO = lines[i].find("<html>")
                    if idxO > -1:
                        entries.append(lines[i][idxO + 6:])
                        isTagClosed = False
        return entries

    def _correct_overwrite(self, moFulNam, document_corr):
        """ This function overwrites the old modeilca files with
       	the corrected files """
        os.remove(moFulNam)
        newfile = open(moFulNam, "w+b")
        newfile.write(document_corr.encode("utf-8"))

    def _backup_old_files(self, moFulNam, document_corr, file_counter):
        """
		This function backups the root folder and creates
		the corrected files """
        rootDir = self.package.replace(".", os.sep)
        if os.path.exists(rootDir + "_backup") is False and file_counter == 1:
            shutil.copytree(rootDir, rootDir + "_backup")
            print("you can find your backup under " + rootDir + "_backup")
        os.remove(moFulNam)
        newfile = open(moFulNam, "w+b")
        newfile.write(document_corr.encode("utf-8"))

    def _return_logfile(self, errMsg):
        """
		This function creates the logfile
		"""
        rootDir = self.package.replace(".", os.sep)
        File = rootDir + os.sep + "HTML-logfile.txt"
        logfile = open(File, "w")
        if len(errMsg) >= 0:
            for line in errMsg:
                logfile.write(line + '\n')
        logfile.close()
        return File

    def read_logFile(self, File):
        exitFile = "bin" + os.sep + "06_Configfiles" + os.sep + "exit.sh"
        font = self.font
        align = self.align
        logfile = open(File, "r")
        Exit = open(exitFile, "w")
        ErrList = []
        for i in logfile:
            FileTag = i.find("--")
            FileNameTag = i.find(".mo")
            ErrWhiteList_table = "Warning: The summary attribute on the <table> element is obsolete in HTML5"
            ErrWhiteList_font = "Warning: <font> element removed from HTML5"
            ErrWhiteList_align = 'Warning: <p> attribute "align" not allowed for HTML5'
            i = i.replace("\n", "")
            ErrorList = "Warning"
            if i.find(ErrWhiteList_table) > -1:
                continue
            if font == False:
                if i.find(ErrWhiteList_font) > -1:
                    continue
            if align == False:
                if i.find(ErrWhiteList_align) > -1:
                    continue
            if FileTag > -1 and FileNameTag > -1:
                continue
            elif i.find(ErrorList) > -1:
                ErrList.append(i)

        logfile.close()
        if len(ErrList) > 0:
            print("Syntax Error: Check HTML-logfile")
            Exit.write("#!/bin/bash" + "\n" + "\n" + "exit 1")
            Exit.close()
            var = 1
            return (var)
        else:
            print("HTML Check was successful!")
            Exit.write("#!/bin/bash" + "\n" + "\n" + "exit 0")
            Exit.close()
            var = 0
            return var

    def _CheckFile(self, moFile):
        """
		This function returns a list that contain the html code of the
		info and revision sections. Each element of the list
		is a string.

		:param moFile: The name of a Modelica source file.
		:return: list The list of strings of the info and revisions
								section.
		"""

        align = self.align
        with io.open(moFile, mode="r", encoding="utf-8-sig") as f:
            lines = f.readlines()
            nLin = len(lines)
        isTagClosed = True
        code = list()
        htmlCode = list()
        errors = list()
        for i in range(nLin):
            if isTagClosed:  # search for opening tag
                idxO = lines[i].find("<html>")
                if idxO > -1:  # if found opening tag insert everything up to opening tag into the code list
                    code.append(lines[i][:idxO + 6])  # search for closing tag on same line as opening tag
                    idxC1 = lines[i].find("</html>")
                    idxC2 = lines[i].find(
                        "<\html>")  # check for both, correct and incorrect html tags, because dymola except also <\html>
                    if idxC1 > -1:
                        idxC = idxC1
                    elif idxC2 > -1:
                        idxC = idxC2
                    else:
                        idxC = -1
                    if idxC > -1:
                        htmlCode.append(lines[i][idxO + 6:idxC] + '\n')
                        code.append(HTML_Tidy._htmlCorrection(self, htmlCode)[0])
                        errors.append(HTML_Tidy._htmlCorrection(self, htmlCode)[1])
                        code.append(lines[i][idxC:])
                        isTagClosed = True
                    else:
                        htmlCode.append(lines[i][idxO + 6:])
                        isTagClosed = False
                else:
                    code.append(lines[i])
                    isTagClosed = True
            else:  # check for both, correct and incorrect html tags, because dymola except also <\html>
                idxC1 = lines[i].find("</html>")
                idxC2 = lines[i].find("<\html>")
                if idxC1 > -1:
                    idxC = idxC1
                elif idxC2 > -1:
                    idxC = idxC2
                else:
                    idxC = -1
                if idxC > -1:
                    htmlCode.append(lines[i][idxO + 6:idxC])
                    code.append(HTML_Tidy._htmlCorrection(self, htmlCode)[0])
                    errors.append(HTML_Tidy._htmlCorrection(self, htmlCode)[1])
                    code.append(lines[i][idxC:])
                    htmlCode = list()
                    idxO = lines[i].find("<html>")
                    if idxO > -1:
                        isTagClosed = False
                    else:
                        isTagClosed = True
                else:
                    htmlCode.append(lines[i])
                    isTagClosed = False
        document_corr = ""
        if len(code) > 0:
            for lines in code:
                document_corr += lines
        errors_string = ""
        if len(errors) > 0:
            for lines in errors:
                errors_string += lines
        document_corr_img = ""
        CloseFound = True
        for line in document_corr.splitlines():
            if self.font == True:
                line, CloseFound = HTML_Tidy.correct_font(
                    self, line, CloseFound)
            if self.align == True:
                line, CloseFound = HTML_Tidy.correct_p_align(
                    self, line, CloseFound)
            document_corr_img += line + '\n'
        return document_corr_img, errors_string

    def _htmlCorrection(self, htmlCode):
        substitutions_dict: dict = {'"': '\\"', '<br>': '<br/>', '<br/>': '<br/>'}
        htmlList = htmlCode
        htmlStr = HTML_Tidy.join_body(self, htmlList=htmlList, substitutions_dict={'\\"': '"'})
        from tidylib import tidy_document
        htmlCorrect, errors = tidy_document(f"{htmlStr}",
                                            options={'doctype': 'html5',
                                                     'show-body-only': 1,
                                                     'numeric-entities': 1,
                                                     'output-html': 1,
                                                     'wrap': 72,
                                                     'alt-text': '', })
        document_corr = HTML_Tidy.make_string_replacements(
            self, theString=htmlCorrect, substitutions_dict=substitutions_dict)
        return document_corr, errors

    def htmlCorrection(self, htmlStr: str,
                       substitutions_dict: dict = {'"': '\\"', '<br>': '<br/>', '<br/>': '<br/>'}) -> (str, str):
        """Returns cleaned html code and found errors
		Calls tidylib which will produce a clean version of the html code
		and also the errors that it has found.
		Parameters
		----------
		htmlStr : str
				The html code as a single string.
		substitutions_dict : dict
				A dictionary with key:value pairs for old and new text.
				The html code must be escaped in Modelica. Generate properly
				escaped code we need to add the escape characters. All the
				while we can replace html errors that Dymola introduces.
				i.e. '<br>' -> '<br />'
		Returns
		-------
		str
				The tidy html code with escape characters as one string.
		str
				The error messages from tidylib.
		"""
        from tidylib import tidy_document
        htmlCorrect, errors = tidy_document(f"{htmlStr}",
                                            options={'doctype': 'html5',
                                                     'show-body-only': 1,
                                                     'numeric-entities': 1,
                                                     'output-html': 1,
                                                     'wrap': 72,
                                                     'alt-text': '', })
        document_corr = HTML_Tidy.make_string_replacements(
            self, theString=htmlCorrect, substitutions_dict=substitutions_dict)
        return document_corr, errors

    def correct_table_summary(self, line, CloseFound):  # delete Summary in table and add <caption> Text </caption>
        if CloseFound == True:
            tableTag = line.encode("utf-8").find(b"<table")
            sumTag = line.encode("utf-8").find(b"summary")
            CloseTagIntex = line.encode("utf-8").rfind(b'">')
            if tableTag > -1 and sumTag > -1:
                line = line[:sumTag] + "> " + \
                       line[sumTag:].replace('summary=', '<caption>', 1)
                line = (line.replace('">', '</caption>', 1))
        return line, CloseFound

    def correct_th_align(self, line, CloseFound):  # Correct algin with th and replace style="text-align"
        if CloseFound == True:
            alignTag = line.encode("utf-8").find(b"align")
            thTag = line.encode("utf-8").find(b"th")
            CloseTagIntex = line.encode("utf-8").rfind(b'">')
            if alignTag > -1 and thTag > -1:
                line = (line.replace('\\', ''))
        return line, CloseFound

    def correct_p_align(self, line, CloseFound):  # Correct align in p and replace style="text-align"
        # Wrong: <p style="text-align:center;">
        # Correct: <p style="text-align:center;">
        # Correct: <p style="text-align:center;font-style:italic;color:blue;">k = c<sub>p</sub>/c<sub>v</sub> </p>
        # Correct: <p style="text-align:center;font-style:italic;">
        if CloseFound == True:
            pTag = line.encode("utf-8").find(b"<p")
            alignTag = line.encode("utf-8").find(b"align")
            etag = line.encode("utf-8").find(b"=")
            closetag = line.encode("utf-8").find(b">")
            styleTag = line.encode("utf-8").find(b"text-align:")
            style = line.encode("utf-8").find(b"style")
            rstyle = style = line.encode("utf-8").find(b"style")
            StyleCount = line.count("style=")
            if styleTag > -1:
                return line, CloseFound
            elif pTag > -1 and alignTag > -1:
                sline = (line[alignTag:closetag + 1].replace('\\', ''))
                sline = (sline.replace('align="', 'style=text-align:'))
                sline = (sline.replace('style=', 'style="'))
                sline = (sline.replace(';', ''))
                CloseTag_2 = sline.encode("utf-8").rfind(b">")
                if CloseTag_2 > -1:
                    sline = (sline.replace('">', ';">'))
                sline = sline.replace('""', '"')
                line = (line[:alignTag] + sline + line[closetag + 1:])
                StyleCount = line.count("style=")
                if StyleCount > 1:
                    line = line.replace('style="', '')
                    line = line.replace('"', '')
                    line = line.replace(';>', ';">')
                    pTag = line.encode("utf-8").find(b"<p")
                    tline = line[pTag + 2:]
                    tline = ('style="' + tline.lstrip())
                    tline = tline.replace(" ", ";")
                    closetag = line.encode("utf-8").find(b">")
                    line = (line[:pTag + 3] + tline + line[closetag + 1:])
        return line, CloseFound

    def correct_font(self, line, CloseFound):  # Replace font to style für html5
        # <h4><font color=\"#008000\">Overview</font></h4>
        # <h4><font color=\"#008000\">Overview</font></h4>
        # <h4><span style="color:#008000">Overview</span></h4>
        #	  <span style="color:#008000">Overview</span>
        #		\"#008000\"
        if CloseFound == True:
            styleTag_1 = line.encode("utf-8").find(b"style=")
            styleTag_2 = line.encode("utf-8").find(b"color")
            fontTag = line.encode("utf-8").find(b"<font")
            rfontTag = line.encode("utf-8").rfind(b"</font>")
            firstCloseTage = line.encode("utf-8").find(b">")
            etag = line.encode("utf-8").find(b"=")
            if styleTag_1 > -1 and styleTag_2 > -1:
                if fontTag > -1 and rfontTag > -1:
                    sline = (line[fontTag:rfontTag].replace('\\', ''))
                    sline = sline.replace('"', '')
                    sline = sline.replace('<font', '<span')
                    sline = (sline.replace('color:', '"color:'))
                    sline = sline.replace(';>', '">')
                    line = line[:fontTag] + sline + \
                           line[rfontTag:].replace('</font>', '</span>')
            elif fontTag > -1 and rfontTag > -1:
                sline = (line[fontTag:rfontTag].replace('\\', ''))
                sline = sline.replace('"', '')
                sline = sline.replace('<font', '<span')
                sline = (sline.replace('color=', 'style="color:'))
                sline = (sline.replace('>', '">'))
                line = line[:fontTag] + sline + \
                       line[rfontTag:].replace('</font>', '</span>')
        return line, CloseFound

    def correct_img_atr(self, line, CloseFound):  # Correct img and check for missing alt attributed
        if CloseFound == True:
            imgTag = line.encode("utf-8").find(b"img")
            if imgTag > -1:
                imgCloseTagIndex = line.find(">", imgTag)
                imgAltIndex = line.find("alt", imgTag)
                if imgCloseTagIndex > -1 and imgAltIndex == -1:  # if close tag exists but no alt attribute, insert alt attribute and change > to />
                    line = line[:imgTag] + \
                           line[imgTag:].replace(">", ' alt="" />', 1)
                    CloseFound = True
                elif imgCloseTagIndex > -1 and imgAltIndex > -1:  # if close tag exists and alt attribute exists, only change > to />
                    line = line[:imgTag] + line[imgTag:].replace(">", ' />', 1)
                    CloseFound = True

                elif imgCloseTagIndex == -1:  # if close tag is not in the same line
                    line = line
                    CloseFound = False
        else:  # if no close tag was found in previous line, but opening tag found search for close on this line with same
            imgCloseTagIndex = line.find(">")
            imgAltIndex = line.find("alt")
            if imgCloseTagIndex > -1 and imgAltIndex == -1:
                line = line[:imgCloseTagIndex] + \
                       line[imgCloseTagIndex:].replace(">", ' alt="" />', 1)
                CloseFound = True
            elif imgCloseTagIndex > -1 and imgAltIndex > -1:
                line = line[:imgCloseTagIndex] + \
                       line[imgCloseTagIndex:].replace(">", ' />', 1)
                CloseFound = True
            elif imgCloseTagIndex == -1:
                CloseFound = False
                line = line
        return line, CloseFound

    def delete_html_revision(self, line, CloseFound):  # Delete revsion
        if CloseFound == True:
            htmlTag = line.encode("utf-8").find(b"</html>")
            htmlCloseTag = line.encode("utf-8").find(b"<html>")
            RevTag = line.encode("utf-8").find(b"revision")
            if htmlTag > -1 and RevTag > -1:
                if htmlCloseTag > -1:
                    line = ""
        return line, CloseFound

    def _listAllModel(self):  # List AixLib and IBPSA model
        rootdir = self.package
        rootdir = rootdir.replace(".", os.sep)
        AixLib_Model = []
        file = open(self.html_wh_file, "r")
        IBPSA_Models = []
        for i in file:
            if i.find(".mo") > -1:
                i = i.replace(self.wh_library, self.library)
                i = i.replace("\n", "")
                IBPSA_Models.append(i)
        file.close()
        for subdir, dirs, files in os.walk(rootdir):  # Return AixLib models
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".mo"):
                    model = filepath.replace(os.sep, ".")
                    model = model[model.rfind("AixLib"):]
                    AixLib_Model.append(model)
        return AixLib_Model, IBPSA_Models

    def _ListAixLibModel(self):  # Remove IBPSA models and list all AixLib model
        AixLib_Models, IBPSA_Models = HTML_Tidy._listAllModel(self)
        WhiteListModel = []
        for element in AixLib_Models:
            for subelement in IBPSA_Models:
                if element == subelement:
                    WhiteListModel.append(element)
        for i in WhiteListModel:
            AixLib_Models.remove(i)
        return AixLib_Models

class HTML_whitelist(object):

    def __init__(self,wh_library,git_url):
    def create_IBPSA_WhiteList(self):  # Create a new whiteList
        git_url = "https://github.com/ibpsa/modelica-ibpsa.git"
        Repo.clone_from(git_url, self.wh_library)
        model_list = []
        for subdir, dirs, files in os.walk(self.wh_library):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith(".mo"):
                    model = filepath
                    model = model.replace(os.sep, ".")
                    model = model[model.rfind(self.wh_library):model.rfind(".mo")]
                    model_list.append(model)
        file = open(self.html_wh_file, "w")
        for i in ModelList:
            file.write("\n" + i + ".mo" + "\n")
        file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run HTML correction on files, print found errors or backup old files')  # Configure the argument parser
    parser.add_argument("--correct-overwrite", action="store_true", default=False,
                        help="correct html code in modelica files and overwrite old files")
    parser.add_argument("--correct-backup", action="store_true", default=False,
                        help="correct html code in modelica "  "files and backup old files")
    parser.add_argument("--log", action="store_true",
                        default=False, help="print logfile of errors found")
    parser.add_argument('-s', "--single-package", metavar="AixLib.Package",
                        help="Test only the Modelica package AixLib.Package")
    parser.add_argument("-p", "--path", default=".",
                        help="Path where top-level package.mo of the library is located")
    parser.add_argument("--font", action="store_true", default=False,
                        help="correct html code: Remove font to span")
    parser.add_argument("--align", action="store_true", default=False,
                        help="correct html code: Remove align  to style=text-algin:")
    parser.add_argument("--WhiteList", action="store_true", default=False,
                        help="Create a new WhiteList Library IBPSA")
    parser.add_argument("--correct-view", action="store_true", default=False,
                        help="Print the Correct HTML Code")
    parser.add_argument("-L", "--library", default="AixLib", help="Library to test")
    parser.add_argument("--wh_library", default="IBPSA", help="Library on whitelist")
    parser.add_argument("--git-url", help="url repository")

    args = parser.parse_args()
    from html_tidy_errors import HTML_Tidy

    HTML_Check = HTML_Tidy(package=args.single_package,
                           rootDir=args.path,
                           correct_overwrite=args.correct_overwrite,
                           correct_backup=args.correct_backup,
                           log=args.log,
                           font=args.font,
                           align=args.align,
                           WhiteList=args.WhiteList,
                           correct_view=args.correct_view,
                           library=args.library,
                           wh_library=args.wh_library)
    if args.correct_overwrite is False and args.correct_backup is False and args.log is False and args.correct_view is False:
        print("please use -h or --help for help")
    if args.WhiteList is True:
        print("Create a Whitelist of IBPSA Library")
        HTML_Check.create_IBPSA_WhiteList()
    elif args.correct_backup is True:
        print("Create a Backup")
        HTML_Check.run_files()
        var = HTML_Check.run_files()
        print(var)

    elif args.correct_overwrite is True:
        print("Overwrite the Library")
        # HTML_Check.run_files()
        var = HTML_Check.run_files()
        HTML = HTML_Tidy(package=args.single_package,
                         rootDir=args.path,
                         correct_overwrite=args.correct_overwrite,
                         correct_backup=args.correct_backup,
                         log=False,
                         font=args.font,
                         align=args.align,
                         WhiteList=args.WhiteList,
                         correct_view=args.correct_view)
        HTML.run_files()
        print(var)
        print("Finish")


    elif args.correct_view is True:
        print("Print the Correct HTML Code")
        HTML_Check.run_files()

        print("Finish")
