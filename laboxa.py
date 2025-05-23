from sentence_transformers import SentenceTransformer, util
import speech_recognition as sr
import os

threshold = 0.85
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
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("話しかけてください...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                
            recognized_text = r.recognize_google(audio, language='ja-JP')
            print("認識結果:", recognized_text)
            
            compVal = cosineScore(recognized_text, "動画を再生して")
            print("類似度スコア:", compVal)
            
            if compVal.item() >= threshold:
                video_path = os.path.expanduser("~/Downloads/01.mp4")
                os.system(f"ffplay '{video_path}'")
        
        except sr.UnknownValueError:
            print("聞き取れませんでした")
        except sr.WaitTimeoutError:
            print("時間内に話されませんでした")
        except Exception as e:
            print("エラー:", e)

if __name__ == "__main__":
    main()
