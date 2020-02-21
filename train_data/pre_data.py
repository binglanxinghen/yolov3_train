import argparse
  
PARSER = argparse.ArgumentParser()
# Input Arguments
PARSER.add_argument('-t','--train',dest='train',help='write trainval file',default=False,nargs=1)
PARSER.add_argument('-e','--test',dest='test',help='write test file',default=False,nargs=1)

ARGUMENTS, _ = PARSER.parse_known_args()
if ARGUMENTS.train:
        with open("./train/ImageSets/Main/trainval.txt",'w') as f:
                run_configure(ARGUMENTS.runconfig)
                    sys.exit()



