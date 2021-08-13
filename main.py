#Hebrew Dictionary mobile aplication python file
#==============================================================================

#This file displays the UI, and the main fuction buttons and input text field, while the .kv file
#displays the the keyboard input keys for the letters of the Hebrew alphabet along with other
#manipulation fuctions.

from kivy.app import App
from kivy.lang import builder
from kivy.lang.builder import BuilderBase
from kivy.uix.gridlayout import GridLayout
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from codecs import decode
import string
import os
import sys
import unicodedata

#color values
red = [1, 0, 0, 1]
green = [0, 1, 0, 1]
sky_biue = [135, 206, 235]
blue = [0, 0, 1, 1]
purple = [1, 0, 1, 1]
white = [1, 1, 1, 1]
black = [0, 0, 0, 0]

finals = {'כ':'ך', 'מ':'ם', 'נ':'ן', 'פ':'ף', 'צ':'ץ'}
unFinals = {'ך':'כ', 'ם':'מ', 'ן':'נ', 'ף':'פ', 'ץ':'צ'}
suffix = ['ונ', 'םכ', 'ןכ', 'םה','ןה', 'ית', 'וה', 'ינ', 'י', 'ה', 'ו', 'ך', 'ם', 'ן']
preffix = ['ה', 'ו', 'מ', 'ב','כ', 'ש', 'ל']
prephrase = ['ת', 'ה', 'ו', 'מ', 'ב','כ', 'ש', 'ל']
plural = ['תו', 'םי', 'םיי']
modern = ['היצ', 'ןקי', 'הקי', 'טסי', 'םזי', 'תוי', 'יקה',  'הז', 'תי', 'יל', 'יא', 'הי']
metathesis = ['ס', 'ש', 'צ']
punctuation = [',', ' ', '.', ';', ':', '-', ')', '(', '[', ']', '[', ']', '}', '{', '*', '–']
vowels = ['ׁ', 'ְ', 'ַ', 'ֶ', 'ִ', 'ֹׁ', 'ֵ', 'ָ', 'ֲ', 'ּ', 'ֹ', 'ֱ', 'ֵּ', 'ּּ']

#This class defines all the properties and methods that a Word object needs to have in order
#use the proper metrics in searching and ordering words.
class Word:
    def __init__(self, t, d):
        
        self.text = t
        self.definition = d
        self.value = 0
        self.prefix = 0
        self.preW = []
        self.sufW = []
        self.suffix1 = 0
        self.suffix2 = 0
        self.suffix3 = 0
        self.irreg = 0
        self.modern = 0
        self.plural = 0
        self.daul = 0
        self.construct = 0
        self.verbform = -1
        self.tense = -1
        self.person = -1
        self.gender = -1
        self.preffix = {"ה":"the", "ו":"and", "ב":"in", "מ":"from", "ל":"to", "כ":"as", "ש":"which"}
        self.suffix = {"ונ":"our", "םכ":"you-all", "ןכ":"you-all(f)", "םה":"their", "ןה":"their(f)", "ית":"me", "וה":"him", "ינ":"me", "י":"my", "ה":"her", "ו":"his", "ך":"your", "ם":"them", "ן":"them(f)"}
        self.Gender = ['m.', 'f.', '', '']
        self.Person = ['1st, sg.', '1st, pl.', '2nd, sg.', '2nd, pl.', '3rd, sg.', '3rd, pl.', '']
        self.tenses = ['Perfect', 'Imperfect', 'Particible', 'Infinitive', 'Imperative', '']
        self.tenseVals = [4, 4, 4, 4, 4, 1]
        self.verbforms = ['Qal', 'Niphal', 'Piel', 'Pual', 'Hiphil', 'Hophal', 'Hithpeal', 'hishtaphel', 'pilpel', '']
        self.verbformVals = [7, 7, 7, 7, 7, 7, 2, 2, 3, 1]
        self.gemontria = {'א':1, 'ב':2, 'ג':3, 'ד':4, 'ה':5, 'ו':6, 'ז':7, 'ח':8, 'ט':9, 'י':10, 'כ':20, 'ל':30, 'מ':40, 'נ':50, 'ס':60, 'ע':70, 'פ':80, 'צ':90, 'ק':100, 'ר':200, 'ש':300, 'ת':400, 'ך':20, 'ם':40, 'ן':50, 'ף':80, 'ץ':90}
        self.millenn = ['ה','ד','ג', 'ב', 'א']

    def __assign__(self, value):
        self.value = value.value
        self.text = value.text
        self.definition = value.definition
        self.prefix = value.prefix
        self.suffix1 = value.suffix1
        self.suffix2 = value.suffix2
        self.suffix3 = value.suffix3
        self.irreg = value.irreg
        self.modern = value.modern
        self.plural = value.plural
        self.daul = value.daul
        self.construct = value.construct
        self.verbform = value.verbform
        self.tense = value.tense
        self.person = value.person
        self.gender = value.gender
        self.preW = value.preW
        self.sufW = value.sufW
    
    def equalTo(self, newWord):
        self.vaule = newWord.value
        self.text = newWord.text
        self.definition = newWord.definition
        self.prefix = newWord.prefix
        self.suffix1 = newWord.suffix1
        self.suffix2 = newWord.suffix2
        self.suffix3 = newWord.suffix3
        self.irreg = newWord.irreg
        self.modern = newWord.modern
        self.plural = newWord.plural
        self.daul = newWord.daul
        self.construct = newWord.construct
        self.verbform = newWord.verbform
        self.tense = newWord.tense
        self.person = newWord.person
        self.gender = newWord.gender
        self.preW = newWord.preW.copy()
        self.sufW = newWord.sufW.copy()
        
    def Is(self, newWord):
        if not (self.text == newWord.text):
            return False
        if not (self.getPrefix() == newWord.getPrefix()):
            return False
        if not (self.getSuffix() == newWord.getSuffix()):
            return False
        #if not (self.getIrreg() == newWord.getIrreg()):
            #return False
        if not (self.getModern() == newWord.getModern()):
            return False
        if not (self.getPlural() == newWord.getPlural()):
            return False
        if not (self.getDaul() == newWord.getDaul()):
            return False
        if not (self.getConstruct() == newWord.getConstruct()):
            return False
        if not (self.verbform == newWord.verbform):
            return False
        if not (self.tense == newWord.tense):
            return False
        if not (self.person == newWord.person):
            return False
        if not (self.preW == newWord.preW):
            return False
        if not (self.sufW == newWord.sufW):
            return False
        if not (self.getGender() == newWord.getGender()):
            return False
        return True
    
    def getText(self):
        return self.text
    
    def getDefinition(self):
        return self.definition
        
    def getTense(self):
        return self.tenses[self.tense]
        
    def getTenseVal(self):
        return self.tense
        
    def getPerson(self):
        return self.Person[self.person]
    
    def getPersonVal(self):
        return self.person
    
    def getGender(self):
        return self.Gender[self.gender]
        
    def getGenderVal(self):
        return self.gender
    
    def getVerbform(self):
        return self.verbforms[self.verbform]
    
    def getVerbformVal(self):
        return self.verbform
        
    def getGemontria(self):
        g = 0
        nText = self.text.strip('"')
        nText = nText.strip("'")
        for letter in nText:
            if letter in self.gemontria:
                g += self.gemontria[letter]   
        return g
        
    def getTGemontria(self, t):
        g = 0
        nText = t.strip('"')
        nText = nText.strip("'")
        for letter in nText:
            if letter in self.gemontria:
                g += self.gemontria[letter]   
        return g
        
    def getValue(self):
        self.value = 100000000 - 10*(self.prefix + 1)*(self.suffix1 + 1)*(self.suffix2 + 1)*(self.suffix3 + 1)*(self.plural + 1)*(self.construct + 1)*(self.modern + 1)*(self.irreg + 1)*(self.tenseVals[self.tense])*(self.verbformVals[self.verbform])
        return self.value
    
    def getPrefix(self):
        if(self.prefix > 0):
            return True
        return False
        
    def getSuffix1(self):
        if(self.suffix1 > 0):
            return True
        return False
        
    def getSuffix2(self):
        if(self.suffix2 > 0):
            return True
        return False
        
    def getSuffix3(self):
        if(self.suffix3 > 0):
            return True
        return False
        
    def getSuffix(self):
        if (self.suffix1 > 0) or (self.suffix2 > 0) or (self.suffix3 > 0):
            return True
        return False
        
    def getIrreg(self):
        if(self.Irreg > 0):
            return True
        return False
        
    def getModern(self):
        if(self.modern > 0):
            return True
        return False
        
    def getPlural(self):
        if(self.plural > 0):
            return True
        return False
        
    def getDaul(self):
        if(self.daul > 0):
            return True
        return False
        
    def getConstruct(self):
        if(self.construct > 0):
            return True
        return False
        
    def getPrefixVal(self):
        return self.prefix + 1
        
    def getPrefixW(self):
        s = ""
        for pre in self.preW:
            s += pre + ', '
        return s[:-2]
        
    def getSuffixW(self):
        s = ""
        for suff in self.sufW:
            s += suff + ', '
        return s[:-2]
            
    def getSuffix1Val(self):
        return self.suffix1 + 1
        
    def getSuffix2Val(self):
        return self.suffix2 + 1
        
    def getSuffix3Val(self):
        return self.suffix3 + 1
        
    def getIrregVal(self):
        return self.irreg + 1
            
    def getModernVal(self):
        return self.modern + 1
        
    def getPluralVal(self):
        return self.plural + 1
        
    def getDaulVal(self):
        return self.daul + 1
        
    def getConstructVal(self):
        return self.construct + 1
        
    def last(self):
        return self.text[0:1]
    
    def last2(self):
        return self.text[0:2]
        
    def last3(self):
        return self.text[0:3]
        
    def first(self):
        return self.text[-1:]
        
    def first2(self):
        return self.text[-2:]
        
    def nextToLast(self):
        return self.text[1:2]
        
    def nextToFirst(self):
        return self.text[-2:-1]

    def setPrefix(self):
        self.prefix += 3
        
    def resetPrefix(self):
        self.prefix = 0
        
    def decPrefix(self):
        self.prefix = self.prefix -3
    
    def setSuffix1(self):
        self.suffix1 += 3
        
    def setSuffix2(self):
        self.suffix2 += 4
        
    def setSuffix3(self):
        self.suffix3 += 5
          
    def setIrreg(self):
        self.irreg += 6
          
    def setModern(self):
        self.modern += 7
        
    def setPlural(self):
        self.plural += 1
        
    def setDaul(self):
        self.daul += 1
        
    def setConstruct(self):
        self.construct += 1
        
    def setTense(self, t):
        self.tense = t
        
    def setPerson(self, p):
        self.person = p
        
    def setGender(self, g):
        self.gender = g
        
    def setVerbform(self, verb):
        self.verbform = verb
    
    def setText(self, t):
        self.text = t
    
    def setDefinition(self, d):
        self.definition = d
    
    def setValue(self, v):
        self.value = v
    
    def addPre(self, pre):
        self.preW.append(pre + '- ' + self.preffix[pre])
        
    def addSuff(self, suff):
        self.sufW.append(suff + '- ' + self.suffix[suff])
        
    def rm(self, pre):
        self.preW.remove(pre + '- ' + self.preffix[pre])
        
    def rmSuf(self, suff):
        self.sufW.remove(suff + '- ' + self.suffix[suff])
        
    def addToValue(self, v):
        self.value = self.value + v
        
    def isYear(self):
        if (self.nextToFirst() == "'") and (self.first() in self.millenn) and (self.nextToLast() == '"') and (self.textIsNumb(self.last() + self.text[2:-2]) == True):
            return True
        if(not self.nextToFirst() == "'") and (self.nextToLast() == '"') and (self.textIsNumb(self.last() + self.text[2:]) == True):
            return True
        return False
        
    def getYear(self):
        if self.isYear() == False:
            return "Error"
            Year = 0;
        if (self.nextToFirst() == "'"):
            textYear = self.last() + self.text[2:-2]
            Year = self.getTGemontria(textYear) + 1000*(self.gemontria[self.first()])
        if (not self.nextToFirst() == "'"):
            textYear = self.last() + self.text[2:]
            Year = self.getTGemontria(textYear) + 5000
        return str(Year - 3761)
        
        
    def isNumb(self):
        nText = self.text.strip('"')
        nText = nText.strip("'")
        if self.nextToLast() == '"':
            nText = self.last() + self.text[2:]
        if len(nText) == 1:
            return True
        if nText == 'וט':
            return True
        if nText == 'זט':
            return True
        if nText == 'הי':
            return False
        if nText == 'וי':
            return False
        for i in range(len(nText)-1):
            if not (nText[i] in self.gemontria):
                if i == 0: 
                    return False
                return True
            if not nText[i+1] in self.gemontria:
                return False
            if self.rank(nText[i]) < 2:
                if self.rank(nText[i]) >= self.rank(nText[i+1]):
                    return False
            elif (self.rank(nText[i]) > self.rank(nText[i+1])) or (self.gemontria[nText[i]] > self.gemontria[nText[i+1]]):
                return False      
        return True
        
    def textIsNumb(self, nText):
        if len(nText) == 1:
            return True
        if nText == 'וט':
            return True
        if nText == 'זט':
            return True
        for i in range(len(nText)-1):
            if not (nText[i] in self.gemontria):
                if i == 0: 
                    return False
                return True
            if not nText[i+1] in self.gemontria:
                return False
            if self.rank(nText[i]) < 2:
                if self.rank(nText[i]) >= self.rank(nText[i+1]):
                    return False
            elif (self.rank(nText[i]) > self.rank(nText[i+1])) or (self.gemontria[nText[i]] > self.gemontria[nText[i+1]]):
                return False      
        return True
    
    def rank(self, n):
        if len(n) > 1:
            return -1
        if self.gemontria[n] < 10:
            return 0
        if (self.gemontria[n] >= 10) and (self.gemontria[n] < 100):
            return 1
        if self.gemontria[n] >= 100:
            return 2

