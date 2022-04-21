# -*- coding: utf-8 -*-
import sys,os,json
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QIcon

import shutil
from _process import Ui_Form as processingui
from _finish import Ui_Form as finishui
from _dwn import Ui_Form as downloadui
from _dwn import ins as pkg_path
from _dwn import pkgname_gb, pkgname_sse

#
RESOURCE = str('resources\\')
LOCATION_UI = str('xml\\mw_new.xml')
LOCATION_ICON = str('favicon.ico')
LOCATION_LANG = str('language.json')
LOCATION_VER = str(RESOURCE+'config\\v')
#

with open(LOCATION_VER) as v:
    appVer = v.read()

if os.path.exists(RESOURCE+'config/d.nfo'):
    with open(RESOURCE+'config/d.nfo') as d:
        debug = d.read()
        if debug == '1011':
            debug = True
        else: debug=False
else: debug=False

try:
    with open(RESOURCE+LOCATION_LANG) as t:
        lang = json.loads(t.read())
except:
    print('cant load language.json, exiting!') ; exit()

class MainApp(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(RESOURCE + LOCATION_UI, self)  # ui file load
        self.setWindowIcon(QIcon(RESOURCE + LOCATION_ICON))  # Icon Loading

        print('<PYRATE> Load finished')
        os.system('taskkill /IM "PYRATE.exe" /F')

        self.defFileDia = 'Select File'
        self.defDirectory = 'Select Directory'
        self.langIndex = 0
        self.langS = 'en'
        #self.calcbut.clicked.connect(self.calculate)  # Connect button to a function
        self.letsCrack.clicked.connect(self.cracking)
        self.gameSearch.clicked.connect(self.selectGame1)
        self.gameSearch2.clicked.connect(self.selectGame2)
        self.dwnButton.clicked.connect(self.downloadSection)
        self.crackInput.currentIndexChanged.connect(self.on_combobox_changed)
        self.comLang.currentIndexChanged.connect(self.changeLanguage)

        #
        self.VERSION_T.setText(appVer)
        #

        if os.path.exists(pkg_path+pkgname_gb):
            self.crackInput.addItem('Goldberg Crack')
        if os.path.exists(pkg_path+pkgname_sse):
            self.crackInput.addItem('SmartSteamEmu Crack')


    def selectGame1(self):
        valueBox = self.crackInput.currentIndex()

        if valueBox == 0:
            getpath = QFileDialog.getOpenFileName(self, self.defFileDia, '', 'All (*);;DLL Files (*.dll)')
        elif valueBox == 1:
            getpath = QFileDialog.getExistingDirectory(self, self.defDirectory)

        if getpath != "":
            if valueBox == 0:
                self.Input1.setText(getpath[0])
            elif valueBox == 1:
                self.Input1.setText(str(getpath))
        else: print('cancelled path selection')

    def selectGame2(self):
        getpath = QFileDialog.getOpenFileName(self, self.defFileDia, '', 'All (*);;DLL Files (*.dll)')
        if getpath != None:
            self.Input2.setText(getpath[0])
        else: print('cancelled path selection')

    def cracking(self):
        self.window2 = QMainWindow()
        self.ui = processingui()
        self.ui.setupUi(self.window2)
        self.window2.show()

        self.window_finish = QMainWindow()
        self.ui = finishui()
        self.ui.setupUi(self.window_finish)
        self.window_finish.hide()

        # Cracking beginns
        valueBox = self.crackInput.currentIndex()
        
        if valueBox == 0:
            print('<PYRATE> Selected Crack-type: Goldberg')

            # BEGINNING GB CRACK
            src = pkg_path+pkgname_gb+'/steam_api.dll'
            dst = self.Input1.text()
            src2 = pkg_path+pkgname_gb+'/steam_api64.dll'
            dst2 = self.Input2.text()
            if dst != '':
                if debug: print('NOT NONE')
                make1 = True
            else: make1 = False
            if dst2 != '':
                if debug: print('SECOND NOT NONE')
                make2 = True
            else: make2 = False
            
            if make1:
                print('<PYRATE> Crack steamapi in', dst)
                shutil.copyfile(src, 'steam_api.dll')
                os.system('move "steam_api.dll" "%s"' % dst)
            if make2:
                print('<PYRATE> Crack steamapi64 in', dst2)
                shutil.copyfile(src2, 'steam_api64.dll')
                os.system('move "steam_api64.dll" "%s"' % dst2)
            self.window2.hide()
            self.window_finish.show()
            # END GB

        elif valueBox == 1:
            print('<PYRATE> Selected Crack-type: SmartSteamEmu')

            # BEGINNING SSE CRACK
            src1 = pkg_path+pkgname_sse+'\\SSELauncher.exe'
            src2 = pkg_path+pkgname_sse+'\\SmartSteamEmu'
            dst = self.Input1.text()
            shutil.copyfile(src1, 'SSELauncher.exe')
            os.system('echo V | xcopy "%s" "SmartSteamEmu"' % src2)
            os.system('move "SmartSteamEmu" "%s"' % dst)
            os.system('move "SSELauncher.exe" "%s"' % dst)

            self.window2.hide()
            self.window_finish.show()
            # END SSE

    def downloadSection(self):
        with open(RESOURCE+'config/temp.drc', 'w') as temp:
            temp.write(str(self.langIndex))
        self.window3 = QMainWindow()
        self.ui = downloadui()
        self.ui.setupUi(self.window3)
        self.window3.show()
        os.remove(RESOURCE+'config/temp.drc')

    def on_combobox_changed(self, value):
        if value == 0:
            self.gameLabel2.setHidden(False)
            self.Input2.setHidden(False)
            self.gameSearch2.setHidden(False)

            self.gameLabel.setText(lang[self.langS][1])
            self.gameLabel2.setText(lang[self.langS][2])
        elif value == 1:
            self.gameLabel2.setHidden(True)
            self.Input2.setHidden(True)
            self.gameSearch2.setHidden(True)

            self.gameLabel.setText(lang[self.langS][11])
            
    def changeLanguage(self, value):
        if value == 0:
            currentLanguage = 'en'
        elif value == 1:
            currentLanguage = 'de'
        elif value == 2:
            currentLanguage = 'es'
        elif value == 3:
            currentLanguage = 'fr'
        else: currentLanguage = 'en'
        self.langIndex = value
        self.langS = currentLanguage
        
        if debug:
            print(str(self.langIndex) + ' ' + str(value))
            print(self.langS + ' ' + currentLanguage)
            print(isinstance(value, int))
        print('<PYRATE> Changing language to', currentLanguage)
        self.lang_changing(language_short=currentLanguage)


    def lang_changing(self, language_short):
        valueBox = self.comLang.currentIndex()
        valuex = self.crackInput.currentIndex()
        
        if debug:
            print(str(valueBox)+' VALUEBOX')
            print(language_short)

        self.defFileDia = lang[language_short][0]
        self.defDirectory = lang[language_short][10]
        if valuex == 1:
            self.gameLabel.setText(lang[language_short][11])
        else: self.gameLabel.setText(lang[language_short][1])
        self.gameLabel2.setText(lang[language_short][2])
        self.crackLabel.setText(lang[language_short][3])
        self.letsCrack.setText(lang[language_short][4])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    appMain = MainApp()
    appMain.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('<PYRATE> Exiting...')
