import asyncio
from bleak import BleakClient
import sys

# UUIDs of interest
uuid_battery_service = '0000180f-0000-1000-8000-00805f9b34fb'
uuid_battery_level = '00002a19-0000-1000-8000-00805f9b34fb'
uuid_device_information = '0000180a-0000-1000-8000-00805f9b34fb'
uuid_current_time = '00002a2b-0000-1000-8000-00805f9b34fb'
uuid_manufacturer_name = '00002a29-0000-1000-8000-00805f9b34fb'
uuid_model_number = '00002a24-0000-1000-8000-00805f9b34fb'
uuid_local_time_info = '00002a0f-0000-1000-8000-00805f9b34fb'

async def get_services(mac):
    async with BleakClient(mac) as client:
        print(f"Connected: {client.is_connected}")
        
        # Access the services property
        svcs = client.services
        found_data = {
            "battery_service": False,
            "battery_level": False,
            "device_info": False,
            "current_time": False,
            "manufacturer": False,
            "model": False,
            "local_time": False,
        }

        for service in svcs:
            for char in service.characteristics:
                # Read battery level
                if char.uuid == uuid_battery_level:
                    battery_level = await client.read_gatt_char(char)
                    battery_level_value = int.from_bytes(battery_level, byteorder="little")
                    print(f'Battery Level: {battery_level_value}%')
                    found_data["battery_level"] = True

                # Read manufacturer name
                elif char.uuid == uuid_manufacturer_name:
                    manufacturer_name = await client.read_gatt_char(char)
                    try:
                        print(f'Manufacturer Name: {manufacturer_name.decode("utf-8")}')
                    except UnicodeDecodeError:
                        print("Manufacturer Name: Non-UTF-8 data received")
                    found_data["manufacturer"] = True
                    
                # Read battery service
                elif char.uuid == uuid_battery_service:
                    model_service = await client.read_gatt_char(char)
                    try:
                        print(f'Model Battery Service: {model_service.decode("utf-8")}')
                    except UnicodeDecodeError:
                        print("Model Battery Service: Non-UTF-8 data received")
                    found_data["battery_service"] = True

                # Read model number
                elif char.uuid == uuid_model_number:
                    model_number = await client.read_gatt_char(char)
                    try:
                        print(f'Model Number: {model_number.decode("utf-8")}')
                    except UnicodeDecodeError:
                        print("Model Number: Non-UTF-8 data received")
                    found_data["model"] = True

                # Read device information
                elif char.uuid == uuid_device_information:
                    device_information = await client.read_gatt_char(char)
                    try:
                        print(f'Device Information: {device_information.decode("utf-8")}')
                    except UnicodeDecodeError:
                        print("Device Information: Non-UTF-8 data received")
                    found_data["device_info"] = True

                # Read current time
                elif char.uuid == uuid_current_time:
                    current_time = await client.read_gatt_char(char)
                    try:
                        print(f'Current Time: {current_time.decode("utf-8")}')
                    except UnicodeDecodeError:
                        print("Current Time: Non-UTF-8 data received")
                    found_data["current_time"] = True

                # Read local time information
                elif char.uuid == uuid_local_time_info:
                    local_time_info = await client.read_gatt_char(char)
                    try:
                        print(f'Local Time Information: {local_time_info.decode("utf-8")}')
                    except UnicodeDecodeError:
                        print("Local Time Information: Non-UTF-8 data received")
                    found_data["local_time"] = True

        # Check for any characteristics not found
        for key, found in found_data.items():
            if not found:
                print(f"{key.replace('_', ' ').title()} characteristic not found.")

        await client.disconnect()

try:
    asyncio.run(get_services("51867DCD-722A-7784-2B85-7FA566E5FDD1"))
except KeyboardInterrupt:
    print("User stopped the program")
    sys.exit(0)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