#This is a helper class which contain the methods for searching and choosing words. 
#It also has at least one container to store and sort certain Word objects.
class SearchWord:
    def __init__(self):
        self.Words = []
    
    def getWords(self):
        return list(self.Words)
        
    def addWord(self, w):
        self.Words.append(w)
        
    def getValue(self, word):
        return word.getValue()
        
    def indexWords(self, w):
        for i in range(len(self.getWords())):
            if w.getText() == self.getWords()[i].getText():
                return i
                
    def checkList(self, w):
        for i in range(len(self.getWords())):
            if w.Is(self.getWords()[i]) == True:
                return True
        return False
        
    def find(self, w, Dict):
        if self.checkList(w) == True:
            index = self.indexWords(w)
            if self.Words[index].getValue() < w.getValue():
                self.Words[index].setValue(w.getValue())
                #w.setDefinition(self.Words[index].getDefinition())
                #self.Words[index].equalTo(w)
            #self.Words[index].addToValue(0)
            return True
        elif w.getText() in Dict.keys():
            definition = Dict[w.getText()]["definition"]
            newWord = Word("", "")
            newWord.equalTo(w)
            newWord.setDefinition(definition)
            self.addWord(newWord)
            return True
        return False
            
#Keyboard interface
class Keyboard(GridLayout):
    
    def __init__(self, instance, **kwargs):
        super(Keyboard, self).__init__(**kwargs)
        self.main = instance
        
    def keyAction(self, k, instance):
        inputT = self.main.Input.text
        if(len(inputT) < 1):
            self.main.Input.text = k
        else:
            if(inputT[0] in unFinals):
                self.main.Input.text = k + unFinals.get(inputT[0]) + inputT[1:]
            else:
                self.main.Input.text = k + inputT
        
    def rCharsAction(self, instance):
        newInput = self.main.Input.text
        revInput = ""
        end = len(self.main.Input.text)-1
        
        for index in range(end+1):
            if newInput[end-index] == '(':
                revInput += ')'
            elif newInput[end-index] == ')':
                revInput += '('
            elif newInput[end-index] == '[':
                revInput += ']'
            elif newInput[end-index] == ']':
                revInput += '['
            elif newInput[end-index] == '{':
                revInput += '}'
            elif newInput[end-index] == '}':
                revInput += '{'
            else:
                revInput += newInput[end-index]
                
        self.main.Input.text = self.revNum(str(revInput))
        
    def revNum(self, words):
        numWords = ""
        n = 0;
        for i in range(len(words)):
            if words[i].isdigit():
                n += 1
            else:
                for j in range(i-1, (i-1)-n, -1):
                    numWords += words[j]
                numWords += words[i]
                n = 0
                
        return str(numWords)
        
    def rWordsAction(self, instance):
        words = self.main.Input.text.split()
        h = int((len(words) - 1)/2)
        for i in range(len(words) - 1, h, -1):
            temp = words[(len(words) - 1) - i]
            words[(len(words) - 1) - i] = words[i]
            words[i] = temp
        self.main.Input.text = " ".join(words)
        
    def clearAction(self, instance):
        self.main.Input.text = ""
        
    def spaceAction(self, instance):
        self.main.Input.text = " " + self.main.Input.text
        
    def backspaceAction(self, instance):
        self.main.Input.text = self.main.Input.text[1:]
    
    def FinalAction(self, instance):
        inputL = self.main.Input.text.split()
        if len(inputL) > 1:
            for i in range(len(inputL)):
                inputL[i] = self.wFinal(inputL[i])
            self.main.Input.text =  " ".join(inputL)  
        else:
            self.main.Input.text = self.wFinal(self.main.Input.text)
                        
    def wFinal(self, text):
        if text[0] in finals.keys():
            return finals.get(text[0]) + text[1:]
        return text
        
    #Interface for displaying the words found, their diffinition, and some gramatical properties.  
class DisplayWords(GridLayout):
    def __init__(self, instance, **kwargs):
        super(DisplayWords, self).__init__(**kwargs)
        self.cols = 1
        self.readText = TextInput(readonly=True, multiline=True, base_direction="rtl", size_hint=[5, 0.4], focus=False, font_name='Arial', font_size=20)
        self.display = TextInput(readonly=True, multiline=True, focus=False, font_name='Arial', font_size=20)
        self.closeB = Button(text='[color=FFFFFF]Close[color=FFFFFF]', size_hint=[5, 0.1], font_size=20, markup=True)
        self.closeB.bind(on_press=instance.closeAction)
        self.add_widget(self.readText)
        self.add_widget(self.display)
        self.add_widget(self.closeB)     
        
