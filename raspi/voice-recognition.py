import asyncio
import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util
import subprocess
import time
from config import SPEAKER_DEVICE, MIC_DEVICE, THRESHOLD
import switchBot
import zunda

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def cosineScore(text1, text2):
    """2つのテキストのコサイン類似度を計算"""
    embeddings1 = model.encode(text1, convert_to_tensor=True)
    embeddings2 = model.encode(text2, convert_to_tensor=True)
    cosine_score = util.pytorch_cos_sim(embeddings1, embeddings2)[0][0]
    return cosine_score

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

def process_voice_command(recognized_text):
    """音声コマンドを処理"""
    if cosineScore(recognized_text, "電気をつけて") >= THRESHOLD:
        subprocess.run(['aplay', '-D', SPEAKER_DEVICE, 'pi.wav'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        zunda.talk("電気をつけます")
        asyncio.run(switchBot.switchBot())
    
    elif cosineScore(recognized_text, "自己紹介してください") >= THRESHOLD:
        subprocess.run(['aplay', '-D', SPEAKER_DEVICE, 'pi.wav'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        zunda.talk("私は音声アシスタント，ラボ草です")

    elif cosineScore(recognized_text, "ただいま") >= 0.95:
        subprocess.run(['aplay', '-D', SPEAKER_DEVICE, 'pi.wav'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        zunda.talk("おかえりなさい．お疲れ様です")

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
    
    print(f"使用設定:")
    print(f"  マイクデバイス: {MIC_DEVICE}")
    print(f"  スピーカーデバイス: {SPEAKER_DEVICE}")
    print(f"  コサイン類似度閾値: {THRESHOLD}")
    
    while True:
        try:
            with sr.Microphone(device_index=mic_device_index) as source:
                r.adjust_for_ambient_noise(source)
                print("話しかけてください...")
                
                # 音声認識の開始時間を記録
                recognition_start_time = time.time()
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                
            recognized_text = r.recognize_google(audio, language='ja-JP')
            recognition_end_time = time.time()
            recognition_duration = recognition_end_time - recognition_start_time
            
            print("認識結果:", recognized_text)
            print(f"音声認識時間: {recognition_duration:.3f}秒")
            
            process_voice_command(recognized_text)
        
        except sr.UnknownValueError:
            print("聞き取れませんでした")
        except sr.WaitTimeoutError:
            print("時間内に話されませんでした")
        except OSError as e:
            print(f"マイクエラー: {e}")
            # デバイスを再検索
            mic_device_index = get_working_microphone()
            if mic_device_index is None:
                break
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    main()
