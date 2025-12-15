from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
from selenium.webdriver.chrome.service import Service
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from nltk.stem.lancaster import LancasterStemmer
from PyQt5 import QtCore, QtGui
from googletrans import Translator
from PyQt5.QtPrintSupport import * 
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
from Desktop import Ui_MainWindow
import speech_recognition as sr
from functools import lru_cache
from selenium import webdriver
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
import face_recognition
from gtts import gTTS
import datetime
import warnings
import requests
import pyttsx3
import asyncio
import smtplib
import random
import pickle
import numpy
import random
import json
import nltk
import sys
import cv2
import os

# nltk.download('punkt')

response = ""

selected_lang_var = open("lang.txt", 'r').read()

stemmer = LancasterStemmer()


warnings.filterwarnings('ignore')
first = "Vatsal"
last = "Dutt"


@lru_cache(maxsize=10)
def web_scrapper(input_data_to_search):
    page_url = 'https://www.google.com/search?q=' + input_data_to_search
    source = requests.get(page_url).text
    soup = BeautifulSoup(source, 'html.parser')
    part_of_speeches = ['noun', 'adjective', 'verb', 'adverb', 'pronoun', 'preposition', 'conjunction', 'interjection', 'exclamation', 'numeral', 'article', 'determiner']

    list1 = []

    for i in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
        for j in i.find_all('div', class_='BNeawe s3v9rd AP7Wnd'):
            list1.append(j.text)
    
    try:
        return soup.find('div', class_='BNeawe iBp4i AP7Wnd').text
    except:
        pass

    if list1[0].split()[0] in part_of_speeches:
        if list1[0].split()[0][0] == "a":
            return 'As an '+list1[0].split()[0]+' it means '+list1[1]
        
        else:
            return 'As a '+list1[0].split()[0]+' it means '+list1[1]
    
    answer_types = ['You would say that ', 'That would be ', "That's "]
    for i in soup.find_all('div'):
        for j in i.find_all('div'):
            for k in j.find_all('div'):
                for m in k.find_all('div'):
                    if 'MUxGbd u31kKd gsrt lyLwlc' in str(m):
                        translation = str(m.text).replace('Translation', '').replace('Translate', '')
    try:
        return random.choice(answer_types) + translation
    
    except:
        pass
    
    try:
        PATH = "D:/chromedriver.exe"
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(options=op, service=Service(PATH))
        driver.get(page_url)
        algebra_result = driver.find_elements_by_class_name('LPBLxf')
        return algebra_result[-1].text.split('\n')[-1]
    except:
        pass

    if "Duration" not in list1[0]:
        if len(list1[0].split()) > 10:
            try:
                return list1[0].split('...')[0].split("·")[1]
            
            except:
                return list1[0].split('...')[0]
            

    for text in list1:
        list_text = text.split()
        if len(list_text) != 0:
            if list_text[-1] == 'Wikipedia':
                return 'According to the Wikipedia, '+str('/'.join(text.split()[0:-1]).replace('/', ' '))
    urls = []
    for a in soup.find_all('a'):
        if a.get('href')[0:15] == '/url?q=https://':
            url = a.get('href').replace('/url?q=https://', '')
            urls.append(url[0: url.index('&sa')])
    
    for u in range(len(urls)):
        urls[u] = 'https://'+urls[u]

    url_source = requests.get(urls[0]).text
    soup = BeautifulSoup(url_source, 'html.parser')
    url_text = []
    for i in soup.find_all("p"):
        url_text.append(i.text)

    paracount = 0
    for j in url_text:
        if len(j.split()) < 11:
            pass
        
        elif paracount == 1:
            return "According to the website "+urls[0].split('/')[2]+", "+j.split("\r\n\r")[0]

        else:
            paracount += 1

def speak_female_better(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 160)
    engine.say(audio)
    engine.runAndWait()

def speak_female(audio):
    if selected_lang_var == 'en':
        print(str(audio))
    else:
        print(str(audio))
        audio = asyncio.run(assis_trans(audio))
        print(str(audio))
    my_obj = gTTS(text=audio, lang=selected_lang_var, slow=False)
    my_obj.save('audio.mp3')
    os.system('mpg123 audio.mp3')
    os.remove('audio.mp3')


