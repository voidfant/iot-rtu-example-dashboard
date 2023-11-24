import serial
from time import sleep
from kafka import KafkaProducer
from random import uniform

producer = KafkaProducer(bootstrap_servers='kafka:9092')
path = './new_data.csv'

with open(path) as f:
    raw_data = [x for x in f.read().split('\n')]

raw_data.pop()
count = 0
delay = 0
producer.send('ti-monitor', f'{raw_data[0]}'.encode())
producer.flush()
for i in raw_data:
    producer.send('ti-monitor', f'{i}'.encode())
    producer.flush()
    delay = 0
    sleep(0.2)

i = i.split(';')
last_line = [int(i[0]), float(i[1]), float(i[2])]

print(last_line)

while True:
    last_line[0] += 1
    last_line[1] += 0.05
    last_line[1] = float("{:.2f}".format(last_line[1]))
    last_line[2] += uniform(-0.05, 0.05)
    last_line[2] = float("{:.2f}".format(last_line[2]))
    if last_line[2] < 0:
        last_line[2] = abs(last_line[2])
    producer.send('ti-monitor', f'{";".join(list(map(str, last_line)))}'.encode())
    print(";".join(list(map(str, last_line))))
    producer.flush()
    sleep(0.2)