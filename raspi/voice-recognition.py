import asyncio
from sentence_transformers import SentenceTransformer, util
import speech_recognition as sr
import switchBot
import zunda

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
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("話しかけてください...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                
            recognized_text = r.recognize_google(audio, language='ja-JP')
            print("認識結果:", recognized_text)
            
            compVal = cosineScore(recognized_text, "電気をつけて")
            print("類似度スコア:", compVal)
            
            if compVal.item() >= threshold:
                zunda.talk("電気をつけます")
                #asyncio.run(switchBot.switchBot("4AA55C06-2EDF-0880-5492-C1374C880086"))
                asyncio.run(switchBot.switchBot())
        
        except sr.UnknownValueError:
            print("聞き取れませんでした")
            zunda.talk("よく聞き取れませんでした")
        except sr.WaitTimeoutError:
            print("時間内に話されませんでした")
            zunda.talk("よく聞き取れませんでした")
        except Exception as e:
            print("エラー:", e)

if __name__ == "__main__":
    main()
