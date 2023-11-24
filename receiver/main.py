import serial
from kafka import KafkaProducer

topic_name = 'ti-monitor'
producer = KafkaProducer(bootstrap_servers='localhost:9092')


with serial.Serial() as ser:
    ser.baudrate = 9600
    ser.port = '/dev/cu.usbserial-110'
    ser.open()
    while True:
        out = ser.readline().decode("utf-8").strip()
        print(out)
        producer.send(topic_name, f"{out}".encode())
        producer.flush()

