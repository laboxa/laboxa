import asyncio
from bleak import BleakScanner, BleakClient
import logging

# ログレベルを WARNING に下げて Bleak の詳細ログを抑制
logging.basicConfig(level=logging.WARNING)

# SwitchBotのGATTキャラクタリスティックUUID
COMMAND_UUID = "cba20002-224d-11e6-9fb8-0002a5d5c51b"
COMMAND = bytearray([0x57, 0x01, 0x00])

async def try_switchbot(device):
    try:
        async with BleakClient(device.address) as client:
            await client.write_gatt_char(COMMAND_UUID, COMMAND)
            print(f"✅ 成功: {device.name} ({device.address})")
            return device
    except Exception as e:
        print(f"❌ 失敗: {device.name} ({device.address}) → {e}")
        return None

async def scan_and_test():
    print("🔍 デバイスをスキャン中...")
    devices = await BleakScanner.discover()
    print(f"検出されたデバイス数: {len(devices)}\n")

    found = []
    for device in devices:
        name = device.name or "Unknown"
        print(f"👉 試行中: {name} ({device.address})")
        result = await try_switchbot(device)
        if result:
            found.append(result)

    print("\n🎉 動作したデバイス一覧:")
    if found:
        for d in found:
            print(f"✅ {d.name or 'Unknown'} ({d.address})")
    else:
        print("⚠️ どのデバイスにも成功しませんでした。")

if __name__ == "__main__":
    asyncio.run(scan_and_test())
