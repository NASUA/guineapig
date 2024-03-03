import os
import speech_recognition as sr
from gtts import gTTS
import openai
import pygame
import tempfile

# Initialize the recognizer
r = sr.Recognizer()

# Set your OpenAI API key here
openai.api_key = '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'

def listen_and_respond():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")
        # Listen for the first phrase and extract it into audio data
        audio_data = r.listen(source)
        try:
            # Recognize speech using Google Web Speech API
            text = r.recognize_google(audio_data)
            print("You said: " + text)

            # Generate response using OpenAI (simplified for example)
            response = openai.Completion.create(
              engine="text-davinci-003",
              prompt="Say something friendly in Spanish in response to: " + text,
              temperature=0.5,
              max_tokens=60,
              top_p=1.0,
              frequency_penalty=0.0,
              presence_penalty=0.0
            )

            response_text = response.choices[0].text.strip()
            print("AI Response: " + response_text)

            # Convert the response to speech
            tts = gTTS(response_text, lang='es')
            with tempfile.NamedTemporaryFile(delete=True) as fp:
                tts.save(f"{fp.name}.mp3")
                # Play the response
                pygame.mixer.init()
                pygame.mixer.music.load(f"{fp.name}.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():  # wait for audio to finish playing
                    continue

        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    listen_and_respond()
