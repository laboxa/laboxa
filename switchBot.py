import asyncio
import argparse
from bleak import *

def scan():
    async def run():
        devices = await BleakScanner.discover()
        for d in devices:
            print(d)
            if "D3:F8:8D" in d.address : # filter switch bot divices
                print(f"python switchbot.py -d {d.address}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    
def switchBot(address):
    UUID = "cba20002-224d-11e6-9fb8-0002a5d5c51b"
    async def run(address, loop):
        async with BleakClient(address, loop=loop) as client:
            await client.write_gatt_char(UUID, bytearray(b'\x57\x01\x00'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop))
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scan', dest='scan', required=False, default=False, action='store_true',
                        help="Run Switchbot in scan mode - scan devices to control")
    parser.add_argument('-d', '--device', dest='device', required=False, default=None,
                        help="Specify the address of a device to control")
    opts, args = parser.parse_known_args(sys.argv[1:])
    if opts.scan:
        scan()
    elif opts.device:
        switchBot(opts.device)
if __name__ == '__main__':
    main()
