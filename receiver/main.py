from serial import *
from time import sleep
from kafka import KafkaProducer
from random import uniform

producer = KafkaProducer(bootstrap_servers='localhost:9092')
path = 'receiver/new_data.csv'


with open(path) as f:
    raw_data = [x for x in f.read().split('\n')]

raw_data.pop()
count = 0

for i in raw_data:
    producer.send('ti-monitor', f'{i}'.encode())
    producer.flush()
    sleep(0.02)

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
    # last_line = list(map(str, last_line))
    producer.send('ti-monitor', f'{";".join(list(map(str, last_line)))}'.encode())
    print(";".join(list(map(str, last_line))))
    producer.flush()
    sleep(0.02)

# for i in iter(int, 1):
#
#     if count == len(raw_data):
#         count = 0
#     producer.send('ti-monitor', f'{raw_data[count]}'.encode())
#     producer.flush()
#     count += 1
#     sleep(0.02)




