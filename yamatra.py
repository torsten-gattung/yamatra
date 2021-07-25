#YAMaTra - Yet Another Mathe Trainer
# Created 2021 by Torsten Gattung
# Version 0.01
#########################################################################################

#active Google Voice for Voice Output
google_voice = True

import random
import datetime

#at the moment pandas is just use for some statistics
import pandas as pd

from mathe_test import Bruchrechnung, Multiplikation, Division

if google_voice:
    from gtts import gTTS
    import os
    from playsound import playsound
else:
    #import pyttsx3
    import espeakng
    # add your favorite tts here


class Trainer:
    def __init__(self, seconds = 10):
        self.name = ''
        self.punkte = 0
        self.trained = 0
        self.praises = ['Perfekt!', 'Super!', 'Gut gemacht!', 'Wow!', 'Toll!', 'Klasse!', 'Mathe-Ass!', 'Cool']
        self.curses = ['Witzbold', 'Scherzkeks']
        self.cursing = True
        self.train_start = None
        self.train_end = None
        self.max_time = datetime.timedelta(seconds=seconds)
        self.max_div_time = datetime.timedelta(seconds=2*seconds)
        self.max_versuche = 2

        if not google_voice:    
            try:
                #Enable if you have to use windows
                #engine = pyttsx3.init(driverName='sapi5') 
                #engine = pyttsx3.init(driverName='nsss')
                #self.engine = pyttsx3.init(driverName='espeak')
                #self.engine.setProperty('voice', self.engine.getProperty('voices')[0].id)
                self.engine = espeakng.Speaker()
                self.engine.voice = 'mb-de1'
            except Exception as error:
                print(error)
                print('No Voice Support found')
                self.engine = None


    def _say(self, text, lang='de'):
        print(text)
        if google_voice:
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save('voice.mp3')
            playsound('voice.mp3')
            #os.system("play voice.mp3 tempo 1.4")

            #Voice output - to disable this, set self.engine to none in constructor
        elif self.engine != None:
            self.engine.say(text)
            self.engine.runAndWait()
        
    def _praise(self):
        """ say something nice for good performance """
        i = random.randint(0, len(self.praises)-1)
        return self.praises[i]

    def _curse(self):
        """ some verbal indication of bad performance """
        if self.cursing:
            i = random.randint(0, len(self.curses)-1)
            return self.curses[i]
        return ""

    def identify(self):
        self._say('Wie heißt du?')
        self.name = input("Dein Name:")
        self._say(f"Hallo {self.name}!")
        self._say("Willkommen zum Training!")

    def save_score(self):
        with open('score.txt', 'a') as f:
            f.write(f"'{datetime.datetime.now()}', '{self.name}', {self.punkte}, {self.trained},  {self.punkte / self.trained}, '{self.train_duration}'\n")

    def train(self):        
        self._say('Gib "Stopp" ein, um das Training zu beenden')
        self.train_start = datetime.datetime.now()
        
        weiter = True
        while weiter:
            typ = random.randint(1,3)
            if typ == 1:
                task = Multiplikation()
            elif typ == 2:
                task = Division()
            elif typ == 3:
                task = Bruchrechnung()
            
            weiter = self.run_test(task)
            
        self.train_end = datetime.datetime.now()
        self.train_duration = self.train_end - self.train_start

        total_seconds = self.train_duration.total_seconds()
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)

        self._say(f"Du hast {minutes} Minuten und {seconds} Sekunden geübt und {self.punkte} Punkte in {self.trained} Versuchen erreicht!")
        self._say(f"{self._praise()}")
        self.save_score()  
 
    def run_test(self, test):
        self._say(test.question)
        start = datetime.datetime.now()
        versuch = 1
        dauer = datetime.timedelta(seconds=0)
        while versuch <= self.max_versuche:
            z = input(test.text)
            ende = datetime.datetime.now()
            dauer += ende - start
        
            if z == 'Stopp':
                return False
            else:
                self.trained += 1
                if test.ok(z):
                    punkte = test.get_points(dauer)
                    if punkte > 3:
                        self._say(f"{self._praise()}")
                        print("(4 Punkte)\n")
                    else:
                        self._say(f"{test.result}! Richtig!")
                        print(f"({punkte} Punkte)\n")
                    self.punkte+=punkte
                    return True
                else:
                    if versuch == 1:
                        self._say("Das ist leider falsch!")
                    else:
                        self._say(f"Das ist wieder falsch, {self._curse()}!")
                    versuch += 1
                    if versuch <= self.max_versuche:
                        self._say("Noch ein Versuch!")
                        test.punktabzug()
                    else:
                        print("Keine Punkte.")
                        self._say(f"Die richtige Antwort ist {test.result}\n")
                        return True
    
    def get_highscore(self):
        print("\n")
        self._say("Dies sind die fünf besten Übungen:")
        df = pd.read_csv('score.txt')
        df = df.sort_values('Punkte')
        print(df.tail())
        self._say("Tada!")
        
        #print(df.columns)

    def quit(self):
        self._say(f"Bis bald, {self.name}!")

if __name__=='__main__':
    t = Trainer()
    t.identify()
    t.train()
    t.get_highscore()
    t.quit()