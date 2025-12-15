from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
from nltk.stem.lancaster import LancasterStemmer
from googletrans import Translator
import speech_recognition as sr
from tkinter import *
from gtts import gTTS
import webbrowser
import wikipedia
import datetime
import warnings
import calendar
import smtplib
import asyncio
import random
import pickle
import numpy
import json
import nltk
import os

root = Tk()
selected_lang_var = "en"
root.geometry("{0}x{1}+1+1".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.minsize("200", "200")
root.configure(bg="#1e243d")
root.title("Crystal AI")

set_set_set = False
selected_lang_var = str(selected_lang_var)


def lang_back_func():
    directions.pack_forget()
    enter_text.pack_forget()
    submit_button.pack_forget()
    back_button.pack_forget()
    selected_lang.pack_forget()
    label_2.pack_forget()
    crystal_speech.pack_forget()
    time_l.pack_forget()
    settings.pack_forget()
    language.pack(pady=15, side=BOTTOM)
    gender.pack(pady=15, side=BOTTOM)
    color.pack(pady=15, side=BOTTOM)
    assis_name.pack(pady=15, side=BOTTOM)
    appearance.pack(pady=15, side=BOTTOM)
    people.pack(pady=15, side=BOTTOM)
    phrase.pack(pady=15, side=BOTTOM)
    back.pack(pady=20, side=BOTTOM)


def lang_func():
    global directions
    global enter_text
    global submit_button
    global back_button
    language.pack_forget()
    gender.pack_forget()
    color.pack_forget()
    assis_name.pack_forget()
    appearance.pack_forget()
    people.pack_forget()
    phrase.pack_forget()
    back.pack_forget()
    directions = Label(text="Enter the language code for the language that you speak", bg='#1e243d',
                       fg="white", font="comicsansms 20 bold", pady=15)
    directions.pack(side=TOP, anchor="w", padx=25)
    enter_text = Entry(root, width=50, bg="grey", font="comicsansms 20 bold")
    enter_text.pack(side=TOP, anchor="w", padx=25)
    back_button = Button(text="Back", fg="black", font="comicsansms 15 bold", pady=20, command=lang_back_func)
    back_button.pack(side=BOTTOM, anchor="w", padx=25)

    def submit():
        global selected_lang_var
        global selected_lang
        selected_lang = Label(text="Your language: "+enter_text.get(), bg='#1e243d', fg="white",
                              font="comicsansms 20 bold", pady=20)
        selected_lang.pack(side=TOP, anchor="w", padx=25)
        if enter_text.get() != "":
            selected_lang_var = enter_text.get()
        submit_button['state'] = DISABLED
    submit_button = Button(text="SUBMIT", bg='#1e243d', fg="black", font="comicsansms 20 bold", command=submit)
    submit_button.pack(pady=15, padx=25, side=TOP, anchor="w")


def home_func():
    global set_set_set
    language.pack_forget()
    gender.pack_forget()
    color.pack_forget()
    assis_name.pack_forget()
    appearance.pack_forget()
    people.pack_forget()
    phrase.pack_forget()
    back.pack_forget()
    label_2.pack(fill=X, pady=10, side=BOTTOM)
    crystal_speech.pack(pady=15, side=BOTTOM)
    time_l.pack(anchor="w", side=TOP)
    settings.pack(anchor="se", pady=1, padx=1)
    set_set_set = False


def set_func():
    global set_set_set
    global language
    global gender
    global color
    global assis_name
    global appearance
    global people
    global phrase
    global back
    label_2.pack_forget()
    crystal_speech.pack_forget()
    time_l.pack_forget()
    settings.pack_forget()
    language = Button(text="LANGUAGE", bg='#1e243d', fg="black", font="comicsansms 25 bold", pady=20, padx=500,
                      command=lang_func)
    language.pack(pady=15, side=BOTTOM)
    gender = Button(text="GENDER", bg='#1e243d', fg="black", font="comicsansms 25 bold", pady=20, padx=515)
    gender.pack(pady=15, side=BOTTOM)
    color = Button(text="COLOR", bg='#1e243d', fg="black", font="comicsansms 25 bold", pady=20, padx=520)
    color.pack(pady=15, side=BOTTOM)
    assis_name = Button(text="NAME", bg='#1e243d', fg="black", font="comicsansms 25 bold", pady=20, padx=525)
    assis_name.pack(pady=15, side=BOTTOM)
    appearance = Button(text="APPEARANCE", bg='#1e243d', fg="black", font="comicsansms 25 bold", pady=20, padx=480)
    appearance.pack(pady=15, side=BOTTOM)
    people = Button(text="PEOPLE", bg='#1e243d', fg="black", font="comicsansms 25 bold", pady=20, padx=515)
    people.pack(pady=15, side=BOTTOM)
    phrase = Button(text="WISH PHRASE", bg='#1e243d', fg="black", font="comicsansms 25 bold", pady=20, padx=477)
    phrase.pack(pady=15, side=BOTTOM)
    back = Button(text="BACK", bg='red', fg="black", font="comicsansms 15 bold", pady=20, command=home_func)
    back.pack(pady=20, side=BOTTOM)
    set_set_set = True


label_2 = Label(text="You said:", bg='#1e243d', fg="green", font="comicsansms 20 bold")
label_2.pack(fill=X, pady=10, side=BOTTOM)
crystal_speech = Label(text="Hello!", bg='#1e243d', fg="white", font="comicsansms 25 bold")
crystal_speech.pack(pady=15, side=BOTTOM)
time_l = Label(text="", bg='#1e243d', fg="yellow", font="comicsansms 25 bold")
time_l.pack(anchor="w", side=TOP)
settings_image = PhotoImage(file="New settings.png")
settings = Button(image=settings_image, anchor="se", command=set_func)
settings.pack(anchor="se", pady=1, padx=1)

stemmer = LancasterStemmer()

warnings.filterwarnings('ignore')
first = "Vatsal"
last = "Dutt"


def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('vatdut8994@gmail.com', '')
    server.sendmail('vatdut8994@nrms.org', to, content)
    server.close()


def get_date():
    today = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    month_num = today.month
    day_num = today.day

    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']

    ordinal_numbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th',
                       '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21th', '22th', '23th', '24th', '25th',
                       '26th', '27th', '28th', '29th', '30th', '31th']

    return 'Today  is ' + weekday + ' ' + month_names[month_num - 1] + ' the ' + ordinal_numbers[day_num - 1] + '. '