speak = speak_female

async def assis_trans(sen):
    try:
        async with Translator() as translator:
            result = await translator.translate(
                sen,
                src='en',
                dest=selected_lang_var
            )
        return result.text
    except Exception as e:
        print("Translation error (assistant):", e)
        return sen



async def translate(sen):
    try:
        async with Translator() as translator:
            result = await translator.translate(
                sen,
                src=selected_lang_var,
                dest='en'
            )
        return result.text
    except Exception as e:
        print("Translation error (assistant):", e)
        return sen



def intro():
    speak("I am Crystal how may I help you?")


def wish_me(person):
    hr = int(datetime.datetime.now().hour)
    if 0 < hr < 12:
        speak("Good Morning " + person.lower().title() + "!")

    elif 12 <= hr <= 16:
        speak("Good Afternoon " + person.lower().title() + "!")

    else:
        speak("Good Evening " + person.lower().title() + "!")
    intro()


def wake_word(word):
    wake_words = ['crystal', 'dude']

    word = word.lower()

    for phr in wake_words:
        if phr in word:
            return True

    return False

sorry_list = ["I am sorry, I could not understand that",
              "I am not sure I understand that",
              "I am sorry, I don't get that"]

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
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
model.compile(
    loss='categorical_crossentropy',
    optimizer=optimizer,
    metrics=['accuracy']
)

model_file = "model.keras.weights.h5"

if os.path.exists(model_file):
    model.load_weights(model_file)
else:
    model.fit(training, output, epochs=1000, batch_size=8, verbose=1)
    model.save_weights(model_file)


def bag_of_words(s, wrd):
    bag2 = [0 for _ in range(len(wrd))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(wrd):
            if w == se:
                bag2[i] = 1

    return numpy.array(bag2)



class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()
    
    def run(self):
        self.chat()
    
    def command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            print("Recognizing...")
        dt = ''
        try:
            dt = r.recognize_google(audio, language=selected_lang_var)
            print("You said: " + dt)

        except sr.UnknownValueError:
            pass

        except sr.RequestError:
            print("Request results from Google Speech Recognition service error")

        english = asyncio.run(translate(dt))
        print(english)
        return english


    def chat(self):
        global face_rec
        path = 'img/known/'
        images = []
        classNames = []
        myList = os.listdir(path)

        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])

        cap = cv2.VideoCapture(0)
        name = ''

        with open('face_rec', 'rb') as file:
            encodeListKnown = pickle.load(file)

        while name == '':
            success, img = cap.read()
            if img is None:
                print('Wrong Image Path')
                exit()
            img = cv2.flip(img, 2)
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                print(faceDis)
                matchIndex = numpy.argmin(faceDis)

                if (
                    matchIndex < len(classNames)
                    and matches[matchIndex]
                    and faceDis[matchIndex] < 0.6
                ):
                    name = classNames[matchIndex].upper()

                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (205, 154, 79))
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (205, 154, 79), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)

            name="Vatsal Dutt"

        cap.release()
        wish_me(name)
        while True:
            global response
            self.inp = self.command()
            self.inp = self.inp.lower()
            if wake_word(self.inp) is True:
                self.inp = self.inp.replace('crystal', '')
                response = ''
                bow = bag_of_words(self.inp, words)
                bow = bow.reshape(1, -1)
                results = model.predict(bow)[0]

                results_index = numpy.argmax(results)
                tag = labels[int(results_index)]

                if results[results_index] > 0.96:
                    print(results[results_index])
                    for tg in data["intents"]:
                        if tg['tag'] == tag:
                            responses = tg['responses']
                            response = random.choice(responses)

                elif self.inp == "":
                    response = response + ""

                else:
                    print(type(response))
                    response = response + web_scrapper(self.inp)

                speak(response)

startExecution = MainThread()

