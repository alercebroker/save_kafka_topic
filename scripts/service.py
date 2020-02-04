import datetime
import logging
import sys
import json
import shutil
import schedule
import time
import os

def service(config):

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("MAIN")

        
    #DATE
    today     = datetime.date.today()
    delta     = datetime.timedelta(1)
    yesterday = today - delta
    date_str = yesterday.strftime("%Y%m%d")

    #DOWNLOAD
    topic = 'ztf_%s_programid1' % (date_str)
    group = '%s_%s' %( config['group'], date_str )
    output_path = os.path.join(config['working_dir'],topic)
    avro_directory = output_path
    command = 'python3 /app/scripts/download_topic.py %s %s %s %s' % ( 
                                                            config['kafka_server'],
                                                            topic,
                                                            output_path,
                                                            group
              )
    logger.info("DOWNLOADING topic %s from %s" % (topic,config['kafka_server']) )
    os.system(command)

    #CONCAT
    input_path  = output_path
    output_path = os.path.join(config['working_dir'],'%s_concatened' % (topic) )
    concat_directory = output_path
    command = 'python3 /app/scripts/concat_avros.py %s %s' % (input_path, output_path)
    logger.info("CONCATENATING topic %s" %(topic) )
    os.system(command)

    #UPLOAD
    input_path  = output_path
    output_path = os.path.join(config['output_bucket'],topic)
    command = 'python3 /app/scripts/upload_to_s3.py %s %s' % (input_path,output_path)
    logger.info("UPLOADING topic %s" %(topic) )
    os.system(command)

    #REMOVE 
    logger.info("REMOVING topic directories %s" %(topic) )
    shutil.rmtree(avro_directory)
    shutil.rmtree(concat_directory)

#READ CONFIG
infile = open('/app/config.json','r')
config = json.load(infile)
infile.close()

service(config)
#schedule.every().day.at(config['start_time']).do(service,config=config)
#while True:
#    schedule.run_pending()
#    time.sleep(10)
