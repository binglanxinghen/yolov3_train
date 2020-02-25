import os
import argparse

PARSER = argparse.ArgumentParser()
# Input Arguments
PARSER.add_argument('-t','--train',dest='train',help='write trainval file',default=False,nargs=1)
PARSER.add_argument('-e','--test',dest='test',help='write test file',default=False,nargs=1)
PARSER.add_argument('-l','--log',help='write test file',nargs="*")

ARGUMENTS, _ = PARSER.parse_known_args()
print(ARGUMENTS)

def process_file(flag,filename):
	jpg_list=[]
	xml_list=[]
	for root,dirs,files in os.walk("./%s/JPEGImages"%(flag),topdown=False):
		for file in files:
			extension = os.path.splitext(file)[1]
			if extension == ".jpg":
				jpg_list.append(os.path.splitext(file)[0])
	for root,dirs,files in os.walk("./%s/Annotations"%(flag),topdown=False):
		for file in files:
			extension = os.path.splitext(file)[1]
			if extension ==".xml":
				xml_list.append(os.path.splitext(file)[0])
	if ARGUMENTS.log is not None and all(ARGUMENTS.log):
		for pic in jpg_list:
			if pic not in xml_list:
				print("%s isn't exist xml file"%(pic))
				jpg_list.remove(pic)
	
	jpg_list = list(map(lambda x:x+"\n",jpg_list))
	with open("./%s/ImageSets/Main/%s"%(flag,filename),"w") as f:
		f.writelines(jpg_list)
	#run_configure(ARGUMENTS.runconfig)

if ARGUMENTS.train:
	print("=======train==========")
	process_file('train','trainval.txt')

if ARGUMENTS.test:
	print("=======test==========")
	process_file('test','test.txt')


