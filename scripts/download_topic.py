import fastavro
import os
import traceback
import numpy as np
import sys
import io
from confluent_kafka import Consumer, KafkaError, TopicPartition
from multiprocessing import Pool

def consume(param):

    kafka_server   = param[0]
    topic          = param[1]
    partition      = int(param[2])
    output_dir     = param[3]
    group          = param[4]

    c = Consumer({
        'bootstrap.servers': kafka_server,
        'group.id': group,
        'auto.offset.reset': 'earliest'
    })

    c.assign([TopicPartition(topic,partition)])

    while True:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().name() == '_PARTITION_EOF':
                break
            continue

        bytes_alert = msg.value()

        bytes_io = io.BytesIO( bytes_alert )
        reader = fastavro.reader(bytes_io)
        data = reader.next()        
        candid = data['candid']
        candid_str = str(candid)
        print(candid_str)

        try:
            output_path = os.path.join(output_dir,"%s.avro"%(candid_str) )
            outfile = open(output_path,"wb")
            outfile.write(bytes_alert)
            outfile.close()
        except:
            print("error %s" % (candid_str) )
            traceback.print_exc()


    c.close()
    print("Closing Consumer (%s)" % ( str(partition) ) )

n = 16
pool = Pool(n)
params = []

kafka_server = sys.argv[1]
topic        = sys.argv[2]
output_dir   = sys.argv[3]
group        = sys.argv[4]

os.mkdir(output_dir)

for i in range(n):
    params.append( [kafka_server,topic,i,output_dir,group] )

pool.map(consume,params)
