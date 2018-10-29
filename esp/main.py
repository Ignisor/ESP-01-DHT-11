import time

import ubinascii
import machine
from umqtt.simple import MQTTClient

from data import conf
from utils.pins import DHT


CLIENT_ID = ubinascii.hexlify(machine.unique_id())
mqtt = MQTTClient(CLIENT_ID, conf.MQTT_SERVER)
mqtt.connect()


def main():
    time.sleep(5)
    DHT.measure()

    temp = DHT.temperature()
    humidity = DHT.humidity()
    mqtt.publish('sensors/temperature/{}'.format(CLIENT_ID).encode(), str(temp).encode())
    mqtt.publish('sensors/humidity/{}'.format(CLIENT_ID).encode(), str(humidity).encode())


retries = 5
while retries:
    try:
        main()
        break
    except Exception as e:
        with open('errors.txt', 'a') as err_file:
            err_file.write(str(e))
            err_file.write('\n')
        mqtt.publish('errors/{}'.format(CLIENT_ID).encode(), str(e).encode())
        retries -= 1

mqtt.disconnect()

rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
rtc.alarm(rtc.ALARM0, 5 * 60 * 1000)

machine.deepsleep()
