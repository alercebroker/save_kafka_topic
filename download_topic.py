import fastavro
import os
import traceback
import numpy as np
import sys
import io
from confluent_kafka import Consumer, KafkaError, TopicPartition
from multiprocessing import Pool

def consume(param):

    topic      = param[0]
    partition  = int(param[1])
    output_dir = param[2]
    group      = param[3]

    c = Consumer({
        'bootstrap.servers': 'kafka1.alerce.online:9092',
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

topic      = sys.argv[1]
output_dir = sys.argv[2]
group      = sys.argv[3]

for i in range(n):
    params.append( [topic,i,output_dir,group] )

pool.map(consume,params)
