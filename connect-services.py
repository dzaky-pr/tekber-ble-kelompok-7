import asyncio
from bleak import BleakClient
import sys

async def get_services(mac):
    async with BleakClient(mac) as client:
        print(f"Connected: {client.is_connected}")
        
        svcs = await client.get_services()
        print("Services:", svcs)
        for service in client.services:
            print('Service: ')
            print(service)
            
            print('\nCharacteristics: ')
            for char in service.characteristics:
                print(char)
                print('\nProperties')
                print(char.properties)
                
        await client.disconnect()

try:
    asyncio.run(get_services("7E7365C3-F167-9C05-74A1-8513CD38DCA2"))
except KeyboardInterrupt:
    print("User stopped the program")
    sys.exit(0)