class Main(QMainWindow):
    global response
    global wbr
    def __init__(self):
        global wbr
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.startTask()
        self.ui.pushButton_14.clicked.connect(self.webbrowser)
        self.ui.label_6.installEventFilter(self)

    def webbrowser(self):
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/lock-nossl.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
        self.urlbar.setStyleSheet('border-radius: 10px; border: black; padding: 5px;')

        stop_btn = QAction(QIcon(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        menubar1 = self.menuBar()

        file_menu = menubar1.addMenu("&File")

        new_tab_action = QAction(QIcon(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/disk--pencil.png')), "Save Page As...", self)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        self.menuBr= QMenuBar(menubar1)
        menubar1.setCornerWidget(self.menuBr, QtCore.Qt.TopRightCorner)
        self.close_s = QMenu(self.menuBr)
        self.close_s.setTitle('🗕')
        self.menuBr.setStyleSheet('font-size: 15px;')
        self.menuBr.addAction(self.close_s.menuAction())

        menubar1.setCornerWidget(self.menuBr, QtCore.Qt.TopRightCorner)
        self.minimize = QMenu(self.menuBr)
        self.minimize.setTitle('🗖 🗗︎')
        self.menuBr.addAction(self.minimize.menuAction())

        menubar1.setCornerWidget(self.menuBr, QtCore.Qt.TopRightCorner)
        self.small = QMenu(self.menuBr)
        self.small.setTitle('🗙︎')
        self.small.triggered.connect(self.close_app)
        self.menuBr.addAction(self.small.menuAction())

        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        self.show()
        self.setWindowIcon(QIcon(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/ma-icon-64.png')))

    def close_app(self):
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        # self.startTask()
        # self.ui.pushButton_14.clicked.connect(self.webbrowser)
        # self.ui.label_6.installEventFilter(self)
        self.browser.close()
        self.ui.show()

    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl('')

        browser = QWebView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "Hypertext Markup Language (*.htm *.html);;"
                                                  "All files (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")

        if filename:
            html = self.tabs.currentWidget().page().toHtml()
            with open(filename, 'w') as f:
                f.write(html.encode('utf8'))

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            return

        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/lock-ssl.png')))

        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    
    def startTask(self):
        self.ui.movie = QtGui.QMovie("Crystal new.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()
    
    def showTime(self):
        global response
        try:
            time = QTime.currentTime()
            date = QDate.currentDate()
            day = datetime.datetime.today().strftime('%A')
            hour_ = time.toString('hh')
            minute_ = time.toString('mm')
            meredian = 'AM'
            if int(hour_) > 12:
                hour_ = str(int(hour_)-12)
                meredian = 'PM'
            label_time = str(hour_)+':'+str(minute_)+meredian
            label_date = date.toString(Qt.ISODate)
            self.ui.textBrowser.setText(label_time)
            self.ui.textBrowser_2.setText(response)
            self.ui.textBrowser_3.setText(label_time)
            self.ui.textBrowser_4.setText(label_date)
            self.ui.textBrowser_5.setText(day)
            self.ui.textBrowser_5.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.textBrowser_4.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.textBrowser_3.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.textBrowser_2.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.textBrowser.setAlignment(QtCore.Qt.AlignCenter)
        except RuntimeError:
            pass
    

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu and source is self.ui.label_6:
            new = [
                {"New": ['File', 'Folder']}
            ]
            menu = QMenu()
            menu.addAction('Copy').setDisabled(True)
            menu.addAction('Cut').setDisabled(True)
            menu.addAction('Paste').setDisabled(True)
            menu.addSeparator()
            self.add_menu(new, menu)
            menu.addSeparator()
            menu.addAction('Info')
            menu.setStyleSheet("font-weight: bold; color: #0504fe; background-color: black; font-family: 'Segeo UI', Tahoma, Geneva, Verdana, sans-serif; border: 1px solid #0504fe; border-radius: 5px;")

            if menu.exec_(event.globalPos()):
                items = source.itemAt(event.pos())
                print(items.text())
            return True
        return super().eventFilter(source, event)
    
    def add_menu(self, data, menu_obj):
        if isinstance(data, dict):
            for k, v in data.items():
                sub_menu = QMenu(k, menu_obj)
                menu_obj.addMenu(sub_menu)
                self.add_menu(v, sub_menu)
        elif isinstance(data, list):
            for element in data:
                self.add_menu(element, menu_obj)
        else:
            action = menu_obj.addAction(data)
            action.setIconVisibleInMenu(False)

app = QApplication(sys.argv)
myos = Main()
myos.show()
exit(app.exec_())

