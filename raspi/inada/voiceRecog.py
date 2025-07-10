import speech_recognition as sr

def voice2text():
    r = sr.Recognizer()
    text = "すみません、聞き取れませんでした。"
    with sr.Microphone(sample_rate=16_000) as source:
        print("聞き取り中")
        audio = r.listen(source)
        print("音声を取得しました")
    try:
        recognized_text = r.recognize_google(audio, language='ja-JP')
        print(recognized_text)
        text = recognized_text
    except sr.exceptions.UnknownValueError:
        print("すみません、聞き取れませんでした。")
        
    return text

if __name__ == "__main__":
    voice2text()