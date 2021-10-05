from buildingspy.development import error_dictionary_jmodelica
from buildingspy.development import error_dictionary_dymola

import codecs
import multiprocessing
import argparse
import os
import sys 
import platform
import buildingspy.development.regressiontest as u
from pathlib import Path
from git import Repo
from sort_models import git_models
import time 
import glob
from threading import Thread, Event

 
class Git_Repository_Clone(object):
	"""work with Repository in Git"""
	def __init__(self, Repository):
		self.Repository = Repository

	def  _CloneRepository(self):
		git_url = "https://github.com/ibpsa/modelica-ibpsa.git"
		repo_dir = "IBPSA"
		if os.path.exists(repo_dir):
			print("IBPSA folder exists already!")
		else:
			print("Clone IBPSA Repo")
			repo = Repo.clone_from(git_url, repo_dir)
			
	def _git_push_WhiteList(self):
		WhiteList_file = "bin"+os.sep+"03_WhiteLists"+os.sep+"WhiteList_CheckModel.txt"
		repo_dir = ""
		try:
			repo = Repo(repo_dir)
			commit_message = "Update new WhiteList [ci skip]"
			repo.git.add(WhiteList_file)
			repo.index.commit(commit_message)
			origin = repo.remote('origin')
			origin.push('master')
			repo.git.add(update=True)
			print("repo push succesfully")
		except Exception as e:
			print(str(e))
		

#class colors(object):
			  
