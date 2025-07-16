import asyncio
from sentence_transformers import SentenceTransformer, util
import speech_recognition as sr
import switchBot
import zunda
import subprocess

threshold = 0.75
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def cosineScore(text1, text2):
    # 文章をベクトルに変換
    embeddings1 = model.encode(text1, convert_to_tensor=True)
    embeddings2 = model.encode(text2, convert_to_tensor=True)

    # コサイン類似度の計算
    cosine_score = util.pytorch_cos_sim(embeddings1, embeddings2)[0][0]
    
    return cosine_score

def main():
    r = sr.Recognizer()
    
    # マイクデバイスの確認
    print("利用可能なマイクデバイス:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  デバイス {index}: {name}")
    
    try:
        # デフォルトマイクをテスト
        with sr.Microphone(device_index=2) as source:
            print("マイクデバイスの初期化に成功しました")
    except Exception as e:
        print(f"マイクデバイスの初期化に失敗: {e}")
        return
    
    while True:
        # try:
        #     with sr.Microphone() as source:
        #         r.adjust_for_ambient_noise(source)
        #         print("話しかけてください...")
        #         audio = r.listen(source, timeout=5, phrase_time_limit=5)
                
        #     recognized_text = r.recognize_google(audio, language='ja-JP')
        #     print("認識結果:", recognized_text)
            
        #     if recognized_text == "ラボ草":
        #         print("ok")
        #         zunda.talk("はい")
        
        # except sr.UnknownValueError:
        #     print("聞き取れませんでした")
        #     zunda.talk("よく聞き取れませんでした")
        #     continue
        # except sr.WaitTimeoutError:
        #     print("時間内に話されませんでした")
        #     zunda.talk("よく聞き取れませんでした")
        #     continue
        # except Exception as e:
        #     print("エラー:", e)
        #     continue
        
        try:
            with sr.Microphone(device_index=2) as source:  # デバイス番号を指定
                r.adjust_for_ambient_noise(source)
                print("話しかけてください...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                
            recognized_text = r.recognize_google(audio, language='ja-JP')
            print("認識結果:", recognized_text)
            
            compVal = cosineScore(recognized_text, "電気をつけて")
            print("類似度スコア:", compVal)
            
            if compVal.item() >= threshold:
                subprocess.run(['aplay', '-D', 'plughw:4,0', 'pi.wav'])
                zunda.talk("電気をつけます")
                #asyncio.run(switchBot.switchBot("4AA55C06-2EDF-0880-5492-C1374C880086"))
                asyncio.run(switchBot.switchBot())
            
            if cosineScore(recognized_text, "自己紹介してください") >= threshold:
                subprocess.run(['aplay', '-D', 'plughw:4,0', 'pi.wav'])
                zunda.talk("私は音声アシスタント，ラボ草です")
        
        except sr.UnknownValueError:
            print("聞き取れませんでした")
            #zunda.talk("よく聞き取れませんでした")
        except sr.WaitTimeoutError:
            print("時間内に話されませんでした")
            #zunda.talk("よく聞き取れませんでした")
        except OSError as e:
            print(f"マイクデバイスエラー: {e}")
            print("マイクが接続されているか、権限があるかを確認してください")
            break
        except Exception as e:
            print("エラー:", e)
            print(f"エラータイプ: {type(e).__name__}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
