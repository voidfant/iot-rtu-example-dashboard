import serial
from time import sleep
from kafka import KafkaProducer
from random import uniform

producer = KafkaProducer(bootstrap_servers='localhost:9092')
path = 'receiver/modified_mock_data.csv'


with open(path) as f:
    raw_data = [x for x in f.read().split('\n')]

raw_data.pop()
count = 0
delay = 0
producer.send('ti-monitor', f'{raw_data[0]}'.encode())
producer.flush()
delay = 0
for i in raw_data:
    delay += 1
    if delay == 2:
        producer.send('ti-monitor', f'{i}'.encode())
        producer.flush()
        delay = 0
    else:
        continue

    sleep(0.02)


i = i.split(';')
last_line = [int(i[0]), float(i[1]), float(i[2]), float(i[3]),
             float(i[4]), float(i[5]), float(i[6]), float(i[7]), float(i[8])]

print(last_line)

while True:

    last_line[0] += 1
    last_line[1] += 0.05
    last_line[1] = float("{:.2f}".format(last_line[1]))
    for i in range(2, 9):
        last_line[i] += uniform(-0.05, 0.05)
        last_line[i] = float("{:.2f}".format(last_line[i]))
        if last_line[i] < 0 and i != 5 and i != 6:
            last_line[i] = abs(last_line[i])
    delay += 1
    # last_line = list(map(str, last_line))
    if delay == 2:
        producer.send('ti-monitor', f'{";".join(list(map(str, last_line)))}'.encode())
        print(";".join(list(map(str, last_line))))
        producer.flush()
        delay = 0
    else:
        continue
    sleep(0.02)


# for i in iter(int, 1):
#
#     if count == len(raw_data):
#         count = 0
#     producer.send('ti-monitor', f'{raw_data[count]}'.encode())
#     producer.flush()
#     count += 1
#     sleep(0.02)




