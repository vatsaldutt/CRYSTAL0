from Desktop import Ui_MainWindow
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtGui import *

import os
import sys


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.startTask()
        self.ui.pushButton_14.clicked.connect(self.webbrowser)
        self.ui.label_6.installEventFilter(self)

    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl('')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
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

    def navigate_to_url(self):  # Does not receive the Url
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        if q.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/lock-ssl.png')))

        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'C:/Users/vatdu/Desktop/OS/lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("Mozarella Ashbadger")
app.setOrganizationName("Mozarella")
app.setOrganizationDomain("mozarella.org")

window = MainWindow()

app.exec_()