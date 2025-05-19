import compSentence
import speech_recognition as sr
import os

threshold = 0.85

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
            
            compVal = compSentence.cosineScore(recognized_text, "動画を再生して")
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
