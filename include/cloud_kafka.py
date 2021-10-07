from kafka import KafkaProducer, KafkaConsumer

CLOUDKARAFKA_BROKERS="glider-01.srvs.cloudkafka.com:9094,glider-02.srvs.cloudkafka.com:9094,glider-03.srvs.cloudkafka.com:9094"
CLOUDKARAFKA_USERNAME="2b581ilu"
CLOUDKARAFKA_PASSWORD="bLWtMKWM4p-apnAFhH-umZni41Bbe3YT"
CLOUDKARAFKA_TOPIC_PREFIX="2b581ilu-"

producer = KafkaProducer(bootstrap_servers=CLOUDKARAFKA_BROKERS,
                         sasl_plain_username=CLOUDKARAFKA_USERNAME,
                         sasl_plain_password=CLOUDKARAFKA_PASSWORD,
                         security_protocol='SASL_SSL',
                         sasl_mechanism='SCRAM-SHA-256',
                         ssl_cafile='tools/cafile.crt',
                        #  api_version=(0,10),
                         retries=5,
                         )
                        

kafka_topic="predict"
kafka_topic = CLOUDKARAFKA_TOPIC_PREFIX+kafka_topic
