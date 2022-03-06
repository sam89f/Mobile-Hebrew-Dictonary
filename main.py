#Hebrew Dictionary mobile aplication python file (Tablet Version)
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
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.base import runTouchApp
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from codecs import decode
import string
import os
import sys
import unicodedata

Display_Size = 30

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
suffix = ['ונ', 'םכ', 'ןכ', 'םה', 'ם', 'ןה', 'ן', 'ית', 'ינ', 'יי', 'י', 'ה', 'הנ', 'וה', 'ו', 'ך']
suffixObj = ['וה', 'וי', 'ינ', 'ה', 'ו', 'ך']
prefixL = ['תת', 'ה', 'ו', 'מ', 'ב','כ', 'ש', 'ל']
modernL = ['קינ', 'רטמ', 'הקס', 'םינו', 'דיאו', 'ןמ', 'הינמ', 'סיזניק', 'פוקס', 'היפרג', 'היצ', 'ןקי', 'הקי', 'טסי', 'םזי', 'הז', 'יל', 'יא', 'תי']
prephrase = ['ת', 'ה', 'ו', 'מ', 'ב','כ', 'ש', 'ל']
plural = ['תו', 'םי', 'םיי']
metathesis = ['ס', 'ש', 'צ']
Obj = ['םתוא', 'ןתוא', 'ךתוא', 'התוא', 'ותוא', 'ונתוא', 'םהתא', 'ןהתא', 'םכתא', 'ןכתא']
punctuation = [',', '.', ';', ':', '-', ')', '(', '[', ']', '}', '{', '*', '!']
vowels = ['ֵ']
a_roots = ['א', 'ב', 'ג', 'ד', 'ז', 'ח', 'ט', 'כ', 'ל', 'מ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ף', 'ץ']
roots = ['ג', 'ד', 'ז', 'ח', 'ט', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ף', 'ץ']
p_roots = ['ג', 'ד', 'ז', 'ח', 'ט', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ף', 'ץ']

#This class defines all the properties and methods that a Word object needs to have in order
#use the proper metrics in searching and ordering words.
class Word:
    def __init__(self, t, d):
        
        self.text = t
        self.definition = d
        self.value = 0
        self.prefix = 0
        self.r_L2 = ""
        self.preW = []
        self.sufW = []
        self.mdrnW = 'sddgfges'
        self.partiW = -1
        self.suffix1 = 0
        self.suffix2 = 0
        self.irreg = 0
        self.Ht = True
        self.modern = 0
        self.plural = 0
        self.daul = 0
        self.construct = 0
        self.verbform = -1
        self.tense = -1
        self.person = -1
        self.gender = -1
        self.Verb = False
        self.Noun = False
        self.prefixD = {"תת":"sub", "ה":"the", "ו":"and", "ב":"in", "מ":"from", "ל":"to", "כ":"as", "ש":"which"}
        self.suffix = {"ןהי":"their/them(f)", "ןה":"their/them(f)", "ן":"their/them(f)", "םהי":"their/them(m)", "םה":"their/them(m)", "ם":"their/them(m)", "הי":"her", "ה":"her", "הנ":"her", "וי":"his/him", "ו":"his/him", "וה":"his/him", "ןכי":"your/you(pl. f)", "ןכ":"your/you(pl. f)", "םכי":"your/you(pl.)", "םכ":"your/you(pl.)", "ךי":"you/your(m)", "ך":"you/your(m)", "וני":"our/us", "ונ":"our/us", "ית":"my/me", "י":"my/me", "יי":"my/me", "ינ":"my/me"}
        self.suffixObj = {"וה":"him", "וי":"his/him", "ינ":"me", "ה":"her", "ו":"his/him", "ך":"you/your"}
        self.Gender = ['m.', 'f.', '', '']
        self.Person = ['1st, sg.', '1st, pl.', '2nd, sg.', '2nd, pl.', '3rd, sg.', '3rd, pl.', '']
        self.tenses = ['Perfect', 'Imperfect', 'Participle', 'Infinitive', 'Imperative', 'Cohortative', '']
        self.parti = {1:'Active', 0:'Passive'}
        self.tenseVals = [4, 4, 4, 4, 4, 4, 1]
        self.verbforms = ['Qal', 'Niphal', 'Piel', 'Pual', 'Hiphil', 'Hophal', 'Hithpeal', 'hishtaphel', 'pilpel', '']
        self.verbformVals = [5, 5, 5, 5, 5, 5, 7, 2, 7, 1]
        self.gemontria = {'א':1, 'ב':2, 'ג':3, 'ד':4, 'ה':5, 'ו':6, 'ז':7, 'ח':8, 'ט':9, 'י':10, 'כ':20, 'ל':30, 'מ':40, 'נ':50, 'ס':60, 'ע':70, 'פ':80, 'צ':90, 'ק':100, 'ר':200, 'ש':300, 'ת':400, 'ך':20, 'ם':40, 'ן':50, 'ף':80, 'ץ':90}
        self.millenn = ['ה','ד','ג', 'ב', 'א']
        self.finals = {'כ':'ך', 'מ':'ם', 'נ':'ן', 'פ':'ף', 'צ':'ץ'}
        self.unFinals = {'ך':'כ', 'ם':'מ', 'ן':'נ', 'ף':'פ', 'ץ':'צ'}
        self.Finals = ['ך', 'ם', 'ן', 'ף', 'ץ']
        
    def __assign__(self, value):
        self.value = value.value
        self.text = value.text
        self.partiW = value.partiW
        self.definition = value.definition
        self.Verb = value.Verb
        self.Noun = value.Noun
        self.prefix = value.prefix
        self.r_L2 = value.r_L2
        self.suffix1 = value.suffix1
        self.suffix2 = value.suffix2
        self.irreg = value.irreg
        self.Ht = value.Ht
        self.modern = value.modern
        self.mdrnW = value.mdrnW
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
        self.value = newWord.value
        self.text = newWord.text
        self.partiW = newWord.partiW
        self.definition = newWord.definition
        self.Verb = newWord.Verb
        self.Noun = newWord.Noun
        self.prefix = newWord.prefix
        self.r_L2 = newWord.r_L2
        self.suffix1 = newWord.suffix1
        self.suffix2 = newWord.suffix2
        self.irreg = newWord.irreg
        self.Ht = newWord.Ht
        self.modern = newWord.modern
        self.mdrnW = newWord.mdrnW
        self.plural = newWord.plural
        self.daul = newWord.daul
        self.construct = newWord.construct
        self.verbform = newWord.verbform
        self.tense = newWord.tense
        self.person = newWord.person
        self.gender = newWord.gender
        self.preW = newWord.preW.copy()
        self.sufW = newWord.sufW.copy()
        
    def __eq__(self, newWord):
        if not (self.text == newWord.text):
            return False
        if not (self.getPrefix() == newWord.getPrefix()):
            return False
        if not (self.partiW == newWord.partiW):
            return False
        if not (self.getSuffix() == newWord.getSuffix()):
            return False
        #if not (self.getIrreg() == newWord.getIrreg()):
            #return False
        if not(self.Ht == newWord.Ht):
            return False
        if not (self.getModern() == newWord.getModern()):
            return False
        if not (self.getModernW() == newWord.getModernW()):
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
        if not (self.isVerb() == newWord.isVerb()):
            return False
        if not (self.isNoun() == newWord.isNoun()):
            return False
        return True
        
    def Is(self, newWord):
        if not (self.text == newWord.text):
            return False
        if not (self.getPrefix() == newWord.getPrefix()):
            return False
        if not (self.r_L2 == newWord.r_L2):
            return False
        if not (self.partiW == newWord.partiW):
            return False
        if not (self.getSuffix() == newWord.getSuffix()):
            return False
        #if not (self.getIrreg() == newWord.getIrreg()):
            #return False
        if not (self.getSuffix() == newWord.getSuffix()):
            return False
        if not (self.getModern() == newWord.getModern()):
            return False
        if not (self.getModernW() == newWord.getModernW()):
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
        if not (self.isVerb() == newWord.isVerb()):
            return False
        if not (self.isNoun() == newWord.isNoun()):
            return False
        return True
    
    def getText(self):
        return self.text
    
    def getDefinition(self):
        return self.definition
        
    def isVerb(self):
        return self.Verb
        
    def isNoun(self):
        return self.Noun
        
    def isParticiple(self):
        if self.partiW == -1:
            return False
        else:
            return True
        
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
        
    def getPartiVal(self):
        return self.partiW
        
    def getLen(self):
        return len(self.text)
        
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
        self.value = 100000000 - 10*(self.prefix + 1)*(self.suffix1 + 1)*(self.suffix2 + 1)*(self.plural + 1)*(self.modern + 1)*(self.irreg + 1)*(self.tenseVals[self.tense])*(self.verbformVals[self.verbform])
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
        
    def getSuffix(self):
        if (self.suffix1 > 0) or (self.suffix2 > 0):
            return True
        return False
        
    def getIrreg(self):
        if(self.irreg > 0):
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
        
    def getPar(self):
        return self.parti[self.partiW]
        
    def getPrefixVal(self):
        return self.prefix
        
    def getPrefixW(self):
        s = ""
        for pre in self.preW:
            s += pre +  '- ' + self.prefixD[pre]+ ', '
        return s[:-2]
        
    def getPrixList(self):
        return self.preW.copy()
        
    def getRL2(self):
        return self.r_L2
        
    def getSuffixW(self):
        s = ""
        for suff in self.sufW:
            s += suff + '- ' + self.suffix[suff] + ', '
        return s[:-2]
        
    def getSufxList(self):
        return self.sufW.copy()
        
    def getSumSuff(self):
        s = 0
        for suff in self.sufW:
            s = s + len(suff)
        return s
            
    def getSuffix1Val(self):
        return self.suffix1
        
    def getSuffix2Val(self):
        return self.suffix2
        
    def getIrregVal(self):
        return self.irreg
            
    def getModernVal(self):
        return self.modern
        
    def getModernW(self):
        return self.mdrnW
        
    def getPluralVal(self):
        return self.plural
        
    def getDaulVal(self):
        return self.daul
        
    def getConstructVal(self):
        return self.construct
        
    def isTense(self):
        if(self.getTenseVal() == -1):
            return False
        else:
            return True
        
    def isVerbf(self):
        if(self.getVerbformVal() == -1):
            return False
        else:
            return True
        
    def isGender(self):
        if(self.getGenderVal() == -1) or (self.getGenderVal() == 2):
            return False
        else:
            return True
        
    def isPerson(self):
        if(self.getPersonVal() == -1):
            return False
        else:
            return True
        
    def last(self):
        if len(self.text) < 1:
            raise Exception('Word object must not be less then 1')
        else:
            return self.text[0:1]
    
    def last2(self):
        if len(self.text) < 2:
            raise Exception('Word object must not be less then 2')
        else:
            return self.text[0:2]
        
    def last3(self):
        if len(self.text) < 3:
            raise Exception('Word object must not be less then 3')
        else:
            return self.text[0:3]
        
    def lastX(self, x):
        if len(self.text) < x:
            raise Exception('Word object must not be less then {}'.format(x))
        else:
            return self.text[0:x]
        
    def first(self):
        if len(self.text) < 1:
            raise Exception('Word object must not be less then 1')
        else:
            return self.text[-1:]
        
    def first2(self):
        if len(self.text) < 2:
            raise Exception('Word object must not be less then 2')
        else:
            return self.text[-2:]
        
    def first3(self):
        if len(self.text) < 3:
            raise Exception('Word object must not be less then 3')
        else:
            return self.text[-3:]
        
    def firstX(self, x):
        if len(self.text) < x:
            raise Exception('Word object must not be less then {}'.format(x))
        else:
            if x == 0:
                return ''
            else:
                return self.text[-x:]
        
    def nextToLast(self):
        if len(self.text) < 2:
            raise Exception('Word object must not be less then 2')
        else:
            return self.text[1:2]
            
    def thirdFromLast(self):
        if len(self.text) < 3:
            raise Exception('Word object must not be less then 3')
        else:
            return self.text[2:3]
        
    def fourthFromLast(self):
        if len(self.text) < 4:
            raise Exception('Word object must not be less then 4')
        else:
            return self.text[3:4]
            
    def XfromLast(self, x):
        if len(self.text) < x:
            raise Exception('Word object must not be less then 4')
        else:
            return self.text[x-1:x]
            
    def nextToFirst(self):
        if len(self.text) < 2:
            raise Exception('Word object must not be less then 2')
        else:
            return self.text[-2:-1]
    
    def fourth(self):
        if len(self.text) < 4:
            raise Exception('Word object must not be less then 4')
        else:
            return self.text[-4:-3]
        
    def third(self):
        if len(self.text) < 3:
            raise Exception('Word object must not be less then 3')
        else:
            return self.text[-3:-2]
            
    def second(self):
        if len(self.text) < 2:
            raise Exception('Word object must not be less then 2')
        else:
            return self.text[-2:-1]
        
    def getX(self, x):
        if len(self.text) < x:
            raise Exception('Word object must not be less then {}'.format(x))
        else:
            if x == 0:
                return self.text[-1:]
            else:
                return self.text[-x:-(x-1)]
        
    def XtoY(self, x, y):
        if len(self.text) < y:
            raise Exception('Word object must not be less then {}'.format(y))
        else:
            if x == 0:
                return self.text[-y:]
            else:
                return self.text[-y:-x]

    def Final(self, text):
        if text[0] in self.finals.keys():
            if len(text) > 1:
                return self.finals.get(text[0]) + text[1:]
            else:
                return finals.get(text[0])
        else:
            return text
            
    def unFinal(self, text):
        if text[0] in unFinals:
            return unFinals.get(text[0]) + text[1:]
        else:
            return text

    def setPrefix(self):
        self.prefix += 3
        
    def setRL2(self, L2):
        self.r_L2 = L2
        
    def resetPrefix(self):
        self.prefix = 0
        
    def decPrefix(self):
        self.prefix = self.prefix -3
        
    def decSuffix1(self):
        self.suffix1 = self.suffix1 -5
        
    def setVerb(self):
        self.Verb = True
        self.Noun = False
        
    def setNoun(self):
        self.Noun = True
        self.Verb = False
        
    def unSetVerb(self):
        self.verb = False
        
    def unSetNoun(self):
        self.Noun = False
    
    def setSuffix1(self):
        self.suffix1 += 5
        
    def setSuffix2(self):
        self.suffix2 += 6
          
    def setIrreg(self):
        self.irreg += 9
          
    def setModern(self):
        self.modern += 6
        
    def setPlural(self):
        self.plural += 1
        
    def resetPlural(self):
        self.plural = 0
        
    def setDaul(self):
        self.daul += 1
        
    def setConstruct(self):
        self.construct = 3
        
    def resetConstruct(self):
        self.construct = 0
        
    def setTense(self, t):
        self.tense = t
        isTense = True
        
    def setPar(self, p):
        self.partiW = p
        
    def setPerson(self, p):
        self.person = p
        isPerson = True
        
    def setGender(self, g):
        self.gender = g
        isGender = True
        
    def setVerbform(self, verb):
        self.verbform = verb
        isVerbf = True
    
    def setText(self, t):
        self.text = t
    
    def setDefinition(self, d):
        self.definition = d
    
    def setValue(self, v):
        self.value = v
    
    def addPre(self, pre):
        self.preW.append(pre)
        
    def addSuff(self, suff):
        self.sufW.append(suff)
        
    def setMdrn(self, modr):
        self.mdrnW = modr
        
    def rm(self, pre):
        self.preW.remove(pre)
        
    def rmSuf(self, suff):
        self.sufW.remove(suff)
        
    def addToValue(self, v):
        self.value = self.value + v
        
    def isFinal(self, l):
        if l in self.Finals:
            return True
        else:
            return False
            
    def isYear(self):
        if (self.getLen() < 2) or (self.isFinal(self.last())):
            return False
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
        Y = Year - 3761
        Ep = ""
        if Y > 0:
            Ep = "C.E."
        if Y < 0:
            Ep = "B.C."
        Year = 'Year: ' + str(Y) + Ep
        return str(abs(Y)) + " " + Ep
        
        
    def isNumb(self):
        if(self.getLen() < 1):
            return False
        if self.isFinal(self.last()):
            return False
            
        nText = self.text.strip('"')
        nText = nText.strip("'")
        if len(self.getText()) > 1:
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
                
    def find(self, w, Dict):
        if  w in self.getWords():
            index = self.indexWords(w)
            if self.Words[index].getValue() < w.getValue():
                self.Words[index].setValue(w.getValue())
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
        
    def rDashAction(self, instance):
        words = self.main.Input.text.split('-')
        h = int((len(words) - 1)/2)
        for i in range(len(words) - 1, h, -1):
            temp = words[(len(words) - 1) - i]
            words[(len(words) - 1) - i] = words[i]
            words[i] = temp
        self.main.Input.text = "-".join(words)
        
    def clearAction(self, instance):
        self.main.Input.text = ""
        
    def spaceAction(self, instance):
        self.main.Input.text = " " + self.main.Input.text
        
    def backspaceAction(self, instance):
        self.main.Input.text = self.main.Input.text[1:]
        
    def backspWAction(self, instance):
        inputL = self.main.Input.text.split()
        if len(inputL) < 2:
            self.main.Input.text = ""
        else:
            inputL = inputL[1:]
            if len(inputL) > 1:
                self.main.Input.text =  " ".join(inputL)
            else:
                self.main.Input.text = inputL[0]
                
    def dashifyAction(self, instance):
        if '-' in self.main.Input.text:
            inputL = self.main.Input.text.split('-')
            self.main.Input.text =  " ".join(inputL)
        else:
            inputL = self.main.Input.text.split()
            self.main.Input.text =  "-".join(inputL)  
        
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
        self.X = 0
        self.Y = 0
        self.readText = TextInput(readonly=True, multiline=True, base_direction='rtl', size_hint=[5, 0.3], focus=False, font_name='data/fonts/times', font_size=Display_Size)
        self.display = TextInput(readonly=True, multiline=True, focus=False, size_hint_x=5, size_hint_y=None, font_name='data/fonts/times', font_size=Display_Size)
        self.display.bind(minimum_height=self.display.setter('height'))
        dRoot = ScrollView(size_hint=(5, 1), size=(Window.width, Window.height))
        dRoot.add_widget(self.display)
        self.SubPanal = GridLayout(rows=1, size_hint=[5, 0.1])
        self.closeB = Button(text='[color=FFFFFF]Close[color=FFFFFF]', font_name='data/fonts/times', font_size=20, markup=True)
        self.closeB.bind(on_press=instance.closeAction)
        self.SubPanal.add_widget(self.closeB)
        self.add_widget(self.readText)
        self.add_widget(dRoot)
        self.add_widget(self.SubPanal)
             
        
#Inerface for adding a new word to the dictionary
class AddWord(GridLayout):
    def __init__(self, instance, **kwargs):
        super(AddWord, self).__init__(**kwargs)
        self.cols = 2
        
        self.wLabel = Label(text='[color=3333ff]Word[color=3333ff]', outline_color=black, font_size=50, markup=True)
        self.dLabel = Label(text='[color=3333ff]Diffinition[color=3333ff]', outline_color=black, font_size=50, markup=True)
        self.Word = TextInput(text="", readonly=False, multiline=False, font_name='data/fonts/times', font_size=Display_Size)
        self.Definition= TextInput(text="", readonly=False, multiline=False, font_name='data/fonts/times', font_size=Display_Size)
        
        self.enterB = Button(text='[color=000000]Enter[color=000000]', font_name='data/fonts/times', font_size=20, markup=True)
        self.enterB.bind(on_press=instance.enterAction) 
        self.cancelB = Button(text='[color=000000]Cancel[color=000000]', font_name='data/fonts/times', font_size=20, markup=True)
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
        self.Plural = ['םי', 'םיי', 'תו']
        self.CurrentWord = Word("", "")
        self.y_end = 0
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
        self.Input = TextInput(readonly=False, multiline=False, base_direction='rtl', font_name='data/fonts/times', font_size=Display_Size)
        self.findB = Button(text='FindW', border=[1,1,1,1], font_name='data/fonts/times', font_size=20, markup=True)
        self.findB.bind(on_press=self.findAction)
        self.addB = Button(text='AddW', border=[1,1,1,1], font_name='data/fonts/times', font_size=20, markup=True)
        self.addB.bind(on_press=self.addAction)
        self.editB = Button(text='EditW', border=[1,1,1,1], font_name='data/fonts/times', font_size=20, markup=True)
        self.editB.bind(on_press=self.editAction)
        self.removeB = Button(text='RemoveW', border=[1,1,1,1], font_name='data/fonts/times', font_size=20, markup=True)
        self.removeB.bind(on_press=self.removeAction)
        self.exitB = Button(text='Exit', border=[1,1,1,1], font_name='data/fonts/times', font_size=20, markup=True)
        self.exitB.bind(on_press=self.exitAction)
        self.KeyboardPanal = Keyboard(self)
        self.MainPanal.add_widget(Label(text='[color=3333ff]Hebrew Dictionary[color=3333ff]', font_name='data/fonts/times', outline_color=white, outline_width=1, font_size=45, markup=True))
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
    
    def Final(self, text):
        if text[0] in finals.keys():
            if len(text) > 1:
                return finals.get(text[0]) + text[1:]
            else:
                return finals.get(text[0])
        else:
            return text
            
    def unFinal(self, text):
        if text[0] in unFinals:
            return unFinals.get(text[0]) + text[1:]
        else:
            return text

    def addAction(self, instance):
        fixedInput = self.revPhWords(self.Input.text, "-")
        if fixedInput not in self.Dict:
            self.Word.Word.text = self.Input.text
            self.Word.Definition.text = ""
            self.popup.open()
        
    def editAction(self, instance):
        fixedInput = self.revPhWords(self.Input.text, "-")
        if fixedInput in self.Dict:
            self.Word.Word.text = self.Input.text
            definition = ",  ".join(self.Dict[fixedInput]["definition"])
            self.Word.Definition.text = definition
            self.popup.title = "Edit Word"
            self.popup.open()
        
    def removeAction(self, instance):
        fixedInput = self.revPhWords(self.Input.text, "-")
        if fixedInput in self.Dict:
            word = fixedInput
            del self.Dict[word]
            self.store.delete(word)
            
    def exitAction(self, instance):
        sys.exit(0)
        
    def closeAction(self, instance):
        self.DWords.X = 0
        self.DWords.Y = 0
        self.wordPopup.dismiss()
        
    def cancelAction(self, instance):
        self.popup.dismiss()
    
    def enterAction(self, instance):
        self.Word.Word.text = self.revPhWords(self.Input.text, "-")
        word = {self.Word.Word.text: {"text": self.Word.Word.text, "definition": self.Word.Definition.text.split(",  ")}}
        self.Dict.update(word)
        self.popup.dismiss()
        self.store.put(self.Word.Word.text, text=self.Word.Word.text, definition=self.Word.Definition.text.split(",  "))
        self.Word.Definition.text = ""
            
    def findAction(self, instance):
        if len(self.Input.text) == 0:
            return
        self.wText = ''
        inputBuff = self.Input.text.replace('-', ' ')
        words = inputBuff.split()

        for i in range(len(words)):
            for j in range(len(punctuation)):
                words[i] = words[i].strip(punctuation[j])
                
        for w in range(len(words)):
            words[w] = words[w].replace("ֹו", "ו")
            words[w] = words[w].replace("ֹ", "ו") 
            words[w] = words[w].replace("ֻ", "ו")
            words[w] = words[w].replace("ִיַ", "יי")
            words[w] = words[w].replace("ֵ", "")
            words[w] = words[w].replace("ִ", "")
            words[w] = words[w].replace("ַ", "")
            words[w] = words[w].replace("ָ", "")
            words[w] = words[w].replace("ׁ", "")
            words[w] = words[w].replace("ׂ", "")
            words[w] = words[w].replace("ּ", "")
            words[w] = words[w].replace("ֱ", "")
            words[w] = words[w].replace("ֵ", "")
            words[w] = words[w].replace("ְ", "")
            words[w] = words[w].replace("ֶ", "")
            words[w] = words[w].replace("ֲ", "")
            words[w] = words[w].replace("ֳ", "")
            words[w] = words[w].replace("ֽ", "")
            words[w] = words[w].replace("ֺ", "ו")

        words = self.revWords(words)
        words = self.getPhrase(words)
        tk = len(words)
        
        self.wordPopup.open()
        for i in range(len(words)):
            k = len(words[i].split('-'))
            self.getWList(words, i, tk, k, 0)
            if not(i == len(words)):
                self.wText += '\n'
                self.wText += "*"*125
                self.wText += '\n\n'
        
        #self.y_end = self.DWords.display.cursor_col
        self.DWords.display.cursor = (0, 0)
        #Popup(title='Word', content=TextInput(text=str(words), readonly=True, multiline=False, base_direction='rtl', font_name='data/fonts/times', font_size=25)).open()
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
                self.CurrentWord.equalTo(phraseW)
                
                cPhrasePl = Word(fixedPhrase, "")
                cPhrasePl.equalTo(self.plural(check, phraseW))
                
                cPhrasePch = Word(fixedPhrase, "")
                cPhrasePch.equalTo(self.prexChainRapper(check, phraseW))

                cPhrasePre = Word(fixedPhrase, "")
                cPhrasePre.equalTo(self.prefix(check, phraseW))
                
                cPhraseSuf = Word(fixedPhrase, "")
                cPhraseSuf.equalTo(self.suffix(check, phraseW, 3))
                
                if (((check.find(phraseW, self.Dict) == True)) or (check.find(cPhrasePch, self.Dict)) or (check.find(cPhrasePl, self.Dict)) or (check.find(cPhrasePre, self.Dict)) or (check.find(cPhraseSuf, self.Dict)) or (check.find(self.suffix(check, self.prefix(check, phraseW), 3), self.Dict)) or (check.find(self.plural(check, self.prefix(check, phraseW)), self.Dict)) or (check.find(self.prexChainRapper(check, self.prefix(check, phraseW)), self.Dict))) and (end > 1):
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
                        zPhrasePre = Word(prephraseW, "")
                        zPhrasePre.equalTo(self.prefix(check, prephraseW))
                        if (check.find(prephraseW, self.Dict) == True) or (check.find(zPhrasePre, self.Dict)):
                            tempWs[i] = prePhrase
                            tempWs[i+1] = tempWs[i+1]
                            break                   
        return tempWs[0:(end)]
        
    def getWList(self, text, i, tk, k, n):
    
        number = ''
        Year = ''
        sText = text[i].strip('"')
        sText = sText.strip("'")
        look = SearchWord()
        isVerb = False
        yWord = Word(text[i], "")
        if yWord.isYear() == True:
            Year = 'Year: ' + str(yWord.getYear())
        word = Word(text[i], "")
        self.CurrentWord.equalTo(word)
        if(tk > i+1):
            if not (((text[i+1] in Obj) or (text[i+1] == 'תא')) and (self.tense(look, word, False) == True)):
                if word.isNumb() == True:
                    number = '#: ' + str(word.getGemontria()) + '; '
                else:
                    preNum = self.smPrefix(look, word)
                    if preNum.getLen() > 0:
                        if (preNum.isNumb() == True) and (not preNum.getText() == ""):
                            number = '#: ' + "with prefix [" + preNum.getPrefixW() + '] ' + str(preNum.getGemontria()) + '; '       
            else:
                isVerb = True
        else:
            if word.isNumb() == True:
                number = '#: ' + str(word.getGemontria()) + '; '
            else:
                preNum = self.smPrefix(look, word)
                if preNum.getLen() > 0:
                    if (preNum.isNumb() == True) and (not preNum.getText() == ""):
                        number = '#: ' + "with prefix [" + preNum.getPrefixW() + '] ' + str(preNum.getGemontria()) + '; '
                        
        self.wText += '\t\t'*n + ':' + (self.revPhWords(text[i], '-')) + '   ' + number + Year + '\n'
         
        if word.getText() == "הוהי":
            word.setNoun()
            look.find(word, self.Dict)
        else:
            if isVerb == True:
                word.setVerb()
            look.find(word, self.Dict)
            self.algorithm(look, word)
            
        WList = look.getWords()
        WList.sort(key=look.getValue, reverse = True)
        if(len(look.getWords()) > 0):
            for wi in WList:  
                w = Word("", "")
                w.equalTo(wi)
                w.setText(self.revPhWords(wi.getText(), '-'))
                val = ""
                if w.isVerb() == True:
                    val = "verb: "
                    if w.isTense() == False:
                        if 'ו' in w.getPrixList():
                            w.setTense(1)
                        else:
                            w.setTense(0)
                        w.setGender(0)
                        w.setPerson(4) 
                        
                if w.isNoun() == True:
                    val = "noun: "
                SPACE = ' '
                TAB = "    "            
                TAB2 = TAB*2
                preSP = ''
                suffSP = ''
                gr = False
                prL = ''
                prR = ''
                pl = ""
                pre = ""
                suff = ""
                dl = ""
                modern = ''   
                constr = ''
                s1 = ""
                s2 = ""
                s3 = ''
                s4 = ''
                s5 = ''
                s6 = ''
                s7 = ''
                s8 = ''
                
                if(not(w.getVerbformVal() == -1)) or (not(w.getTenseVal() == -1)) or (not(w.getPersonVal() == -1)) or (not(w.getGenderVal() == -1)) or (w.getPlural() == True) or (w.getDaul() == True) or (w.getSuffix() == True) or (w.getPrefix() == True) or (w.getConstruct() == True):
                    gr = True
                if w.getModern() == True:
                    if gr == True:
                        modern = "modern suffix:" + " [" + w.getModernW() + ']' + " "
                    else:
                        modern = "modern suffix:" + " [" + w.getModernW() + ']'
                if (not(w.getVerbform() == '')):
                    if(w.getPlural() == True) or (w.getDaul() == True) or (not(w.getTenseVal() == -1)) or (w.getSuffix() == True) or (w.getConstruct() == True) or (w.isGender() == True) or (w.isPerson() == True):
                        s1 = " "
                if (not(w.getTense() == '')):
                    if(w.getPlural() == True) or (w.getDaul() == True) or (w.getSuffix() == True) or (w.getConstruct() == True) or (w.isGender() == True) or (w.isPerson() == True):
                        s2 = " "
                if (w.isPerson() == True):
                    if(w.getPlural() == True) or (w.getDaul() == True) or (w.getSuffix() == True) or (w.getConstruct() == True) or (w.isGender() == True):
                        s3 = " "
                if (w.getGenderVal() == 0) or (w.getGenderVal() == 1):
                    if(w.getPlural() == True) or (w.getDaul() == True) or (w.getSuffix() == True) or (w.getConstruct() == True):
                        s4 = " "
                if w.getConstruct() == True:
                    constr = "const."
                    if(w.getPlural() == True) or (w.getDaul() == True) or (w.getSuffix() == True):
                        s5 = " "
                if w.getPrefix() == True:
                    pre = "prefix"
                    s6 = " [" + w.getPrefixW() + ']'
                    if(w.getPlural() == True) or (w.getDaul() == True) or (not(w.getTenseVal() == -1)) or (w.getSuffix() == True) or (w.getConstruct() == True) or (w.isGender() == True) or (w.isPerson() == True) or (w.isVerbf() == True):
                        preSP = ' '
                if w.getSuffix() == True:
                    suff = "suffix"
                    s7 = " [" + w.getSuffixW() + ']'
                    if(w.getPlural() == True) or (w.getDaul() == True):
                        suffSP = ' '
                if w.getPlural() == True:
                    pl = "pl."
                    s8 = " "
                if w.getDaul() == True:
                    pl = "daul"
                    s8 = " "
                
                #val = "val = " + str(w.getValue()) + " -- "
                    
                definition = ", ".join(w.definition)
                if gr == True:
                    prL = '('
                    prR = ')'
                    
                verbform = w.getVerbform()
                mult = 1
                if(w.getTense() == 'Participle'):
                    tense = w.getPar() + " " + w.getTense()
                    tense2 = w.getPar() + "        "
                    #mult = 2
                else:
                    tense = w.getTense()
                    tense2 = tense
                    mult = 6
                person = w.getPerson()
                gender = w.getGender()
                
                preN = w.getPrefixVal()
                cn = 0
                if (w.getConstruct() == True) and (w.getSuffix() == True):
                    cn = 5
                
                script = TAB2*n + TAB2 + val + (modern[:-3])*2 + prL + (pre) + (s6[:-(preN-1)])*(2) + preSP + (verbform)*2 + s1 + (tense2)*(2) + s2*mult + person + s3 + gender + s4 + (constr[:-1])*2 + s5 + (suff) + (s7[:-1])*(2) + suffSP + pl*2 + prR + "- " + (w.getText()[:-1])*(2) + TAB + '-' + TAB
                spaces = len(script) - cn
                self.wText += '\t\t'*n +  '\t\t' + val + modern + prL + pre + s6 + preSP + w.getVerbform() + s1 + tense + s2 + w.getPerson() + s3 + w.getGender() + s4 + constr + s5 + suff + s7 + suffSP + pl + prR + "- " + w.getText() + '\t' + '-' + '\t' + self.fixDef(definition, spaces) + ';' + ' gmra. = ' + str(w.getGemontria()) + '\n'
        else:
            self.wText += '\t\t'*n +  "No words found"
            self.wText += '\n'
            
        if k > 1:
            self.wText += '\t\t'*(n+1) + "-"*181
            self.wText += '\n'
            Lwords = []
            t1 = text[i].split('-')[0]
            Lwords.append(t1)
            subText = text[i].split('-')[1:]
            Lwords.extend(self.getPhrase(subText))
            #Lwords = text.split('-')
            for lw in range(len(Lwords)):
                if (len(Lwords[lw]) == 1) and (k == 2):
                    self.wText += '\t\t'*(n+1) + Lwords[lw] + " " + "(prefix)"
                    if not(lw == len(Lwords)-1):
                        self.wText += '\t\t'*(n+1) + "-"*181
                    self.wText += '\n'
                else:
                    self.getWList(Lwords, lw, len(Lwords), len(Lwords[lw].split('-')), n+1)
                    if not(lw == len(Lwords)-1):
                        self.wText += '\t\t'*(n+1) + "-"*181
                        self.wText += '\n'
            
        #self.wText += "*********" + self.CurrentWord.last2() + "*********"
        self.DWords.readText.text = self.fix(self.Input.text)
        self.DWords.display.text = self.wText
        
        
        
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
        n = 150
        diff = 0
        for i in range(len(words)):
            diff += len(words[i]) + 1
            if ((diff + spaces*0.70) > n):
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
        
                
    def num_of_roots(self, s):
        if len(s) == 0:
            return 0
            
        n = 0
        for i in s:
            if i in roots:
                n = n+1
                
        return n
        
        
    def num_of_a_roots(self, s):
        if len(s) == 0:
            return 0
        
        rev_s = self.rev(s)
        suf = ['ה', 'ת']
        n = 0
        temp = 0
        for i in rev_s:
            if i in a_roots:
                n = n+1 
                n = n+temp
                temp = 0
            elif i in suf:
                temp = temp+1
                          
        return n
      
      
    def num_of_p_roots(self, s):
        if len(s) == 0:
            return 0
            
        pre = ['ה', 'ת', 'א', 'ב', 'כ', 'ל', 'מ', 'ש']
        n = 0
        temp = 0
        for i in s:
            if i in p_roots:
                n = n+1
                n = n+temp
                temp = 0
            elif i in pre:
                temp = temp+1
                
        return n
      
      
    def algorithm(self, look, word):
        if word.getLen() < 2:
            return Word("", "")
        plural = False
        
        self.prexChainRapper(look, word)

        self.prefix(look, word)
        
        self.participle(look, word)
        
        self.suffix(look, word, 2)

        if(word.isVerb() == False):
            self.plural(look, word)
            self.constr(look, word)
            self.modern(look, word)
        
        
        if(word.isNoun() == False):
            #self.suffixObj(look, word)
            if self.plural(look, word) == Word("", ""):
                self.tense(look, word, True)
        self.verbForms(look, word)
            
        
        self.irreg(look, word)
                
    def FindHelper(self, look, w, Dict):
        if ((w.getLen() < 3) and ((w.getTense() == 'Participle')or(w.getVerbform() == 'Hiphil')or(w.getVerbform() == 'Pual')or(w.getVerbform() == 'Piel'))):
            return False
        else:
            return look.find(w, Dict)
    
    def modern(self, look, word):
        if(word.getLen() < 3) or (word.isTense() == True) or (word.isVerbf() == True):
            return Word("", "")
                
            if (word.first2() == 'תת') and (word.getSuffix() == False) and (not(word.getPartiVal() == 1)):
                mdrnW = Word("","")
                mdrnW.equalTo(word)
                mdrnW.setText(word.getText()[:-2])
                #mdrnW.setModern()
                mdrnW.setPrefix()
                mdrnW.addPre('תת')
                self.FindHelper(look, mdrnW, self.Dict)
                self.algorithm(look, mdrnW)
                return mdrnW
                
        if(word.getPartiVal() == 0) or (word.getSuffix() == True):
            return Word("","")
                
        if(word.getLen() > 6):
            if word.lastX(5) in modernL:
                mdrnW = Word("","")
                mdrnW.equalTo(word)
                mdrnW.setText(self.Final(word.getText()[5:]))
                mdrnW.setModern()
                mdrnW.setMdrn(word.lastX(5))
                self.FindHelper(look, mdrnW, self.Dict)
                self.algorithm(look, mdrnW)
                if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())):
                    mdrnWh = Word("","")
                    mdrnWh.equalTo(mdrnW)
                    mdrnWh.setText('ה' + self.unFinal(mdrnW.getText()))
                    self.FindHelper(look, mdrnWh, self.Dict)
                return mdrnW
                
        if(word.getLen() > 5):
            if word.lastX(4) in modernL:
                mdrnW = Word("","")
                mdrnW.equalTo(word)
                mdrnW.setText(self.Final(word.getText()[4:]))
                mdrnW.setModern()
                mdrnW.setMdrn(word.lastX(4))
                self.FindHelper(look, mdrnW, self.Dict)
                self.algorithm(look, mdrnW)
                if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())):
                    mdrnWh = Word("","")
                    mdrnWh.equalTo(mdrnW)
                    mdrnWh.setText('ה' + self.unFinal(mdrnW.getText()))
                    self.FindHelper(look, mdrnWh, self.Dict)
                return mdrnW
                
        if(word.getLen() > 4):
            if word.last3() in modernL:
                mdrnW = Word("","")
                mdrnW.equalTo(word)
                mdrnW.setText(self.Final(word.getText()[2:]))
                mdrnW.setModern()
                mdrnW.setMdrn(word.last2())
                self.FindHelper(look, mdrnW, self.Dict)
                mdrnW2 = Word("","")
                mdrnW2.equalTo(word)
                mdrnW2.setText(self.Final(word.getText()[3:]))
                mdrnW2.setModern()
                mdrnW2.setMdrn(word.last3())
                self.FindHelper(look, mdrnW2, self.Dict)
                self.algorithm(look, mdrnW2)
                if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())):
                    mdrnWh = Word("","")
                    mdrnWh.equalTo(mdrnW2)
                    mdrnWh.setText('ה' + self.unFinal(mdrnW2.getText()))
                    self.FindHelper(look, mdrnWh, self.Dict)
                return mdrnW2
                
        if(word.getLen() > 3):
            if (word.last2() in modernL):
                mdrnW = Word("","")
                mdrnW.equalTo(word)
                mdrnW.setText(self.Final(word.getText()[2:]))
                mdrnW.setModern()
                mdrnW.setMdrn(word.last2())
                self.FindHelper(look, mdrnW, self.Dict)
                self.algorithm(look, mdrnW)
                if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())):
                    mdrnWh = Word("","")
                    mdrnWh.equalTo(mdrnW)
                    mdrnWh.setText('ה' + self.unFinal(mdrnW.getText()))
                    self.FindHelper(look, mdrnWh, self.Dict)
                return mdrnW
            
        if (word.last() in modernL):
            mdrnW = Word("","")
            mdrnW.equalTo(word)
            mdrnW.setText(self.Final(word.getText()[1:]))
            mdrnW.setModern()
            mdrnW.setMdrn(word.last())
            self.FindHelper(look, mdrnW, self.Dict)
            self.algorithm(look, mdrnW)
            if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())):
                mdrnWh = Word("","")
                mdrnWh.equalTo(mdrnW)
                mdrnWh.setText('ה' + self.unFinal(mdrnW.getText()))
                self.FindHelper(look, mdrnWh, self.Dict)
                
            return mdrnW
            
        return Word("", "")

    def tense(self, look, word, alg):
        if(word.getLen() < 3) or (word.isTense() == True) or ((word.getVerbform() == 'Niphal')or((word.getVerbform() == 'Hophal') and (self.CurrentWord.first() == 'ה'))or((word.getVerbform() == 'Hiphil') and (self.CurrentWord.first() == 'ה'))):
            return False
            
        revCW = self.rev(self.CurrentWord.getText())
        posTov = revCW.find("ת", 0, 4)
        if not ((posTov == -1) or (posTov == 0)):
            if(revCW[posTov-1] == 'ה') and (word.getVerbform() == 'Hithpeal'):
                return False
                
        parti = Word("","")
        parti.equalTo(self.participle(look, word))
        #if not (parti.getText() == ""):
            #if alg == True:
                #self.algorithm(look, parti)
            #return True
            
        if(word.isNoun() == True):
            return False
            
        if (word.getPlural() == True) or (word.getDaul() == True) or (word.getConstruct() == True) or ('מ' in word.getPrixList()) or ('ל' in word.getPrixList()) or ('ה' in word.getPrixList()):
            return False
        
        perf = Word("","")
        perf.equalTo(self.perfect(look, word))
        if not (perf.getText() == ""):
            if alg == True:
                self.algorithm(look, perf)
            #return True
        
        infin = Word("","")
        if (not (('מ' in word.getPrixList()) or ('ל' in word.getPrixList()) or ('כ' in word.getPrixList()) or ('ה' in word.getPrixList()))) and (word.getTenseVal() == -1):
            infin.equalTo(self.infinitive(look, word))
            if not (infin.getText() == ""):
                if alg == True:
                    self.algorithm(look, infin)
                #return True
        
        imp = Word("","")
        if(word.isTense() == False):
            imp.equalTo(self.future(look, word))
            if not (imp.getText() == ""):
                if alg == True:
                    self.algorithm(look, imp)
                #return True
            
        if(word.isTense() == False):
            imper = Word("","")
            imper.equalTo(self.imperative(look, word))
            if not (imper.getText() == ""):
                if alg == True:
                    self.algorithm(look, imper)
                #return True
                
        if(word.isTense() == False):
            cohor = Word("","")
            cohor.equalTo(self.cohortative(look, word))
            if not (cohor.getText() == ""):
                if alg == True:
                    self.algorithm(look, cohor)
                
        if (not (infin.getText() == "")) or (not (perf.getText() == "")) or (not (imp.getText() == "")):
            return True
        else:
            return False

    def verbForms(self, look, word):
        if (word.getLen() < 2) or (word.isVerbf() == True) or (word.getIrreg() == True):
            return Word("","")

        nifalW = Word("","")
        nifalW.equalTo(self.nifal(look, word))
        if not (nifalW.getText() == ""):
            self.algorithm(look, nifalW)

        pilpelW = Word("","")
        pilpelW.equalTo(self.pilpel(look, word))
        if not (pilpelW.getText() == ""):
            self.irreg(look, pilpelW)

        pielW = Word("","")
        pielW.equalTo(self.piel(look, word))
        if not (pielW.getText() == ""):
            self.algorithm(look, pielW)

        pualW = Word("","")
        pualW.equalTo(self.pual(look, word))
        if not (pualW.getText() == ""):
            self.algorithm(look, pualW)
            
        hifilW = Word("","")
        hifilW.equalTo(self.hifil(look, word))
        if not(hifilW.getText() == ""):
            self.algorithm(look, hifilW)
            
        hufalW = Word("","")
        hufalW.equalTo(self.hufal(look, word))
        if not (hufalW.getText() == ""):
            self.algorithm(look, hufalW)
            
        hitpaelW = Word("","")
        hitpaelW.equalTo(self.hitpael(look, word))
        if not (hitpaelW.getText() == ""):
            self.algorithm(look, hitpaelW)
            
        return Word("", "")

    def pilpel(self, look, word):
        if(word.getLen() < 3):
            return Word("","")

        tempW = Word("","")
        tempW.equalTo(word)
        tempW.setText(self.unFinal(word.getText()))
        while tempW.nextToLast() == self.unFinal(tempW.last()):
            tempW.setText(self.Final(tempW.getText()[1:]))
            tempWf = Word("","")
            tempWf.equalTo(tempW)
            if(not((tempW.last() == 'י') or (tempW.last() == 'ו'))):
                tempWf.setText(self.Final(tempW.getText()))
                tempWf.setVerbform(8)
            self.FindHelper(look, tempWf, self.Dict)
            if (not (tempW.nextToLast() == self.unFinal(tempW.last()))) or (len(tempW.getText()) < 3):
                return tempWf
        
        tempW = Word("","")
        tempW.equalTo(word)
        tempW.setText(self.unFinal(word.getText()))
        if tempW.last2() == self.Final(tempW.getText()[2:4]): 
            tempW.setText(self.Final(tempW.getText()[2:]))
            tempWf = Word("","")
            tempWf.equalTo(tempW)
            tempWf.setText(self.Final(tempW.getText()))
            tempWf.setVerbform(8)
            self.FindHelper(look, tempWf, self.Dict)
            return tempWf
        return Word("", "")  

    def nifal(self, look, word):
        if(len(word.getText()) < 3) or (word.getIrreg() == True):
            return Word("","")

        if(word.first() == 'נ'):
            nifalW = Word("","")
            nifalW.equalTo(word)
            nifalW.setText(word.getText()[:-1])
            nifalW.setVerbform(1)
            self.FindHelper(look, nifalW, self.Dict)
            return nifalW
        return Word("", "")
    
    def piel(self, look, word):
        if(len(word.getText()) < 4):
            return Word("","")

        if(word.XtoY(1, 3) == 'יי') and (self.num_of_a_roots(word.getText()[:-3]) < 3):
            pielW = Word("","")
            pielW.equalTo(word)
            pielW.setText(word.getText()[:-3] + word.first())
            pielW.setVerbform(2)
            self.FindHelper(look, pielW, self.Dict)
        
        if(word.nextToFirst() == 'י') and (self.num_of_a_roots(word.getText()[:-2]) < 3):
            pielW = Word("","")
            pielW.equalTo(word)
            pielW.setText(word.getText()[:-2] + word.first())
            pielW.setVerbform(2)
            self.FindHelper(look, pielW, self.Dict)
            return pielW
        return Word("", "")
    
    def pual(self, look, word):
        if(len(word.getText()) < 4):
            return Word("","")
        
        if(word.nextToFirst() == 'ו') and (self.num_of_a_roots(word.getText()[:-2]) < 3):
            pualW = Word("","")
            pualW.equalTo(word)
            pualW.setText(word.getText()[:-2] + word.first())
            pualW.setVerbform(3)
            self.FindHelper(look, pualW, self.Dict)
            return pualW
        return Word("", "")
    
    def hifil(self, look, word):
        if(word.getLen() < 5) or (word.getPartiVal() == 1) or (word.getTenseVal() == 0) or (word.getConstruct() == True):
            return Word("","")
        
        if((self.num_of_a_roots(word.last3()) < 2)and(not (word.last3() in plural))):
            if(word.getLen() > 7):
                if((word.first() == 'י') or (word.first() == 'נ' ) or (word.first() == 'ת' ) or (word.first() == 'א')) and ((word.fourthFromLast() == 'י')and(word.XfromLast(5) == 'י')) and (self.num_of_p_roots(word.getText()[5:-1]) < 3):
                    hifilW = Word("","")
                    hifilW.equalTo(word)
                    hifilW.setText(word.last3() + word.getText()[5:])
                    hifilW.setRL2(hifilW.thirdFromLast() + hifilW.fourthFromLast())
                    hifilW.setVerbform(4)
                    return self.future(look, hifilW)
                    
                if(((word.first() == 'ה')) and ((word.fourthFromLast() == 'י')and(word.XfromLast(5) == 'י'))) and (self.num_of_p_roots(word.getText()[5:-1]) < 3):
                    hifilW = Word("","")
                    hifilW.equalTo(word)
                    hifilW.setText(word.last3() + word.getText()[5:-1])
                    hifilW.setRL2(hifilW.thirdFromLast() + hifilW.fourthFromLast())
                    hifilW.setVerbform(4)
                    self.FindHelper(look, hifilW, self.Dict)
                    
                    if(word.first2() == 'יה'):
                        hifilW2 = Word("","")
                        hifilW2.equalTo(word)
                        hifilW2.setText(word.last3() + word.getText()[5:-2])
                        hifilW2.setRL2(hifilW2.thirdFromLast() + hifilW2.fourthFromLast())
                        hifilW2.setVerbform(4)
                        return self.perfect(look, hifilW)
                    return hifilW
                    
            if(word.getLen() > 6):
                if((word.first() == 'י') or (word.first() == 'נ' ) or (word.first() == 'ת' ) or (word.first() == 'א')) and (word.fourthFromLast() == 'י') and (self.num_of_p_roots(word.getText()[4:-1]) < 3):
                    hifilW = Word("","")
                    hifilW.equalTo(word)
                    hifilW.setText(word.last3() + word.getText()[4:])
                    hifilW.setRL2(hifilW.thirdFromLast() + hifilW.fourthFromLast())
                    hifilW.setVerbform(4)
                    return self.future(look, hifilW)
                
                if(((word.first() == 'ה')) and (word.fourthFromLast() == 'י')) and (self.num_of_p_roots(word.getText()[4:-1]) < 3):
                    hifilW = Word("","")
                    hifilW.equalTo(word)
                    hifilW.setText(word.last3() + word.getText()[4:-1])
                    hifilW.setRL2(hifilW.thirdFromLast() + hifilW.fourthFromLast())
                    hifilW.setVerbform(4)
                    self.perfect(look, hifilW)
                    
                    if(word.first2() == 'יה'):
                        hifilW2 = Word("","")
                        hifilW2.equalTo(word)
                        hifilW2.setText(word.last3() + word.getText()[4:-2])
                        hifilW2.setRL2(hifilW2.thirdFromLast() + hifilW2.fourthFromLast())
                        hifilW2.setVerbform(4)
                        self.FindHelper(look, hifilW2, self.Dict)
                        return self.perfect(look, hifilW2)
                    return hifilW
        
        if((self.num_of_a_roots(word.last2()) < 2)and(not (word.last2() in plural))):
            if(word.getLen() > 6):
                if((word.first() == 'י') or (word.first() == 'נ' ) or (word.first() == 'ת' ) or (word.first() == 'א')) and ((word.thirdFromLast() == 'י')and(word.fourthFromLast() == 'י')) and (self.num_of_p_roots(word.getText()[4:-1]) < 3):
                    hifilW = Word("","")
                    hifilW.equalTo(word)
                    hifilW.setText(word.last2() + word.getText()[4:])
                    hifilW.setRL2(hifilW.nextToLast() + hifilW.thirdFromLast())
                    hifilW.setVerbform(4)
                    return self.future(look, hifilW)
                    
                if(((word.first() == 'ה')) and ((word.thirdFromLast() == 'י')and(word.fourthFromLast() == 'י'))) and (self.num_of_p_roots(word.getText()[4:-1]) < 3):
                    hifilW = Word("","")
                    hifilW.equalTo(word)
                    hifilW.setText(word.last2() + word.getText()[4:-1])
                    hifilW.setRL2(hifilW.nextToLast() + hifilW.thirdFromLast())
                    hifilW.setVerbform(4)
                    self.FindHelper(look, hifilW, self.Dict)
                    self.perfect(look, hifilW)
                    
                    if(word.first2() == 'יה'):
                        hifilW2 = Word("","")
                        hifilW2.equalTo(word)
                        hifilW2.setText(word.last2() + word.getText()[4:-2])
                        hifilW2.setRL2(hifilW2.nextToLast() + hifilW2.thirdFromLast())
                        hifilW2.setVerbform(4)
                        self.FindHelper(look, hifilW2, self.Dict)
                        return self.perfect(look, hifilW2)
            
            if(word.getLen() > 5):
                if((word.first() == 'י') or (word.first() == 'נ' ) or (word.first() == 'ת' ) or (word.first() == 'א')) and (word.thirdFromLast() == 'י') and (self.num_of_p_roots(word.getText()[3:-1]) < 3):
                    hifilW = Word("","")
                    hifilW.equalTo(word)
                    hifilW.setText(word.last2() + word.getText()[3:])
                    hifilW.setRL2(hifilW.nextToLast() + hifilW.thirdFromLast())
                    hifilW.setVerbform(4)
                    return self.future(look, hifilW)
                
                if(((word.first() == 'ה')) and (word.thirdFromLast() == 'י')) and (self.num_of_p_roots(word.getText()[3:-1]) < 3):
                    hifilW = Word("","")
                    hifilW.equalTo(word)
                    hifilW.setText(word.last2() + word.getText()[3:-1])
                    hifilW.setRL2(hifilW.nextToLast() + hifilW.thirdFromLast())
                    hifilW.setVerbform(4)
                    self.perfect(look, hifilW)
                    
                    if(word.first2() == 'יה'):
                        hifilW2 = Word("","")
                        hifilW2.equalTo(word)
                        hifilW2.setText(word.last2() + word.getText()[3:-2])
                        hifilW2.setRL2(hifilW2.nextToLast() + hifilW2.thirdFromLast())
                        hifilW2.setVerbform(4)
                        self.FindHelper(look, hifilW2, self.Dict)
                        return self.perfect(look, hifilW2)
                    return hifilW
                
        if((word.first() == 'י') or (word.first() == 'נ' ) or (word.first() == 'ת' ) or (word.first() == 'א')) and ((word.nextToLast() == 'י')and(word.thirdFromLast() == 'י')) and (self.num_of_p_roots(word.getText()[3:-1]) < 3):
            hifilW = Word("","")
            hifilW.equalTo(word)
            hifilW.setText(word.last() + word.getText()[3:])
            hifilW.setRL2(hifilW.last() + hifilW.nextToLast())
            hifilW.setVerbform(4)
            return self.future(look, hifilW)
            
        if((word.first() == 'י') or (word.first() == 'נ' ) or (word.first() == 'ת' ) or (word.first() == 'א')) and (word.nextToLast() == 'י') and (self.num_of_p_roots(word.getText()[2:-1]) < 3):
            hifilW = Word("","")
            hifilW.equalTo(word)
            hifilW.setText(word.last() + word.getText()[2:])
            hifilW.setRL2(hifilW.last() + hifilW.nextToLast())
            hifilW.setVerbform(4)
            return self.future(look, hifilW)
                
        if(((word.first() == 'ה')) and ((word.nextToLast() == 'י')and(word.thirdFromLast() == 'י'))) and (self.num_of_p_roots(word.getText()[3:-1]) < 3):
            hifilW = Word("","")
            hifilW.equalTo(word)
            hifilW.setText(word.last() + word.getText()[3:-1])
            hifilW.setRL2(hifilW.last() + hifilW.nextToLast())
            hifilW.setVerbform(4)
            self.FindHelper(look, hifilW, self.Dict)
            
            if(word.first2() == 'יה'):
                hifilW2 = Word("","")
                hifilW2.equalTo(word)
                hifilW2.setText(word.last() + word.getText()[3:-2])
                hifilW2.setRL2(hifilW2.last() + hifilW2.nextToLast())
                hifilW2.setVerbform(4)
                self.FindHelper(look, hifilW2, self.Dict)
                return hifilW2
            return hifilW
            
        if(((word.first() == 'ה')) and (word.nextToLast() == 'י')) and (self.num_of_p_roots(word.getText()[2:]) < 3):
            hifilW = Word("","")
            hifilW.equalTo(word)
            hifilW.setText(word.last() + word.getText()[2:-1])
            hifilW.setRL2(hifilW.last() + hifilW.nextToLast())
            hifilW.setVerbform(4)
            self.FindHelper(look, hifilW, self.Dict)
            
            if(word.first2() == 'יה'):
                hifilW2 = Word("","")
                hifilW2.equalTo(word)
                hifilW2.setText(word.last() + word.getText()[2:-2])
                hifilW2.setRL2(hifilW2.last() + hifilW2.nextToLast())
                hifilW2.setVerbform(4)
                self.FindHelper(look, hifilW2, self.Dict)
                return hifilW2
            return hifilW
        return Word("", "")
    
    def hufal(self, look, word):
        if(len(word.getText()) < 4):
            return Word("","")
            
        if(word.getPartiVal() == 1):
            return Word("","")
       
        if(word.nextToFirst() == 'ו'):
            if(word.first() == 'ה'):
                hufalW = Word("","")
                hufalW.equalTo(word)
                hufalW.setText(word.getText()[:-2])
                hufalW.setVerbform(5)
                self.FindHelper(look, hufalW, self.Dict)
                return hufalW
        
            if(word.first() in prefixL):
                hufalW = Word("","")
                hufalW.equalTo(word)
                hufalW.setText(word.getText()[:-2] + word.first())
                hufalW.setVerbform(5)
                if(word.first() == 'מ'):
                    self.participle(look, hufalW)
                return self.smPrefix(look, hufalW)
                
            if((word.first() == 'י') or (word.first() == 'נ' ) or (word.first() == 'ת' ) or (word.first() == 'א')):
                hufalW = Word("","")
                hufalW.equalTo(word)
                hufalW.setText(word.getText()[:-2] + word.first())
                hufalW.setVerbform(5)
                return self.future(look, hufalW)
                
        return Word("", "")
    
    def hitpael(self, look, word):
        if(len(word.getText()) < 4) or (word.getPartiVal() == 1):
            return Word("","")
        
        if((word.nextToFirst() == "ש") or (word.nextToFirst() == "ס") or (word.nextToFirst() == "צ")) and (word.first() in prefixL):
            metaW = Word("","")
            metaW.equalTo(self.metathesis(look, word))
            if not (metaW.getText() == ""):
                return self.hitpael(look, metaW)
               
        #This loop checks for any possible assimilation and undoes it.
        if((word.nextToFirst() == "ט") or (word.nextToFirst() == "ד") or (word.nextToFirst() == "נ") or (word.nextToFirst() == "ס")) and (word.first() in prefixL):
            if(word.nextToFirst() == "ט"):
                if(word.third() == "צ"):
                    tempW = Word("","")
                    tempW.equalTo(word)
                    tempW.setText(word.getText()[:-2] + "ת" + word.first())
                    return self.hitpael(look, tempW)
            else:
                tempW = Word("","")
                tempW.equalTo(word)
                tempW.setText(word.getText()[:-1] + "ת" + word.first())
                return self.hitpael(look, tempW)
                
        if(word.first2() == 'תה') and (not ((word.Ht == False) or (word.third() == 'ו'))):
            hitpaelW = Word("","")
            hitpaelW.equalTo(word)
            hitpaelW.setText(word.getText()[:-2])
            hitpaelW.setVerbform(6)
            self.FindHelper(look, hitpaelW, self.Dict)
            return hitpaelW
            
        if(word.nextToFirst() == 'ת') and (word.first() in prefixL) and (not ((word.Ht == False) or (word.third() == 'ו'))):
            hitpaelW = Word("","")
            hitpaelW.equalTo(word)
            hitpaelW.setText(word.getText()[:-2] + word.first())
            hitpaelW.setVerbform(6)
            if(word.first() == 'מ'):
                    self.participle(look, hitpaelW)
            return self.smPrefix(look, hitpaelW)
            
        if((word.first2() == 'תי') or (word.first2() == 'תת' ) or (word.first2() == 'תא') or (word.first2() == 'תנ')) and (not ((word.Ht == False) or (word.third() == 'ו'))):
            hitpaelW = Word("","")
            hitpaelW.equalTo(word)
            hitpaelW.setText(word.getText()[:-2] + word.first())
            hitpaelW.setVerbform(6)
            return self.future(look, hitpaelW)
            
        return Word("", "")
        
    def metathesis(self, look, word):
        if(len(word.getText()) < 3):
            return Word("","")

        if(((word.third() == 'ת') or ((word.third() == 'ט'))) and (word.nextToFirst() in metathesis)):
            tempW = Word("","")
            tempW.equalTo(word)
            tempW.setText(word.getText()[:-3] + self.rev(word.XtoY(1, 3)) + word.first())
            return tempW
        return Word("", "")
         
    def rev(self, text):
        revText = ""
        end = len(text)-1
        for i in range(len(text)):
            revText += text[end-i]
        return str(revText)
            
    def perfect(self, look, word):
        if(word.getLen() < 3) or (word.isTense() == True) or (word.isNoun() == True) or (word.getRL2() == word.last2()):
            return Word("","")

        if(word.getLen() > 3):
            if(word.last2() == 'ית'): 
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[2:]))
                perfW.setVerb()
                
                if 'ו' in word.getPrixList():
                    perfW.setTense(1)
                else:
                    perfW.setTense(0)
                    
                perfW.setPerson(0)
                perfW.setGender(0)
                f = self.FindHelper(look, perfW, self.Dict)
                #self.irreg(look, perfW)
                
                fh = False
                if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())) and (not (perfW.last() == 'ה')):
                    perfWh = Word("","")
                    perfWh.equalTo(perfW)
                    perfWh.setText('ה' + self.unFinal(perfW.getText()))
                    fh = self.FindHelper(look, perfWh, self.Dict)
                    self.algorithm(look, perfWh)
                
                return perfW
                
            if(word.last2() == 'ונ') and (not(word.getRL2() == word.nextToLast() + word.thirdFromLast())):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[2:]))
                perfW.setVerb()
                
                if 'ו' in word.getPrixList():
                    perfW.setTense(1)
                else:
                    perfW.setTense(0)
                    
                perfW.setPerson(1)
                perfW.setGender(2)
                f = self.FindHelper(look, perfW, self.Dict)
                #self.irreg(look, perfW)
                
                fh = False
                if(not (perfW.last() == 'ה')):
                    perfWh = Word("","")
                    perfWh.equalTo(perfW)
                    perfWh.setText('ה' + self.unFinal(perfW.getText()))
                    fh = self.FindHelper(look, perfWh, self.Dict)
                    self.algorithm(look, perfWh)
                
                return perfW
                
            if(word.last2() == 'םת') and (not(word.getRL2() == word.nextToLast() + word.thirdFromLast())):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[2:]))
                perfW.setVerb()
                
                if 'ו' in word.getPrixList():
                    perfW.setTense(1)
                else:
                    perfW.setTense(0)
                    
                perfW.setPerson(3)
                perfW.setGender(0)
                f = self.FindHelper(look, perfW, self.Dict)
                #self.irreg(look, perfW)
                
                fh = False
                if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())) and (not (perfW.last() == 'ה')):
                    perfWh = Word("","")
                    perfWh.equalTo(perfW)
                    perfWh.setText('ה' + self.unFinal(perfW.getText()))
                    fh = self.FindHelper(look, perfWh, self.Dict)
                    self.algorithm(look, perfWh)
                
                return perfW 
                
            if(word.last2() == 'ןת') and (not(word.getRL2() == word.nextToLast() + word.thirdFromLast())):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[2:]))
                perfW.setVerb()
                
                if 'ו' in word.getPrixList():
                    perfW.setTense(1)
                else:
                    perfW.setTense(0)
                    
                perfW.setPerson(3)
                perfW.setGender(1)
                f = self.FindHelper(look, perfW, self.Dict)
                #self.irreg(look, perfW)
                
                fh = False
                if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())) and (not (perfW.last() == 'ה')):
                    perfWh = Word("","")
                    perfWh.equalTo(perfW)
                    perfWh.setText('ה' + self.unFinal(perfW.getText()))
                    fh = self.FindHelper(look, perfWh, self.Dict)
                    self.algorithm(look, perfWh)
                
                return perfW 
                
        if(word.last() == 'ו'):
            perfW = Word("","")
            perfW.equalTo(word)
            perfW.setText(self.Final(word.getText()[1:]))
            perfW.setVerb()
            
            if 'ו' in word.getPrixList():
                perfW.setTense(1)
            else:
                perfW.setTense(0)
                
            perfW.setPerson(5)
            perfW.setGender(2)
            f = self.FindHelper(look, perfW, self.Dict)
            #self.irreg(look, perfW)
            
            fh = False
            if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())) and (not (perfW.last() == 'ה')):
                perfWh = Word("","")
                perfWh.equalTo(perfW)
                perfWh.setText('ה' + self.unFinal(perfW.getText()))
                fh = self.FindHelper(look, perfWh, self.Dict)
                self.algorithm(look, perfWh)
                
            return perfW
            
        if(word.last() == 'ת'):
            perfW = Word("","")
            perfW.equalTo(word)
            perfW.setText(self.Final(word.getText()[1:]))
            perfW.setVerb()
            
            if 'ו' in word.getPrixList():
                perfW.setTense(1)
            else:
                perfW.setTense(0)
                
            perfW.setPerson(2)
            perfW.setGender(2)
            f = self.FindHelper(look, perfW, self.Dict)
            #self.irreg(look, perfW)
            
            fh = False
            if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())) and (not (perfW.last() == 'ה')):
                perfWh = Word("","")
                perfWh.equalTo(perfW)
                perfWh.setText('ה' + self.unFinal(perfW.getText()))
                fh = self.FindHelper(look, perfWh, self.Dict)
                self.algorithm(look, perfWh)
              
            return perfW
            
        #may have to be changed later upon further knowledge    
        if(word.last() == 'ה') and (self.CurrentWord.last() == 'ה'):
            f = False
            perfW = Word("","")
            perfW.equalTo(word)
            perfW.setText(self.Final(word.getText()[1:]))
            perfW.setVerb()
            
            if 'ו' in word.getPrixList():
                perfW.setTense(1)
            else:
                perfW.setTense(0)
                
            perfW.setPerson(4)
            perfW.setGender(1)
            f = self.FindHelper(look, perfW, self.Dict)
            #self.irreg(look, perfW)
            fh = False
            if(perfW.last() == 'ת'):
                irreg = Word("","")
                irreg.equalTo(perfW)
                irreg.setText(self.Final(perfW.getText()[1:]))
                self.irreg(look, irreg)
                
                fh = False
                if(not ('ה' in word.getSufxList())):
                    perfWh = Word("","")
                    perfWh.equalTo(perfW)
                    perfWh.setText('ה' + perfW.getText()[1:])
                    fh = self.FindHelper(look, perfWh, self.Dict)
                    self.algorithm(look, perfWh)
            
            return perfW 

        return Word("", "")
                      
    def future(self, look, word):
        if(word.getLen() < 3) or (word.isTense() == True) or (word.isNoun() == True) or (word.getVerbform() == 'Pual') or (word.getVerbform() == 'Piel'):
            return Word("","")

        if(word.getLen() > 3):
            if((word.first() == 'ת')and(word.last2() == 'הנ')) and (self.imperRules(word, 'ת') == True):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(self.Final(word.getText()[2:-1]))
                futurW.setVerb()
                
                if 'ו' in word.getPrixList():
                    futurW.setTense(0)
                else:
                    futurW.setTense(1)
                futurW.setPerson(3)
                futurW.setGender(1)
                
                if(futurW.getLen() > 1):
                    if futurW.getText()[1:2] == 'ו':
                        futurW.setText(futurW.last() + futurW.getText()[2:])   
                    f = self.FindHelper(look, futurW, self.Dict)
                    self.algorithm(look, futurW)
                    fh = False
                    if(not (futurW.last() == 'ה')):
                        futurWh = Word("","")
                        futurWh.equalTo(futurW)
                        futurWh.setText('ה' + self.unFinal(futurW.getText()))
                        fh = self.FindHelper(look, futurWh, self.Dict)
                        self.algorithm(look, futurWh)
                elif 'ו' in word.getPrixList():
                    self.irreg(look, futurW)
                
                futurW2 = Word("","")
                futurW2.equalTo(futurW)
                 
                if 'ו' in word.getPrixList():
                    futurW2.setTense(0)
                else:
                    futurW2.setTense(1)
                futurW2.setPerson(5)
                futurW2.setGender(1)
                
                if(futurW2.getLen() > 1):
                    f2 = self.FindHelper(look, futurW2, self.Dict)
                    self.irreg(look, futurW2)
                    f2h = False
                    if(not (futurW2.last() == 'ה')):
                        futurW2h = Word("","")
                        futurW2h.equalTo(futurW2)
                        futurW2h.setText('ה' + self.unFinal(futurW2.getText()))
                        f2h = self.FindHelper(look, futurW2h, self.Dict)
                        self.algorithm(look, futurW2h)
                    return futurW2
                elif 'ו' in word.getPrixList():
                    return self.irreg(look, futurW2)
                    
            if (word.first2() == 'וי') and (word.last() == 'ו') and (self.imperRules(word, 'וי') == True):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(word.getText()[1:-2])
                futurW.setVerb()
                 
                if 'ו' in word.getPrixList():
                    futurW.setTense(0)
                else:
                    futurW.setTense(1)
                futurW.setPerson(2)
                futurW.setGender(1)
                
                if(futurW.getLen() > 1):
                    if futurW.getText()[1:2] == 'ו':
                        futurW.setText(futurW.getText()[0:1] + futurW.getText()[2:])
                    f = self.FindHelper(look, futurW, self.Dict)
                    self.irreg(look, futurW)
                    fh = False
                    if(not (futurW.last() == 'ה')):
                        futurWh = Word("","")
                        futurWh.equalTo(futurW)
                        futurWh.setText('ה' + self.unFinal(futurW.getText()))
                        fh = self.FindHelper(look, futurWh, self.Dict)
                        self.algorithm(look, futurWh)
                    return futurW
                elif 'ו' in word.getPrixList():
                    return self.irreg(look, futurW)
               
        if(word.getLen() > 2):
            if (word.first2() == 'וי') and (self.imperRules(word, 'וי') == True):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(word.getText()[:-2])
                futurW.setVerb()
                 
                if 'ו' in word.getPrixList():
                    futurW.setTense(0)
                else:
                    futurW.setTense(1)
                futurW.setPerson(4)
                futurW.setGender(0)
                
                if(futurW.getLen() > 1):
                    if futurW.nextToLast() == 'ו':
                        futurW.setText(futurW.last() + futurW.getText()[2:])
                    f = self.FindHelper(look, futurW, self.Dict)
                    self.irreg(look, futurW)
                    fh = False
                    if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())):
                        futurWh = Word("","")
                        futurWh.equalTo(futurW)
                        futurWh.setText('ה' + self.unFinal(futurW.getText()))
                        fh = self.FindHelper(look, futurWh, self.Dict)
                        self.algorithm(look, futurWh)
                    return futurW
                elif 'ו' in word.getPrixList():
                    return self.irreg(look, futurW)
              
            if((word.first() == 'ת')and(word.last() == 'ו') and (self.imperRules(word, 'ת') == True)):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(self.Final(word.getText()[1:-1]))
                futurW.setVerb()
                 
                if 'ו' in word.getPrixList():
                    futurW.setTense(0)
                else:
                    futurW.setTense(1)
                futurW.setPerson(3)
                futurW.setGender(0)
                
                if(futurW.getLen() > 1):
                    f = self.FindHelper(look, futurW, self.Dict)
                    self.irreg(look, futurW)
                    fh = False
                    if(not(('וה' in futurW.getSufxList())or('ןהי' in futurW.getSufxList())or('םה' in futurW.getSufxList()))) and (not('ה' in futurW.getSufxList())) and (not(futurW.last() == 'ה')):
                        futurWh = Word("","")
                        futurWh.equalTo(futurW)
                        futurWh.setText('ה' + self.unFinal(futurW.getText()))
                        fh = self.FindHelper(look, futurWh, self.Dict)
                        self.algorithm(look, futurWh)
                    return futurW
                elif 'ו' in word.getPrixList():
                    return self.irreg(look, futurW)

            if((word.first() == 'ת')and(word.last() == 'י') and (self.imperRules(word, 'ת') == True)):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(self.Final(word.getText()[1:-1]))
                futurW.setVerb()
                 
                if 'ו' in word.getPrixList():
                    futurW.setTense(0)
                else:
                    futurW.setTense(1)
                futurW.setPerson(2)
                futurW.setGender(1)
                
                if(futurW.getLen() > 1):
                    f = self.FindHelper(look, futurW, self.Dict)
                    self.irreg(look, futurW)
                    fh = False
                    if(not(('וה' in futurW.getSufxList())or('ןהי' in futurW.getSufxList())or('םה' in futurW.getSufxList()))) and (not('ה' in futurW.getSufxList())) and (not(futurW.last() == 'ה')):
                        futurWh = Word("","")
                        futurWh.equalTo(futurW)
                        futurWh.setText('ה' + self.unFinal(futurW.getText()))
                        fh = self.FindHelper(look, futurWh, self.Dict)
                        self.algorithm(look, futurWh)
                    return futurW
                elif 'ו' in word.getPrixList():
                    return self.irreg(look, futurW)
                    
            if((word.first() == 'י') and (word.last()== 'ו') and (self.imperRules(word, 'י') == True)):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(self.Final(word.getText()[1:-1]))
                futurW.setVerb()
                 
                if 'ו' in word.getPrixList():
                    futurW.setTense(0)
                else:
                    futurW.setTense(1)
                futurW.setPerson(5)
                futurW.setGender(0)

                if(futurW.getLen() > 1):
                    f = self.FindHelper(look, futurW, self.Dict)
                    self.irreg(look, futurW)
                    fh = False
                    if(not (futurW.last() == 'ה')):
                        futurWh = Word("","")
                        futurWh.equalTo(futurW)
                        futurWh.setText('ה' + self.unFinal(futurW.getText()))
                        fh = self.FindHelper(look, futurWh, self.Dict)
                        self.algorithm(look, futurWh)
                    return futurW
                elif 'ו' in word.getPrixList():
                    return self.irreg(look, futurW)

        if(word.first() == 'א') and (self.imperRules(word, 'א') == True):
            futurW = Word("","")
            futurW.equalTo(word)
            futurW.setText(word.getText()[:-1])
            futurW.setVerb()
             
            if 'ו' in word.getPrixList():
                futurW.setTense(0)
            else:
                futurW.setTense(1)
            futurW.setPerson(0)
            futurW.setGender(2)
            
            if(futurW.getLen() > 1):
                if futurW.nextToLast() == 'ו':
                    futurW.setText(futurW.last() + futurW.getText()[2:])
                f = self.FindHelper(look, futurW, self.Dict)
                fh = False
                if(not (futurW.last() == 'ה')):
                    futurWh = Word("","")
                    futurWh.equalTo(futurW)
                    futurWh.setText('ה' + self.unFinal(futurW.getText()))
                    fh = self.FindHelper(look, futurWh, self.Dict)
                    self.algorithm(look, futurWh)
                return futurW
            elif 'ו' in word.getPrixList():
                return self.irreg(look, futurW)
                
            elif 'ו' in word.getPrixList():
                self.irreg(look, futurW)
            
        if(word.first() == 'י') and (self.imperRules(word, 'י') == True):
            futurW = Word("","")
            futurW.equalTo(word)
            futurW.setText(word.getText()[:-1])
            futurW.setVerb()
             
            if 'ו' in word.getPrixList():
                futurW.setTense(0)
            else:
                futurW.setTense(1)
            futurW.setPerson(4)
            futurW.setGender(0)
            
            if(futurW.getLen() > 1):
                if futurW.nextToLast() == 'ו':
                    futurW.setText(futurW.last() + futurW.getText()[2:])   
                f = self.FindHelper(look, futurW, self.Dict)
              
                fh = False
                if (not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and ('ו' in word.getPrixList()) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())):
                    futurWh = Word("","")
                    futurWh.equalTo(futurW)
                    futurWh.setText('ה' + self.unFinal(futurW.getText()))
                    fh = self.FindHelper(look, futurWh, self.Dict)
                    self.algorithm(look, futurWh)
                return futurW
            elif 'ו' in word.getPrixList():
                self.irreg(look, futurW)
                
            return futurW
  
        if(word.first() == 'ת') and (self.imperRules(word, 'ת') == True):
            futurW = Word("","")
            futurW.equalTo(word)
            futurW.setText(word.getText()[:-1])
            futurW.setVerb()
             
            if 'ו' in word.getPrixList():
                futurW.setTense(0)
            else:
                futurW.setTense(1)
            futurW.setPerson(2)
            futurW.setGender(0)
            
            if(futurW.getLen() > 1):
                if futurW.nextToLast() == 'ו':
                    futurW.setText(futurW.last() + futurW.getText()[2:])
                f = self.FindHelper(look, futurW, self.Dict)
                self.algorithm(look, futurW)
                fh = False
                if(not (futurW.last() == 'ה')):
                    futurWh = Word("","")
                    futurWh.equalTo(futurW)
                    futurWh.setText('ה' + self.unFinal(futurW.getText()))
                    fh = self.FindHelper(look, futurWh, self.Dict)
                    self.algorithm(look, futurWh)
            elif 'ו' in word.getPrixList():
                self.irreg(look, futurW)
                
            futurW2 = Word("","")
            futurW2.equalTo(futurW)
             
            if 'ו' in word.getPrixList():
                futurW2.setTense(0)
            else:
                futurW2.setTense(1)
            futurW2.setPerson(4)
            futurW2.setGender(1)
            
            if(futurW2.getLen() > 1):
                f2 = self.FindHelper(look, futurW2, self.Dict)
                self.algorithm(look, futurW2)
                fh = False
                if(not (futurW2.last() == 'ה')):
                    futurW2h = Word("","")
                    futurW2h.equalTo(futurW2)
                    futurW2h.setText('ה' + self.unFinal(futurW2.getText()))
                    fh = self.FindHelper(look, futurW2h, self.Dict)
                    self.algorithm(look, futurW2h)
                return futurW2
            elif 'ו' in word.getPrixList():
                self.irreg(look, futurW2)
  
        if(word.first() == 'נ') and (self.imperRules(word, 'נ') == True):
            futurW = Word("","")
            futurW.equalTo(word)
            futurW.setText(word.getText()[:-1])
            futurW.setVerb()
             
            if 'ו' in word.getPrixList():
                futurW.setTense(0)
            else:
                futurW.setTense(1)
            futurW.setPerson(1)
            futurW.setGender(2)
            
            if(futurW.getLen() > 1):
                if futurW.nextToLast() == 'ו':
                    futurW.setText(futurW.getText()[0:1] + futurW.getText()[2:])               
                f = self.FindHelper(look, futurW, self.Dict)
                fh = False
                if(not (futurW.last() == 'ה')):
                    futurWh = Word("","")
                    futurWh.equalTo(futurW)
                    futurWh.setText('ה' + self.unFinal(futurW.getText()))
                    fh = self.FindHelper(look, futurWh, self.Dict)
                    self.algorithm(look, futurWh)
                return futurW
            elif 'ו' in word.getPrixList():
                self.irreg(look, futurW)

        return Word("", "")
    
    def imperRules(self, word, l):
        if ('ה' in word.getPrixList()) or ((('ל' in word.getPrixList()) or ('מ' in word.getPrixList()) or ('ב' in word.getPrixList())) and (not('ש' in word.getPrixList()))):
            return False
        return True
    
    def imperative(self, look, word):
        if(word.getLen() < 3) or (self.imperRules(word, word.last()) == False) or (len(word.getPrixList()) > 0) or (not(word.getTenseVal() == -1)) or (word.isNoun() == True) or (word.getModern == True) or (word.getRL2() == word.last2()):
            return Word("","")
        
        if word.last() == 'ו':
            imperW = Word("","")
            imperW.equalTo(word)
            imperW.setText(self.Final(word.getText()[1:]))
            imperW.setVerb()
            imperW.setTense(4)
            imperW.setPerson(3)
            imperW.setGender(0)
            self.FindHelper(look, imperW, self.Dict)
            return imperW
            
        if (word.last() == 'י') and (word.getPlural == False):
            imperW = Word("","")
            imperW.equalTo(word)
            imperW.setText(self.Final(word.getText()[1:]))
            imperW.setVerb()
            imperW.setTense(4)
            imperW.setPerson(2)
            imperW.setGender(1)
            self.FindHelper(look, imperW, self.Dict)
            return imperW
        
        if(word.getLen() > 3) and (not((word.getRL2() == word.nextToLast() + word.thirdFromLast()))):
            if word.last2() == 'הנ':
                imperW = Word("","")
                imperW.equalTo(word)
                imperW.setText(self.Final(word.getText()[2:]))
                imperW.setVerb()
                imperW.setTense(4)
                imperW.setPerson(3)
                imperW.setGender(1)
                if imperW.nextToLast() == 'ו':
                    imperW.setText(imperW.last() + imperW.getText()[2:])
                self.FindHelper(look, imperW, self.Dict)
                return imperW
                
            if word.nextToLast() == 'ו':
                imperW = Word("","")
                imperW.equalTo(word)
                imperW.setText(word.last() + word.getText()[2:])
                imperW.setVerb()
                imperW.setTense(4)
                imperW.setPerson(2)
                imperW.setGender(0)
                self.FindHelper(look, imperW, self.Dict)
                return imperW
     
        return Word("", "")
        
    def infinitive(self, look, word):
        if(word.getLen() < 3) or (word.isTense() == True) or (word.isNoun() == True) or (word.getVerbform() == 'Pual') or (word.getVerbform() == 'Piel'):
            return Word("","")
        fh = False
        singleW2 = Word("","") 
        if(word.getLen() > 3):
            if((word.first() == 'ל') and (word.last2() == 'תו')):
                infW = Word("","")
                infW.equalTo(word)
                infW.setText(self.Final(word.getText()[2:-1]))
                if(infW.getLen() > 2):
                    if(infW.nextToLast() == 'ו') and (self.num_of_p_roots(infW.getText()[2:]) < 3):
                        infW.setText(infW.last() + infW.getText()[2:])
                infW.setVerb()
                infW.setTense(3)
                infW.setPlural()
                self.algorithm(look, infW)
                
                singleW = Word("","")
                singleW.equalTo(infW)
                singleW.setText('ה' + self.unFinal(infW.getText()))
                singleW.setTense(3)
                singleW.setPlural()
                fh = self.FindHelper(look, singleW, self.Dict)
                return singleW
                    
        if(word.getLen() > 2):
            if((word.first() == 'ל') and (word.last() == 'ת')):
                infW = Word("","")
                infW.equalTo(word)
                infW.setText(self.Final(word.getText()[1:-1]))
                if(infW.getLen() > 2):
                    if(infW.nextToLast() == 'ו') and (self.num_of_p_roots(infW.getText()[2:]) < 3):
                        infW.setText(infW.last() + infW.getText()[2:])
                infW.setVerb()
                infW.setTense(3)
                self.algorithm(look, infW)
                
                singleW2.equalTo(infW)
                singleW2.setText('ה' + self.unFinal(infW.getText()))
                fh = self.FindHelper(look, singleW2, self.Dict)
                #self.algorithm(look, singleW2)
        if(word.first() == 'ל'):
            infW = Word("","")
            infW.equalTo(word)
            infW.setText(word.getText()[:-1])
            if(infW.getLen() > 2):
                if(infW.nextToLast() == 'ו') and (self.num_of_p_roots(infW.getText()[2:]) < 3):
                        infW.setText(infW.last() + infW.getText()[2:])
            infW.setVerb()
            infW.setTense(3)
            f = self.FindHelper(look, infW, self.Dict)
            return infW
                
        return Word("", "")

    def cohortative(self, look, word):
        if(word.getLen() < 3) or (word.isTense() == True) or (word.isNoun() == True) or (word.getRL2() == word.last2()) or (word.getVerbform() == 'Pual') or (word.getVerbform() == 'Piel'):
            return Word("","")
            
        if(word.getLen() > 3):   
            if((word.first() == 'א')and(word.last() == 'ה')and(self.CurrentWord.last() == 'ה')):
                cohorW = Word("","")
                cohorW.equalTo(word)
                cohorW.setText(self.Final(word.getText()[1:-1]))
                cohorW.setVerb()
               
                cohorW.setTense(5)
                cohorW.setPerson(0)
                cohorW.setGender(2)
                
                if(cohorW.getLen() > 1):
                    if cohorW.nextToLast() == 'ו':
                        cohorW.setText(cohorW.last() + cohorW.getText()[2:])
                    self.FindHelper(look, cohorW, self.Dict)
                    return cohorW          
                elif 'ו' in word.getPrixList():
                    return self.irreg(look, cohorW)
                
                return Word("","")
                    
        if((word.first() == 'נ')and(word.last() == 'ה')and(self.CurrentWord.last() == 'ה')):
                cohorW = Word("","")
                cohorW.equalTo(word)
                cohorW.setText(self.Final(word.getText()[1:-1]))
                cohorW.setVerb()
               
                cohorW.setTense(5)
                cohorW.setPerson(1)
                cohorW.setGender(2)
                
                if(cohorW.getLen() > 1):
                    if cohorW.nextToLast() == 'ו':
                        cohorW.setText(cohorW.last() + cohorW.getText()[2:])
                    self.FindHelper(look, cohorW, self.Dict)
                    return cohorW
                elif 'ו' in word.getPrixList():
                    return self.irreg(look, cohorW)
                    
                return Word("","")
                    
        return Word("", "")
  
    def plural(self, look, word):
        if(word.getLen() < 3) or (word.isVerb() == True) or (word.getPlural() == True) or (word.getDaul() == True) or (word.getConstruct() == True) or (word.getModern == True) or (word.getRL2() == word.last2()) or (word.getRL2() == word.nextToLast() + word.thirdFromLast()) or (word.getPartiVal() == 1):
             return Word("", "")
            
        cPhrasePl = Word("","")
        cPhrasePl.equalTo(word)
        cPhrasePl.setText(self.revPhWords(word.getText(), "-"))
            
        if(cPhrasePl.getLen() > 3): 
            if(cPhrasePl.last3() == 'םיי') and (cPhrasePl.getSuffix() == False) and (not (cPhrasePl.getTense() == 'Perfect')) and (not (cPhrasePl.getTense() == 'Imperfect')) and (not (cPhrasePl.getTense() == 'Imperative')) and (not (cPhrasePl.getTense() == 'Infinitive')) and (not(word.getConstruct() == True)):
                plW = Word("","")
                plW.equalTo(cPhrasePl)
                plW.setText(cPhrasePl.Final(cPhrasePl.getText()[3:]))
                plW.setNoun()
                plW.setDaul()
                plW.setText(self.revPhWords(plW.getText(), "-"))
                self.FindHelper(look, plW, self.Dict)
                self.algorithm(look, plW)
        if(cPhrasePl.getLen() > 2):
            if(cPhrasePl.last2() == 'םי') and (cPhrasePl.getSuffix() == False) and (not (cPhrasePl.getTense() == 'Perfect')):
                plW = Word("","")
                plW.equalTo(cPhrasePl)
                plW.setText(cPhrasePl.Final(cPhrasePl.getText()[2:]))
                plW.setNoun()
                plW.setPlural()
                plW.setText(self.revPhWords(plW.getText(), "-"))
                self.FindHelper(look, plW, self.Dict)
                self.algorithm(look, plW)
                return plW
            if(cPhrasePl.last2() == 'תו') and (not (cPhrasePl.getTense() == 'Perfect')) and (not (cPhrasePl.getTense() == 'Imperfect')) and (not (cPhrasePl.getTense() == 'Imperative')) and (not (cPhrasePl.getTense() == 'Infinitive')):
                plW = Word("","")
                plW.equalTo(cPhrasePl)
                plW.setText(cPhrasePl.Final(cPhrasePl.getText()[2:]))
                plW.setNoun()
                plW.setPlural()
                plW.setText(self.revPhWords(plW.getText(), "-"))
                self.FindHelper(look, plW, self.Dict)
                self.algorithm(look, plW)
                singleW = Word("","")
                singleW.equalTo(plW)
                singleW.setText('ה' + self.unFinal(plW.getText()))
                singleW.setPlural()
                self.FindHelper(look, singleW, self.Dict)
                #self.algorithm(look, singleW)
                return singleW
        constr = Word("","")
        constr.equalTo(self.constr(look, cPhrasePl))
        if not (constr.getText() == ""):
            self.algorithm(look, constr)
        #return constr
        return Word("","")
            
    def prefixRuls(self, word, p):
        if(word.getVerbform() == 'Pual') or (word.getVerbform() == 'Piel') or (word.getPartiVal() == 1):
            return False
        revCW = self.rev(self.CurrentWord.getText())
        posTov = revCW.find("ת", 0, 4)
        if not ((posTov == -1) or (posTov == 0)):
            if(revCW[posTov-1] == 'ה') and (word.getVerbform() == 'Hithpeal'):
                return False
        if (word.isTense() == True) or ((word.getTense() == 'Perfect') and ('ו' in word.getPrixList())) or (word.getTense() == 'Infinitive') or (word.getVerbform == 'Niphal') or ((word.getVerbform() == 'Hophal') and (self.CurrentWord.first() == 'ה'))or((word.getVerbform() == 'Hiphil') and (self.CurrentWord.first() == 'ה')): 
            return False
        if (p in word.getPrixList()):
            return False
        if ((p == 'ב') or (p == 'ל')) and (('ב' in word.getPrixList()) or ('ל' in word.getPrixList())):
            return False
        if (word.getPrefix() == True) and (word.prefixD[p] == "and"):
            return False
        if ('ה' in word.getPrixList()):
            return False
        if (p == 'ש') and ('ש' in word.getPrixList()):
            return False
        if ((p == 'מ') or (p == 'ל')) and (('ב' in word.getPrixList()) or ('ל' in word.getPrixList())):
            return False
        if (p == 'כ') and (('ל' in word.getPrixList()) or ('ב' in word.getPrixList()) or ('כ' in word.getPrixList()) or ('ש' in word.getPrixList()) or ("מ" in word.getPrixList())):
            return False
        if (p == 'ה') and (word.isVerb() == True):
            return False
        if(word.getLen() > 2):
            if(word.second() == 'ו') and (not (word.XtoY(1, 3) == "וו")) and (not (word.XtoY(1, 3) == "וי")):
                return False
        return True
            
    def prefix(self, look, word):
        if(word.getLen() < 2):
            return Word("","")
        
        if not ('-' in word.getText()):
            return self.smPrefix(look, word)
            
        cPhrasePre = Word("","")
        cPhrasePre.equalTo(word)
        cPhrasePre.setText(self.revPhWords(cPhrasePre.getText(), "-"))
          
        if (cPhrasePre.first() in prefixL) and (self.prefixRuls(cPhrasePre, cPhrasePre.first()) == True):
            preW = Word("","")
            preW.equalTo(cPhrasePre)
            preW.setText(cPhrasePre.getText()[:-1])
            preW.setPrefix()
            preW.addPre(cPhrasePre.first())
            preW.setText(self.revPhWords(preW.getText(), "-"))
            
            if self.FindHelper(look, preW, self.Dict) == False:
                self.algorithm(look, preW)
                preWend = Word("","")
                preWend.equalTo(self.prefix(look, preW))
                if preWend.getText() == "":
                    return preW
                else:
                    return preWend
            else:
                return preW   
                
        return Word("", "")
    
    def prexChainRapper(self, look, word):
        if(word.getLen() < 2):
            return Word("","")
        
        if not ('-' in word.getText()):
            return Word("","")
            
        cPhrasePre = Word("","")
        cPhrasePre.equalTo(word)
          
        preChain1 = Word("","")
        preChain1.equalTo(self.prexChain(look, cPhrasePre))
        
        if (not(preChain1.getText() == "")):
            return preChain1
        return Word("", "")
    
    def prexChain(self, look, word):
        if(word.getLen() < 2):
            return Word("", "")
              
        temp1 = Word("", "")
        temp1.equalTo(word)
        temp1.setText(self.revPhWords(temp1.getText(), "-"))
            
        s = temp1.getText().count("ה-")
        if s == 0:
            return Word("", "")
        
        for i in range(1, s + 1):
            temp2 = Word("", "")
            temp2.equalTo(temp1)
            temp2.setText(temp1.getText().replace("ה-", "-", i))
            if(not('ה' in temp2.getPrixList())):
                temp2.setPrefix()
                temp2.addPre('ה')
                
            temp2.setText(self.revPhWords(temp2.getText(), "-"))
            if self.FindHelper(look, temp2, self.Dict) == True:
                return temp2
            
        return Word("", "")

    def smPrefix(self, look, word):
        if(word.getLen() < 2) or (not(self.CurrentWord.first() in prefixL)): #or (word.getModern == True):
            return Word("","")
                
        if (word.first() in prefixL) and (self.prefixRuls(word, word.first()) == True):
            preW = Word("","")
            preW.equalTo(word)
            preW.setText(word.getText()[:-1])
            if(word.first() == 'ה') or (word.first() == 'ל'):
                if word.isVerb() == False:
                    preW.setNoun()
                else:
                    return word
            preW.setPrefix()
            preW.addPre(word.first())
            self.FindHelper(look, preW, self.Dict)
            self.algorithm(look, preW)
            return preW
        return Word("", "")  

    def suffixObj(self, look, word):
        if(word.getLen() < 2) or (word.isTense() == True) or (word.isNoun() == True) or (word.getSuffix() == True) or (word.getPlural() == True) or (word.getDaul() == True) or (word.getConstruct() == True) or (word.getModern == True) or (word.getRL2() == word.last2()) or (word.getPartiVal() == 0):
            return Word("","")
            
        if word.getLen() > 2:
            if(word.last2() == 'םי'):
                return Word("","")
        if word.getLen() > 3:
            if(word.last3() == 'םיי'):
                return Word("","")
            if(self.CurrentWord.last2() == word.last2()) and (word.last2() in suffixObj) and (not(word.getRL2() == word.nextToLast() + word.thirdFromLast())):
                suffW = Word("","")
                suffW.equalTo(word)
                suffW.setText(self.Final(word.getText()[2:]))
                suffW.setVerb()
                suffW.setSuffix2()
                suffW.addSuff(word.last2())
                self.FindHelper(look, suffW, self.Dict)
                self.algorithm(look, suffW)
                
                if (suffW.last() == 'י'):
                    suffW2 = Word("","")
                    suffW2.equalTo(suffW)
                    suffW2.setText(self.Final(suffW.getText()[1:]))
                    #look.find(suffW2, self.Dict)
                    self.algorithm(look, suffW2)
                    
                    if(not(suffW2.last() == 'ה')):
                        suffW2h = Word("","")
                        suffW2h.equalTo(suffW2)
                        suffW2h.setText('ה' + self.unFinal(suffW2.getText()))
                        self.FindHelper(look, suffW2h, self.Dict)
                        #self.algorithm(look, suffW2h)
               
                elif(not(suffW.last() == 'ה')) and (not('וה' in suffW.getSufxList())) and (not 'ה' in suffW.getSufxList()) and (not ('ה' in word.getSufxList())) and (not(('ו' in word.getPrixList())and(word.getTense() == 'Imperfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))) and (not((not ('ו' in word.getPrixList()))and(word.getTense() == 'Perfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))):
                    suffWh = Word("","")
                    suffWh.equalTo(suffW)
                    suffWh.setText('ה' + self.unFinal(suffW.getText()))
                    self.FindHelper(look, suffWh, self.Dict)
                    #self.algorithm(look, suffWh)
                
                return suffW
                
        if(self.CurrentWord.last() == word.last()) and (word.last() in suffixObj):
            if ((word.last() == 'ה') and (word.getPlural() == True)):
                return Word("", "")
            suffW = Word("","")
            suffW.equalTo(word)
            suffW.setText(self.Final(word.getText()[1:]))
            suffW.setVerb()    
            suffW.setSuffix1()
            suffW.addSuff(word.last())
            self.FindHelper(look, suffW, self.Dict)
            self.algorithm(look, suffW)
            
            if (suffW.getLen() > 2) and (suffW.last() == 'י') and (not (word.last() == 'י')):
                suffW2 = Word("","")
                suffW2.equalTo(suffW)
                suffW2.setText(self.Final(suffW.getText()[1:]))
                #look.find(suffW2, self.Dict)
                self.algorithm(look, suffW2)
                if(not(suffW2.last() == 'ה')) and (not 'ה' in suffW2.getSufxList()) and (not ('ה' in word.getSufxList())) and (not(('ו' in word.getPrixList())and(word.getTense() == 'Imperfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))) and (not((not ('ו' in word.getPrixList()))and(word.getTense() == 'Perfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))):
                    suffW2h = Word("","")
                    suffW2h.equalTo(suffW2)
                    suffW2h.setText('ה' + self.unFinal(suffW2.getText()))
                    self.FindHelper(look, suffW2h, self.Dict)
                    #self.algorithm(look, suffW2h)
            
            elif(not(suffW.last() == 'ה')) and (not 'ה' in suffW.getSufxList()) and (not ('ה' in word.getSufxList())) and (not(('ו' in word.getPrixList())and(word.getTense() == 'Imperfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))) and (not((not ('ו' in word.getPrixList()))and(word.getTense() == 'Perfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))):
                suffWh = Word("","")
                suffWh.equalTo(suffW)
                suffWh.setText('ה' + word.getText()[1:])
                self.FindHelper(look, suffWh, self.Dict)
                #self.algorithm(look, suffWh)
                
            return suffW
        return Word("", "")
    
    def suffix(self, look, word, p):
        if(word.getLen() < 3) or (word.getConstruct() == True)or (word.isVerb() == True) or (word.getSuffix() == True) or (word.getPlural() == True) or (word.getDaul() == True) or (not (word.getTenseVal() == -1)) or (word.getModern == True) or (word.getPartiVal() == 0):
            return Word("","")
            
        suff1 = Word("","")
        suff2 = Word("","")
        suff1 = self.suffix1(look, word)
        suff2 = self.suffix2(look, word)

        if(word.last2() == 'םי'):
            return Word("","")
        if p == 1:
            if not (suff1 == Word("","")):
                return suff1
        if p == 2:
            if not (suff2 == Word("","")):
                return suff2
            if not (suff1 == Word("","")):
                return suff1
        if not (suff2 == Word("","")):
            return suff2
        if not (suff1 == Word("","")):
            return suff1
                
        return Word("","")
        
    def suffix1(self, look, word):
        if(word.getLen() < 2) or (word.isVerb() == True) or (word.getSuffix() == True) or (word.getPlural() == True) or (word.getDaul() == True) or (word.getConstruct() == True) or (word.last2() == 'םי') or (word.last3() == 'םיי') or (word.getModern == True) or (word.getRL2() == word.last2()) or (word.getPartiVal() == 0):
            return Word("","")
                
        cPhraseSuf = Word("","")
        cPhraseSuf.equalTo(word)
        cPhraseSuf.setText(self.revPhWords(word.getText(), "-"))
        if ((cPhraseSuf.last() == 'ה') and (cPhraseSuf.getPlural() == True)) or (cPhraseSuf.getLen() < 3):
            return Word("","")
  
        if (self.CurrentWord.last() == cPhraseSuf.last()) and (cPhraseSuf.last() in suffix) and (not((self.CurrentWord.nextToLast() == "י")and(cPhraseSuf.getVerbform() == 'Hiphil'))):
            suffW = Word("","")
            suffW.equalTo(cPhraseSuf)
            suffW.setText(self.Final(cPhraseSuf.getText()[1:]))
            suffW.setSuffix1()
            if(suffW.getLen() > 1):
                if (suffW.last() == 'י') and (cPhraseSuf.last2() in suffix):
                    suffW2 = Word("","")
                    suffW2.equalTo(suffW)
                    suffW2.setText(self.Final(suffW.getText()[1:]))
                    #suffW2.setPlural()
                    #suffW2.setConstruct()
                    suffW2.addSuff(cPhraseSuf.last2())
                    suffW2.setText(self.revPhWords(suffW2.getText(), "-"))
                    if suffW2.getLen() > 3:
                        if suffW2.last2() == 'ות':
                            self.FindHelper(look, suffW2, self.Dict)
                            self.algorithm(look, suffW2)
            
            suffW.addSuff(cPhraseSuf.last())    
            suffW.setText(self.revPhWords(suffW.getText(), "-"))
            self.FindHelper(look, suffW, self.Dict)
            self.algorithm(look, suffW)
            
            if(not(suffW.last() == 'ה')) and (not 'ה' in suffW.getSufxList()) and (not ('ה' in cPhraseSuf.getSufxList())) and (not ((cPhraseSuf.getGender() == "f.")and(cPhraseSuf.getPerson() == '3rd, sg.')and(cPhraseSuf.getTense() == 'Perfect')and(not("ו" in cPhraseSuf.getPrixList())))) and (not ((cPhraseSuf.getGender() == "f.")and(cPhraseSuf.getTense() == 'Imperfect')and(cPhraseSuf.getPerson() == '3rd, sg.')and("ו" in cPhraseSuf.getPrixList()))):
                suffWh = Word("","")
                suffWh.equalTo(suffW)
                suffWh.setText('ה' + cPhraseSuf.getText()[1:])
                suffWh.setText(self.revPhWords(suffWh.getText(), "-"))
                self.FindHelper(look, suffWh, self.Dict)
                #self.algorithm(look, suffWh)
                return suffWh
                
            return suffW
                
        return Word("","")

    def suffix2(self, look, word):
        if(word.getLen() < 3) or (word.isVerb() == True) or (word.getSuffix() == True) or (word.getPlural() == True) or (word.getDaul() == True) or (word.getConstruct() == True) or (word.getModern == True) or (word.getRL2() == word.last2()) or (word.getRL2() == word.nextToLast() + word.thirdFromLast()) or (word.getPartiVal() == 0):
            return Word("","")

        cPhraseSuf = Word("","")
        cPhraseSuf.equalTo(word)
        cPhraseSuf.setText(self.revPhWords(word.getText(), "-"))
            
        if (self.CurrentWord.last2() == cPhraseSuf.last2()) and (cPhraseSuf.last2() in suffix) and (not(((self.CurrentWord.nextToLast() == "י")or(self.CurrentWord.thirdFromLast() == "י"))and(cPhraseSuf.getVerbform() == 'Hiphil'))):
            suffW = Word("","")
            suffW.equalTo(cPhraseSuf)
            suffW.setText(self.Final(cPhraseSuf.getText()[2:]))
            suffW.setSuffix2()
            if(suffW.getLen() > 1):
                if (suffW.last() == 'י') and (cPhraseSuf.last3() in suffix):
                    suffW3 = Word("","")
                    suffW3.equalTo(suffW)
                    suffW3.setText(self.Final(suffW.getText()[1:]))
                    #suffW3.setPlural()
                    #suffW3.setConstruct()
                    suffW3.addSuff(cPhraseSuf.last3())
                    suffW3.setText(self.revPhWords(suffW3.getText(), "-"))
                    if suffW3.getLen() > 3:
                        if suffW3.last2() == 'ות':
                            self.FindHelper(look, suffW3, self.Dict)
                            self.algorithm(look, suffW3)

            suffW.addSuff(cPhraseSuf.last2())    
            suffW.setText(self.revPhWords(suffW.getText(), "-"))
            self.FindHelper(look, suffW, self.Dict)
            self.algorithm(look, suffW)
            
            if(not(('וה' in suffW.getSufxList())or('ןהי' in suffW.getSufxList())or('םה' in suffW.getSufxList()))) and (not(suffW.last() == 'ה')) and (not 'ה' in suffW.getSufxList()) and (not ('ה' in cPhraseSuf.getSufxList())) and (not ((cPhraseSuf.getGender() == "f.")and(cPhraseSuf.getPerson() == '3rd, sg.')and(cPhraseSuf.getTense() == 'Perfect')and(not("ו" in cPhraseSuf.getPrixList())))) and (not ((cPhraseSuf.getGender() == "f.")and(cPhraseSuf.getTense() == 'Imperfect')and(cPhraseSuf.getPerson() == '3rd, sg.')and("ו" in cPhraseSuf.getPrixList()))):
                suffWh = Word("","")
                suffWh.equalTo(suffW)
                suffWh.setText('ה' + cPhraseSuf.getText()[2:])
                suffWh.setText(self.revPhWords(suffWh.getText(), "-"))
                self.FindHelper(look, suffWh, self.Dict)
                #self.algorithm(look, suffWh)
                return suffWh
                
            return suffW

        return Word("","")
        
    def participle(self, look, word):
        if(word.getLen() < 4) or (word.isTense() == True):
            return Word("","")
        #if(word.last2() == 'תו') and (self.num_of_p_roots(word.getText()[2:]) > 2):
            #return Word("","")
            
        isPar = False
        if(word.last() == 'ת') and (not(word.nextToLast() == 'ו')) and (word.getLen() > 4):
            fimW = Word("","")
            fimW.equalTo(word)
            fimW.setText(self.Final(word.getText()[1:]))
            pfimW = Word("","")
            
            if(fimW.first() == 'מ') and (fimW.getLen() > 4):
                if(fimW.third() == 'ו') and (self.num_of_a_roots(fimW.getText()[:-3]) < 3):
                    pfimW.equalTo(fimW)
                    pfimW.setText('ה' + self.unFinal(fimW.getText()[:-3] + fimW.nextToFirst()))
                    pfimW.setConstruct()
                    if fimW.first() == 'ת':
                        pfimW.Ht = False
                    pfimW.setTense(2)
                    pfimW.setPar(1)
                    self.FindHelper(look, pfimW, self.Dict)
                    self.algorithm(look, pfimW)     
                if(fimW.nextToLast() == 'ו') and (self.num_of_p_roots(fimW.getText()[2:]) < 3) and (not(fimW.last() == 'י')) and (not(fimW.last() == 'ו')):
                    isPar = True
                    pfimW2 = Word("","")
                    pfimW2.equalTo(fimW)
                    pfimW2.setText('ה' + self.unFinal(fimW.last() + fimW.getText()[2:-1]))
                    pfimW2.setConstruct()
                    pfimW2.setTense(2)
                    pfimW2.setPar(0)
                    self.FindHelper(look, pfimW2, self.Dict)
                    self.algorithm(look, pfimW2) 
                    return pfimW2
                
            elif(fimW.nextToFirst() == 'ו') and (self.num_of_a_roots(fimW.getText()[:-2]) < 3):
                isPar = True
                pfimW.equalTo(fimW)
                pfimW.setText('ה' + self.unFinal(fimW.getText()[:-2] + fimW.first()))
                pfimW.setConstruct()
                if fimW.first() == 'ת':
                    pfimW.Ht = False
                pfimW.setTense(2)
                pfimW.setPar(1)
                self.FindHelper(look, pfimW, self.Dict)
                self.algorithm(look, pfimW)        
            if(fimW.nextToLast() == 'ו') and (self.num_of_p_roots(fimW.getText()[2:]) < 3) and (not(fimW.last() == 'י')) and (not(fimW.last() == 'ו')):
                isPar = True
                pfimW2 = Word("","")
                pfimW2.equalTo(fimW)
                pfimW2.setText('ה' + self.unFinal(fimW.last() + fimW.getText()[2:]))
                pfimW2.setConstruct()
                pfimW2.setTense(2)
                pfimW2.setPar(0)
                self.FindHelper(look, pfimW2, self.Dict)
                self.algorithm(look, pfimW2)
                return pfimW2
                
            if isPar == True:
                return pfimW
        else:
            pword = Word("","")
            d = 0
            if word.getSuffix1() == True:
                d = 1
            if word.getSuffix2() == True:
                d = 2
            if(word.first() == 'מ')and (word.getLen() > 4):
                if(word.third() == 'ו') and (not((word.last() == 'ה')and(self.CurrentWord.getText()[d:1+d] == 'ת'))) and (self.num_of_a_roots(word.getText()[:-3]) < 3):
                    isPar = True
                    pword.equalTo(word)
                    pword.setText(word.getText()[:-3] + word.nextToFirst())
                    pword.setTense(2)
                    pword.setPar(1)
                    if word.first() == 'ת':
                        pword.Ht = False
                    self.FindHelper(look, pword, self.Dict)
                    self.algorithm(look, pword)
                if(word.nextToLast() == 'ו') and (self.num_of_p_roots(word.getText()[2:]) < 3) and (not(word.last() == 'י')) and (not((word.last() == 'ה')and(not(self.CurrentWord.last() == 'ה')))) and (not(word.last() == 'ו')) and (word.getConstruct() == False):
                    isPar = True
                    pword2 = Word("","")
                    pword2.equalTo(word)
                    pword2.setText(word.last() + word.getText()[2:-1])
                    pword2.setTense(2)
                    pword2.setPar(0)
                    self.FindHelper(look, pword2, self.Dict)
                    self.algorithm(look, pword2)
                    return pword2
                    
            elif(word.nextToFirst() == 'ו') and (not((word.last() == 'ה')and(self.CurrentWord.getText()[d:1+d] == 'ת'))) and (self.num_of_a_roots(word.getText()[:-2]) < 3):
                isPar = True
                pword.equalTo(word)
                pword.setText(word.getText()[:-2] + word.first())
                pword.setTense(2)
                pword.setPar(1)
                if word.first() == 'ת':
                    pword.Ht = False
                self.FindHelper(look, pword, self.Dict)
                self.algorithm(look, pword)      
            if(word.nextToLast() == 'ו') and (self.num_of_p_roots(word.getText()[2:]) < 3) and (not(word.last() == 'י')) and (not((word.last() == 'ה')and(not(self.CurrentWord.last() == 'ה')))) and (not(word.last() == 'ו')) and (word.getConstruct() == False):
                isPar = True
                pword2 = Word("","")
                pword2.equalTo(word)
                pword2.setText(word.last() + word.getText()[2:])
                pword2.setTense(2)
                pword2.setPar(0)
                self.FindHelper(look, pword2, self.Dict)
                self.algorithm(look, pword2)
                return pword2
                
            if isPar == True:
                return pword
        return Word("", "")
       
    def constr(self, look, word):
        if(word.getLen() < 2) or (word.getConstruct() == True) or (word.isVerb() == True) or (word.getPlural() == True) or (word.getDaul() == True) or (word.getTense() == 'Perfect') or (word.getTense() == 'Imperfect') or (word.getTense() == 'Imperative') or (word.getTense() == 'Infinitive') or (word.getPartiVal() == 0) or (word.getRL2() == word.last2()):
            return Word("", "")

        if(word.getLen() > 2):
            if(not ('י' in word.getSufxList())) and (word.last() == 'י') and ((self.CurrentWord.last() == 'י')or(word.getSuffix() == True)) and (not('ם' in word.getSufxList())):
                constW = Word("","")
                constW.equalTo(word)
                constW.setText(self.Final(constW.getText()[1:]))
                if(word.last2() == 'יי'):
                    daulW = Word("","")
                    daulW.equalTo(word)
                    daulW.setText(self.Final(constW.getText()[1:]))
                    daulW.setDaul()
                    daulW.setConstruct()
                    daulW.setNoun()
                    self.FindHelper(look, daulW, self.Dict)
                    self.algorithm(look, daulW)
                    
                    daulW2 = Word("","")
                    daulW2.equalTo(word)
                    daulW2.setText('ם' + word.getText())
                    daulW2.setConstruct()
                    daulW2.setNoun()
                    self.FindHelper(look, daulW2, self.Dict)
                else:   
                    constW.setPlural()
                    constW.setConstruct()
                    constW.setNoun()
                    self.FindHelper(look, constW, self.Dict)                
                    
                    constW2 = Word("","")
                    constW2.equalTo(word)
                    constW2.setText('ם' + word.getText())
                    constW2.setConstruct()
                    constW2.setNoun()
                    self.FindHelper(look, constW2, self.Dict)
                    self.algorithm(look, constW)
                return constW
                
        if(word.getLen() > 2) and (word.last() == 'ת'):
            constW = Word("","")
            constW.equalTo(word)
            constW.setText(self.Final(word.getText()[1:]))
            self.FindHelper(look, constW, self.Dict)
            self.irreg(look, constW)
            constW2 = Word("", "")
            constW2.equalTo(constW)
            constW2.setText('ה' + word.getText()[1:])
            constW2.setNoun()
            constW2.setConstruct()
            self.FindHelper(look, constW2, self.Dict)
            self.algorithm(look, constW2)
            return constW
        return Word("", "")    
                
    def irreg(self, look, word):
        if(word.getLen() < 1) or (word.getIrregVal() > 15):
            return Word("", "")
            
        if(word.getLen() > 1):
            if ((word.first() == 'ה') or (word.first() == 'י')) and (not(('ו' in word.getPrixList())and(word.getTense() == 'Perfect')and(word.getPerson() == '1st, pl.'))) and (not((not ('ו' in word.getPrixList()))and(word.getTense() == 'Imperfect')and(word.getPerson() == '1st, pl.'))) and (not (word.getVerbform() == 'Niphal')) and (not((word.getVerbform() == 'Pual') or (word.getVerbform() == 'Piel') or (word.getPartiVal() == 1))):
                irregW5 = Word("","")
                irregW5.equalTo(word)
                irregW5.setText(word.getText()[:-1] + 'נ')
                irregW5.setIrreg()
                self.FindHelper(look, irregW5, self.Dict)
                self.irreg(look, irregW5)
                
            if(word.last() == 'י') and (not(word.getConstruct() == True)) and (not(self.CurrentWord.last() == 'י')) and (not(word.getRL2() == word.last2)) and (not(word.getPartiVal() == 0)):
                irregW6 = Word("","")
                irregW6.equalTo(word)
                irregW6.setText('ה' + word.getText()[1:])
                irregW6.setIrreg()
                self.FindHelper(look, irregW6, self.Dict)
                self.irreg(look, irregW6)
                if(irregW6.getLen() > 2) and (irregW6.nextToLast() == 'י') or (irregW6.nextToLast() == 'ו'):
                    irregW7 = Word("","")
                    irregW7.equalTo(word)
                    irregW7.setText('ה' + word.getText()[2:])
                    irregW7.setIrreg()
                    self.FindHelper(look, irregW7, self.Dict)
                    self.irreg(look, irregW7)
                      
        if ((word.getLen() == 1) or ((word.getLen() == 2)and(word.last() == 'ת'))) and ((word.isTense() == True) or (word.getPrefix() == True)) and (not(('ו' in word.getPrixList())and(word.getTense() == 'Perfect')and(word.getPerson() == '1st, pl.'))) and (not((not ('ו' in word.getPrixList()))and(word.getTense() == 'Imperfect')and(word.getPerson() == '1st, pl.'))) and (not (word.getVerbform() == 'Niphal')):
            irregW = Word("","")
            irregW.equalTo(word)
            if(word.getLen() == 2):
                if(not(word.first() == 'נ')) and (not(self.CurrentWord.first() == 'נ')) and (not(word.getRL2() == word.last2())):
                    irregW.setText(self.Final(word.getText()[1:]) + 'נ')
            elif ((word.getPrefix() == True) or (word.getTense() == 'Infinitive') or (word.getTense() == 'Imperfect') or (word.getTense() == 'Cohortative')):
                irregW.setText(word.getText() + 'נ')
            if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not('ה' in word.getSufxList())) and (not(word.last() == 'ה')) and (not (self.CurrentWord.last() == 'ה')) and (not(('ו' in word.getPrixList())and(word.getTense() == 'Imperfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))) and (not((not ('ו' in word.getPrixList()))and(word.getTense() == 'Perfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))):
                irregWh = Word("","")
                irregWh.equalTo(irregW)
                irregWh.setText('ה' + self.unFinal(word.getText()))
                if(word.last() == 'ת') and (word.isNoun() == True):
                    irregWh.setConstruct()  
                self.FindHelper(look, irregWh, self.Dict)
            self.FindHelper(look, irregW, self.Dict)
            
            if (not(word.last() == 'ן')) and (not(self.CurrentWord.last() == 'ן')):
                irregWNN = Word("","")
                irregWNN.equalTo(irregW)
                irregWNN.setText('ן' + self.unFinal(irregW.getText()))
                irregWNN.setIrreg()
                self.FindHelper(look, irregWNN, self.Dict)
                if word.getLen() == 1:
                    return Word("", "")
        
        if(word.getLen() == 2):
            if(not(word.getTense() == 'Participle')) and (not(word.getVerbform() == 'Pual')):
                irreg1 = Word("","")
                irreg1.equalTo(word)
                irreg1.setText(word.last() + 'ו' + word.first())
                if irreg1.getTenseVal() == 2:
                    irreg1.setTense(-1)
                irreg1.setIrreg()
                self.FindHelper(look, irreg1, self.Dict)
            
            if(not(word.getVerbform() == 'Piel')):
                irreg2 = Word("","")
                irreg2.equalTo(word)
                irreg2.setText(word.last() + 'י' + word.first())
                irreg2.setIrreg()
                self.FindHelper(look, irreg2, self.Dict)
                
            if(self.CurrentWord.first() == word.first()) and (self.CurrentWord.getLen() == 2):
                irregipW = Word("","")
                irregipW.equalTo(word)
                irregipW.setText(word.getText() + 'ה')
                irregipW.setIrreg()
                irregipW.setTense(4)
                self.FindHelper(look, irregipW, self.Dict)
                self.irreg(look, irregipW)
                
                irregipW2 = Word("","")
                irregipW2.equalTo(word)
                irregipW2.setText(word.getText() + 'י')
                irregipW2.setIrreg()
                irregipW2.setTense(4)
                self.FindHelper(look, irregipW2, self.Dict)
                self.irreg(look, irregipW2)
                
                irregipW3 = Word("","")
                irregipW3.equalTo(word)
                irregipW3.setText(word.getText() + 'נ')
                irregipW3.setIrreg()
                irregipW3.setTense(4)
                self.FindHelper(look, irregipW3, self.Dict)
                self.irreg(look, irregipW3)
                
        if(word.getLen() == 3):
            if (word.nextToLast() == 'ו') or (word.nextToLast() == 'י'):
                hollow = Word("","")
                hollow.equalTo(word)
                hollow.setText(word.last() + word.first())
                hollow.setIrreg()
                self.FindHelper(look, hollow, self.Dict)
        
        if (word.isVerb() == True) and (((word.getTense() == "Infinitive")and(word.getLen() < self.CurrentWord.getLen()-len(word.getPrixList()) - 1)and(not(self.CurrentWord.last() == word.last()))) or ((word.getTense() == "Imperfect")and('ו' in word.getPrixList())and(word.getLen() < self.CurrentWord.getLen()-len(word.getPrixList())-1)and(not(self.CurrentWord.last() == word.last()))) or ((word.getTense() == "Perfect")and(not('ו' in word.getPrixList()))and(word.getLen() < self.CurrentWord.getLen()-len(word.getPrixList())-1)and(not(self.CurrentWord.last() == word.last())))) and (not ('ן' in word.getSufxList())) and (not(word.last() == 'ן')) and (not(self.CurrentWord.last() == 'ן')):
            irregWN = Word("","")
            irregWN.equalTo(word)
            irregWN.setText('ן' + self.unFinal(word.getText()))
            irregWN.setIrreg()
            self.FindHelper(look, irregWN, self.Dict)
            #return Word("", "")
            
        if(word.getLen() > 2):
            irregWnun2 = Word("","")
            irregWnun2.equalTo(word)
            if(word.nextToFirst() == 'נ') and (word.isParticiple() == False):
                irregWnun2.setText(word.getText()[:-2] + word.first())
                irregWnun2.setIrreg()
                self.FindHelper(look, irregWnun2, self.Dict)
                if word.isTense == False:
                    self.tense(look, irregWnun2, True)
                    return Word("", "")
            
            if(not(word.getText()) == self.CurrentWord.getText()):
                if(word.nextToFirst() == 'י'):
                    irreg3 = Word("","")
                    irreg3.equalTo(word)
                    irreg3.setText(word.getText()[:-2] + word.first())
                    irreg3.setIrreg()
                    self.FindHelper(look, irreg3, self.Dict)
          
                if(word.nextToLast() == 'י') and (word.getPlural == False) and (not(word.last2()  in suffix)):
                    irreg3 = Word("","")
                    irreg3.equalTo(word)
                    irreg3.setText(word.last() + word.getText()[2:])
                    irreg3.setIrreg()
                    self.FindHelper(look, irreg3, self.Dict)
 
        #checking to see if any tavs or hays have been removed form the end of the word, or if any extra vawls have been added within the word
        if (word.getLen() > 3) and (not(word.getPartiVal() == 0)) and ((word.getSuffix() == True) or (not (word.last3() == self.CurrentWord.last3()))) and (('ו' in word.getPrixList()) or (word.getTense() == "Perfect") or (word.getTense() == "Imperfect") or (word.getTense() == "Imperative") or (word.getTense() == "Infinitive")):
            if((not(((word.getConstruct() == True) and (((word.getPlural() == True)and(self.CurrentWord.getX(self.CurrentWord.getLen() - 2) == word.last())) or ((word.getDaul() == True)and(self.CurrentWord.getX(self.CurrentWord.getLen() - 3) == word.last())))) or ((word.getConstruct() == False) and (((word.getPlural() == True)and(self.CurrentWord.getX(self.CurrentWord.getLen() - 3) == word.last())) or ((word.getDaul() == True)and(self.CurrentWord.getX(self.CurrentWord.getLen() - 4) == word.last())))))) and (not((word.getConstruct() == True)and((word.getPlural() == False)and(word.getDaul() == False)) and (self.CurrentWord.last2()[-1:] == word.last()))) or ((word.getTense() == "Imperfect")and('ו' in word.getPrixList())) or ((word.getTense() == "Perfect")and(not 'ו' in word.getPrixList()))) and (word.getSuffix() == True) and (not ('ה' in word.getSufxList())):
                if(not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())) and (not(('ו' in word.getPrixList())and(word.getTense() == 'Imperfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))) and (not((not ('ו' in word.getPrixList()))and(word.getTense() == 'Perfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))):
                    irregW = Word("","")
                    irregW.equalTo(word)
                    irregW.setText('ה' + self.unFinal(word.getText()))
                    irregW.setIrreg()
                    self.FindHelper(look, irregW, self.Dict)
            elif (not(('וה' in word.getSufxList())or('ןהי' in word.getSufxList())or('םה' in word.getSufxList()))) and (word.getTense() == "Imperative") and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())) and (not ('ה' in word.getSufxList())) and (not(('ו' in word.getPrixList())and(word.getTense() == 'Imperfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))) and (not((not ('ו' in word.getPrixList()))and(word.getTense() == 'Perfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))):
                irregW = Word("","")
                irregW.equalTo(word)
                irregW.setText('ה' + self.unFinal(word.getText()))
                irregW.setIrreg()
                self.FindHelper(look, irregW, self.Dict)
            elif (word.getTense() == "Perfect") and (not(self.CurrentWord.last3() == word.last3())):
                if((word.last3() == 'יוו') or (word.last3() == 'ווי') or (word.last3() == 'ויו')):
                    irregWa = Word("","")
                    irregWa.equalTo(word)
                    irregWa.setText('ה' + word.getText()[3:])
                    irregWa.setIrreg()
                    self.FindHelper(look, irregWa, self.Dict)
                elif((word.last2() == 'וי') or (word.last2() == 'יו') or (word.last2() == 'וו')):
                    irregWb = Word("","")
                    irregWb.equalTo(word)
                    irregWb.setText('ה' + word.getText()[2:])
                    irregWb.setIrreg()
                    self.FindHelper(look, irregWb, self.Dict)
                elif((word.last() == 'י') or (word.last() == 'ו')):
                    irregWc = Word("","")
                    irregWc.equalTo(word)
                    irregWc.setText('ה' + word.getText()[1:])
                    irregWc.setIrreg()
                    self.FindHelper(look, irregWc, self.Dict)
            elif (word.getTense() == "Imperfect") and (not(self.CurrentWord.last3() == (word.last3()))):
                if(word.getLen() > 3) and ((word.last3() == 'יוו') or (word.last3() == 'ווי') or (word.last3() == 'ויו')):
                    irregWa = Word("","")
                    irregWa.equalTo(word)
                    irregWa.setText('ה' + word.getText()[3:])
                    irregWa.setIrreg()
                    self.FindHelper(look, irregWa, self.Dict)
                elif(word.getLen() > 2) and ((word.last2() == 'וי') or (word.last2() == 'יו') or (word.last2() == 'וו')):
                    irregWb = Word("","")
                    irregWb.equalTo(word)
                    irregWb.setText('ה' + word.getText()[2:])
                    irregWb.setIrreg()
                    self.FindHelper(look, irregWb, self.Dict)
                elif((word.last() == 'י') or (word.last() == 'ו')):
                    irregWc = Word("","")
                    irregWc.equalTo(word)
                    irregWc.setText('ה' + word.getText()[1:])
                    irregWc.setIrreg()
                    self.FindHelper(look, irregWc, self.Dict)
         
        #checking to see if any letters have been assimilated from the beginning of the word.         
        if ((word.getPrefix() == True) or (word.getTense() == 'Infinitive') or (word.getTense() == 'Imperfect') or (word.getTense() == 'Cohortative')) and (not(word.getPartiVal() == 1)):
            if (not((word.getVerbform() == 'Hophal')or(word.getVerbform() == 'Hiphil')or(word.getVerbform() == 'Hithpeal'))) and (not(word.getIrregVal() > 0)) and ((not ('ה' in word.getPrixList())) and (not (self.CurrentWord.first() == 'ה')) and (not (word.first() == 'ה'))):
                irregW = Word("","")
                irregW.equalTo(word)
                irregW.setText(word.getText() + 'ה')
                irregW.setIrreg()
                self.FindHelper(look, irregW, self.Dict)
                self.irreg(look, irregW)
                
            if(not(('ו' in word.getPrixList())and(word.getTense() == 'Perfect')and(word.getPerson() == '1st, pl.'))) and (not((not ('ו' in word.getPrixList()))and(word.getTense() == 'Imperfect')and(word.getPerson() == '1st, pl.'))) and (not (word.getVerbform() == 'Niphal')) and (not ((word.first() == 'נ') and (word.getIrregVal() > 0))):
                irregW2 = Word("","")
                irregW2.equalTo(word)
                irregW2.setText(word.getText() + 'נ')
                irregW2.setIrreg()
                self.FindHelper(look, irregW2, self.Dict)
                self.irreg(look, irregW2)
            if(not(('ו' in word.getPrixList())and(word.getTense() == 'Perfect')and(word.getGender() == 'm.')and((word.getPerson() == '3rd, sg.')or(word.getPerson() == '')))) and (not((not ('ו' in word.getPrixList()))and(word.getTense() == 'Imperfect')and(word.getGender() == 'm.')and((word.getPerson() == '3rd, sg.')or(word.getPerson() == '')))) and (not ((word.first() == 'י') and (word.getIrregVal() > 0))):
                irregW3 = Word("","")
                irregW3.equalTo(word)
                irregW3.setText(word.getText() + 'י')
                irregW3.setIrreg()
                self.FindHelper(look, irregW3, self.Dict)
                
            return Word("", "")
                        
        return Word("", "")       
        
    def build(self):
        #collecting user words form Json file (the database)
        self.store = JsonStore('data/WordsFinalFixed.json')
        
        # Building .kv file
        #with open('hebrewdictionary2.kv', encoding='utf8') as f:
            #root_widget = builder.Builder.load_string(f.read())
            
        return self.startInterface()
      
if __name__ == '__main__':
    HebrewDictionary().run()