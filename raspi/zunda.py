# voicevoxを起動しておく必要がある
import os
import requests
import json
import subprocess
import tempfile
import time
from config import SPEAKER_DEVICE

def talk(text):
    """音声合成して再生する"""
    try:
        host = "localhost"
        port = 50021
        
        params = (('text', text), ('speaker', 2))
        
        # 音声合成の開始時間を記録
        synthesis_start_time = time.time()
        
        # 音声合成用のクエリ作成
        query = requests.post(f'http://{host}:{port}/audio_query', params=params)
        
        # 音声合成を実施
        synthesis = requests.post(
            f'http://{host}:{port}/synthesis',
            headers={"Content-Type": "application/json"},
            params=params,
            data=json.dumps(query.json())
        )
        
        # 音声合成の終了時間を記録
        synthesis_end_time = time.time()
        synthesis_duration = synthesis_end_time - synthesis_start_time
        print(f"音声合成時間: {synthesis_duration:.3f}秒")
        
        # 音声データを一時ファイルに保存
        voice = synthesis.content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file.write(voice)
            temp_file_path = temp_file.name
        
        # aplayで音声再生
        subprocess.run(['aplay', '-D', SPEAKER_DEVICE, temp_file_path], 
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
        
        # 一時ファイルを削除
        os.unlink(temp_file_path)
                
    except requests.exceptions.ConnectionError:
        print("Voicevoxを起動して下さい")
    except Exception as e:
        print(f"音声合成エラー: {e}")
    
if __name__ == "__main__":
    while True:
        text = input("ここに入力：")
        talk(text)
