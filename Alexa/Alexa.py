import webbrowser
from time import ctime
from datetime import datetime
import os
import playsound
from gtts import gTTS
import random
import speech_recognition as sr
import firelink
import sys
import requests
import json
import pprint
import csv

class voice_assistant:

    recognizer = sr.Recognizer()
    notes = "notes.csv"

    
    def take_note(self):
        """
        Prompts the user to speak a note, records it, recognizes the speech, and saves it to a CSV file.
        
        The function repeatedly prompts the user to speak until a valid note is recognized. The recognized note is appended to the notes.csv file.
        """
        self.speak('قل ملاحظتك','ar')
        while True:
            print("Start speaking...")
            audio_data = self.record_audio()
            print("Recognizing speech...")
            recognized_text = self.recognize_speech(audio_data)
            if recognized_text:  # If recognizer successfully understood the speech
                with open(self.notes, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow([recognized_text])  
                break  # Exit the loop once a valid note is recorded


    def delete_note(self):
        """
        Reads all notes, prompts the user to choose a note to delete by its number, and deletes the selected note.
        
        The function first reads all notes and speaks them out. It then prompts the user to choose a note number to delete. The chosen note is deleted from the notes.csv file.
        """
        self.read_notes()
        if os.path.exists(self.notes):
            self.speak('اختر رقم الملاحظة التي تريد حذفها', 'ar')
            while True:
                print("Choose the number of the note you want to delete...")
                audio_data = self.record_audio()
                print("Recognizing speech...")
                recognized_text = self.recognize_speech(audio_data)

                if recognized_text.isdigit():
                    note_number = int(recognized_text)
                    with open(self.notes, 'r') as csvfile:
                        notes = list(csv.reader(csvfile))

                    if 1 <= note_number <= len(notes):
                        del notes[note_number - 1]
                        with open(self.notes, 'w', newline='') as csvfile:
                            csvwriter = csv.writer(csvfile)
                            csvwriter.writerows(notes)
                        self.speak('تم حذف الملاحظة', 'ar')
                        print("Note deleted.")
                        break  # Exit the loop once the note is deleted
                    else:
                        self.speak('رقم غير صالح. حاول مرة أخرى.', 'ar')
                        print("Invalid number. Please try again.")
                else:
                    self.speak('رقم غير صالح. حاول مرة أخرى.', 'ar')
                    print("Invalid number. Please try again.")
        else:
            self.speak('لا توجد ملاحظات لحذفها', 'ar')
            print("No notes to delete.")



    def read_notes(self):
        """
        Reads and speaks all saved notes from the notes.csv file.
        
        The function reads all notes from the notes.csv file and speaks each note along with its number. If no notes are found, it informs the user.
        """
        if os.path.exists(self.notes):
            self.speak('هذه ملاحظاتك', 'ar')
            with open(self.notes, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for i, row in enumerate(csvreader, start=1):
                    note = ', '.join(row).strip()  # Remove any leading/trailing whitespace
                    if note:  # Check if the note is not empty
                        print(f"{i}: {note}")
                        self.speak(f"{i}: {note}", 'ar')
        else:
            self.speak('لا توجد ملاحظات بعد', 'ar')
            print("No notes yet.")


    def delete_all_notes(self):
        """
        Deletes all notes by clearing the contents of the CSV file.
        """
        if os.path.exists(self.notes):
            with open(self.notes, 'w', newline='') as csvfile:
                csvfile.truncate()  # Clear the contents of the file
            self.speak('تم حذف جميع الملاحظات', 'ar')
            print("All notes deleted.")
        else:
            self.speak('لا توجد ملاحظات لحذفها', 'ar')
            print("No notes to delete.")



    def get_weather(self):
        """
        Retrieves current weather information from OpenWeatherMap API for Cairo.
    
        Uses latitude and longitude coordinates for Cairo, Egypt.
        Displays temperature, 'feels like' temperature, and weather conditions.
    
        API Key: Replace '147a96c172c30c411af5cb1c24236853' with your own OpenWeatherMap API key.
    
        Returns:
        None. Outputs weather information using self.speak() method.
        If unable to fetch data (status code other than 200), returns an error message.
        """

        api_key='147a96c172c30c411af5cb1c24236853'
        lat=30.0444
        lon=31.2357
        url=f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)  # Parse JSON response
            pprint.pprint(data)
            temp = data["main"]["temp"] - 273.15  # Convert Kelvin to Celsius
            feelsliketemp=data["main"]["feels_like"] - 273.15
            conditions = data["weather"][0]["description"]
            self.speak(f"In Cairo, the temperature is {temp:.2f} degrees Celsius, It feels {feelsliketemp:.2f} and it's {conditions}.",'en')
        else:
            return "Sorry, couldn't get weather information."
        

    def record_audio(self):
        """
        Records audio from the microphone.
        """
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        return audio


    def recognize_speech(self, audio):
        """
        Converts recorded audio into text using Google's Speech Recognition API.
        
        Parameters:
        audio (AudioData): Audio data captured from record_audio().
        
        Returns:
        string: Recognized text from the audio input.
        """
        text = ""
        try:
            # Try recognizing in Arabic first
            text = self.recognizer.recognize_google(audio, language="ar-EG")
            print(f"You said (Arabic): {text[::-1]}")
        except sr.UnknownValueError:
            # If recognition in Arabic fails, try recognizing in English
            try:
                text = self.recognizer.recognize_google(audio, language="en-US")
                print(f"You said (English): {text}")
            except sr.UnknownValueError:
                self.speak('عذرًا، لم أفهم. حاول مرة أخرى.', 'ar')
                print("Sorry, I couldn't understand that.")
            except sr.RequestError:
                print("Sorry, there was an error processing your request.")
        except sr.RequestError:
            print("Sorry, there was an error processing your request.")
        
        return text




    def speak(self, text,language):
        """
        Converts text into speech using Google Text-to-Speech (gTTS) and plays the generated speech.
        
        Parameters:
        text (string): Text to be spoken aloud.
        """
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save("audio.mp3")
        playsound.playsound("audio.mp3")


    def open_link(self):
        """
        Prompts the user to choose a website to open (Facebook, Google, YouTube, Twitter) and opens it in a web browser.
        """
        websites = {
            "فيسبوك": firelink.facebook_link,
            "جوجل": firelink.google_link,
            "يوتيوب": firelink.youtube_link,
            "تويتر": firelink.twitter_link
                }
    
        while True:
            self.speak('اختار الموقع','ar')
            print("Say the website name...")
            audio_data = self.record_audio()
            print("Recognizing speech...")
            text = self.recognize_speech(audio_data)
            if text in websites:
                url = websites[text]
                firelink.firefox(url)
                break  # Exit the loop once a valid website is recognized



    def get_current_time(self):
        """
        Retrieves and speaks the current time in "HH:MM:SS" format.
        """
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time)
        self.speak(current_time,'ar')


    def greeting(self, text):
        """
        Responds with a greeting based on recognized text input.
        
        Parameters:
        text (string): Recognized text input.
        """
        if text in ['صباح الخير', 'صباح الفل', 'صباح النور']:
            self.speak('صباح النور','ar')
        elif text in ['مساء الخير', 'مساء الفل', 'مساء النور']:
            self.speak('مساء النور','ar')
        else:
            self.speak('اهلا','ar')


    def start_alexa(self):
        """
        Main function for the voice assistant, handling different recognized commands.
        """
        print("Say something...")
        audio_data = self.record_audio()
        print("Recognizing speech...")
        recognized_text = self.recognize_speech(audio_data)
        if recognized_text in ['صباح الخير', 'صباح الفل', 'صباح النور', 'مساء الخير', 'مساء الفل', 'مساء النور', 'اهلا', 'هاي', 'هالو']:
            self.greeting(recognized_text)
        elif recognized_text in ["الوقت", "الساعة كام", "ساعة", "الساعة"]:
            self.get_current_time()
        elif recognized_text in ["موقع", "افتحي موقع","افتحي موقع", "ويب سايت"]:
            self.open_link()
        elif recognized_text in ["الطقس","طقس","الحرارة","درجة الحرارة"]:
            self.get_weather()
        elif recognized_text in ["ملاحظة","ملاحظه","note"]:
            self.take_note()
        elif recognized_text in ["امسح ملاحظة","امسح ملاحظه","delete note"]:
            self.delete_note()
        elif recognized_text in ["my notes","ملاحظاتي","ملاحظات"]:
            self.read_notes()
        elif recognized_text in ["امسح كل الملاحظات", "delete all notes"]:
            self.delete_all_notes()
        elif recognized_text in ["اقفل", "اقفلي", "close", "اطفي"]:
            sys.exit()







if __name__ == "__main__":
    assistant = voice_assistant()
    while True:
        assistant.start_alexa()

    