class ValidateTest(object):
	"""Class to Check Packages and run CheckModel Tests"""
	"""Import Python Libraries"""
	def __init__(self,package,lib_path, batch, tool, n_pro, show_gui, WhiteList, SimulateExamples, Changedmodels, dymola, dymola_exception, mo_library, FilterWhiteList):
		self.package = package
		self.lib_path = lib_path
		self.batch = batch
		self.tool = tool
		self.n_pro = n_pro
		self.show_gui = show_gui
		self.CreateWhiteList = WhiteList
		self.SimulateExamples = SimulateExamples
		self.Changedmodels = Changedmodels
		self.dymola = dymola
		self.dymola_exception = dymola_exception
		self.mo_library = mo_library
		self.FilterWhiteList = FilterWhiteList
		#self.path = path 
		###Set Dymola Tool		
		if tool	 == 'jmodelica':
			e = error_dictionary_jmodelica
		else:
			e = error_dictionary_dymola
		if tool in ['dymola', 'omc', 'jmodelica']:
			self._modelica_tool = tool
		else:
			raise ValueError("Value of 'tool' of constructor 'Tester' must be 'dymola', 'omc' or 'jmodelica'. Received '{}'.".format(tool))

	def dym_check_lic(self):
		from dymola.dymola_interface import DymolaInterface
		from dymola.dymola_exception import DymolaException
		
		dym_sta_lic_available = dymola.ExecuteCommand('RequestOption("Standard");')
		if not dym_sta_lic_available:
			dymola.ExecuteCommand('DymolaCommands.System.savelog("Log_NO_DYM_STANDARD_LIC_AVAILABLE.txt");')
			print("No Dymola License is available")
			dymola.close()
			exit(1)
		else:
			print("Dymola License is available")
	
		
	''' Write a new Whitelist with all models in IBPSA Library of those models who have not passed the Check Test'''
	def _WriteWhiteList(self,version):
		#_listAllModel
		#rootdir = r"D:\Gitlab\modelica-ibpsa\IBPSA"
		
		from dymola.dymola_interface import DymolaInterface
		from dymola.dymola_exception import DymolaException
		CRED = '\033[91m'
		CEND = '\033[0m'
		green = "\033[0;32m"
		
		Package = self.package.replace("AixLib","IBPSA")
		Package = Package.split(".")[0]
		Package = Package.replace(".",os.sep)
		rootdir = "IBPSA"+os.sep+Package
		# Read the last version of whitelist 
		
		filename= "bin"+os.sep+"03_WhiteLists"+os.sep+"WhiteList_CheckModel.txt"
		vfile = open(filename,"r")
		lines = vfile.readlines()
		vlist = []
		for line in lines:
			if line.strip("\n") == version:
				print("Whitelist is on Version " + version)
				print("The Whitelist is already up to date")
				vlist.append(line)
		vfile.close()	
				
		if len(vlist) == 0:		
					
			ModelList = []
			for subdir, dirs, files in os.walk(rootdir):
				for file in files:
					filepath = subdir + os.sep + file
					if filepath.endswith(".mo") and file != "package.mo":
						model = filepath
						model = model.replace(os.sep,".")
						model = model[model.rfind("IBPSA"):model.rfind(".mo")]
						ModelList.append(model)
			
			Library = rootdir = "IBPSA"+os.sep+Package+os.sep+"package.mo"
			dymola = self.dymola
			
			try:
				PackageCheck = dymola.openModel(Library)
				
				if PackageCheck == True:
					print("Found IBPSA Library and start Checkmodel Tests \n Check Package " + self.package+" \n")
				elif PackageCheck == False:
					print("Library Path is wrong. Please Check Path of IBPSA Library Path")
					exit(1)
				if len(ModelList) == 0: ## Check the Package
					print("Wrong path")
					exit(1)
				ErrorList = []	
				for i in ModelList:
					result=dymola.checkModel(i)
					if result == True:
						print('\n'+green+' Successful: '+CEND+i+'\n')
					if result == False:
						print('\n'+CRED+' Error: '+CEND+i+'\n')
						Log = dymola.getLastError()
						print(Log)
						ErrorList.append(i)
				dymola.savelog("IBPSA-log.txt")
				dymola.close()
				IBPSA_PackageName = []
				for i in ModelList: ### Write the Package Names of IBPSA
					i = i.split(".")
					i = i[1]
					if i not in IBPSA_PackageName:
						IBPSA_PackageName.append(i)
				
				file = open(filename,"w")
				
				print(version)
				file.write("\n"+version+"\n" +"\n")
				for i in IBPSA_PackageName:
					List  = []
					for l in ErrorList:
						Package = l.split(".")[1]
						if Package == i:
							List.append(l)
					file.write(i+"\n"+str(List)+"\n"+"\n")
				file.close()
				print("Write Whitelist")
			except DymolaException as ex:
				print(("2: Error: " + str(ex)))
			finally:
				if dymola is not None:
					dymola.close()
					dymola = None

	def read_l_whitelist_v(self):
		#
		aixlib_dir = "AixLib" + os.sep + "Resources" + os.sep + "Scripts"
		filelist = (glob.glob(aixlib_dir+os.sep+"*.mos"))
		
		list = []
		for i in filelist:
			i = i.replace(".mos","")
			list.append(i)
		data = (sorted(list, key=lambda x: float(x[x.find("_to_0")+6:])))
		data = (data[len(data)-1])
		
		d = data[data.find("_to_0")+6:data.rfind(".")]
		last_conv_list = []
		for i in list:
			num = i[i.find("_to_0")+6:i.rfind(".")]
			if num == str(d):
				last_conv_list.append(i)
				continue
		data = (sorted(last_conv_list, key=lambda x: int(x[x.rfind(".")+1:])))
		data = (data[len(data)-1])
		data = data.split(os.sep)
		data = (data[len(data)-1])
		return data
		
	def _WriteErrorlog(self,log_package): # Write a Error log with all models, that don´t pass the check
		log = self.mo_library + os.sep+log_package + "-log.txt"
		log_Error = self.mo_library+os.sep+log_package+"-Errorlog.txt"
		file = open(log, "r")
		errorlog = open(log_Error, "w")
		errorList = []
		falseList = []
		checkList = []
		for line in file:
			if line.find('checkModel("'+self.mo_library+'.') > -1:
				errorList.append(line)
				checkList.append(line)
			elif len(checkList) > 0:
				errorList.append(line)
			if line.find(' = false') > -1:
				falseList.append(line)
			if line.find(' = true') > -1: 
				errorList = []
				checkList = []
			if len(falseList) > 0 and len(checkList) > 0:
				errorlog.write("\n--------------------------------------\n")
				if len(errorList) > 0:
					for i in errorList:
						errorlog.write(i)
				errorlog.write("\n--------------------------------------\n")
				errorList = []
				checkList = []
				falseList = []
		file.close()
		errorlog.close()
		
	def _CompareWhiteList(self,WhiteList,AixLibModels): # Compare AixLib models with IBPSA models of those have not  passed the Check. Remove all models from the WhiteList and will not be checked
		WhiteListModel = []
		for element in AixLibModels:
			for subelement in WhiteList:
				if element == subelement:
					WhiteListModel.append(element)
		WhiteListModel = list(set(WhiteListModel))
		for i in WhiteListModel:
			AixLibModels.remove(i)
		return AixLibModels
	
	def _CompareWhiteSimulateList(self):
		SimulateList = ValidateTest._listAllExamples(self)
		WhiteList = ValidateTest._IgnoreWhiteList(self)
		WhiteListModel = []
		for element in SimulateList:
			for subelement in WhiteList:
				if element == subelement:
					WhiteListModel.append(element)
		WhiteListModel = list(set(WhiteListModel))
		for i in WhiteListModel:
			SimulateList.remove(i)
		return SimulateList
		
	def _IgnoreWhiteList(self): # Return a List with all models from the Whitelist
		Package = self.package
		if len(Package) > 1:
			Package = Package.split(".")[1]
		
		filename= r"bin/03_WhiteLists/WhiteList_CheckModel.txt"
		file = open(filename,"r")
		RowNumer = 0
		WhiteListPackage = []
		for line in file:
			if line.rstrip() == Package:
				#print("WhiteList Package "+Package)
				RowNumer = RowNumer + 1 
				continue
			elif RowNumer > 0:
				#WhiteListPackage = []
				line = line.rstrip() 
				line = line.replace("[","")
				line = line.replace("]","")
				line = line.replace("'","")
				line = line.replace(" ","")
				line = line.replace("IBPSA","AixLib")
				line = str(line)
				line = line.split(",")
				WhiteListPackage = line
				break
		file.close()
		return WhiteListPackage

	def _listAllModel(self): # List all models in AixLib Library
		rootdir = self.package
		rootdir = rootdir.replace(".",os.sep)
		ModelList = []
		for subdir, dirs, files in os.walk(rootdir):
			for file in files:
				filepath = subdir + os.sep + file
				if filepath.endswith(".mo") and file != "package.mo":
					model = filepath.replace(os.sep, ".")
					model = model[model.rfind("AixLib"):model.rfind(".mo")]
					ModelList.append(model)
		return ModelList

	def _listAllExamples(self): # List all Examples and Validation examples
		Package = self.package
		rootdir = Package.replace(".",os.sep)
		ModelList = []
		for subdir, dirs, files in os.walk(rootdir):
			for file in files:
				filepath = subdir + os.sep + file
				test = subdir.split(os.sep)
				'''
				if filepath.find("Examples") > -1  or filepath.find("Validation")> -1:
					if filepath.endswith(".mo") and file != "package.mo":
						model = filepath.replace(os.sep,".")
						model = model[model.rfind("AixLib"):model.rfind(".mo")]
						ModelList.append(model)
						continue
				'''
				if test[len(test)-1] == "Examples" or test[len(test)-1] == "Validation":
					#print((test))
					if filepath.endswith(".mo") and file != "package.mo":
						model = filepath.replace(os.sep,".")
						model = model[model.rfind("AixLib"):model.rfind(".mo")]
						ModelList.append(model)
						continue
		return ModelList

	def _get_Model(self):
		rootdir = self.mo_library+os.sep+self.package
		modelList = []
		for subdir, dirs, files in os.walk(rootdir):
			for file in files:
				filepath = subdir + os.sep + file
				if filepath.endswith(".mo") and file != "package.mo":
					model = filepath.replace(os.sep, ".")
					model = model[model.rfind(self.mo_library):model.rfind(".mo")]
					modelList.append(model)
		return modelList

	def _get_examples(self):
		rootdir = self.mo_library + os.sep + self.package
		example_list = []
		for subdir, dirs, files in os.walk(rootdir):
			for file in files:
				filepath = subdir + os.sep + file
				ex_folder = subdir.split(os.sep)
				ex_folder = ex_folder[len(ex_folder) - 1]
				if ex_folder == "Examples" or ex_folder == "Validation" or ex_folder == "Tests":
					# print((test))
					if filepath.endswith(".mo") and file != "package.mo":
						model = filepath.replace(os.sep, ".")
						model = model[model.rfind(self.mo_library):model.rfind(".mo")]
						example_list.append(model)
						continue
		return example_list

	def _checkmodel(self,model_list): # Check models and return a Error Log, if the check failed
		from dymola.dymola_interface import DymolaInterface
		from dymola.dymola_exception import DymolaException
		CRED = '\033[91m'
		CEND = '\033[0m'
		green = "\033[0;32m"
		dymola = self.dymola
		try:
			library = self.mo_library+os.sep+"package.mo"
			PackageCheck = dymola.openModel(library)
			if PackageCheck == True:
				print(f'Found AixLib Library and start Checkmodel Tests \n Check Package {self.package} \n')
			elif PackageCheck == False:
				print(f'Library Path is wrong. Please Check Path of AixLib Library Path')
				exit(1)
			ErrorList = []
			for i in model_list:
				result = dymola.checkModel(i)
				if result == True:
					print(f'\n {green} Successful: {CEND} {i} \n')
				if result == False:
					print(f'Check for Model {i} {CRED} failed! {CEND} \n')
					print(f'\n {CRED} Error: {CEND} {i} \n')
					print(f'Second Check Test for model {i}')
					sec_result = dymola.checkModel(i)
					if sec_result == True:
						print(f'\n {green} Successful: {CEND} {i} \n')
						continue
					if sec_result == False:
						ErrorList.append(i)
						print(f'\n {CRED} Error: {CEND} {i} \n')
						continue
			dymola.savelog(self.package+"-log.txt")
			dymola.close()
			logfile = self.package+"-log.txt"
			ValidateTest._WriteErrorlog(self,logfile)
			return ErrorList
		except DymolaException as ex:
			print(f'2: Error:  {str(ex)}')
		finally:
			if dymola is not None:
				dymola.close()

	def _sim_examples(self,example_list):
		from dymola.dymola_interface import DymolaInterface
		from dymola.dymola_exception import DymolaException
		CRED = '\033[91m'
		CEND = '\033[0m'
		green = "\033[0;32m"
		dymola = self.dymola

		### Sets the Dymola path to activate the GUI
		try:
			packageCheck = dymola.openModel(self.lib_path)
			if packageCheck == True:
				print("Found "+self.mo_library +"Library and start Checkmodel Tests \n Check Package " + self.package + " \n")
			elif packageCheck == None:
				print("Library Path is wrong. Please Check Path of AixLib Library Path")
				exit(1)
			errorList = []
			if self.Changedmodels == False:
				if len(example_list) == 0:
					print(CRED + "Error: " + CEND + "Found no Examples")
					exit(0)
				for i in example_list:
					print("Check Model: " + i)
					result = dymola.checkModel(i, simulate=True)
					if result == True:
						print('\n ' + green + 'Successful: ' + CEND + i + '\n')
					if result == False:
						print("Check for Model " + i + CRED + " failed!" + CEND + '\n')
						print("Second Check Test for model " + i)
						result = dymola.checkModel(i, simulate=True)
						if result == True:
							print('\n ' + green + 'Successful: ' + CEND + i + '\n')
						if result == False:
							print('\n ' + CRED + 'Error: ' + CEND + i + '\n')
							errorList.append(i)
							Log = dymola.getLastError()
							print(Log)


			log_package = self.mo_library + "." + self.package
			dymola.savelog(log_package + "-log.txt")
			dymola.close()

			ValidateTest._WriteErrorlog(self, log_package)
			return errorList

		except DymolaException as ex:
			print(("2: Error: " + str(ex)))
		finally:
			if dymola is not None:
				dymola.close()
				dymola = None

	def _SimulateModel(self): # Simulate examples and validation and return a Error log, if the check failed.
		from dymola.dymola_interface import DymolaInterface
		from dymola.dymola_exception import DymolaException
		CRED = '\033[91m'
		CEND = '\033[0m'
		green = "\033[0;32m"
		dymola = self.dymola
		try:
			PackageCheck = dymola.openModel(self.Library) # Sets the Dymola path to activate the GUI
			if PackageCheck == True:
				print("Found AixLib Library and start Checkmodel Tests \n Check Package " + self.Package+" \n")
			elif PackageCheck == None:
				print("Library Path is wrong. Please Check Path of AixLib Library Path")
				exit(1)
		
			ErrorList = []
			if self.Changedmodels == False:	
				ModelList = ValidateTest._CompareWhiteSimulateList(self)
				if len(ModelList) == 0:
					print(CRED+"Error: "+CEND+"Found no Examples")
					exit(0)
				for i in ModelList:
					print("Check Model: "+i) 
					
					result=dymola.checkModel(i,simulate=True)
					if result == True:
						print('\n '+green+'Successful: '+CEND+i+'\n')
						
					if result == False:
						print("Check for Model "+i+CRED+" failed!"+CEND+'\n')
						print("Second Check Test for model "+i)
						result=dymola.checkModel(i,simulate=True)
						if result == True:
							print('\n '+green+'Successful: '+CEND+i+'\n')
								
						if result == False:
							print('\n '+CRED+'Error: '+CEND+i+'\n')
							ErrorList.append(i)
							Log = dymola.getLastError()
							print(Log)
				IBPSA_Model = str(ValidateTest._IgnoreWhiteList(self))
				print("\n"+"\n")
				if len(IBPSA_Model) > 0:
					print("Don´t Check these Models "+IBPSA_Model)			
						
			if self.Changedmodels == True:
				list_path = 'bin'+os.sep+'03_WhiteLists'+os.sep+'changedmodels.txt'
				list_mo_models = git_models(".mo",self.Package, list_path)
				model_list= list_mo_models.sort_mo_models()
				examplelist= []
				for e in model_list:
					examples = e.split(".")
					if examples[len(examples)-2] == "Examples" or examples[len(examples)-2] == "Validation":
						examplelist.append(e)
				ErrorList = []
				if len(examplelist) == 0:
					print(f'No changed examples in Package:  {self.Package}')
					exit(0)	
				for i in examplelist:
					result=dymola.checkModel(i,simulate=True)
					if result == True:
						print('\n'+green+ 'Successful: '+CEND+i+'\n')
					if result == False:
						print("Check for Model "+i+CRED+" failed!"+CEND+'\n')
						
						print("Second Check Test for model "+i)
						result=dymola.checkModel(i,simulate=True)
						if result == True:
							print('\n'+green+ 'Successful: '+CEND+i+'\n')
						if result == False:
							print('\n' +CRED+' Error: '+CEND+i+'\n')
							ErrorList.append(i)
							Log = dymola.getLastError()
							print(Log)
							
			dymola.savelog(self.Package+"-log.txt")
			dymola.close()
			logfile = self.Package+"-log.txt"
			ValidateTest._WriteErrorlog(self,logfile)
			return ErrorList
		
		except DymolaException as ex:
			print(("2: Error: " + str(ex)))
		finally:
			if dymola is not None:
				dymola.close()
				dymola = None

	def _CreateIBPSALog(self): # Create a LogFIle from a package in IPBSA Library
		from dymola.dymola_interface import DymolaInterface
		from dymola.dymola_exception import DymolaException
		import buildingspy.development.regressiontest as u
		
		""" Check the IBPSA Model Automatical """	
		cmd = "git clone https://github.com/ibpsa/modelica-ibpsa.git"
		returned_value = os.system(cmd)  # returns the exit code in unix
		print('returned value:', returned_value)
		cmd = "cd modelica-ibpsa-master"
		os.system(cmd)
		Library = IBPSA/package.mo
		dymola = self.dymola
		dymola_exception = self.dymola_exception
		try:
		
			PackageCheck = dymola.openModel(Library)
			if PackageCheck == True:
				print("Found AixLib Library and start Checkmodel Tests \n Check Package " + self.Package+" \n")
			elif PackageCheck == None:
				print("Library Path is wrong. Please Check Path of AixLib Library Path")
				exit(1)
			result=dymola.checkModel(self.Package)
			dymola.savelog(self.Package+"-log.txt")
			Log = dymola.getLastError()
			if result == True:
				print('\n Check of Package '+self.Package+' was Successful! \n')
				dymola.close()
				#exit(0)
			if result == False:
				print('\n ModelCheck Failed in Package ' + self.Package+ ' Show Savelog \n')
				print(Log)
				dymola.clearlog()
				dymola.close()
				#exit(1)
		except dymola_exception as ex:
			print(("2: Error: " + str(ex)))
		finally:
			if dymola is not None:
				dymola.close()
				dymola = None
	
	
	
	def _compareIBPSA(self):
		AixLibPackage = self.Package
		IBPSAPackage = self.Package.replace("AixLib", "IBPSA")
		""" Check the IBPSA Model Automatical """	
		cmd = "git clone https://github.com/ibpsa/modelica-ibpsa.git"
		returned_value = os.system(cmd)  # returns the exit code in unix
		print('returned value:', returned_value)
		Path = r"bin/CITests/UnitTests/CheckPackages/LogFiles"
		IBPSA_Data = Path+"//"+IBPSAPackage+"-log.txt"
		# Check if the Log File exists
		#if IBPSA_Data.is_file():
		IBPSAFile = open(IBPSA_Data,"r")
		#else:
		#	print("No Log deposited")
		#		exit(1)
		IBPSA_ErrorList = []
		AixLib_ErrorList = []
		for line in  IBPSAFile:
			List = line.split()
			if len(List) > 1:
				if List[0] == "Error:":
					IBPSA_ErrorList.append(line)
		IBPSAFile.close() 
		Path = r"AixLib/"	
		AixLibFile = open(Path+AixLibPackage+"-log.txt","r")
		for line in AixLibFile:
			List = line.split()
			if len(List) > 1:
				if List[0] == "Error:":
					AixLib_ErrorList.append(line)
		AixLibFile.close()
		if len(AixLib_ErrorList) == len(IBPSA_ErrorList):
			print("Errors are already in IPBSA Library")
			exit(0)
		elif len(AixLib_ErrorList) != len(IBPSA_ErrorList):
			print("Error in "+ AixLibPackage)
			for element in AixLib_ErrorList:
				if not element in IBPSA_ErrorList:
					print(element)	
			exit(1)
		
	
	def _setLibraryRoot(self):
		"""Set the root directory of the library.   
		The root directory is the directory that contains the ``Resources`` folder
        and the top-level ``package.mo`` file."""
		self._libHome = os.path.abspath(rootDir)
        
	def _validate_experiment_setup(path):
		import buildingspy.development.validator as v
		val = v.Validator()
		retVal = val.validateExperimentSetup(path)


