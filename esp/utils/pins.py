import dht
from machine import I2C, Pin


ON = 1
OFF = 0

LED = Pin(1, Pin.OUT)
DHT = dht.DHT11(Pin(2, Pin.IN, Pin.PULL_UP))