async def assis_trans(sen):
    async with Translator() as translator:
        translate_text = await translator.translate(sen, src='en', dest=selected_lang_var)
        print(translate_text.text)
    return translate_text.text


def speak_female(audio):
    crystal_speech['text'] = audio
    print(audio)

    audio = asyncio.run(assis_trans(audio))
    print(audio)

    my_obj = gTTS(text=audio, lang=selected_lang_var, slow=False)
    my_obj.save('audio.wav')
    os.system('mpg123 audio.wav')
    os.remove('audio.wav')


print(selected_lang_var)


def command():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        print("Recognizing...")
    dt = ''
    try:
        dt = r.recognize_google(audio, language=selected_lang_var)
        label_2['text'] = "You said: " + dt
        print("You said: " + dt)

    except sr.UnknownValueError:
        crystal_speech['text'] = "Sorry, I could not understand that try saying it again"
        print("Sorry, I could not understand that try saying it again")

    except sr.RequestError:
        crystal_speech['text'] = "Request results from Google Speech Recognition service error"
        print("Request results from Google Speech Recognition service error")

    english = asyncio.run(translate(dt))
    print(english)
    return english


async def translate(sen):
    async with Translator() as translator:
        translate_text = await translator.translate(sen, src=selected_lang_var, dest='en')
        print(translate_text.text)
    return translate_text.text


def intro():
    speak("I am Crystal how may I help you?")


def wish_me():
    hr = int(datetime.datetime.now().hour)
    if 0 < hr < 12:
        speak("Good Morning Sir " + first + "!")

    elif 12 <= hr <= 16:
        speak("Good Afternoon Sir " + first + "!")

    else:
        speak("Good Evening Sir " + first + "!")
    intro()


def wake_word(word):
    wake_words = ['crystal', 'dude']

    word = word.lower()

    for phrase in wake_words:
        if phrase in word:
            return True

    return False


speak = speak_female

sorry_list = ["I am sorry, I could not understand that",
              "I am not sure I understand that",
              "I am sorry, I don't get that"]

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

except RuntimeError:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

training = numpy.array(training)
output = numpy.array(output)

