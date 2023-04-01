import serial
import time
import io
from time import sleep
from kafka import KafkaProducer

topic_name = 'ti-monitor'
producer = KafkaProducer(bootstrap_servers='localhost:9092')
# producer.send('ti-monitor', f'{raw_data[0]}'.encode())
# producer.flush()

# cnt = 0
with serial.Serial() as ser:
    ser.baudrate = 9600
    ser.port = '/dev/cu.usbserial-120'
    ser.open()
    # start = time.time()
    while True:
        # if time.time() - start >= 2:
        #     print(cnt)
        #     exit()
        # cnt += 1
        out = ser.readline().decode("utf-8").strip()
        # print(out.decode("utf-8"), end='')
        print(out)
        producer.send(topic_name, f"{out}".encode())
        producer.flush()

# for i in range(5):
#     producer.send(topic_name, f'{"негры" * i}'.encode())
#     producer.flush()
