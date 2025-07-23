from config import SPEAKER_DEVICE, MIC_DEVICE, THRESHOLD
import speech_recognition as sr
def get_working_microphone():
    """利用可能なマイクデバイスを見つける"""
    microphone_names = sr.Microphone.list_microphone_names()
    
    # MIC_DEVICEが数字の場合はデバイス番号として使用
    if MIC_DEVICE.isdigit():
        device_index = int(MIC_DEVICE)
        if 0 <= device_index < len(microphone_names):
            try:
                with sr.Microphone(device_index=device_index) as source:
                    print(f"マイクデバイス {device_index} ({microphone_names[device_index]}) を使用します")
                    return device_index
            except:
                pass
    
    # デバイス名で検索
    for index, name in enumerate(microphone_names):
        if MIC_DEVICE in name:
            try:
                with sr.Microphone(device_index=index) as source:
                    print(f"マイクデバイス {index} ({name}) を使用します")
                    return index
            except:
                continue
    
    # 優先キーワードで検索
    priority_keywords = ["MIC", "USB Device", "USB Audio"]
    for keyword in priority_keywords:
        for index, name in enumerate(microphone_names):
            if keyword in name:
                try:
                    with sr.Microphone(device_index=index) as source:
                        print(f"マイクデバイス {index} ({name}) を使用します")
                        return index
                except:
                    continue
    
    print("利用可能なマイクデバイスが見つかりません")
    return None

def main():
    """メイン処理"""
    r = sr.Recognizer()
    
    # 利用可能なマイクデバイス一覧を表示
    print("利用可能なマイクデバイス:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  {index}: {name}")
    
    # マイクデバイス選択
    mic_device_index = get_working_microphone()
    if mic_device_index is None:
        print("マイクデバイスが見つかりません")
        return

if __name__ == "__main__":
    main()
