import asyncio
import argparse
import sys
from bleak import BleakScanner, BleakClient

# E1:3D:04:86:18:7C

def scan():
    async def run():
        devices = await BleakScanner.discover()
        for d in devices:
            print(d)
    asyncio.run(run())

async def switchBot(address):
    # SwitchBot のボタン押下コマンド
    COMMAND_UUID = "cba20002-224d-11e6-9fb8-0002a5d5c51b"
    command = bytearray([0x57, 0x01, 0x00])
    async with BleakClient(address) as client:
        await client.write_gatt_char(COMMAND_UUID, command)

def main():
    parser = argparse.ArgumentParser()
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
        print("引数が必要です。--scan または --device <MACアドレス> を指定してください。")

if __name__ == '__main__':
    main()
