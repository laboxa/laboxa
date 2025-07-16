# voicevoxを起動しておく必要がある

import os
import requests
import json
import subprocess
import tempfile

# 音声関連のエラーを抑制するための環境変数設定
# aplay -lでちぇっくせよ
os.environ['ALSA_PCM_CARD'] = '4'
os.environ['ALSA_PCM_DEVICE'] = '0'

def talk(text):
    try:
        # エンジン起動時に表示されているIP、portを指定
        host = "localhost"
        port = 50021
        
        # 音声化する文言と話者を指定(3で標準ずんだもんになる)
        params = (
            ('text', text),
            ('speaker', 2),
        )
        
        # 音声合成用のクエリ作成
        query = requests.post(
            f'http://{host}:{port}/audio_query',
            params=params
        )
        
        # 音声合成を実施
        synthesis = requests.post(
            f'http://{host}:{port}/synthesis',
            headers = {"Content-Type": "application/json"},
            params = params,
            data = json.dumps(query.json())
        )
        
        # 音声データを一時ファイルに保存
        voice = synthesis.content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file.write(voice)
            temp_file_path = temp_file.name
        
        # aplayで音声再生（カード4のスピーカーを指定）
        try:
            subprocess.run(['aplay', '-D', 'plughw:4,0', temp_file_path], 
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
            print("音声再生完了")
        except:
            print("音声再生に失敗しました")
        
        # 一時ファイルを削除
        try:
            os.unlink(temp_file_path)
        except:
            pass
                
    except requests.exceptions.ConnectionError:
        print("Voicevoxを起動して下さい")
        return
    except Exception as e:
        print(f"エラー: {e}")
        return
    
if __name__ == "__main__":
    while True:
        text = input("ここに入力：")
        print("生成中")
        talk(text)