def _setEnvironmentVariables(var,value): ### Add to the environemtn variable 'var' the value 'value'
	import os
	import platform
	if var in os.environ:
		if platform.system() == "Windows":
			os.environ[var] = value + ";" + os.environ[var]
		else:
			os.environ[var] = value + ":" + os.environ[var]
	else:
		os.environ[var] = value				

if  __name__ == '__main__':
	# python bin\02_CITests\UnitTests\CheckPackages\validatetest.py -DS 2019 --single-package "Fluid"
	# Parser
	parser = argparse.ArgumentParser(description = "Check and Validate single Packages") # Configure the argument parser
	check_test_group = parser.add_argument_group("arguments to run check tests")
	check_test_group.add_argument("-b", "--batch", action ="store_true", help="Run in batch mode without user Interaction")
	check_test_group.add_argument("-t", "--tool", metavar="dymola",default="dymola", help="Tool for the Checking Tests. Set to Dymola")
	check_test_group.add_argument('-s',"--single-package",metavar="AixLib.Package", help="Test only the Modelica package AixLib.Package")
	check_test_group.add_argument("-p","--path", default=".", help = "Path where top-level package.mo of the library is located")
	check_test_group.add_argument("-n", "--number-of-processors", type=int, default= multiprocessing.cpu_count(), help="Maximum number of processors to be used")
	check_test_group.add_argument("--show-gui", help="show the GUI of the simulator" , action="store_true")
	check_test_group.add_argument("-WL", "--WhiteList", help="Create a WhiteList of IBPSA Library: y: Create WhiteList, n: Don´t create WhiteList" , action="store_true")
	check_test_group.add_argument("-SE", "--SimulateExamples", help="Check and Simulate Examples in the Package" , action="store_true")
	check_test_group.add_argument("-DS", "--DymolaVersion",default="2020", help="Version of Dymola(Give the number e.g. 2020")
	check_test_group.add_argument("-CM", "--Changedmodels",default=False, action="store_true")
	check_test_group.add_argument("-FW", "--FilterWhiteList", default=False, action="store_true")
	check_test_group.add_argument("-L", "--library", default="AixLib", help="Library to test")


	args = parser.parse_args() # Parse the arguments
	CRED = '\033[91m'
	CEND = '\033[0m'
	green = "\033[0;32m"

	if platform.system()  == "Windows": ### Checks the Operating System, Important for the Python-Dymola Interface
		_setEnvironmentVariables("PATH", os.path.join(os.path.abspath('.'), "Resources", "Library", "win32"))
		sys.path.insert(0, os.path.join('C:\\',
                            'Program Files',
                            'Dymola '+ args.DymolaVersion,
                            'Modelica',
                            'Library',
                            'python_interface',
                            'dymola.egg'))
	else:

		_setEnvironmentVariables("LD_LIBRARY_PATH", os.path.join(os.path.abspath('.'), "Resources", "Library", "linux32") + ":" +
								os.path.join(os.path.abspath('.'),"Resources","Library","linux64"))
		sys.path.insert(0, os.path.join('opt',
							'dymola-'+args.DymolaVersion+'-x86_64',
							'Modelica',
							'Library',
							'python_interface',
							'dymola.egg'))

	print(f'operating system {platform.system()}')
	sys.path.append(os.path.join(os.path.abspath('.'), "..", "..", "BuildingsPy"))
	if args.single_package is None:
		print(f'Error: Package is missing!')
		exit(1)
	#if args.library is None:




	from dymola.dymola_interface import DymolaInterface
	from dymola.dymola_exception import DymolaException
	dymola = None
	try:
		print(f'1: Starting Dymola instance')
		if platform.system()  == "Windows":
			dymola = DymolaInterface()
		else:
			dymola = DymolaInterface(dymolapath="/usr/local/bin/dymola")
		dymola.ExecuteCommand("Advanced.TranslationInCommandLog:=true;") 	### Writes all information in the log file, not only the last entries
		dym_sta_lic_available = dymola.ExecuteCommand('RequestOption("Standard");')
		lic_counter = 0
		'''
		while dym_sta_lic_available == False:
			print(f'{CRED} No Dymola License is available {CEND}')
			dymola.close()
			print(f'Check Dymola license after 60.0 seconds')
			time.sleep(180.0)
			### Sets the Dymola path to activate the GUI
			if platform.system()  == "Windows":
				dymola = DymolaInterface()
			else:
				dymola = DymolaInterface(dymolapath="/usr/local/bin/dymola")
			dym_sta_lic_available = dymola.ExecuteCommand('RequestOption("Standard");')
			lic_counter = lic_counter + 1
			if lic_counter > 30:
				if dym_sta_lic_available == False:
					print(f'There are currently no available Dymola licenses available. Please try again later.')
					dymola.close()
					exit(1)
		print(f'2: Using Dymola port   {str(dymola._portnumber)}')
		print(f'{green} Dymola License is available {CEND}')
	'''
		from validatetest import ValidateTest
		# Set environment variables
		CheckModelTest = ValidateTest(package = args.single_package,
								lib_path = args.path,
								batch = args.batch,
								tool = args.tool,
								n_pro = args.number_of_processors,
								show_gui = args.show_gui,
								WhiteList = args.WhiteList,
								SimulateExamples = args.SimulateExamples,
								Changedmodels = args.Changedmodels,
								dymola = dymola,
								dymola_exception = DymolaException,
								mo_library = args.library,
							    FilterWhiteList = args.FilterWhiteList)

		Git_Operation_Class = Git_Repository_Clone(Repository="Repo")
	
		"""Start Check and Validate Test"""
		if args.single_package:
			single_package = args.single_package
		else:
			single_package = None
		
		"""Write a new WhiteList"""
		if args.WhiteList == True:
			print(f'Write new Writelist from IBPSA Library')
			version =  CheckModelTest.read_l_whitelist_v()
			Git_Operation_Class._CloneRepository()
			CheckModelTest._WriteWhiteList(version)
			exit(0)
		
		"""Simulate all Examples and Validation in a Package"""
		if args.SimulateExamples == True:
			print(f'Simulate examples and validations')
			if args.library != "AixLib":
				example_list = CheckModelTest._get_examples()
				error = CheckModelTest._sim_examples(example_list)
			else:
				error = CheckModelTest._SimulateModel()
			if error is None:
				exit(1)
			if len(error) == 0:
				print(f'{green} Simulate of all Examples was successful! {CEND}')
				exit(0)
			elif len(error) > 0:
				print(f'{CRED} Simulate Failed {CEND}')
				for i in error:
					print(f'{CRED} Error: {CEND} Check Model {i}')
				exit(1)
		#****************************************************************
		else: #Check all Models in a Package
			modellist = CheckModelTest._get_Model()
			if args.Changedmodels == True:
				print(f'	Test only changed or new models')
				list_path = 'bin' + os.sep + '03_WhiteLists' + os.sep + 'changedmodels.txt'
				list_mo_models = git_models(".mo", self.package, list_path)
				model_list = list_mo_models.sort_mo_models()
				if len(model_list) == 0:
					print(f'No changed models in Package: {self.package}')
					exit(0)
			else:
				if args.FilterWhiteList == True:
					whitelist = ValidateTest._IgnoreWhiteList(self)
					if len(whitelist) > 0:
						print(f'Don´t Check these Models {IBPSA_Model}')
					models = ValidateTest._listAllModel(self)
					model_list = ValidateTest._CompareWhiteList(self, whitelist, models)
				else:
					model_list = modellist
				if len(model_list) == 0:
					print(f'Wrong Path')
					exit(1)
			errorList = CheckModelTest._checkmodel(model_list)
			if len(errorList) == 0:
				print(f'Test was {green} Successful! {CEND}')
				exit(0)
			if len(errorList) > 0:
				print(f'Test {CRED}  failed!  {CEND}')
				for i in errorList:
					print(f'{CRED} Error: {CEND}  Check Model {i}')
				exit(1)
			if errorList is None:
				exit(1)
	except DymolaException as ex:
		print(f'2: Error:   {str(ex)}')
	finally:
		if dymola is not None:
			dymola.close()
			dymola = None