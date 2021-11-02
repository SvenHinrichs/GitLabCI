import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import numpy as np
import sys,difflib
import os 
from git import Repo
from shutil import copyfile
import shutil
import pathlib
import glob
import pandas as pd
import argparse

class Plot_Charts(object):

	def __init__(self, package, library):
		self.package = package
		self.library = library

		# Set files for informations, templates and storage locations
		self.temp_file = f'bin{os.sep}07_templates{os.sep}01_google_templates{os.sep}google_chart.txt'  # path for google chart template
		self.index_temp_file = f'bin{os.sep}07_templates{os.sep}01_google_templates{os.sep}index.txt'
		self.layout_temp_file = f'bin{os.sep}07_templates{os.sep}01_google_templates{os.sep}layout_index.txt'
		self.f_log = f'{self.library}{os.sep}unitTests-dymola.log'  # path for unitTest-dymola.log, important for errors
		self.csv_file = f'reference.csv'
		self.test_csv = f'test.csv'

		self.index_path = f'bin{os.sep}07_templates{os.sep}02_charts'  # path for layout index
		self.temp_chart_path = f'bin{os.sep}07_templates{os.sep}02_charts{os.sep}{self.package}'  # path for every single package
		self.funnel_path = f'{self.library}{os.sep}funnel_comp'
		self.ref_path = f'{self.library}{os.sep}Resources{os.sep}ReferenceResults{os.sep}Dymola'
		self.index_html_file = f'{self.temp_chart_path}{os.sep}index.html'
		self.layout_html_file = f'{self.index_path}{os.sep}index.html'
		self.green = '\033[0;32m'
		self.CRED = '\033[91m'
		self.CEND = '\033[0m'

	def _get_values(self, lines):
		time_list = []
		measure_list = []
		for line in lines:  # searches for values and time intervals
			if line.find("last-generated=") > -1:
				continue
			if line.find("statistics-simulation=") > -1:
				continue
			if line.split("="):
				line = line.replace("[", "")
				line = line.replace("]", "")
				line = line.replace("'", "")
				values = (line.replace("\n","").split("="))
				if len(values) < 2:
					continue
				else:
					legend = values[0]
					measures = values[1]
					if legend.find("time") > -1:
						#time_list.append(f'{legend}:{measures}'
						time_str = f'{legend}:{measures}'
					else:
						measure_len = len(measures.split(","))
						measure_list.append(f'{legend}:{measures}')
		return time_str, measure_list, measure_len


	def _get_time_int(self, time_list, measure_len):

		time_val = time_list.split(":")[1]
		time_beg = time_val.split(",")[0]
		time_end = time_val.split(",")[1]
		time_int = float(time_end) - float(time_beg)
		tim_seq = time_int / float(measure_len)
		time_num = float(time_beg)
		time_list = []
		for time in range(0, measure_len):
			time_list.append(time_num)
			time_num = time_num + tim_seq
		return time_list

	def _createFolder(self, directory):
		try:
			if not os.path.exists(directory):
				os.makedirs(directory)
		except OSError:
			print('Error: Creating directory. ' +  directory)

	def _func(self, label):  # For Matplot Plots: Create a Hitbox for different variables
		index = labels.index(label)
		lines[index].set_visible(not lines[index].get_visible())
		plt.draw()

	def _read_unitTest_log(self):  # Read unitTest_log from regressionTest, write variable and modelname with difference
		log_file = open(self.f_log, "r")
		lines = log_file.readlines()
		model_var_list = []
		for line in lines:
			if line.find("*** Warning:") > -1:
				if line.find(".mat") > -1:
					model = line[line.find(("Warning:"))+9:line.find(".mat")]  # modelname
					var = line[line.find((".mat:"))+5:line.find("exceeds ")].lstrip()  # variable name
					model_var_list.append(f'{model}:{var}')
		return model_var_list

	def _get_ref_file(self, model):
		for file in os.listdir(self.ref_path):
			if file.find(model) > -1:
				return file
			else:
				continue

	def _sort_mo_var(self, dic):  # Search for variables in referencefiles
		mo_list = []
		var_mod_dic = {}
		for i in dic:
			mo_list.append(i)
		for file in os.listdir(self.ref_path):
			for l in mo_list:
				if file.find(l)>-1:
					var_mod_dic[self.ref_path+os.sep+file] = dic[l]
		return var_mod_dic

	def _read_csv_funnel(self, url):  # Read the differenz variables from csv_file and test_file
		csv_file = f'{url.strip()}{os.sep}{self.csv_file}'
		test_csv = f'{url.strip()}{os.sep}{self.test_csv}'
		try:
			var_model = pd.read_csv(csv_file)
			var_test = pd.read_csv(test_csv)
			temps = var_model[['x', 'y']]
			d = temps.values.tolist()
			c = temps.columns.tolist()
			test_tmp = var_test[['x', 'y']]
			e = test_tmp.values.tolist()
			e_list = []
			for i in range(0,len(e)):
				e_list.append((e[i][1]))

			result = zip(d, e_list)
			result_set = list(result)
			value_list = []
			for i in result_set:
				i = str(i)
				i = i.replace("(", "")
				i = i.replace("[", "")
				i = i.replace("]", "")
				i = i.replace(")", "")
				value_list.append("[" + i + "]")
			return value_list
		except pd.errors.EmptyDataError:
			print(f'{csv_file} is empty')

	def _check_folder_path(self):
		if os.path.isdir(self.temp_chart_path) is False:
			os.mkdir(self.temp_chart_path)
		else:
			print(f'Save plot in {self.temp_chart_path}')

	def _mako_line_html_chart(self, model, var):  # Load and read the templates, write variables in the templates
		from mako.template import Template

		path_name = (f'{self.library}{os.sep}funnel_comp{os.sep}{model}.mat_{var}'.strip())

		folder = os.path.isdir(path_name)
		if folder is False:
			print(f'Cant find folder: {self.CRED}{model}{self.CEND} with variable {self.CRED}{var}{self.CEND}')
		else:
			print(f'Plot model: {self.green}{model}{self.CEND} with variable:{self.green} {var}{self.CEND}')
			value = Plot_Charts._read_csv_funnel(self, path_name)

			mytemplate = Template(filename=self.temp_file)  # Render Template
			hmtl_chart = mytemplate.render(values=value, var=[f'{var}_ref',var], model=model, title=f'{model}.mat_{var}')
			file_tmp = open(f'{self.temp_chart_path}{os.sep}{model}_{var.strip()}.html', "w")
			file_tmp.write(hmtl_chart)
			file_tmp.close()

	def _mako_line_ref_chart(self, model, var):  # Load and read the templates, write variables in the templates
		from mako.template import Template

		path_name = (f'{self.library}{os.sep}funnel_comp{os.sep}{model}.mat_{var}'.strip())

		folder = os.path.isdir(path_name)
		if folder is False:
			print(f'Cant find folder: {self.CRED}{model}{self.CEND} with variable {self.CRED}{var}{self.CEND}')
		else:
			print(f'Plot model: {self.green}{model}{self.CEND} with variable:{self.green} {var}{self.CEND}')
			value = Plot_Charts._read_csv_funnel(self, path_name)

			mytemplate = Template(filename=self.temp_file)  # Render Template
			hmtl_chart = mytemplate.render(values=value, var=[f'{var}_ref',var], model=model, title=f'{model}.mat_{var}')
			file_tmp = open(f'{self.temp_chart_path}{os.sep}{model}_{var.strip()}.html', "w")
			file_tmp.write(hmtl_chart)
			file_tmp.close()

	def _create_index_layout(self):  # Create a index layout from a template
		from mako.template import Template
		html_file_list = []
		for file in os.listdir(self.temp_chart_path):
			if file.endswith(".html") and file != "index.html":
				html_file_list.append(file)
		mytemplate = Template(filename=self.index_temp_file)
		if len(html_file_list) == 0:
			print(f'No html files')
			os.rmdir(self.temp_chart_path)
			exit(0)
		else:
			hmtl_chart = mytemplate.render(html_model=html_file_list)
			file_tmp = open(self.index_html_file, "w")
			file_tmp.write(hmtl_chart)
			file_tmp.close()
			print(f'Create html file with reference results.')

	def _create_layout(self):  # Creates a layout index that has all links to the subordinate index files
		package_list = []
		for folder in os.listdir(self.index_path):
			if folder == "style.css" or folder == "index.html":
				continue
			else:
				package_list.append(folder)

		from mako.template import Template
		mytemplate = Template(filename=self.layout_temp_file)
		if len(package_list) == 0:
			print(f'No html files')
			exit(0)
		else:
			hmtl_chart = mytemplate.render(single_package=package_list)
			file_tmp = open(self.layout_html_file, "w")
			file_tmp.write(hmtl_chart)
			file_tmp.close()

	def _check_file(self):
		file_check = os.path.isfile(self.f_log)
		if file_check is False:
			print(f'{self.f_log} does not exists.')
			exit(1)
		else:
			print(f'{self.f_log} exists.')

	def _get_lines(self, ref_file):
		ref = open(f'{self.ref_path}{os.sep}{ref_file}', "r")
		lines = ref.readlines()
		ref.close()
		return lines