#Inerface for adding a new word to the dictionary
class AddWord(GridLayout):
    def __init__(self, instance, **kwargs):
        super(AddWord, self).__init__(**kwargs)
        self.cols = 2
         
        self.wLabel = Label(text='[color=3333ff]Word[color=3333ff]', outline_color=black, font_size=50, markup=True)
        self.dLabel = Label(text='[color=3333ff]Diffinition[color=3333ff]', outline_color=black, font_size=50, markup=True)
        self.Word = TextInput(text="", readonly=False, multiline=False, font_name='Arial', font_size=25)
        self.Definition= TextInput(text="", readonly=False, multiline=False, font_name='Arial', font_size=25)
        
        self.enterB = Button(text='[color=000000]Enter[color=000000]', font_size=20, markup=True)
        self.enterB.bind(on_press=instance.enterAction) 
        self.cancelB = Button(text='[color=000000]Cancel[color=000000]', font_size=20, markup=True)
        self.cancelB.bind(on_press=instance.cancelAction)
        
        self.add_widget(self.wLabel)
        self.add_widget(self.dLabel)
        self.add_widget(self.Word)
        self.add_widget(self.Definition)
        self.add_widget(self.enterB)
        self.add_widget(self.cancelB)     
 
#top level of app.  
class HebrewDictionary(App):
    
    def startInterface(self):
    
        self.Dict = {}
        self.AlefBet = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת', 'ך', 'ם', 'ן', 'ף', 'ץ']
        
        for i in range(len(vowels)):
            vowels[i] = vowels[i].encode('UTF-8')
        for item in self.store:
            word = {item:  {"text": self.store.get(item)['text'], "definition": self.store.get(item)['definition']}}
            self.Dict.update(word)
            
        self.Word = AddWord(self)
        self.popup = Popup(title='Add Word', content=self.Word)
        self.DWords = DisplayWords(self)
        self.wordPopup = Popup(title='Word', content=self.DWords)
        
        self.UserInterface = GridLayout(cols=1)
        self.MainPanal = GridLayout(cols=1)
        self.Input = TextInput(readonly=False, multiline=False, base_direction='rtl', font_name='Arial', font_size=25)
        self.findB = Button(text='FindW', border=[1,1,1,1], font_name='Arial', font_size=20, markup=True)
        self.findB.bind(on_press=self.findAction)
        self.addB = Button(text='AddW', border=[1,1,1,1], font_name='Arial', font_size=20, markup=True)
        self.addB.bind(on_press=self.addAction)
        self.editB = Button(text='EditW', border=[1,1,1,1], font_name='Arial', font_size=20, markup=True)
        self.editB.bind(on_press=self.editAction)
        self.removeB = Button(text='RemoveW', border=[1,1,1,1], font_name='Arial', font_size=20, markup=True)
        self.removeB.bind(on_press=self.removeAction)
        self.exitB = Button(text='Exit', border=[1,1,1,1], font_name='Arial', font_size=20, markup=True)
        self.exitB.bind(on_press=self.exitAction)
        self.KeyboardPanal = Keyboard(self)
        self.MainPanal.add_widget(Label(text='[color=3333ff]Hebrew Dictionary[color=3333ff]', outline_color=white, outline_width=1, font_size=25, markup=True))
        self.MainPanal.add_widget(self.Input)
        self.SubPanal = GridLayout(cols=5)
        self.SubPanal.add_widget(self.findB)
        self.SubPanal.add_widget(self.addB)
        self.SubPanal.add_widget(self.editB)
        self.SubPanal.add_widget(self.removeB)
        self.SubPanal.add_widget(self.exitB)
        self.MainPanal.add_widget(self.SubPanal)
        self.UserInterface.add_widget(self.MainPanal)
        self.UserInterface.add_widget(self.KeyboardPanal)
        return self.UserInterface       
            
    def findAction(self, instance):
        self.wText = ''
        inputBuff = self.Input.text.replace('-', ' ')
        words = inputBuff.split()
        
        for i in range(len(words)):
            words[i] = words[i].strip(str(punctuation))
            words[i] = words[i].strip(str(vowels))
        
        words = self.revWords(words)
        words = self.getPhrase(words)
        
        for i in range(len(words)):
            k = len(words[i].split('-'))
            self.getWList(words[i], k, 0)
            if not(i == len(words)):
                self.wText += '\n'
                self.wText += "*********************************************************"
                self.wText += '\n\n'
        
        self.DWords.display.cursor = (0, 0)
        #Popup(title='Word', content=TextInput(text=str(words), readonly=True, multiline=False, base_direction='rtl', font_name='Arial', font_size=25)).open()
    def revPhWords(self, phrase, s):
        lph = phrase.split(s)
        rLph = []
        end = len(lph)-1
        
        for i in range(len(lph)):
            rLph.append(lph[end-i])  
        return s.join(rLph)       
        
    def getPhrase(self, words):
        if len(words) < 2:
            return words
        check = SearchWord()
        tempWs = words
        Ws2 = words
        k = 0
        end = len(tempWs)                 
        for i in range(end):
            N = 1
            s = 0
            while (N + i) < (end):
                revPhrase = '-'.join(self.revWords(Ws2[i:(N+i+1)]))
                fixedPhrase = '-'.join(tempWs[i:(N+i+1)])
                
                phraseW = Word(fixedPhrase, "")
                rPhraseW = Word(revPhrase, "")
                
                cPhrasePl = Word(fixedPhrase, "")
                cPhrasePl.equalTo(self.plural(check, phraseW))
                
                cPhrasePre = Word(fixedPhrase, "")
                cPhrasePre.equalTo(self.prefix(check, phraseW))
                
                cPhraseSuf = Word(fixedPhrase, "")
                cPhraseSuf.equalTo(self.suffix(check, phraseW, 3))
                
                if (((check.find(phraseW, self.Dict) == True)) or (check.find(cPhrasePl, self.Dict)) or (check.find(cPhrasePre, self.Dict)) or (check.find(cPhraseSuf, self.Dict)) or (check.find(self.suffix(check, self.prefix(check, phraseW), 3), self.Dict)) or (check.find(self.plural(check, self.prefix(check, phraseW)), self.Dict))) and (end > 1):
                    Ws2[i] = revPhrase
                    tempWs[i] = fixedPhrase
                    s = i
                    end = end - N
                    for n in range(i+1, end):
                        tempWs[n] = tempWs[n+N]
                        Ws2[n] = Ws2[n + N]  
                    k += N
                    N = 1
                else:
                    N = N + 1
            k = 0
            if(i < end-1):
                for p in range(-3 , 0, 1):
                    if(tempWs[i+1][p:] in prephrase) and (not (len(tempWs[i+1][:p]) < 2)):
                        prePhrase = tempWs[i] + "-" + tempWs[i+1][p:]
                        prephraseW = Word(prePhrase, "")
                        if (check.find(prephraseW, self.Dict) == True):
                            tempWs[i] = prePhrase
                            tempWs[i+1] = tempWs[i+1][:p]
                            break                   
        return tempWs[0:(end)]
        
    def getWList(self, text, k, n):
        number = ''
        Year = ''
        sText = text.strip('"')
        sText = sText.strip("'")
        look = SearchWord()
        yWord = Word(text, "")
        if yWord.isYear() == True:
            Year = 'Year: ' + str(yWord.getYear())
        word = Word(sText, "")
        if word.isNumb() == True:
            number = '#: ' + str(word.getGemontria()) + '; '
        else:
            preNum = self.smPrefix(look, word)
            if (preNum.isNumb() == True) and (not preNum.getText() == ""):
                number = '#: ' + "with prefix [" + preNum.getPrefixW() + '] ' + str(preNum.getGemontria()) + '; '
          
        self.wText += '\t\t'*n + ':' + (self.revPhWords(text, '-')) + '   ' + number + Year + '\n'
        look.find(word, self.Dict)
        
        self.algorithm(look, word)
        WList = look.getWords()
        WList.sort(key=look.getValue, reverse = True)
        if(len(look.getWords()) > 0):
            for wi in WList:
                w = Word("", "")
                w.equalTo(wi)
                w.setText(self.revPhWords(wi.getText(), '-'))
                pl = ""
                pre = ""
                suff = ""
                dl = ""
                modern = ''   
                constr = ''
                s1 = " "
                s2 = " "
                s3 = ''
                s4 = ''
                s5 = ''
                s6 = ''
                s7 = ''
                s8 = ''
                s9 = ''
                if w.getModern() == True:
                    modern = "modern word: "
                if w.getVerbform() == '':
                    s1 = ""
                if w.getTense() == '':
                    s2 = ""
                if (w.getTenseVal() == 0) or (w.getTenseVal() == 1) or (w.getTenseVal() == 4):
                    s3 = " "
                if (w.getGenderVal() == 0) or (w.getGenderVal() == 1):
                    s4 = " "
                if w.getConstruct() == True:
                    constr = "const."
                    s5 = " "
                if w.getPrefix() == True:
                    pre = "preffix"
                    s6 = " [" + w.getPrefixW() + '] '
                if w.getSuffix() == True:
                    suff = "suffix"
                    s7 = " [" + w.getSuffixW() + '] '
                if w.getPlural() == True:
                    pl = "pl."
                    s8 = " "
                elif w.getDaul() == True:
                    dl = "daul"
                    s9 = " "

                #val = "val = " + str(w.getValue()) + " -- "
                val = ""
                definition = ", ".join(w.definition)
                script = '(with other pre  ' + '\t\t' + val + modern + "(" + w.getVerbform() + s1*2 + w.getTense() + s2*2 + w.getPerson() + s3*2 + w.getGender() + s4*2 + constr + s5*2 + pre*2 + s6 + suff + s7*2 + pl + s8*2 + dl + s9*2 + "form of)- " + w.text + '\t' + '-' + '\t'
                spaces = len(script)
                self.wText += '\t\t'*n +  '\t\t' + val + modern + "(" + pre + s6 + w.getVerbform() + s1 + w.getTense() + s2 + w.getPerson() + s3 + w.getGender() + s4 + constr + s5 + suff + s7 + pl + s8 + dl + s9 + "form of)- " + w.text + '\t' + '-' + '\t' + self.fixDef(definition, spaces) + ';' + ' gmra. = ' + str(w.getGemontria()) + '\n'
        else:
            self.wText += '\t\t'*n +  "No words found"
            self.wText += '\n'
            
        if k > 1:
            self.wText += '\t\t'*(n+1) + "--------------------------------------------------"
            self.wText += '\n'
            Lwords = []
            t1 = text.split('-')[0]
            Lwords.append(t1)
            subText = text.split('-')[1:]
            Lwords.extend(self.getPhrase(subText))
            #Lwords = text.split('-')
            for lw in range(len(Lwords)):
                if (len(Lwords[lw]) == 1) and (k == 2):
                    self.wText += '\t\t'*(n+1) + Lwords[lw] + " " + "(prefix)"
                    if not(lw == len(Lwords)-1):
                        self.wText += '\t\t'*(n+1) + "--------------------------------------------------"
                    self.wText += '\n'
                else:
                    self.getWList(Lwords[lw], len(Lwords[lw].split('-')), n+1)
                    if not(lw == len(Lwords)-1):
                        self.wText += '\t\t'*(n+1) + "--------------------------------------------------"
                        self.wText += '\n'
            
        self.DWords.readText.text = self.fix(self.Input.text)
        self.DWords.display.text = self.wText
        
        self.wordPopup.open()
        
        print ('\n' + str(look.getWords()) + '\n')
    
    def revWords(self, wList):
        words = wList
        h = int((len(words) - 1)/2)
        for i in range(len(words) - 1, h, -1):
            temp = words[(len(words) - 1) - i]
            words[(len(words) - 1) - i] = words[i]
            words[i] = temp
        return words
    
    def fixDef(self, definition, spaces):
        words = definition.split()
        fixedL = words
        n = 60
        diff = 0
        for i in range(len(words)):
            diff += len(words[i])
            if (diff > n):
                fixedL[i] = words[i] + '\n' + (' ')*spaces
                diff = 0
            else:
                fixedL[i] = words[i]
        fixedW = " ".join(fixedL)
        return fixedW
    
    def fix(self, text):
        words = text.split()
        fixedL = words
        n = 70
        diff = 0
        for i in range(len(words) - 1, -1, -1):
            diff += len(words[i])
            if (diff > n):
                fixedL[i] = words[i] + '\n'
                diff = 0
            else:
                fixedL[i] = words[i]
                
        fixingW = " ".join(fixedL)
        fixedL = fixingW.split('\n')
        fixedL = self.revWords(fixedL)
        fixedW = "\n".join(fixedL)
        return fixedW
            
    def algorithm(self, look, word):
        if len(word.getText()) < 2:
            return
        pre = Word("","")
        pre.equalTo(self.prefix(look, word))
        self.algorithm(look, pre)
        verbW = Word("","")
        verbW.equalTo(self.verbForms(look, word))
        pl = Word("","")
        pl.equalTo(self.plural(look, word))
        pre = Word("","")
        pre.equalTo(self.prefix(look, word))
        tenseW = Word("","")
        tenseW.equalTo(self.tense(look, word, False))
        
        htenseW = Word("","")
        htenseW.equalTo(self.tense(look, word, True))
        suff = Word("","")
        suff.equalTo(self.suffix(look, word, 3))
        suff2 = Word("","")
        suff2.equalTo(self.suffix(look, word, 2))
        suff1 = Word("","")
        suff1.equalTo(self.suffix(look, word, 2))
        suffObj = Word("","")
        suffObj.equalTo(self.suffixObj(look, word))
        
        self.algorithm(look, suffObj)
        
        tenpl = Word("","")
        tenpl.equalTo(self.plural(look, tenseW))
        
        self.plural(look, word)
        self.plural(look, suff1)
        self.plural(look, suff2)
        self.plural(look, suffObj)

        
        hpre = Word("","")
        hpre.equalTo(pre)
  
        self.plural(look, pre)
        self.plural(look, hpre)
        irreg = Word("","")
        irreg.equalTo(self.irreg(look, word))
        mdrn = Word("","")
        mdrn.equalTo(self.modern(look, word))
        
        self.verbForms(look, pl)
        
        self.verbForms(look, tenpl)
        
        self.verbForms(look, pre)
        pretense = Word("","")
        pretense.equalTo(self.tense(look, pre, False))
        self.tense(look, pl, True)
        
        pretensesuff = Word("","")
        pretensesuff.equalTo(self.suffixObj(look, pretense))
        
        pretensesuffs = Word("","")
        pretensesuffs.equalTo(self.plural(look, pretensesuff))
        
        self.verbForms(look, pretensesuff)
        self.verbForms(look, pretensesuffs)
        
        mdrnpl = Word("","")
        mdrnpl.equalTo(self.plural(look, mdrn))
        plmdrn = Word("","")
        plmdrn.equalTo(self.modern(look, pl))
        
        self.modern(look, pre)
        
        sufftenseW = Word("","")
        sufftenseW.equalTo(self.tense(look, suffObj, False))
        suffhtenseW = Word("","")
        suffhtenseW.equalTo(self.tense(look, suffObj, True))
        self.tense(look, suff2, False)
        self.tense(look, suff2, True)

   
        self.verbForms(look, hpre)
        
        verbtenW = Word("","")
        verbtenW.equalTo(self.verbForms(look, tenseW))
        verbhtenW = Word("","")
        #verbhtenW.equalTo(self.verbForms(look, htenseW))
        verbsuftenW = Word("","")
        verbsuftenW.equalTo(self.verbForms(look, sufftenseW))
        verbsufhtenW = Word("","")
        verbsufhtenW.equalTo(self.verbForms(look, suffhtenseW))
        
        prepl = Word("","")
        prepl.equalTo(self.plural(look, pre))
        psuff = Word("","")
        psuff.equalTo(self.suffix(look, pre, 3))
        psuff2 = Word("","")
        psuff2.equalTo(self.suffix(look, pre, 2))
        psuff1 = Word("","")
        psuff1.equalTo(self.suffix(look, pre, 1))
        hpsuff = Word("","")
        hpsuff.equalTo(self.suffixObj(look, hpre))
        self.plural(look, psuff2)
        self.plural(look, psuff1)
        self.plural(look, hpsuff)
        ppre = Word("","")
        ppre.equalTo(self.prefix(look, pre))
        hppre = Word("","")
        hppre.equalTo(self.prefix(look, pre))
    
        plsu = Word("","")
        plsu.equalTo(self.suffix(look, pl, 3))
        plsu2 = Word("","")
        plsu2.equalTo(self.suffix(look, pl, 2))
        plsu1 = Word("","")
        plsu1.equalTo(self.suffix(look, pl, 1))
        self.plural(look, suff)
        self.plural(look, suff2)
        self.plural(look, suff1)
        ppsuff = Word("","")
        ppsuff.equalTo(self.suffix(look, ppre, 3))
        ppsuff2 = Word("","")
        ppsuff2.equalTo(self.suffix(look, ppre, 2))
        ppsuff1 = Word("","")
        ppsuff1.equalTo(self.suffix(look, ppre, 1))
        self.plural(look, ppsuff2)
        self.plural(look, ppsuff1)
        pprepl = Word("","")
        pprepl.equalTo(self.plural(look, ppre))
        plsupre = Word("","")
        plsupre.equalTo(self.prefix(look, plsu))
        plsupre2 = Word("","")
        plsupre2.equalTo(self.prefix(look, plsu2))
        plsupre1 = Word("","")
        plsupre1.equalTo(self.prefix(look, plsu1))
        pppre = Word("","")
        pppre.equalTo(self.prefix(look, ppre))
        
        self.verbForms(look, psuff)
        self.verbForms(look, psuff2)
        self.verbForms(look, psuff1)
        self.verbForms(look, hpsuff)
        
        self.verbForms(look, pre)
        self.tense(look, pre, False)
        self.verbForms(look, ppre)
        self.tense(look, ppre, False)
        self.verbForms(look, hppre)
        self.tense(look, hppre, False)
        self.verbForms(look, pppre)
        self.tense(look, pppre, False)
        
    def modern(self, look, word):
        if(len(word.getText()) < 3):
            return Word("", "")
        last = word.getText()[0:1]
        last2 = word.getText()[0:2]
        if(len(word.getText()) > 3):
            if(last2 == 'תי'): 
                mdrnW = Word("","")
                mdrnW.equalTo(word)
                mdrnW.setText(self.Final(word.getText()[2:]))
                mdrnW.setModern()
                look.find(mdrnW, self.Dict)
                return mdrnW
        if(len(word.getText()) > 4):
            last3 = word.getText()[0:3]
            if last3 in modern:
                mdrnW = Word("","")
                mdrnW.equalTo(word)
                mdrnW.setText(self.Final(word.getText()[3:]))
                mdrnW.setModern()
                look.find(mdrnW, self.Dict)
                return mdrnW
        if(len(word.getText()) > 3):
            first2 = word.getText()[-2:]
            last2 = word.getText()[0:2]
            if last2 in modern:
                mdrnW = Word("","")
                mdrnW.equalTo(word)
                mdrnW.setText(self.Final(word.getText()[2:]))
                mdrnW.setModern()
                look.find(mdrnW, self.Dict)
                return mdrnW
            if first2 == 'תת':
                mdrnW = Word("","")
                mdrnW.equalTo(word)
                mdrnW.setText(word.getText()[:-2])
                mdrnW.setModern()
                look.find(mdrnW, self.Dict)
                return mdrnW
        if last in modern:
            mdrnW = Word("","")
            mdrnW.equalTo(word)
            mdrnW.setText(self.Final(word.getText()[1:]))
            mdrnW.setModern()
            look.find(mdrnW, self.Dict)
            return mdrnW
        return Word("", "")

    def tense(self, look, word, irr):
        if(len(word.getText()) < 3):
            return Word("", "")
        if irr == False:
            perf = Word("","")
            perf.equalTo(self.perfect(look, word))
            if not (perf.getText() == ""):
                return perf
        infin = Word("","")
        infin.equalTo(self.infinitive(look, word))
        if not (infin.getText() == ""):
            return infin
        imp = Word("","")
        imp.equalTo(self.future(look, word))
        if not (imp.getText() == ""):
            return imp
        imper = Word("","")
        imper.equalTo(self.imperative(look, word))
        if not (imper.getText() == ""):
            return imper
        parti = Word("","")
        parti.equalTo(self.participle(look, word))
        if not (parti.getText() == ""):
            return parti
        return Word("", "")

    def verbForms(self, look, word):
        nifalW = Word("","")
        nifalW.equalTo(self.nifal(look, word))
        if not (nifalW.getText() == ""):
            return nifalW
        pilpelW = Word("","")
        pilpelW.equalTo(self.pilpel(look, word))
        if not (pilpelW.getText() == ""):
            return pilpelW
        pielW = Word("","")
        pielW.equalTo(self.piel(look, word))
        if not (pielW.getText() == ""):
            return pielW
        pualW = Word("","")
        pualW.equalTo(self.pual(look, word))
        if not (pualW.getText() == ""):
            return pualW
        hifilW = Word("","")
        hifilW.equalTo(self.hifil(look, word))
        if not(hifilW.getText() == ""):
            return hifilW 
        hufalW = Word("","")
        hufalW.equalTo(self.hufal(look, word))
        if not (hufalW.getText() == ""):
            return hufalW
        hitpaelW = Word("","")
        hitpaelW.equalTo(self.hitpael(look, word))
        if not (hitpaelW.getText() == ""):
            return hitpaelW
        hishtaphelW = Word("","")
        hishtaphelW.equalTo(self.hishtaphel(look, word))
        if not (hishtaphelW.getText() == ""):
            return hishtaphelW
        return Word("", "")

    def pilpel(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
        first = word.getText()[-1:]
        first2 = word.getText()[-2:]
        first3 = word.getText()[-3:]
        nextF = word.getText()[-2:-1]
        last = word.getText()[0:1]
        last2 = word.getText()[0:2]
        last3 = word.getText()[0:3]
        nextL = word.getText()[1:2]

        tempW = Word("","")
        tempW.equalTo(word)
        tempW.setText(self.unFinal(word.getText()))
        while tempW.getText()[1:2] == tempW.getText()[0:1]:
            tempW.setText(tempW.getText()[1:])
            tempWf = Word("","")
            tempWf.equalTo(tempW)
            tempWf.setText(self.Final(tempW.getText()))
            tempWf.setVerbform(8)
            look.find(tempWf, self.Dict)
            if (not (tempW.getText()[1:2] == tempW.getText()[0:1])) or (len(tempW.getText()) < 3):
                return tempWf
        
        tempW = Word("","")
        tempW.equalTo(word)
        tempW.setText(self.unFinal(word.getText()))
        if tempW.getText()[0:2] == tempW.getText()[2:4]: 
            tempW.setText(tempW.getText()[2:])
            tempWf = Word("","")
            tempWf.equalTo(tempW)
            tempWf.setText(self.Final(tempW.getText()))
            tempWf.setVerbform(8)
            look.find(tempWf, self.Dict)
            return tempWf
        return Word("", "")  

    def nifal(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
        first = word.getText()[-1:]
        nextF = word.getText()[-2:-1]
        if(first == 'נ'):
            nifalW = Word("","")
            nifalW.equalTo(word)
            nifalW.setText(word.getText()[:-1])
            nifalW.setVerbform(1)
            look.find(nifalW, self.Dict)
            return nifalW
        return Word("", "")
    
    def piel(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
        nextF = word.getText()[-2:-1]
        if(nextF == 'י'):
            pielW = Word("","")
            pielW.equalTo(word)
            pielW.setText(word.getText()[:-2] + word.getText()[-1])
            pielW.setVerbform(2)
            look.find(pielW, self.Dict)
            return pielW
        return Word("", "")
    
    def pual(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
        nextF = word.getText()[-2:-1]
        if(nextF == 'ו'):
            pualW = Word("","")
            pualW.equalTo(word)
            pualW.setText(word.getText()[:-2] + word.getText()[-1])
            pualW.setVerbform(3)
            look.find(pualW, self.Dict)
            return pualW
        return Word("", "")
    
    def hifil(self, look, word):
        if(len(word.getText()) < 4):
            return self.irreg(look, word)
        first = word.getText()[-1:]
        last = word.getText()[0:1]
        nextL = word.getText()[1:2]
        last2 = word.getText()[0:2]
        if((first == 'ה')and(nextL == 'י')):
            hifilW = Word("","")
            hifilW.equalTo(word)
            hifilW.setText(word.getText()[0:1] + word.getText()[2:-1])
            hifilW.setVerbform(4)
            look.find(hifilW, self.Dict)
            return hifilW
        if((first == 'ה') and (last == 'ת') and (not (last2 in plural))):
            hifilW = Word("","")
            hifilW.equalTo(word)
            hifilW.setText(word.getText()[1:-1])
            hifilW.setVerbform(4)
            look.find(hifilW, self.Dict)
            return hifilW
        return Word("", "")
    
    def hufal(self, look, word):
        if(len(word.getText()) < 4):
            return self.irreg(look, word)
        first2 = word.getText()[-2:]
        if(first2 == 'וה'):
            hufalW = Word("","")
            hufalW.equalTo(word)
            hufalW.setText(word.getText()[:-2])
            hufalW.setVerbform(5)
            look.find(hufalW, self.Dict)
            return hufalW
        return Word("", "")
    
    def hitpael(self, look, word):
        if(len(word.getText()) < 4):
            return self.irreg(look, word)
        first = word.getText()[-1:]
        first2 = word.getText()[-2:]
        nextF = word.getText()[-2:-1]
        last = word.getText()[0:1]
        last2 = word.getText()[0:2]
        nextL = word.getText()[1:2]
        
        metaW = Word("","")
        metaW.equalTo(self.metathesis(look, word))
        if not (metaW.getText() == ""):
            return self.hitpael(look, metaW)
        
        if((nextF == "ט") or (nextF == "ד") or (nextF == "נ")) and (first in preffix):
            tempW = Word("","")
            tempW.equalTo(word)
            tempW.setText(word.getText() + "ת" + first)
            return self.hitpael(look, tempW)
        
        if((first2 == 'תה') or (first2 == 'תמ' )or (first2 == 'תל') or (first2 == 'תב') or (first2 == 'תא')):
            hitpaelW = Word("","")
            hitpaelW.equalTo(word)
            hitpaelW.setText(word.getText()[:-2])
            hitpaelW.setVerbform(6)
            look.find(hitpaelW, self.Dict)
            return hitpaelW
        return Word("", "")
        
    def hishtaphel(self, look, word):
        if(len(word.getText()) < 5):
            return self.irreg(look, word)
        first3 = word.getText()[-3:]
        if(first3 == 'תשה'):
            hishtaphelW = Word("","")
            hishtaphelW.equalTo(word)
            hishtaphelW.setText(word.getText()[:-3])
            hishtaphelW.setVerbform(7)
            look.find(hishtaphelW, self.Dict)
            return hishtaphelW
        return Word("", "")
       
    def metathesis(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
        first = word.getText()[-1:]
        first2 = word.getText()[-2:]
        nextF = word.getText()[-2:-1]
        third = word.getText()[-3:-2]
        if((third == 'ת') and (nextF in metathesis)):
            tempW = Word("","")
            tempW.equalTo(word)
            tempW.setText(word.getText()[:-3] + self.rev(word.getText()[-3:-1]) + first)
            return tempW
        return Word("", "")
         
    def rev(self, text):
        revText = ""
        end = len(text)-1
        for i in range(len(text)):
            revText += text[end-i]
        return str(revText)
            
    def perfect(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
        last = word.getText()[0:1]
        last2 = word.getText()[0:2]
        if(len(word.getText()) > 3):
            if(last2 == 'ית'): 
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[2:]))
                perfW.setTense(0)
                perfW.setPerson(0)
                perfW.setGender(0)
                look.find(perfW, self.Dict)
                return perfW
            if(last2 == 'ונ'):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[2:]))
                perfW.setTense(0)
                perfW.setPerson(1)
                perfW.setGender(2)
                look.find(perfW, self.Dict)
                #return perfW
            if(last2 == 'םת'):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[2:]))
                perfW.setTense(0)
                perfW.setPerson(3)
                perfW.setGender(0)
                look.find(perfW, self.Dict)
                return perfW
            if(last2 == 'ןת'):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[2:]))
                perfW.setTense(0)
                perfW.setPerson(3)
                perfW.setGender(1)
                look.find(perfW, self.Dict)
                return perfW
        if(last == 'ו'):
            perfW = Word("","")
            perfW.equalTo(word)
            perfW.setText(self.Final(word.getText()[1:]))
            perfW.setTense(0)
            perfW.setPerson(5)
            perfW.setGender(2)
            look.find(perfW, self.Dict)
            return perfW
        if(last == 'ת'):
            perfW = Word("","")
            perfW.equalTo(word)
            perfW.setText(self.Final(word.getText()[1:]))
            perfW.setTense(0)
            perfW.setPerson(2)
            perfW.setGender(2)
            look.find(perfW, self.Dict)
            return perfW
        if(last == 'ה'):
            perfW = Word("","")
            perfW.equalTo(word)
            perfW.setText(self.Final(word.getText()[1:]))
            perfW.setTense(0)
            perfW.setPerson(4)
            perfW.setGender(1)
            look.find(perfW, self.Dict)
            return perfW
        return Word("", "")
                
    def imperRules(self, word, l):
        if ("ה- the" in word.preW) or ("ל- to" in word.preW):
            return False
        return True
                
    def future(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
        first = word.getText()[-1:]
        nextF = word.getText()[-2:-1]
        first2 = word.getText()[-2:]
        last = word.getText()[0:1]
        nextL = word.getText()[1:2]
        last2 = word.getText()[0:2]
        if(len(word.getText()) > 4):
            if((first == 'ת')and(last2 == 'הנ')) and (self.imperRules(word, 'ת') == True):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(self.Final(word.getText()[2:-1]))
                futurW.setTense(1)
                futurW.setPerson(3)
                futurW.setGender(1)
                if futurW.getText()[1:2] == 'ו':
                    futurW.setText(futurW.getText()[0:1] + futurW.getText()[2:])
                    look.find(futurW, self.Dict)
                    return futurW
                look.find(futurW, self.Dict)
                return futurW
            if (first2 == 'וי') and (last == 'ו') and (self.imperRules(word, 'וי') == True):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(word.getText()[1:-2] + word.getText()[-1])
                futurW.setTense(1)
                futurW.setPerson(2)
                futurW.setGender(1)
                if futurW.getText()[1:2] == 'ו':
                    futurW.setText(futurW.getText()[0:1] + futurW.getText()[2:])
                    look.find(futurW, self.Dict)
                    return futurW
                look.find(futurW, self.Dict)
                return futurW
        if(len(word.getText()) > 3):
            if (first2 == 'וי') and (self.imperRules(word, 'וי') == True):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(word.getText()[:-2] + word.getText()[-1])
                futurW.setTense(1)
                futurW.setPerson(4)
                futurW.setGender(0)
                if futurW.getText()[1:2] == 'ו':
                    futurW.setText(futurW.getText()[0:1] + futurW.getText()[2:])
                    look.find(futurW, self.Dict)
                    return futurW
                look.find(futurW, self.Dict)
                return futurW
            if((first == 'ת')and(last == 'ו') and (self.imperRules(word, 'ת') == True)):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(self.Final(word.getText()[1:-1]))
                futurW.setTense(1)
                futurW.setPerson(3)
                futurW.setGender(0)
                look.find(futurW, self.Dict)
                return futurW
            if((first == 'ת')and(last == 'י') and (self.imperRules(word, 'ת') == True)):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(self.Final(word.getText()[1:-1]))
                futurW.setTense(1)
                futurW.setPerson(2)
                futurW.setGender(1)
                look.find(futurW, self.Dict)
                return futurW
            if((first == 'י')and(last == 'ו') and (self.imperRules(word, 'י') == True)):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(self.Final(word.getText()[1:-1]))
                futurW.setTense(1)
                futurW.setPerson(5)
                futurW.setGender(0)
                look.find(futurW, self.Dict)
                return futurW
        if(first == 'א') and (self.imperRules(word, 'א') == True):
            futurW = Word("","")
            futurW.equalTo(word)
            futurW.setText(word.getText()[:-1])
            futurW.setTense(1)
            futurW.setPerson(0)
            futurW.setGender(2)
            if futurW.getText()[1:2] == 'ו':
                futurW.setText(futurW.getText()[0:1] + futurW.getText()[2:])
                look.find(futurW, self.Dict)
                return futurW
            look.find(futurW, self.Dict)
            return futurW
        if(first == 'י') and (self.imperRules(word, 'י') == True):
            futurW = Word("","")
            futurW.equalTo(word)
            futurW.setText(word.getText()[:-1])
            futurW.setTense(1)
            futurW.setPerson(4)
            futurW.setGender(0)
            if futurW.getText()[1:2] == 'ו':
                futurW.setText(futurW.getText()[0:1] + futurW.getText()[2:])
                look.find(futurW, self.Dict)
                return futurW
            look.find(futurW, self.Dict)
            return futurW
        if(first == 'ת') and (self.imperRules(word, 'ת') == True):
            futurW = Word("","")
            futurW.equalTo(word)
            futurW.setText(word.getText()[:-1])
            futurW.setTense(1)
            futurW.setPerson(2)
            futurW.setGender(0)
            if futurW.getText()[1:2] == 'ו':
                futurW.setText(futurW.getText()[0:1] + futurW.getText()[2:])
                look.find(futurW, self.Dict)
                
                futurW2 = Word("","")
                futurW2.equalTo(futurW)
                futurW2.setTense(1)
                futurW2.setPerson(4)
                futurW2.setGender(1)
                look.find(futurW2, self.Dict)
                return futurW
            look.find(futurW, self.Dict)
            
            futurW2 = Word("","")
            futurW2.equalTo(futurW)
            futurW2.setTense(1)
            futurW2.setPerson(4)
            futurW2.setGender(1)
            look.find(futurW2, self.Dict)
            return futurW
        if(first == 'נ') and (self.imperRules(word, 'נ') == True):
            futurW = Word("","")
            futurW.equalTo(word)
            futurW.setText(word.getText()[:-1])
            futurW.setTense(1)
            futurW.setPerson(1)
            futurW.setGender(2)
            if futurW.getText()[1:2] == 'ו':
                futurW.setText(futurW.getText()[0:1] + futurW.getText()[2:])
                look.find(futurW, self.Dict)
                return futurW
            look.find(futurW, self.Dict)
            return futurW
        return Word("", "")
        
    def imperative(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
        first = word.getText()[-1:]
        last = word.getText()[0:1]
        nextL = word.getText()[1:2]
        last2 = word.getText()[0:2]
        if(len(word.getText()) > 3):
            if last2 == 'הנ':
                imperW = Word("","")
                imperW.equalTo(word)
                imperW.setText(self.Final(word.getText()[2:]))
                imperW.setTense(4)
                imperW.setPerson(3)
                imperW.setGender(1)
                if imperW.getText()[1:2] == 'ו':
                    imperW.setText(imperW.getText()[0:1] + imperW.getText()[2:])
                    look.find(imperW, self.Dict)
                    return imperW
                look.find(imperW, self.Dict)
                return imperW
        if nextL == 'ו':
            imperW = Word("","")
            imperW.equalTo(word)
            imperW.setText(word.getText()[0:1] + word.getText()[2:])
            imperW.setTense(4)
            imperW.setPerson(2)
            imperW.setGender(0)
            look.find(imperW, self.Dict)
        if last == 'ו':
            imperW = Word("","")
            imperW.equalTo(word)
            imperW.setText(self.Final(word.getText()[1:]))
            imperW.setTense(4)
            imperW.setPerson(3)
            imperW.setGender(0)
            look.find(imperW, self.Dict)
            return imperW
        if (last == 'י') and (word.getPlural == False):
            imperW = Word("","")
            imperW.equalTo(word)
            imperW.setText(self.Final(word.getText()[1:]))
            imperW.setTense(4)
            imperW.setPerson(2)
            imperW.setGender(1)
            look.find(imperW, self.Dict)
            return imperW
        return Word("", "")
        
    def plural(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
            
        cPhrasePl = Word("","")
        cPhrasePl.equalTo(word)
        cPhrasePl.setText(self.revPhWords(word.getText(), "-"))
            
        last2 = cPhrasePl.getText()[0:2]
        last3 = cPhrasePl.getText()[0:3]
        if(len(cPhrasePl.getText()) > 4): 
            if(last3 == 'םיי') and (cPhrasePl.getSuffix() == False) and (not (cPhrasePl.getTense() == 'Perfect')):
                plW = Word("","")
                plW.equalTo(cPhrasePl)
                plW.setText(self.Final(cPhrasePl.getText()[3:]))
                plW.setDaul()
                plW.setText(self.revPhWords(plW.getText(), "-"))
                look.find(plW, self.Dict)
                return plW
        if(len(cPhrasePl.getText()) > 3):
            if(last2 == 'םי') and (cPhrasePl.getSuffix() == False) and (not (cPhrasePl.getTense() == 'Perfect')):
                plW = Word("","")
                plW.equalTo(cPhrasePl)
                plW.setText(self.Final(cPhrasePl.getText()[2:]))
                plW.setPlural()
                plW.setText(self.revPhWords(plW.getText(), "-"))
                look.find(plW, self.Dict)
                return plW
            if(last2 == 'תו'):
                plW = Word("","")
                plW.equalTo(cPhrasePl)
                plW.setText(self.Final(cPhrasePl.getText()[2:]))
                plW.setPlural()
                plW.setText(self.revPhWords(plW.getText(), "-"))
                look.find(plW, self.Dict)
                singleW = Word("","")
                singleW.equalTo(plW)
                singleW.setText('ה' + self.unFinal(plW.getText()))
                singleW.setPlural()
                look.find(singleW, self.Dict)
                return singleW
        return self.constr(look, cPhrasePl)
            
    def prefixRuls(self, word, p):
        if word.getTense() == 'Imperfect':
            return False
        if (p + '-' + " " + word.preffix[p] in word.preW):
            return False
        if ((word.preffix[p] == "in") or (word.preffix[p] == "to")) and (("ב- in" in word.preW) or ("ל- to" in word.preW)):
            return False
        if (word.getPrefix() == True) and (word.preffix[p] == "and"):
            return False
        if ("ה- the" in word.preW):
            return False
        if ((word.preffix[p] == "from") or (word.preffix[p] == "to")) and (("ב- in" in word.preW) or ("ל- to" in word.preW)):
            return False
        if (word.preffix[p] == "as") and ("ל- to" in word.preW):
            return False
        if(word.getText()[-2:-1] == 'ו') and (not (word.getText()[-3:-1] == "וו")) and (not (word.getText()[-3:-1] == "וי")):
            return False
        return True
            
    def prefix(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
            
        cPhrasePre = Word("","")
        cPhrasePre.equalTo(word)
        cPhrasePre.setText(self.revPhWords(word.getText(), "-"))
            
        first = cPhrasePre.getText()[-1:]
        
        if (first in preffix) and (self.prefixRuls(cPhrasePre, first) == True):
            preW = Word("","")
            preW.equalTo(cPhrasePre)
            preW.setText(cPhrasePre.getText()[:-1])
            preW.setPrefix()
            preW.addPre(first)
            preW.setText(self.revPhWords(preW.getText(), "-"))
            self.future(look, preW)
            if not ('-' in word.getText()):
                self.algorithm(look, preW)
            else:
                if look.find(preW, self.Dict) == False:
                    preWend = Word("","")
                    preWend.equalTo(self.prefix(look, preW))
                    if preWend.getText() == "":
                        return preW
                    else:
                        return preWend
                else:
                    return preW
        return Word("", "")
        
    def smPrefix(self, look, word):
        if(len(word.getText()) < 2):
            return self.irreg(look, word)
        first = word.getText()[-1:]
        if first in preffix:
            preW = Word("","")
            preW.equalTo(word)
            preW.setText(word.getText()[:-1])
            preW.setPrefix()
            preW.addPre(first)
            look.find(preW, self.Dict)
            return preW
        return Word("", "")  

    def suffixObj(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
        last = word.getText()[0:1]
        last2 = word.getText()[0:2]
        if(last2 == 'םי') or (word.getSuffix() == True):
            return self.irreg(look, word)
        if len(word.getText()) > 3:
            if last2 in suffix:
                suffW = Word("","")
                suffW.equalTo(word)
                suffW.setText(self.Final(word.getText()[2:]))
                suffW.setSuffix2()
                suffW.addSuff(last2)
                look.find(suffW, self.Dict)
                return suffW
        if last in suffix:
            if ((last == 'ה') and (word.getPlural() == True)):
                return Word("", "")
            suffW = Word("","")
            suffW.equalTo(word)
            suffW.setText(self.Final(word.getText()[1:]))
            suffW.setSuffix1()
            suffW.addSuff(last)
            look.find(suffW, self.Dict)
            return suffW
        return Word("", "")
    
    def suffix(self, look, word, p):
        if(len(word.getText()) < 3) or (word.getSuffix() == True):
            return self.irreg(look, word)
            
        last2 = word.getText()[0:2]
        suff1 = self.suffix1(look, word)
        suff2 = self.suffix2(look, word)
        suff3 = self.suffix3(look, word)
        if(last2 == 'םי'):
            return self.irreg(look, word)
        if p == 1:
            if not (suff1.getText() == ""):
                return suff1
        if p == 2:
            if not (suff2.getText() == ""):
                return suff2
            if not (suff1.getText() == ""):
                return suff1
        if not (suff3.getText() == ""):
            return suff3
        if not (suff2.getText() == ""):
            return suff2
        if not (suff1.getText() == ""):
            return suff1
        return Word("", "")
        
    def suffix1(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
            
        cPhraseSuf = Word("","")
        cPhraseSuf.equalTo(word)
        cPhraseSuf.setText(self.revPhWords(word.getText(), "-"))
            
        last = cPhraseSuf.getText()[0:1]
        last2 = cPhraseSuf.getText()[0:2]
        if last in suffix:
            if ((last == 'ה') and (cPhraseSuf.getPlural() == True)):
                return Word("", "")
            suffW = Word("","")
            suffW.equalTo(cPhraseSuf)
            suffW.setText(self.Final(cPhraseSuf.getText()[1:]))
            suffW.setSuffix1()
            suffW.addSuff(last)
            suffW.setText(self.revPhWords(suffW.getText(), "-"))
            look.find(suffW, self.Dict)
            return suffW
        return Word("", "")
        
    def suffix2(self, look, word):
        if(len(word.getText()) < 4):
            return self.irreg(look, word)
            
        cPhraseSuf = Word("","")
        cPhraseSuf.equalTo(word)
        cPhraseSuf.setText(self.revPhWords(word.getText(), "-"))
            
        last2 = cPhraseSuf.getText()[0:2]
        if last2 in plural:
            return self.plural(look, word)
        if last2 in suffix:
            suffW = Word("","")
            suffW.equalTo(cPhraseSuf)
            suffW.setText(self.Final(cPhraseSuf.getText()[2:]))
            suffW.setSuffix2()
            suffW.addSuff(last2)
            suffW.setText(self.revPhWords(suffW.getText(), "-"))
            look.find(suffW, self.Dict)
            return suffW
        return Word("", "")
        
    def suffix3(self, look, word):
        if(len(word.getText()) < 5):
            return self.irreg(look, word)
            
        cPhraseSuf = Word("","")
        cPhraseSuf.equalTo(word)
        cPhraseSuf.setText(self.revPhWords(word.getText(), "-"))
            
        last3 = cPhraseSuf.getText()[0:3]
        last2 = cPhraseSuf.getText()[0:2]
        if(last3 == 'וני'):
            suffW = Word("","")
            suffW.equalTo(cPhraseSuf)
            suffW.setText(self.Final(cPhraseSuf.getText()[3:]))
            suffW.setSuffix3()
            suffW.addSuff(last2)
            suffW.setPlural()
            suffW.setConstruct()
            suffW.setText(self.revPhWords(suffW.getText(), "-"))
            look.find(suffW, self.Dict)
            return suffW
        if(last3 == 'םכי'):
            suffW = Word("","")
            suffW.equalTo(cPhraseSuf)
            suffW.setText(self.Final(cPhraseSuf.getText()[3:]))
            suffW.setSuffix3()
            suffW.addSuff(last2)
            suffW.setPlural()
            suffW.setConstruct()
            suffW.setText(self.revPhWords(suffW.getText(), "-"))
            look.find(suffW, self.Dict)
            return suffW
        if(last3 == 'ןכי'):
            suffW = Word("","")
            suffW.equalTo(cPhraseSuf)
            suffW.setText(self.Final(cPhraseSuf.getText()[3:]))
            suffW.setSuffix3()
            suffW.addSuff(last2)
            suffW.setPlural()
            suffW.setConstruct()
            suffW.setText(self.revPhWords(suffW.getText(), "-"))
            look.find(suffW, self.Dict)
            return suffW
        if(last3 == 'םהי'):
            suffW = Word("","")
            suffW.equalTo(cPhraseSuf)
            suffW.setText(self.Final(cPhraseSuf.getText()[3:]))
            suffW.setSuffix3()
            suffW.addSuff(last2)
            suffW.setPlural()
            suffW.setConstruct()
            suffW.setText(self.revPhWords(suffW.getText(), "-"))
            look.find(suffW, self.Dict)
            return suffW
        if(last3 == 'ןהי'):
            suffW = Word("","")
            suffW.equalTo(cPhraseSuf)
            suffW.setText(self.Final(cPhraseSuf.getText()[3:]))
            suffW.setSuffix3()
            suffW.addSuff(last2)
            suffW.setPlural()
            suffW.setConstruct()
            suffW.setText(self.revPhWords(suffW.getText(), "-"))
            look.find(suffW, self.Dict)
            return suffW
        return Word("", "")
                
    def participle(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
        nextF = word.getText()[-2:-1]
        last = word.getText()[0:1]
        nextL = word.getText()[1:2]
        if(nextF == 'ו'):
            pword = Word("","")
            pword.equalTo(word)
            pword.setText(word.getText()[:-2] + word.getText()[-1])
            pword.setTense(2)
            look.find(pword, self.Dict)
            return pword        
        if(nextL == 'ו') and (not (last == 'ת')):
            pword = Word("","")
            pword.equalTo(word)
            pword.setText(word.getText()[0:1] + word.getText()[2:])
            pword.setTense(2)
            look.find(pword, self.Dict)
            return pword
        if(last == 'ת'):
            fimW = Word("","")
            fimW.equalTo(word)
            fimW.setText(self.Final(word.getText()[1:]))
            if(fimW.getText()[-2:-1] == 'ו'):
                pfimW = Word("","")
                pfimW.equalTo(fimW)
                pfimW.setText('ה' + self.unFinal(fimW.getText()[:-2] + fimW.getText()[-1]))
                pfimW.setTense(2)
                look.find(pfimW, self.Dict)
                return pfimW        
            if(fimW.getText()[1:2] == 'ו'):
                pfimW = Word("","")
                pfimW.equalTo(fimW)
                pfimW.setText('ה' + self.unFinal(fimW.getText()[0:1] + fimW.getText()[2:]))
                pfimW.setTense(2)
                look.find(pfimW, self.Dict)
                return pfimW
        return Word("", "")
    
    def infinitive(self, look, word):
        if(len(word.getText()) < 3):
            return self.irreg(look, word)
        first = word.getText()[-1:]
        last = word.getText()[0:1]
        last2 = word.getText()[0:2]
        if(len(word.getText()) > 3):
            if((first == 'ל')and(last2 == 'תו')):
                singleW = Word("","")
                singleW.equalTo(word)
                singleW.setText('ה' + word.getText()[2:-1])
                singleW.setTense(3)
                singleW.setPlural()
                look.find(singleW, self.Dict)
                return singleW
        if(len(word.getText()) > 3):
            if((first == 'ל')and(last == 'ת')):
                singleW = Word("","")
                singleW.equalTo(word)
                singleW.setText('ה' + word.getText()[1:-1])
                singleW.setTense(3)
                look.find(singleW, self.Dict)
                return singleW
        if(first == 'ל'):
            infW = Word("","")
            infW.equalTo(word)
            infW.setText(word.getText()[:-1])
            infW.setTense(3)
            look.find(infW, self.Dict)
            return infW
        return Word("", "")
       
    def constr(self, look, word):
        if(len(word.getText()) < 2):
            return self.irreg(look, word)
        last = word.getText()[0:1]
        nextL = word.getText()[1:2]
        if(len(word.getText()) > 3):
            if((nextL == 'ת') and (last in suffix) and (not(word.getSuffix() == True))):
                constW = Word("", "")
                constW.equalTo(word)
                constW.setText('ה' + word.getText()[2:])
                constW.setSuffix2()
                constW.setConstruct()
                constW.addSuff(last)
                constW2 = Word("", "")
                constW2.equalTo(word)
                constW2.setText(self.Final(word.getText()[2:]))
                constW2.setSuffix2()
                constW2.setConstruct()
                constW2.addSuff(last)
                look.find(constW, self.Dict)
                look.find(constW2, self.Dict)
                return constW
        if(len(word.getText()) > 2):
            if(last == 'י'):
                constW = Word("","")
                constW.equalTo(word)
                if (nextL == 'י'):
                    daulW = Word("","")
                    daulW.equalTo(word)
                    daulW.setText('ם' + word.getText())
                    daulW.setConstruct()
                    look.find(daulW, self.Dict)
                constW.setText(self.Final(word.getText()[1:]))
                constW.setPlural()
                constW.setConstruct()
                constW2 = Word("","")
                constW2.equalTo(word)
                constW2.setText('ם' + word.getText())
                constW2.setConstruct()
                look.find(constW2, self.Dict)
                look.find(constW, self.Dict)
                return constW
        if(last == 'ת'):
            constW = Word("","")
            constW.equalTo(word)
            constW.setText('ה' + word.getText()[1:])
            constW.setConstruct()
            constW2 = Word("", "")
            constW2.equalTo(word)
            constW2.setText(self.Final(word.getText()[1:]))
            constW2.setConstruct()
            look.find(constW, self.Dict)
            look.find(constW2, self.Dict)
            return constW
        return Word("", "")    
                
    def irreg(self, look, word):
        if(len(word.getText()) < 2):
            return Word("", "")
        first = word.getText()[-1:]
        nextF = word.getText()[-2:-1]
        last = word.getText()[0:1]
        nextL = word.getText()[1:2]
        
        if not ("ה- the" in word.preW):
            irregWh = Word("","")
            irregWh.equalTo(word)
            irregWh.setText('ה' + word.getText())
            irregWh.setIrreg()
            look.find(irregWh, self.Dict)
            if word.getIrreg == False:
                self.algorithm(look, irregWh)
        if(len(word.getText()) > 2):
            irregWnun = Word("","")
            irregWnun.equalTo(word)
            if(nextF == 'נ'):
                irregWnun.setText(word.getText()[:-2] + first)
                irregWnun.setIrreg()
                look.find(irregWnun, self.Dict)
                self.irreg(look, irregWnun)
        if (word.getPrefix() == True) or (word.getTense() == 'Infinitive'):
            irregW = Word("","")
            irregW.equalTo(word)
            irregW.setText(word.getText() + 'ה')
            if ("ה- the" in irregW.preW):
                irregW.rm('ה')
                irregW.decPrefix()   
            irregW.setIrreg()
            look.find(irregW, self.Dict)
            irregW2= Word("","")
            irregW2.equalTo(word)
            irregW2.setText(word.getText() + 'נ')
            irregW2.setIrreg()
            look.find(irregW2, self.Dict)
            irregW3= Word("","")
            irregW3.equalTo(word)
            irregW3.setText(word.getText() + 'י')
            irregW3.setIrreg()
            look.find(irregW3, self.Dict)
            if(len(word.getText()) > 2):
                irregWnun2 = Word("","")
                irregWnun2.equalTo(word)
                if(nextF == 'נ'):
                    irregWnun2.setText(word.getText()[:-2] + first)
                    irregWnun2.setIrreg()
                    look.find(irregWnun2, self.Dict)
                    self.irreg(look, irregWnun2)
        if(len(word.getText()) < 3):
            irreg1 = Word("","")
            irreg1.equalTo(word)
            irreg1.setText(last + 'ו' + first)
            if irreg1.getTenseVal() == 2:
                irreg1.setTense(-1)
            irreg1.setIrreg()
            look.find(irreg1, self.Dict)
       
            irreg2 = Word("","")
            irreg2.equalTo(word)
            irreg2.setText(last + 'י' + first)
            irreg2.setIrreg()
            look.find(irreg2, self.Dict)
        return Word("", "")
        
    def Final(self, text):
        if text[0] in finals.keys():
            return finals.get(text[0]) + text[1:]
        else:
            return text
            
    def unFinal(self, text):
        if text[0] in unFinals:
            return unFinals.get(text[0]) + text[1:]
        else:
            return text

    def addAction(self, instance):
        self.Word.Word.text = self.Input.text
        self.Word.Definition.text = ""
        self.popup.open()
        
    def editAction(self, instance):
        if self.Input.text in self.Dict:
            self.Word.Word.text = self.Input.text
            definition = ",  ".join(self.Dict[self.Input.text]["definition"])
            self.Word.Definition.text = definition
            self.popup.title = "Edit Word"
            self.popup.open()
        
    def removeAction(self, instance):
        if self.Input.text in self.Dict:
            word = self.Input.text
            del self.Dict[word]
            self.store.delete(word)
            
    def exitAction(self, instance):
        sys.exit(0)
        
    def closeAction(self, instance):
        self.wordPopup.dismiss()
    
        
    def cancelAction(self, instance):
        self.popup.dismiss()
    
    def enterAction(self, instance):
        word = {self.Word.Word.text: {"text": self.Word.Word.text, "definition": self.Word.Definition.text.split(",  ")}}
        self.Dict.update(word)
        self.popup.dismiss()
        self.store.put(self.Word.Word.text, text=self.Word.Word.text, definition=self.Word.Definition.text.split(",  "))
        self.Word.Definition.text = ""
        
    def build(self):
        #collecting user words form Json file (the database)
        self.store = JsonStore('data/WordsFinalFixed.json')
        
        # Building .kv file
        #with open('hebrewdictionary2.kv', encoding='utf8') as f:
            #root_widget = builder.Builder.load_string(f.read())
            
        return self.startInterface()
      
if __name__ == '__main__':
    HebrewDictionary().run()