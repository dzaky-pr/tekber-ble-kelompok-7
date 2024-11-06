import asyncio
from bleak import BleakClient
import sys

async def get_services(mac):
    async with BleakClient(mac) as client:
        print(f"Connected: {client.is_connected}")
        
        # Directly access the services property
        svcs = client.services
        print("Services:", svcs)
        
        for service in svcs:
            print('Service:')
            print(service)
            
            print('\nCharacteristics:')
            for char in service.characteristics:
                print(char)
                print('\nProperties:')
                print(char.properties)
        
        await client.disconnect()

try:
    asyncio.run(get_services("51867DCD-722A-7784-2B85-7FA566E5FDD1"))
except KeyboardInterrupt:
    print("User stopped the program")
    sys.exit(0)