if  __name__ == '__main__':
	# Set colors
	green = "\033[0;32m"
	CRED = '\033[91m'
	CEND = '\033[0m'

	## Initialize a Parser
	# Set environment variables
	parser = argparse.ArgumentParser(description='Plot diagramms')
	unit_test_group = parser.add_argument_group("arguments to plot diagrams")

	unit_test_group.add_argument("--line-html",
								 help='plot a google html chart in line form',
								 action="store_true")
	unit_test_group.add_argument("--create-layout",
								 help='plot a google html chart in line form',
								 action="store_true")
	unit_test_group.add_argument("--line-matplot",
								 help='plot a google html chart in line form',
								 action="store_true")

	unit_test_group.add_argument("-m", "--modellist",
								metavar = "Modelica.Model",
								help = "Plot this model")

	unit_test_group.add_argument("-pM", "--plotModel",
								 help="Plot this model",
								 action="store_true")
	unit_test_group.add_argument("--all-model",
								 help='Plot all model',
								 action="store_true")
	unit_test_group.add_argument("-e", "--error",
								 help='Plot only model with errors',
								 action="store_true")

	unit_test_group.add_argument('-s', "--single-package",
								 metavar="Modelica.Package",
								 help="Test only the Modelica package Modelica.Package")
	unit_test_group.add_argument("-L", "--library", default="AixLib", help="Library to test")
	unit_test_group.add_argument('-fun', "--funnel-comp",
								 help="Take the datas from funnel_comp",
								 action = "store_true")
	unit_test_group.add_argument('-ref', "--ref-txt",
								 help="Take the datas from reference datas",
								 action="store_true")
	# Parse the arguments
	args = parser.parse_args()

	# *********************************************************************************************************
	from google_charts import Plot_Charts

	charts = Plot_Charts(package=args.single_package, library=args.library)
	# python bin/02_CITests/Converter/google_charts.py --line-html --error --funnel-comp --single-package Airflow
	# python bin/02_CITests/Converter/google_charts.py --line-html --error --ref-txt --single-package Airflow

	if args.line_html is True:  # Create Line chart html
		if args.error is True:  # Plot all data with an error
			charts._check_file()
			model_var_list = charts._read_unitTest_log()
			charts._check_folder_path()
			print(f'Plot line chart with different reference results.\n')
			for model_var in model_var_list:
				list = model_var.split(":")
				model = list[0]
				var = list[1]
				if args.funnel_comp is True:  # Data from funnel comp
					charts._mako_line_html_chart(model, var)

				if args.ref_txt is True:  # Data from reference files
					ref_file = charts._get_ref_file(model)
					if ref_file is None:
						print(f'Referencefile for model {model} does not exist.')
						continue
					else:
						lines = charts._get_lines(ref_file)
						result = charts._get_values(lines)
						time_list = result[0]
						measure_list = result[1]
						measure_len = result[2]
						time_list = charts._get_time_int(time_list, measure_len)
						charts._mako_line_ref_chart(model, var)
			charts._create_index_layout()

		if args.single_package is False:  # Plot a Package
			data = read_unitTest_log(f_log)
			mako_line_html_chart(data, temp, temp_chart, f_log, csv_file, test_csv)
	if args.create_layout is True:
		charts.create_layout()