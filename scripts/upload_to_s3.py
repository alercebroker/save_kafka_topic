import os
import sys

input_dir   = sys.argv[1]
output_path = sys.argv[2]

command = 'aws s3 sync %s %s' % (input_dir,output_path)
os.system(command)
