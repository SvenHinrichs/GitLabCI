import os
import sys 
import shutil
import glob


def copy_mos(ibpsa_dir,dst):
	#IBPSA/Resources/Scripts/Dymola/ConvertIBPSA_from_3.0_to_4.0.mos
	# D:\01_Arbeit\04_Github\01_GitLabCI\master\GitLabCI\IBPSA\IBPSA\Resources\Scripts\Dymola
	#D:\01_Arbeit\04_Github\01_GitLabCI\master\GitLabCI
	''' Copy the ConvertIBPSA mos Script'''
	if  os.path.isdir(dst) :
		pass
	else:
		os.mkdir(dst)
	#for file in glob(ibpsa_dir):
	file = (glob.glob(ibpsa_dir))
	# Look which ConvertScript is the latest
	if len(file)==0:
		print("Cant find a Conversion Script in IBPSA Repo")
		exit(0)
	
	if len(file)>1:
		list = []
		for i in file:
			i = i.replace(".mos","")
			list.append(i)
		
		data = (sorted(list, key=lambda x: float(x[x.find("_to_")+4:])))
		data = (data[len(data)-1])
		i = data+".mos"
		data = data.split(os.sep)
		data = data[len(data)-1]
		data = dst +os.sep+ data+".mos"
		
		shutil.copy(i,dst)
	if len(file) == 1:
		for i in file:
			shutil.copy(i, dst)
		file = file[len(file)-1]
		data = file.split(os.sep)
		data = data[len(data)-1]
		data = dst +os.sep+ data
		
	
	return data 
	
	
	'''for root, subdirs, files in os.walk('D:\\01_Arbeit\\04_Github\\01_GitLabCI\\master'):
		
		for d in subdirs:
			if d == "IBPSA":
				print(root)
				print(files)
	'''			
# Read the last aixlib mos sciprt
def read_aixlib_convert(aixlib_dir):
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
	data = (data[len(data)-1])+".mos"
	return data
	
#  change the paths in the script from IBPSA.Package.model -> AixLib.Package.model
def create_convert_aixlib(data,dst,l_conv_aix,comp):
	if comp is False:
		print("The latest conversion script is up to date from the IBPSA")
	if comp is True:
		conv_number =  l_conv_aix[l_conv_aix.find("ConvertAixLib_from_")+19:l_conv_aix.rfind(".mos")]
		# Update from Number
		from_numb =  int(conv_number[conv_number.find(".",2)+1:conv_number.find("_to_0")])+1
		from_numb = conv_number[:conv_number.find(".",2)+1] + str(from_numb)
		
		# Update to Number
		to_numb = int(conv_number[conv_number.rfind(".")+1:]) +1
		to_numb = conv_number[conv_number.find("_to_0")+4:conv_number.rfind(".")+1] + str(to_numb)
		
		new_conv_number = str(from_numb)+"_to_"+str(to_numb)
		file_new_conv = "ConvertAixLib_from_"+new_conv_number+".mos"
		
		aixlib_mos = dst+os.sep+file_new_conv
		f = open(data, "r")
		r = open(aixlib_mos,"w+")
		for line in f:
			r.write(line.replace("IBPSA","AixLib"))
		f.close()
		r.close()
		return aixlib_mos
# D:\01_Arbeit\04_Github\01_GitLabCI\master\GitLabCI\AixLib\Resources\Scripts
def copy_aixlib_mos(aixlib_mos,aixlib_dir,dst):
	shutil.copy(aixlib_mos, aixlib_dir)
	shutil.rmtree(dst)
def compare_conversions(data,aixlib_dir,l_conv_aix):
	ipbsa_conv = data
	aix_conv = aixlib_dir+os.sep+l_conv_aix
	f = open(ipbsa_conv, "r")
	r = open(aix_conv,"r")
	IBPSA = f.readlines()
	aixlib = r.readlines()
	f.close()
	r.close()
	x = 0
	list = []
	if len(IBPSA) == len(aixlib):
		for i in IBPSA:
			i = i.replace("IBPSA","AixLib")
			if i != aixlib[x]: 
				list.append(i)
				
			x = x+1
	else:
		list.append(x)
	if len(list)>0:
		return True
	if len(list)==0:
		return False
	
if  __name__ == '__main__':
	aixlib_dir = "D:\\01_Arbeit\\04_Github\\01_GitLabCI\\master\\GitLabCI\\AixLib\\Resources\\Scripts"
	ibpsa_dir = 'D:\\01_Arbeit\\04_Github\\01_GitLabCI\\master\\GitLabCI\\IBPSA\\IBPSA\\Resources\\Scripts\\Dymola\\ConvertIBPSA_*'
	dst = "D:\\01_Arbeit\\04_Github\\01_GitLabCI\\master\\GitLabCI\\Convertmos"
	data = copy_mos(ibpsa_dir,dst)
	
	
	l_conv_aix = read_aixlib_convert(aixlib_dir)
	comp = compare_conversions(data,aixlib_dir,l_conv_aix)
	aixlib_mos = create_convert_aixlib(data,dst,l_conv_aix,comp)
	if aixlib_mos is None:
		print("please check when the last merge took place")
		shutil.rmtree(dst)
	else:	
		copy_aixlib_mos(aixlib_mos,aixlib_dir,dst)
		print("New Aixlib Conversion skrip was created")