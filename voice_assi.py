import webbrowser
import pyttsx3
import speech_recognition as sr
import musicLibrary
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "09cfade1e84c4d3e9046b852b6857034"

# This function will speak any text whenever we call this function

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiprocess(command):
    client = OpenAI(api_key='sk-proj-79CAt5YBQpJOPzh3SYKcT3BlbkFJHt2PeyOOaXYUz4PTKElE')
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role':'system','content':'You are a virtual assistant named Devansh skilled in general tasks like Alexa and Google cloud'},
            {'role':'user','content':command }
        ]
    )
    return completion.choices[0].message.content

def processCommand(c):

    # Opening any app in webbrowse
    if "open google" in c.lower():  
        speak("Opening Google")
        webbrowser.open('https://google.com')

    elif "open facebook" in c.lower():
        speak("Opening Facebbok")
        webbrowser.open('https://facebook.com')
    
    elif "open youtube" in c.lower():
        speak("Opening Youtube")
        webbrowser.open('https://youtube.com')
    
    elif "open linkedin" in c.lower():
        speak("Opening Linkedin")
        webbrowser.open('https://linkedin.com')
    
    elif c.lower().startswith('play'):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif 'how are you' in c.lower():
        speak("I am fine! What about you")

    elif 'good morning' in c.lower():
        speak("Good morning! Have a nice day")

    elif 'good afternoon' in c.lower():
        speak("good afternoon")

    elif 'good night' in c.lower():
        speak("Good night! Sweet dreams")
    
    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=09cfade1e84c4d3e9046b852b6857034")
        if r.status_code == 200:
            data = r.json()

            articles = data.get('articles',[])

            for article in articles:
                speak(article['title'])
    
    # else:
    #     # OpenAI will handle now
    #     output = aiprocess(c)
    #     speak(output)


if __name__ == "__main__":
    speak("Initializing Devansh...")

    while True:
        # First activate by "Devansh"
        # Get audio from the User
        r = sr.Recognizer()
        
        # Recognize the user's speech 
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)

            word = r.recognize_google(audio)
            if(word.lower() == 'devansh'):
                speak("Ya")
                
            # Listen for command
                with sr.Microphone() as source:
                    print("Devansh activated...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    
                    processCommand(command)

        except Exception as e:
            print(f"Error : {e}")
