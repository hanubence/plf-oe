import bluetooth
import asyncio
import aioble
import struct

from moo import Moo

# Characteristic UUIDs
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
_ENV_SENSE_ACC_UUID = bluetooth.UUID(0x2713)
_ENV_SENSE_GYRO_UUID = bluetooth.UUID(0x2744)
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)

_GENERIC_THERMOMETER = 768

_ADV_INTERVAL_US = 250000

class BLEServer:
    
    def __init__(self) -> None:
        self.moo = Moo()
        esp_service = aioble.Service(_ENV_SENSE_UUID)
        
        self.acc_char = aioble.Characteristic(esp_service, _ENV_SENSE_ACC_UUID, read=True, notify=True)
        self.gyro_char = aioble.Characteristic(esp_service, _ENV_SENSE_GYRO_UUID, read=True, notify=True)
        self.temp_char = aioble.Characteristic(esp_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True)

        aioble.register_services(esp_service)

    def encode_temp(self, temp):
        return str(temp).encode('utf-8')
    
    def encode_acc(self, acc):
        return b';'.join(str(x).encode('utf-8') for x in acc)
    
    def encode_gyro(self, gyro):
        return b';'.join(str(x).encode('utf-8') for x in gyro)

    async def sensor_task(self):
        while True:
            self.acc_char.write(self.encode_acc(self.moo.acc), send_update=True)
            self.gyro_char.write(self.encode_gyro(self.moo.gyro), send_update=True)
            self.temp_char.write(self.encode_temp(self.moo.object_temp), send_update=True)
            await asyncio.sleep_ms(1000)

    async def advertise_task(self):
        while True:
            try:
                async with await aioble.advertise(
                    _ADV_INTERVAL_US,
                    name="Moonitor",
                    services=[_ENV_SENSE_UUID],
                    appearance=_GENERIC_THERMOMETER,
                    manufacturer=(0xabcd, b"1234"),
                ) as connection:
                    print('BLE Connected: ', connection.device)
                    await connection.disconnected()
            except Exception as e:
                print('BLE Advertise failed: ', e)
            await asyncio.sleep(1)

    async def run(self):
        advertise_task = asyncio.create_task(self.advertise_task())
        sensor_task = asyncio.create_task(self.sensor_task())
        await asyncio.gather(advertise_task, sensor_task)