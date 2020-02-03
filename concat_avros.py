import sys
import os
import numpy as np

input_directory  = sys.argv[1]
output_directory = sys.argv[2]

names = os.listdir(input_directory)

chunk_size = 2200
partitions = int(np.ceil(len(names) / chunk_size) )

os.chdir(input_directory)
os.mkdir(output_directory)

chunks = np.array_split(names,partitions)

count = 0
for chunk in chunks:
    print(count)
    files = ' '.join(chunk.tolist())
    output_path = os.path.join(output_directory,'partition_%d.avro'% (count) )
    command = 'java -jar /opt/libs/avro-tools-1.8.2.jar concat %s %s' % (files,output_path) 
    os.system(command)
    count = count+1
