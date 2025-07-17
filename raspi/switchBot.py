import asyncio
import argparse
from bleak import BleakScanner, BleakClient
from config import SWITCHBOT_MAC_ADDRESS

def scan():
    async def run():
        devices = await BleakScanner.discover()
        for d in devices:
            print(d)
    asyncio.run(run())

async def switchBot(address=None):
    if address is None:
        address = SWITCHBOT_MAC_ADDRESS
    
    # SwitchBot のボタン押下コマンド
    COMMAND_UUID = "cba20002-224d-11e6-9fb8-0002a5d5c51b"
    command = bytearray([0x57, 0x01, 0x00])
    async with BleakClient(address) as client:
        await client.write_gatt_char(COMMAND_UUID, command)

def main():
    parser = argparse.ArgumentParser(description="SwitchBot controller")
    parser.add_argument('-s', '--scan', action='store_true',
                        help="Scan BLE devices")
    parser.add_argument('-d', '--device', type=str,
                        help="SwitchBot device MAC address to control")
    args = parser.parse_args()

    if args.scan:
        scan()
    elif args.device:
        asyncio.run(switchBot(args.device))
    else:
        asyncio.run(switchBot())

if __name__ == '__main__':
    main()