with open("data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)

model = Sequential()
model.add(Dense(8, input_shape=(len(training[0]),), activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(len(output[0]), activation='softmax'))

optimizer = SGD(learning_rate=0.01, momentum=0.9)
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

model_file = "model.keras.weights.h5"

if os.path.exists(model_file):
    model.load_weights(model_file)
else:
    model.fit(training, output, epochs=1000, batch_size=8, verbose=1)
    model.save_weights(model_file)



def bag_of_words(s, wd):
    bgw = [0 for _ in range(len(wd))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(wd):
            if w == se:
                bgw[i] = 1

    return numpy.array(bgw)


wish_me()


def chat():
    if set_set_set is False:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        if now.hour > 12:
            meridian = 'P.M'
            hour = hour - 12
        else:
            meridian = 'A.M'

        if len(str(minute)) != 2:
            minute = "0" + str(minute)

        hour = str(hour)
        minute = str(minute)
        time_l['text'] = hour + ":" + minute + " " + meridian
        response = ''
        inp = command()
        inp = inp.lower()
        inp2 = inp
        bow = bag_of_words(inp, words)
        bow = bow.reshape(1, -1)
        results = model.predict(bow)[0]

        results_index = numpy.argmax(results)
        tag = labels[int(results_index)]

        if results[results_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
                    response = random.choice(responses)

        elif inp == "":
            print("")

        else:
            response = response + random.choice(sorry_list)

        if inp == "quit":
            quit()

        if tag == "web-opener":
            name = inp
            name = name.replace("open", "")
            name = name.replace("website", "")
            name = name.replace("the", "")
            name = name.lower()

            if name == "youtube":
                webbrowser.open("https://www.youtube.com")

            elif name == "google":
                webbrowser.open("https://www.google.com")

            elif name == "rapid identity":
                webbrowser.open("https://my.ncedcloud.org/portal/p/applications")

            elif name == "stackoverflow":
                webbrowser.open("https://www.stackoverflow.com")
        if tag == "emailMom":
            try:
                print("What should I say to mom")
                speak("What should I say to mom")
                content = inp
                to = "gdatt22@gmail.com"
                send_email(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Sir the could not be sent")

        if tag == "internet":
            try:
                inp = inp.replace("what", "")
                inp = inp.replace("is", "")
                inp = inp.lower().replace("crystal", "")
                results = wikipedia.summary(inp, sentences=2)
                response = response + 'According to the wikipedia: ' + results
            except wikipedia.exceptions.PageError:
                new = 2
                tab_url = "http://www.google.com/search?q="
                term = inp2
                term = term.replace("search", "")
                term = term.lower().replace("crystal", "")
                term = term.replace(" ", "+")
                webbrowser.open(tab_url + term, new=new)
                response = response + "Here are your results "
            except wikipedia.exceptions.DisambiguationError:
                new = 2
                tab_url = "http://www.google.com/search?q="
                term = inp2
                term = term.replace("search", "")
                term = term.lower().replace("crystal", "")
                term = term.replace(" ", "+")
                webbrowser.open(tab_url + term, new=new)
                response = response + "Here are your results "

        try:
            crystal_speech['text'] = response
            speak(response)

        except AssertionError:
            crystal_speech['text'] = ""

            crystal_speech['text'] = ""
            print("")

        if crystal_speech['text'] == "":
            print("")

        elif len(crystal_speech['text']) >= 500:
            crystal_speech['text'] = crystal_speech['text'][0:100] + '\n' + crystal_speech['text'][100:200] \
                                     + '\n' + crystal_speech['text'][200:300] + '\n' + crystal_speech['text'][300:400] \
                                     + '\n' + crystal_speech['text'][400:500] + '\n' + crystal_speech['text'][500:601]

        elif 500 >= len(crystal_speech['text']) >= 400:
            crystal_speech['text'] = crystal_speech['text'][0:100] + '\n' + crystal_speech['text'][100:200] \
                                     + '\n' + crystal_speech['text'][200:300] + '\n' + crystal_speech['text'][300:400] \
                                     + '\n' + crystal_speech['text'][400:501]

        elif 400 >= len(crystal_speech['text']) >= 300:
            crystal_speech['text'] = crystal_speech['text'][0:100] + '\n' + crystal_speech['text'][100:200] \
                                     + '\n' + crystal_speech['text'][200:300] + '\n' + crystal_speech['text'][300:401]

        elif 300 >= len(crystal_speech['text']) >= 200:
            crystal_speech['text'] = crystal_speech['text'][0:100] + '\n' + crystal_speech['text'][100:200] \
                                     + '\n' + crystal_speech['text'][200:301]

        elif 100 >= len(crystal_speech['text']) >= 100:
            crystal_speech['text'] = crystal_speech['text'][0:100] + '\n' + crystal_speech['text'][100:200]
    root.after(1000, chat)


root.after(1000, chat)
root.mainloop()
