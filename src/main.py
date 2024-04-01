from machine import I2C, Pin
import network
import mip
import asyncio
from time import sleep

def main():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect('Bence', 'Cica1234')

    while not wifi.isconnected():
        print('Connecting to wifi...')
        sleep(1)

    print('Connected to wifi')
    print(wifi.ifconfig())

    mip.install('aioble')

    wifi.active(False)
    del wifi

    from ble import BLEServer
    server = BLEServer()
    asyncio.run(server.run())
    
