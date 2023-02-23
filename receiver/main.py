from serial import *
from kafka import KafkaProducer
from copy import deepcopy
from typing import Union
from time import sleep

producer = KafkaProducer(bootstrap_servers='localhost:9092')
path = 'receiver/test_data.csv'


with open(path) as f:
    raw_data = [x for x in f.read().split('\n')]

raw_data.pop()
count = 0

for i in iter(int, 1):
    if count == len(raw_data):
        count = 0
    producer.send('ti-monitor', f'{raw_data[count]}'.encode())
    producer.flush()
    count += 1




