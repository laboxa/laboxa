import zunda
import speech_recognition as sr
import os

b = False
def voice():
    while True:
        r = sr.Recognizer()
        text = "聞き取れなかったのだ"
        zunda.talk("何か話して欲しいのだ")
        print("何か話して欲しいのだ")
        with sr.Microphone(sample_rate=16_000) as source:
            audio = r.listen(source)
            # print("音声を取得しました")
        try:
            recognized_text = r.recognize_google(audio, language='ja-JP')
            print(recognized_text)
            text = recognized_text
            
            if text == "終了":
                break
            elif text == "フォルダを開く":
                os.system("open .")
            elif text == "動画を再生":
                os.system("ffplay /Users/inadajiei/Movies/リコリス素材/op.mp4")
            elif text == "残酷な天使のテーゼを再生":
                os.system("ffplay /Users/inadajiei/Movies/EVA/eva_op.mp4")
                
            zunda.talk(text)
        except sr.exceptions.UnknownValueError:
            print("聞き取れなかったのだ")
            zunda.talk(text)    
    
    zunda.talk("了解なのだ！")        
    
if __name__ == "__main__":
    voice()