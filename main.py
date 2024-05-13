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
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.base import runTouchApp
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from codecs import decode
from kivy.core.clipboard import Clipboard
import math
import string
import os
import sys
import unicodedata

Display_Size = 22

# color values
red = [1, 0, 0, 1]
green = [0, 1, 0, 1]
sky_biue = [135, 206, 235]
blue = [0, 0, 1, 1]
purple = [1, 0, 1, 1]
white = [1, 1, 1, 1]
black = [0, 0, 0, 0]

AlefBet = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת', 'ך', 'ם', 'ן', 'ף', 'ץ']
Gender = ['m.', 'f.', '', '']
Person = ['1st, sg.', '1st, pl.', '2nd, sg.', '2nd, pl.', '3rd, sg.', '3rd, pl.', '']
tenses = ['Perfect', 'Imperfect', 'Participle', 'Infinitive', 'Imperative', 'Cohortative', 'Infinitive abs.', '']
tenseVals = [3, 3, 3, 3, 3, 3, 3, 1]
verbforms = ['Qal', 'Niphal', 'Piel', 'Pual', 'Hiphil', 'Hophal', 'Hithpeal', 'Hishtaphel', 'Pilpel', 'Nithpael', 'Pilel', 'Pulal', 'Tiphil', 'Hithpoel', 'Hithpolel', 'Hithpalpel', 'Hothpaal', '']
verbformVals = [1, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 1]
millenn = ['ה','ד','ג', 'ב', 'א']
Hithpeal = ['Hithpeal', 'Hithpalpel', 'Hithpoel', 'Hithpolel', 'Nithpael', 'Hothpaal']
Hiphil = ['Hiphil', 'Tiphil', 'Hishtaphel']
Pual = ['Pual', 'Pulal', 'Poal', 'Polpal']
Piel = ['Piel', 'Poel', 'Pilpel', 'Pilel', 'Palel', 'Polel', 'Pealal']
Qal = ['Qal']
Niphal = ['Niphal']
Hophal = ['Hophal']
suffix = ['הנה', 'ןכ', 'ונ', 'םכ', 'ןכ', 'םה', 'ומ', 'ם', 'ןה', 'ן', 'ית', 'ינ', 'י', 'ה', 'הנ', 'וה', 'ו', 'ך']
suffixPos= ['הנהי', 'םכי', 'ןכי', 'םהי', 'ןהי', 'הי', 'וי', 'ךי', 'יי', 'ןי', 'וני']
prefixL = ['תת', 'ה', 'ו', 'מ', 'ב','כ', 'ש', 'ל']
prefixV = {"תת":4, 'ה':0.5, 'ו':0.25, 'מ':2, 'ב':2,'כ':3, 'ש':3, 'ל':3}
modernL = ['קינ', 'רטמ', 'הקס', 'םינו', 'דיאו', 'ןמ', 'הינמ', 'סיזניק', 'פוקס', 'היפרג', 'היצ', 'ןקי', 'הק', 'הקי', 'טסי', 'םזי', 'הז', 'יל', 'יא', 'תי', 'תויו']
prephrase = ['ת', 'ה', 'ו', 'מ', 'ב','כ', 'ש', 'ל']
plural = ['תו', 'םי', 'םיי']
metathesis = ['ס', 'ש', 'צ']
Obj = ['םתוא', 'ןתוא', 'ךתוא', 'התוא', 'ותוא', 'ונתוא', 'םהתא', 'ןהתא', 'םכתא', 'ןכתא']
vowels = ['ֵ']
a_roots = ['א', 'ב', 'ג', 'ד', 'ז', 'ח', 'ט', 'כ', 'ל', 'מ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ף', 'ץ']
roots = ['ג', 'ד', 'ז', 'ח', 'ט', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ף', 'ץ']
p_roots = ['ג', 'ד', 'ז', 'ח', 'ט', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ף', 'ץ']
Finals = ['ך', 'ם', 'ן', 'ף', 'ץ']
finals = {'כ':'ך', 'מ':'ם', 'נ':'ן', 'פ':'ף', 'צ':'ץ'}
unFinals = {'ך':'כ', 'ם':'מ', 'ן':'נ', 'ף':'פ', 'ץ':'צ'}
prefixD = {"תת":"sub", "ה":"the", "ו":"and", "ב":"in/at/with/by/during", "מ":"from", "ל":"to/toward/for", "כ":"as/like", "ש":"which"}
ssuffix = {"ןה":"their/them (f.)", "הנה":"their/them (f.)", "ן":"their/them (f.)", "םה":"their/them (m.)", "ם":"their/them (m.)", "ומ":"their/them (m.)", "ה":"hers/her", "הנ":"hers/her", "ו":"his/him", "וה":"his/him", "ןכ":"your/you (pl. f.)", "םכ":"your/you (pl. m.)", "ך":"you/your (m.)", "ונ":"our/us", "ית":"my/me", "י":"my/me", "ינ":"my/me"}
suffFactors = {"ןה":5, "הנה":7, "ן":6, "םה":5, "ם":6, "ומ":6, "ה":4, "הנ":6, "ו":6, "וה":4.5, "ןכ":5, "םכ":5, "ך":5, "ונ":5, "ית":5, "י":4, "ינ":5}
#suffixObj = {"וה":"him", "וי":"his/him", "ינ":"me", "ה":"her", "ו":"his/him", "ך":"you/your"}
parti = {1:'Active', 0:'Passive', 2:''}
gemontria = {'א':1, 'ב':2, 'ג':3, 'ד':4, 'ה':5, 'ו':6, 'ז':7, 'ח':8, 'ט':9, 'י':10, 'כ':20, 'ל':30, 'מ':40, 'נ':50, 'ס':60, 'ע':70, 'פ':80, 'צ':90, 'ק':100, 'ר':200, 'ש':300, 'ת':400, 'ך':20, 'ם':40, 'ן':50, 'ף':80, 'ץ':90}
brackets = ['(', ')', '[', ']', '{', '}']
punctuation = ['\"','”', '\'', '.', '?', '׃', ';', ':', ')', '(', '[', ']', '}', '{', '!']
delimiter = [',', '־', ' ', '-', ')', '(', '[', ']', '}', '{']
operators = ['&', '|', '∥', '+', '-', '*', '/', '>', '<', '¬', '=', '<>', '¬=', '¬<', '¬>', '**', '<=', '>=']
special_char = ['#', ')', '$', '&', '@', '^', '%', '~', '`', '*']
punctuation2 = ['\"','”', '\'', ',', '.', '?', ';', ':', ')', '(', '[', ']', '}', '{', '!']
delimiter2 = ['–', ',', ':', ' ', '=', ';', '.', '%', '-', ')', '(', '[', ']', '}', '{']
special_char2 = special_char+punctuation2+delimiter2+operators
escape_char = ['\"','”', '\'', '\b', '\f', '\ooo', '\\', '\n', '\r', '\t']
dirHey = "ה- to/toward"
INF = 100000000000

# This class defines all the properties and methods that a Word object needs to have in order
# use the proper metrics in searching and ordering words.
class Word:
    def __init__(self, t, d):
        
        self.text = t
        self.definition = d
        self.value = INF
        self.heyVal = 0.5
        self.lamedVal = 3
        self.memVal = 2
        self.betVal = 2
        self.cafVal = 3
        self.shinVal = 3
        self.vavVal = 0.25
        self.vrbFactor = 0
        self.nonFactor = 0
        self.prefactor = 4
        self.suffactor2 = 5
        self.suffactor3 = 6
        self.suffactor = 6
        self.hey1factor = 4
        self.plFactor = 1
        self.plFactor2 = 2
        self.dlFactor = 2
        self.dlFactor2 = 3
        self.mdrnFactor = 8
        self.cnstFactor = 3
        self.cnstFactor2 = 3
        self.irrgFactor = 8
        self.root = "000"
        self.preW = []
        self.sufW = []
        self.mdrnW = '###'
        self.prefix = 0
        self.partiW = 2
        self.suffix1 = 0
        self.suffix2 = 0
        self.suffix3 = 0
        self.hey1 = 0
        self.irreg = 0
        self.Ht = True
        self.modern = 0
        self.plural = 0
        self.dual = 0
        self.construct = 0
        self.verbform = -1
        self.tense = -1
        self.person = -1
        self.gender = -1
        self.Verb = False
        self.Noun = False
        self.VavSeq = False

    def __assign__(self, value):
        self.value = value.value
        self.text = value.text
        self.partiW = value.partiW
        self.hey1 = value.hey1
        self.hey1factor = value.hey1factor
        self.definition = value.definition
        self.Verb = value.Verb
        self.Noun = value.Noun
        self.VavSeq = value.VavSeq
        self.vrbFactor = newWord.vrbFactor
        self.nonFactor = newWord.nonFactor
        self.prefix = value.prefix
        self.root = value.root
        self.suffix1 = value.suffix1
        self.suffix2 = value.suffix2
        self.suffix3 = value.suffix3
        self.irreg = value.irreg
        self.Ht = value.Ht
        self.modern = value.modern
        self.mdrnW = value.mdrnW
        self.plural = value.plural
        self.dual = value.dual
        self.construct = value.construct
        self.verbform = value.verbform
        self.tense = value.tense
        self.person = value.person
        self.gender = value.gender
        self.preW = value.preW.copy()
        self.sufW = value.sufW.copy()
    
    def equalTo(self, newWord):
        self.value = newWord.value
        self.text = newWord.text
        self.partiW = newWord.partiW
        self.hey1 = newWord.hey1
        self.hey1factor = newWord.hey1factor
        self.definition = newWord.definition
        self.Verb = newWord.Verb
        self.Noun = newWord.Noun
        self.VavSeq = newWord.VavSeq
        self.vrbFactor = newWord.vrbFactor
        self.nonFactor = newWord.nonFactor
        self.prefix = newWord.prefix
        self.root = newWord.root
        self.suffix1 = newWord.suffix1
        self.suffix2 = newWord.suffix2
        self.suffix3 = newWord.suffix3
        self.irreg = newWord.irreg
        self.Ht = newWord.Ht
        self.modern = newWord.modern
        self.mdrnW = newWord.mdrnW
        self.plural = newWord.plural
        self.dual = newWord.dual
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
        if not (self.hey1 == newWord.hey1):
            return False
        if not (self.Noun == newWord.Noun):
            return False
        if not (self.Verb == newWord.Verb):
            return False
        if not (self.hey1factor == newWord.hey1factor):
            return False
        if not (self.getSuffix() == newWord.getSuffix()):
            return False
        if not (self.isVavSeq() == newWord.isVavSeq()):
            return False
        if not(self.Ht == newWord.Ht):
            return False
        if not (self.getModern() == newWord.getModern()):
            return False
        if not (self.getModernW() == newWord.getModernW()):
            return False
        if not (self.getPlural() == newWord.getPlural()):
            return False
        if not (self.getDual() == newWord.getDual()):
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
        #if not (self.isVerb() == newWord.isVerb()):
            #return False
        #if not (self.isNoun() == newWord.isNoun()):
            #return False
        return True
        
    def Is(self, newWord):
        if not (self.text == newWord.text):
            return False
        if not (self.getPrefix() == newWord.getPrefix()):
            return False
        if not (self.root == newWord.root):
            return False
        if not (self.Noun == newWord.Noun):
            return False
        if not (self.value == newWord.value):
            return False
        if not (self.Verb == newWord.Verb):
            return False
        if not (self.partiW == newWord.partiW):
            return False
        if not (self.hey1 == newWord.hey1):
            return False
        if not (self.hey1factor == newWord.hey1factor):
            return False
        if not (self.getSuffix() == newWord.getSuffix()):
            return False
        if not (self.isVavSeq() == newWord.isVavSeq()):
            return False
        if not (self.getSuffix() == newWord.getSuffix()):
            return False
        if not (self.getModern() == newWord.getModern()):
            return False
        if not (self.getModernW() == newWord.getModernW()):
            return False
        if not (self.getPlural() == newWord.getPlural()):
            return False
        if not (self.getDual() == newWord.getDual()):
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
        
    def hasRoot(self):
        if(self.root == "000"):
            return False
        else:
            return True
            
    def isRoot(self):
        if(self.text == self.root):
            return True
        else:
            return False
    
    def getText(self):
        return self.text
    
    def getDefinition(self):
        return self.definition
        
    def isVerb(self):
        return self.Verb
        
    def isNoun(self):
        return self.Noun
        
    def isVavSeq(self):
        return self.VavSeq
    
    def getHey1(self):
        return self.hey1

    def getHeyDir(self):
        if(self.hey1 > 0):
            return True
        else:
            return False

    def isParticiple(self):
        if self.partiW == 2:
            return False
        else:
            return True
            
    def isPhrase(self):
        if(self.NumWsInPhr() > 1):
            return True
        else:
            return False

    def getTense(self):
        return tenses[self.tense]
        
    def getTenseVal(self):
        return self.tense
        
    def getPerson(self):
        return Person[self.person]
    
    def getPersonVal(self):
        return self.person
    
    def getGender(self):
        return Gender[self.gender]
        
    def getGenderVal(self):
        return self.gender
    
    def getVerbform(self):
        return verbforms[self.verbform]
    
    def getVerbformVal(self):
        return self.verbform
        
    def getPartiVal(self):
        return self.partiW
        
    def getLen(self):
        return len(self.text)
        
    def getGrstphLen(self):
        temp = self.text.replace("-", " ")
        inputL = temp.split()
        sz = 0
        for w in inputL:
            if(len(w) > sz):
                sz = len(w)
        return sz
        
    def getGrstExphLen(self):
        temp = self.text.replace("-", " ")
        inputL = temp.split()
        sz = 0
        for w in range(len(inputL)):
            if(len(inputL[w]) > sz) and (not(w == 0)):
                sz = len(inputL[w])
        return sz
        
    def getphLen(self):
        temp = self.text.replace("-", " ")
        inputL = temp.split()
        sz = len(temp)
        for w in inputL:
            if(len(w) < sz):
                sz = len(w)
        return sz
        
    def getExphLen(self):
        temp = self.text.replace("-", " ")
        inputL = temp.split()
        sz = len(temp)
        for w in range(len(inputL)):
            if(len(inputL[w]) < sz) and (not(w == 0)):
                sz = len(inputL[w])
        return sz

    def NumWsInPhr(self):
        temp = self.text.replace("-", " ")
        inputL = temp.split()

        return len(inputL)

    def getFrsLen(self):
        temp = self.text.replace("-", " ")
        inputL = temp.split()
        first = len(inputL) - 1
        
        if(len(inputL) == 0):
            return 0
        
        return len(inputL[first])
        
    def getLstLen(self):
        temp = self.text.replace("-", " ")
        inputL = temp.split()
        
        if(len(inputL) == 0):
            return 0
        
        return len(inputL[0])
        
    def getGemontria(self):
        g = 0
        nText = self.text.strip('"')
        nText = nText.strip("'")
        for letter in nText:
            if letter in gemontria:
                g += gemontria[letter]   
        return g
        
    def getTGemontria(self, t):
        g = 0
        nText = t.strip('"')
        nText = nText.strip("'")
        for letter in nText:
            if letter in gemontria:
                g += gemontria[letter]   
        return g
        
    #def calValue(self):
        #if(self.value == 0):
            #self.value = 100000000000 - 10*((self.prefix + 1)*(self.suffix1 + 1)*(self.suffix2 + 1)*(self.suffix3 + 1)*(self.plural + 1)*(self.modern + 1)*(self.irreg + 1)*(tenseVals[self.tense])*(self.verbformVals[self.verbform]))
        #return self.value
        
    def getValue(self):
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
        if(self.irreg > 0):
            return True
        return False
        
    def getModern(self):
        if(self.mdrnW == '###'):
            return False
        else:
            return True
        
    def getPlural(self):
        if(self.plural > 0):
            return True
        return False
        
    def getDual(self):
        if(self.dual > 0):
            return True
        return False
        
    def getConstruct(self):
        if(self.construct > 0):
            return True
        return False
        
    def getPar(self):
        return parti[self.partiW]
        
    def getPrefixVal(self):
        return self.prefix
        
    def getPrefixW(self):
        s = ""
        for pre in self.preW:
            s += pre +  '- ' + prefixD[pre]+ ', '
        return s[:-2]
        
    def getPrixListEnd(self):
        s = ''
        for pre in self.preW:
            s = pre
        return s
        
    def getPrixList(self):
        return self.preW.copy()
        
    def getRoot(self):
        return self.root
        
    def getRootFirst(self):
        return self.root[-1:]
        
    def getRootFirst2(self):
        return self.root[-2:]
        
    def getRootLast(self):
        return self.root[:1]
        
    def getRootLast2(self):
        return self.root[:2]
        
    def getRootMiddle(self):
        return self.root[-1:1]
        
    def getSuffixW(self):
        s = ""
        for suff in self.sufW:
            s += suff + '- ' + ssuffix[suff] + ', '
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
        
    def getSuffix3Val(self):
        return self.suffix3
        
    def getIrregVal(self):
        return self.irreg
            
    def getModernVal(self):
        return self.modern
        
    def getModernW(self):
        return self.mdrnW
        
    def getPluralVal(self):
        return self.plural
        
    def getDualVal(self):
        return self.dual
        
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

    def setPrefixN(self, n):
        self.prefix = self.prefix +  n
        self.value = self.value - (n*(self.prefix/2))
        
    
    def setPrefix(self):
        self.prefix = self.prefix +  self.prefactor
        self.value = self.value - (self.prefactor*(self.prefix/2)) 
        
    def setRoot(self, R2):
        if(not('-' in self.text)):
            self.root = R2
        
    #def resetPrefix(self):
        #self.prefix = 0
        
    def setHey1(self):
        self.hey1 = self.hey1factor
        self.value = self.value - self.hey1factor
        
    def decPrefix(self):
        temp = self.prefix
        self.prefix = self.prefix - self.prefactor
        self.value = self.value + (self.prefactor*(temp/2))
        
    def decSuffix1(self):
        self.suffix1 = self.suffix1 - self.suffactor
        self.value = self.value + self.suffactor
            
    def setVavSeq(self):
        self.VavSeq = True
        self.value = self.value + (self.vavVal/2)
        
    def setVerb(self):
        if self.Verb == True:
            return
        self.Verb = True
        self.Noun = False
        self.value = self.value + self.vrbFactor
       
    def setNoun(self):
        if self.Noun == True:
            return
        self.Noun = True
        self.Verb = False
        self.value = self.value + self.nonFactor
        
    def unSetVerb(self):
        if self.Verb == False:
            return
        self.verb = False
        self.value = self.value - self.vrbFactor
        
    def setVfactor(self, num):
        self.vrbFactor = num
        
    def unSetNoun(self):
        if self.Noun == False:
            return
        self.Noun = False
        self.value = self.value - self.nonFactor
        
    def setNfactor(self, num):
        self.nonFactor = num
    
    def setSuffixX(self, suff):
        if(len(suff) == 1):
            self.suffix1 += suffFactors[suff]
        elif(len(suff) == 2):
            self.suffix2 += suffFactors[suff]
        elif(len(suff) == 3):
            self.suffix3 += suffFactors[suff]
        self.value = self.value - suffFactors[suff]
    
    def setSuffix1(self):
        self.suffix1 += self.suffactor
        self.value = self.value - self.suffactor
        
    def setSuffix2(self):
        self.suffix2 += (self.suffactor2)
        self.value = self.value - (self.suffactor2)
        
    def setSuffix3(self):
        self.suffix3 += (self.suffactor3) 
        self.value = self.value - (self.suffactor3)
          
    def setIrreg(self):
        self.irreg += self.irrgFactor
        self.value = self.value - self.irrgFactor
          
    def setModern(self):
        self.modern += self.mdrnFactor
        self.value = self.value - self.mdrnFactor
        
    def setPlural(self):
        self.plural += self.plFactor
        self.value = self.value - self.plFactor
        
    def setPlural2(self):
        self.plural += self.plFactor2
        self.value = self.value - self.plFactor2
        
    def resetPlural(self):
        if self.plural == 0:
            return
        self.plural = 0
        self.value = self.value + self.plFactor
        
    def setDual(self):
        self.dual += self.dlFactor
        self.value = self.value - self.dlFactor
        
    def setDual2(self):
        self.dual += self.dlFactor2
        self.value = self.value - self.dlFactor2
        
    def setConstruct(self):
       self.construct = self.cnstFactor
       self.value = self.value - self.cnstFactor
       
    def setConstruct2(self):
       self.construct = self.cnstFactor2
       self.value = self.value - self.cnstFactor2
        
    def resetConstruct(self):
        if self.construct == 0:
            return
        self.construct = 0
        self.value = self.value + self.cnstFactor
        
    def setTense(self, t):
        self.tense = t
        isTense = True
        if(self.tense == 2):
            self.value = self.value - (tenseVals[self.tense]*(1 + len(self.preW)))
        else:
            self.value = self.value - tenseVals[self.tense]
        if self.verbform == -1:
            self.setVerbform(0)
        
    def setPar(self, p):
        self.partiW = p
        
    def setPerson(self, p):
        self.person = p
        isPerson = True
        
    def setGender(self, g):
        if(self.getGenderVal() == -1):
            self.gender = g
            
    def setGenderF(self, g):
        self.gender = g
            
    def chanGender(self, g):
        self.gender = g
        
    def setVerbform(self, verb):
        self.verbform = verb
        isVerbf = True
        self.value = self.value - 2*(verbformVals[self.verbform])
    
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
        
    def remSuff(self):
        if(len(self.sufW[0]) == 1):
            self.suffix1 = 0
        elif(len(self.sufW[0]) == 2):
            self.suffix2 = 0
        elif(len(self.sufW[0]) == 3):
            self.suffix3 = 0
        self.value = self.value + (suffFactors[self.sufW[0]])
        self.sufW.pop(0)
        
    def setMdrn(self, modr):
        self.mdrnW = modr
        
    def rm(self, pre):
        self.preW.remove(pre)
        
    def rmSuf(self, suff):
        self.sufW.remove(suff)
        
    def addToValue(self, v):
        self.value = self.value - v
        
    def isFinal(self, l):
        if l in Finals:
            return True
        else:
            return False
            
    def isYear(self):
        if (self.getLen() < 2): #or (self.isFinal(self.last())):
            return False
        if (self.nextToFirst() == "'") and (self.first() in millenn) and (self.nextToLast() == '"') and (self.textIsNumb(self.unFinal(self.last()) + self.text[2:-2]) == True):
            return True
        if(not self.nextToFirst() == "'") and (self.nextToLast() == '"') and (self.textIsNumb(self.unFinal(self.last()) + self.text[2:]) == True):
            return True
        return False
        
    def getYear(self):
        if self.isYear() == False:
            return "Error"
            Year = 0;
        if (self.nextToFirst() == "'"):
            textYear = self.last() + self.text[2:-2]
            Year = self.getTGemontria(textYear) + 1000*(gemontria[self.first()])
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
            if nText in AlefBet:
                return True
            else:
                return False
        if nText == 'וט':
            return True
        if nText == 'זט':
            return True
        if nText == 'הי':
            return False
        if nText == 'וי':
            return False
        for i in range(len(nText)-1):
            if not (nText[i] in gemontria):
                if i == 0: 
                    return False
                return True
            if not nText[i+1] in gemontria:
                return False
            if self.rank(nText[i]) < 2:
                if self.rank(nText[i]) >= self.rank(nText[i+1]):
                    return False
            elif (self.rank(nText[i]) > self.rank(nText[i+1])) or (gemontria[nText[i]] > gemontria[nText[i+1]]):
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
            if not (nText[i] in gemontria):
                if i == 0: 
                    return False
                return True
            if not nText[i+1] in gemontria:
                return False
            if self.rank(nText[i]) < 2:
                if self.rank(nText[i]) >= self.rank(nText[i+1]):
                    return False
            elif (self.rank(nText[i]) > self.rank(nText[i+1])) or (gemontria[nText[i]] > gemontria[nText[i+1]]):
                return False
        return True
    
    def rank(self, n):
        if len(n) > 1:
            return -1
        if gemontria[n] < 10:
            return 0
        if (gemontria[n] >= 10) and (gemontria[n] < 100):
            return 1
        if gemontria[n] >= 100:
            return 2

class Word_ref:
    
    def __init__(self, Index):
        self.value = 0
        self.text= ""
        self.index = Index
        
    def getVal(self):
        return self.value
        
    def getText(self):
        return self.text
    
    def getIndex(self):
        return self.index
        
    def setVal(self, newVal):
        self.value = newVal
        
    def setText(self, newText):
        self.text = newText
        
    def setIndex(self, newIndex):
        self.index = newIndex

# This is a helper class which contain the methods for searching and choosing words. 
# It also has at least one container to store and sort certain Word objects.
class SearchWord:

    def __init__(self):
        self.Words = []
    
    def getWords(self):
        return list(self.Words.copy())
        
    def getNumWds(self):
        return len(self.Words)
        
    def addWord(self, w):
        self.Words.append(w)
        
    def getValue(self, word):
        return word.getValue()
        
    def indexWords(self, w):
        for i in range(len(self.getWords())):
            if w.getText() == self.getWords()[i].getText():
                return i
        return -1
        
    def indexComplWords(self, w):
        for i in range(len(self.getWords())):
            if w == self.getWords()[i]:
                return i
        return -1
        
    def indexW_Plus(self, w):
        indexes = []
        for i in range(len(self.getWords())):
            if w.getText() == self.getWords()[i].getText():
                indexes.append(i)
        return indexes
                
    def findText(self, w):
        for word in self.getWords():
            if (w.getText() == word.getText()):
                return True
        return False
        
    def HasWord(self, w):
        if w in self.getWords():
            return True
        return False
        
    def findref_Text(self, w, refW):
        for word in refW:
            if (w.getText() == word.getText()):
                return True
        return False
        
    def sumOfV(self, index):
        sumV = 0
        start = False
        largest = 0
        for i in index:
            if start == False:
                largest = self.Words[i].getValue()
                start = True
            elif largest < self.Words[i].getValue():
                largest = self.Words[i].getValue()
            
            sumV = sumV + self.Words[i].getValue()
            
        return largest + sumV/((len(index)))
        
    def getSumOfV(self, ref):
        return ref.getVal()
    
    def getValPerIndex(self, iV):
        return self.getWords()[iV].getValue()
    
    def group(self):
        temp_Words = []
        W_ref = []
        
        for word in self.getWords():
            if(self.findref_Text(word, W_ref) == False):
                index = self.indexW_Plus(word)
                index.sort(key=self.getValPerIndex, reverse = True)
                new_ref = Word_ref(index)
                new_ref.setText(word.getText())
                new_ref.setVal(self.sumOfV(index))
                W_ref.append(new_ref)
           
        W_ref.sort(key=self.getSumOfV, reverse = True)
        
        for ref in W_ref:
            for i in ref.getIndex():
                temp_Words.append(self.Words[i])
        
        self.Words = temp_Words.copy()
                
    def find(self, w, Dict):
        if w in self.getWords():
            index = self.indexComplWords(w)
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
            
            
# Keyboard interface
class Keyboard(GridLayout):
    
    def __init__(self, instance, **kwargs):
        super(Keyboard, self).__init__(**kwargs)
        self.main = instance
        
    def keyAction(self, k, instance):
        inputT = self.main.Input.text
        if(len(inputT) < 1):
            self.main.Input.text = k
        else:
            if((inputT[0] in unFinals) and (not (k == '-'))):
                self.main.Input.text = k + unFinals.get(inputT[0]) + inputT[1:]
            else:
                self.main.Input.text = k + inputT
        
    def rCharsAction(self, instance):
        newInput = self.main.Input.text
        revInput = ""
        word = ""
        words = newInput.split()
        wordsb = self.clean_vol(words)
        #end = len(self.main.Input.text)-1
        for index in range(len(wordsb)):
            wordsb[index] = self.parse(wordsb[index], ['|'])
        word = ' '.join(wordsb)
        #for index in range(end+1):
        #    if newInput[end-index] == '(':
        #        revInput += ')'
        #    elif newInput[end-index] == ')':
        #        revInput += '('
        #    elif newInput[end-index] == '[':
        #        revInput += ']'
        #    elif newInput[end-index] == ']':
        #        revInput += '['
        #    elif newInput[end-index] == '{':
        #        revInput += '}'
        #    elif newInput[end-index] == '}':
        #        revInput += '{'
        #    else:
            #revInput += newInput[end-index]
                
        revInput = self.chainParse(word, '|')
        
        brac = [['{','}'],['[',']'],['(',')']]
        self.main.Input.text =  self.revChar(self.parseAnybrac(revInput, brac, 0))
                
        #self.main.Input.text = self.revChar(self.num_parser(str(revInput)))
     
    def chainParse(self, str_words, delim):
        temp = str_words.split(' ')
        words = []
        for w in temp:
            words.append(self.rrev_wds(w, delim))
        return ' '.join(words)
    
    def parse(self, str_words, delims):
        cdelims = delims.copy()
        new_list = []
        words_plus = ""
        if(len(cdelims) > 0):
            d = cdelims.pop()
            list_words = str_words.split(d)
            for index in range(len(list_words)-1, -1, -1):
                new_list.append(self.parse(list_words[index], cdelims))
            words_plus = d.join(new_list)
            return words_plus
        else:
            return self.revS(str_words)
    
    def parseAnybrac(self, str_words, brac, n):
        if(n > len(brac)-1):
            return str_words
        l = 0
        r = 0
        opn = 0
        clsd = 0
        cl = -1
        op = -1
        list_words = []
        new_list = []
        L = brac[n][0]
        R = brac[n][1]
        Ls = []
        C = False
        Opn = L
        Cls = R
            
        for c in range(len(str_words)):
            if(c == 0):
                if(str_words[c] == Cls):
                    list_words.append(str_words[c])
                    r = 1
                    C = True
                elif(str_words[c] == Opn):
                    l = 0
                    Ls.append(c)
                    C = True
                    opn = 1
                    
            elif(c == len(str_words) - 1):
                if(opn == 0):
                    if(str_words[c] == Opn):
                        list_words.append(str_words[r:c])
                        list_words.append(str_words[c])
                    else:
                        list_words.append(str_words[r:c+1])
                elif(opn == 1):
                    if(str_words[c] == Opn):
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:c])
                            list_words.append(str_words[c])
                        else:
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:cl])
                            list_words.append(str_words[cl:c])
                            list_words.append(str_words[c])
                    elif(str_words[c] == Cls):
                        list_words.append(str_words[l:c+1])
                    else:
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:c+1])
                        else:
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:c1])    #((XX(X)XX(--
                            list_words.append(str_words[c1:c+1])
                elif(opn > 1):
                    if(str_words[c] == Cls):
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:l1])
                            list_words.append(str_words[l1:c+1])
                        else:             
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:c1])    #((XX(X)XX(--
                            list_words.append(str_words[c1:c+1])
                    elif(str_words[c] == Opn):
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:c])
                            list_words.append(str_words[c])
                        else:
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:cl])
                            list_words.append(str_words[cl:c])
                            list_words.append(str_words[c])
                    else:
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:c+1])
                        else:
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:cl])
                            list_words.append(str_words[cl:c+1])
            else:
                if(str_words[c] == Opn):
                    
                    Ls.append(c)
                    if(opn == 0):
                        if(c > r):
                            list_words.append(str_words[r:c])
                        l = c
                    opn += 1
                    
                elif(str_words[c] == Cls):
                    opn = opn - 1
                    if(opn < 0):
                        list_words.append(str_words[r:c] + str_words[c])
                        cl = -1
                        r = c + 1
                        opn = 0
                    else:
                        p = Ls.pop
                        if(opn == 0):
                            cl = -1
                            if(c > l):
                                list_words.append(str_words[l:c] + str_words[c])
                            else:
                                list_words.append(str_words[c])
                            r = c + 1
                        elif(opn > 0):
                            cl = c+1
                            op = p
 
        if(r > 0) or (l > 0) or (C == True):
            for index in range(len(list_words)-1, -1, -1):
                if(list_words[index][0] == Opn) and (list_words[index][-1] == Cls):
                    new_list.append(Opn + self.parseAnybrac(list_words[index][1:-1], brac, n) + Cls)
                elif(list_words[index][0] == Opn):
                    new_list.append(self.parseAnybrac(list_words[index][1:], brac, n) + Cls)
                elif(list_words[index][-1] == Cls):
                    new_list.append(Opn + self.parseAnybrac(list_words[index][:-1], brac, n))
                else:
                    new_list.append(self.parseAnybrac(list_words[index], brac, n))
            if(len(new_list) > 1):
                return ''.join(new_list)
            elif (len(new_list) > 0):
                return new_list[0]
            else: 
                return str_words
            
        elif(n < len(brac)-1):
            return self.parseAnybrac(str_words, brac, n+1)
        else:
            return self.num_parser(self.revS(str_words))
        
    def num_parser(self, words):
        fixText = ""
        c = False
        p = False
        d = []
        s =-1
        brackets = ['(', ')', '[', ']', '{', '}']
        plus = ['+', '-']
        for num in range(len(words)):
            if(words[num] == '|'):
                return words
            if(words[num].isdigit() == True) or (not(words[num] in AlefBet+delimiter+punctuation+special_char+operators)):
                c = False
                p = False
                if(s == -1):
                    s = num
                
                if(num == len(words)-1):
                    fixText += self.revS(words[s:num+1])
            elif((c == True)):
                temp = ""
                tempW = words[s:num-1]
                if(p == True):
                    d.pop()
                temp = self.revS(words[s:num-1])
                for x in d:
                    if(x in special_char+plus):
                        if(words[num-1] in brackets):
                            if(temp == ""):
                                temp = words[s:num-1]
                            else:
                                temp = temp
                        else:     
                            if(temp == ""):
                                temp = words[s:num-1]
                            else:
                                temp = temp
                    elif(x in punctuation):
                        if(words[num-1] in brackets):
                            if(temp == ""):
                                 temp = words[s:num-1]
                            else:
                                temp = temp
                        else:     
                            if(temp == ""):
                                 temp = words[s:num-1]
                            else:
                                temp = temp
                    elif(x in delimiter):
                        if(temp == ""):
                            temp = words[s:num-1]
                        else:
                            temp = temp
                    else:
                        if(temp == ""):
                            temp = self.revS(words[s:num-1])
                        else:
                            temp = self.revS(temp)
                fixText = fixText + (temp + words[num-1] + words[num])
                d = []  
                s = -1
                c = False
                p = False
            elif(c == False):
                if(not(s == -1)):
                    if(words[num] in (delimiter+special_char+punctuation+plus)):
                        c = True
                        if(not(words[num] in d)):
                            p = True
                            d.append(words[num])
                    if(num == len(words)-1):
                        fixText += self.revS(words[s:num+1])
                else:
                    fixText += words[num]
        return fixText
        
    
    def exclude(self, b, a):
        c = []
        for e in b:
            if(not(e in a)):
                c.append(e)
        return c
        
    def intrsc(self, h, g):
        v = []
        for e in h:
            if(e in g):
                v.append(e)
        return v
    
    def revChar(self, words):
        numWords = ""
        n = 0;
        pre = False
        c = False
        spch = [':', '-']
        brackets = ['(', ')', '[', ']', '{', '}']
        d = []
        for i in range(len(words)):
            if(i > 0):
                if(not(words[i-1] in AlefBet+punctuation+spch)) and (words[i-1].isdigit() == False):
                    pre = True
            if((i+1) < len(words)):
                if((not(words[i+1] in AlefBet+delimiter+spch)) and (words[i+1].isdigit() == False)):
                    c = True
            if(i < len(words)-1) and ((not(words[i] in AlefBet+punctuation+spch)) and (words[i].isdigit() == False) or ((words[i] == ':') and ((c == True)and(pre == True)))):# or (words[i].isdigit() == True):
                if(words[i] in delimiter+punctuation+spch):
                    if(not(words[i] in d)):
                        d.append(words[i])
                n += 1
            else:
                temp = words[i-n:i]
                for x in d:
                    if(x == ':'):
                        index = temp.index(x)
                        if(temp[index] == temp[-1]):
                            temp = temp
                        else:
                            temp = self.rev_wds((temp), x)
                            #index2 = temp.index(x)
                            #temp = (self.revS(temp[:index2]) + temp[index2-1:])
                    elif(x == '-'):
                        temp = self.revS(temp)
                    elif(x == ' '):
                        temp = temp
                    else:
                        temp = temp
                if(words[i] in AlefBet):
                    if(words[i-1] == '-'):
                        numWords += (temp + words[i])
                    else:
                        numWords += (temp + words[i])
                elif(words[i] == ' '):
                    numWords += (temp + words[i])
                elif(words[i] == ':'):
                    numWords += self.revS(temp + words[i])
                else:
                    numWords += temp
                    numWords += words[i]
                n = 0
                d = []
        return str(numWords)
            
    def rrev_wds(self, Num, d):
        LstNum = Num.split(d)
        rLstNum = []
        FixNum = ""
        end = len(LstNum)-1
        for i in range(len(LstNum)):
            rLstNum.append(self.revS(LstNum[end-i]))
        FixNum = d.join(rLstNum)
        return FixNum
        
    def rev_wds(self, Num, d):
        LstNum = Num.split(d)
        rLstNum = []
        FixNum = ""
        end = len(LstNum)-1
        for i in range(len(LstNum)):
            rLstNum.append(LstNum[end-i])
        FixNum = d.join(rLstNum)
        return FixNum
        
    def revS(self, text):
        revText = ""
        end = len(text)-1
        for i in range(len(text)):
            revText += text[end-i]
        return str(revText)
        
    def clean_vol(self, words):
        words2 = list(words)
        for w in range(len(words)):
            words2[w] = words2[w].replace("וֹ", "ו")
            words2[w] = words2[w].replace("שׁ", "ש")
            words2[w] = words2[w].replace("שׂ", "ש")
            words2[w] = words2[w].replace("ׁ", "")
            words2[w] = words2[w].replace("ׂ", "")
            words2[w] = words2[w].replace("ּ", "")
            words2[w] = words2[w].replace("וּ", "ו")
            words2[w] = words2[w].replace("אָ", "א")
            words2[w] = words2[w].replace("אַ", "א")
            words2[w] = words2[w].replace("בּ", "ב")
            words2[w] = words2[w].replace("גּ", "ג")
            words2[w] = words2[w].replace("דּ", "ד")
            words2[w] = words2[w].replace("הּ", "ה")
            words2[w] = words2[w].replace("זּ", "ז")
            words2[w] = words2[w].replace("טּ", "ט")
            words2[w] = words2[w].replace("יּ", "י")
            words2[w] = words2[w].replace("יִ", "י")
            words2[w] = words2[w].replace("כּ", "כ")
            words2[w] = words2[w].replace("לּ", "ל")
            words2[w] = words2[w].replace("מּ", "מ")
            words2[w] = words2[w].replace("נּ", "נ")
            words2[w] = words2[w].replace("סּ", "ס")
            words2[w] = words2[w].replace("פּ", "פ")
            words2[w] = words2[w].replace("צּ", "צ")
            words2[w] = words2[w].replace("קּ", "ק")
            words2[w] = words2[w].replace("שּׁ", "ש")
            words2[w] = words2[w].replace("שּׂ", "ש")
            words2[w] = words2[w].replace("תּ", "ת")
            
            word = words2[w]
            for l in range(len(word)):
                if(l < len(word)-1) and (l > 0):
                    if(word[l] + word[l+1] == "וֹ")and(word[l-1] in AlefBet):
                        words2[w] = words2[w].replace("וֹ","ו")
                    if(word[l] + word[l+1] == "וֺ")and(word[l-1] in AlefBet):
                        words2[w] = words2[w].replace("וֺ","ו")
                    word = words2[w]

            words2[w] = words2[w].replace("ֹ", "ו") 
            words2[w] = words2[w].replace("ֻ", "ו")
            words2[w] = words2[w].replace("ֹיּ", "י")
            words2[w] = words2[w].replace("ִיַ", "יי")
            words2[w] = words2[w].replace("ֵ", "")
            words2[w] = words2[w].replace("ִ", "")
            words2[w] = words2[w].replace("ַ", "")
            words2[w] = words2[w].replace("ָ", "")
            words2[w] = words2[w].replace("ׇ", "")
            words2[w] = words2[w].replace("ֱ", "")
            words2[w] = words2[w].replace("ֵ", "")
            words2[w] = words2[w].replace("ְ", "")
            words2[w] = words2[w].replace("ֶ", "")
            words2[w] = words2[w].replace("ֲ", "")
            words2[w] = words2[w].replace("ֳ", "")
            words2[w] = words2[w].replace("ֽ", "")
            words2[w] = words2[w].replace("ֺ", "ו")
            
        return words2
        
        
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
        
        
# custom TextInput class with custom methods and overridden parent methods
class CustomInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # override function to paste text from clipboard when the input field is triple tapped
    def on_triple_tap(self):
        if(not(self.text == "")):
            super(CustomInput, self).on_triple_tap()  # performs it's original function
        else:
            inputBuff = Clipboard.paste()
            words = inputBuff.split()
            words_1b = self.clean_vol(words)
            words2 = self.clean(words)
            temp = ' '.join(words2)
            for index in range(len(words_1b)):
                words_1b[index] = self.parse(words_1b[index], ['|'])
            word = ' '.join(words_1b)
 
            if self.check(temp): # maker sure text order is correct; if not, reverse input text
                self.text = self.revT(word)
            else:
                self.text = temp
                
        print("triple tap confirmed")
     
    # reverses text of parameter
    def revT(self, text):
        newInput = text
        revInput = ""
        end = len(text)-1
 
        text = self.chainParse(text, '|')
        brac = [['{','}'],['[',']'],['(',')']]
        return self.revChar(self.parseAnybrac(text, brac, 0))
        
    def chainParse(self, str_words, delim):
        temp = str_words.split(' ')
        words = []
        for w in temp:
            words.append(self.rrev_wds(w, delim))
        return ' '.join(words)
            
    def parse(self, str_words, delims):
        cdelims = delims.copy()
        new_list = []
        words_plus = ""
        if(len(cdelims) > 0):
            d = cdelims.pop()
            list_words = str_words.split(d)
            for index in range(len(list_words)-1, -1, -1):
                new_list.append(self.parse(list_words[index], cdelims))
            words_plus = d.join(new_list)
            return words_plus
        else:
            return self.revS(str_words)
            
    def parse_bracs(self, str_words):
        l = 0
        r = 0
        opn = 0
        clsd = 0
        cl = -1
        op = -1
        list_words = []
        new_list = []
        Prth = ['(',')']
        L = Prth[0]
        R = Prth[1]
        Ls = []
        C = False
        Opn = L
        Cls = R
            
        for c in range(len(str_words)):
            if(c == 0):
                if(str_words[c] == Cls):
                    list_words.append(str_words[c])
                    r = 1
                    C = True
                elif(str_words[c] == Opn):
                    l = 0
                    Ls.append(c)
                    C = True
                    opn = 1
                    
            elif(c == len(str_words) - 1):
                if(opn == 0):
                    if(str_words[c] == Opn):
                        list_words.append(str_words[r:c])
                        list_words.append(str_words[c])
                    else:
                        list_words.append(str_words[r:c+1])
                elif(opn == 1):
                    if(str_words[c] == Opn):
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:c])
                            list_words.append(str_words[c])
                        else:
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:cl])
                            list_words.append(str_words[cl:c])
                            list_words.append(str_words[c])
                    elif(str_words[c] == Cls):
                        list_words.append(str_words[l:c+1])
                    else:
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:c+1])
                        else:
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:c1])    #((XX(X)XX(--
                            list_words.append(str_words[c1:c+1])
                elif(opn > 1):
                    if(str_words[c] == Cls):
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:l1])
                            list_words.append(str_words[l1:c+1])
                        else:             
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:c1])    #((XX(X)XX(--
                            list_words.append(str_words[c1:c+1])
                    elif(str_words[c] == Opn):
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:c])
                            list_words.append(str_words[c])
                        else:
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:cl])
                            list_words.append(str_words[cl:c])
                            list_words.append(str_words[c])
                    else:
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:c+1])
                        else:
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:cl])
                            list_words.append(str_words[cl:c+1])
            else:
                if(str_words[c] == Opn):
                    
                    Ls.append(c)
                    if(opn == 0):
                        if(c > r):
                            list_words.append(str_words[r:c])
                        l = c
                    opn += 1
                    
                elif(str_words[c] == Cls):
                    opn = opn - 1
                    if(opn < 0):
                        list_words.append(str_words[r:c] + str_words[c])
                        cl = -1
                        r = c + 1
                        opn = 0
                    else:
                        p = Ls.pop
                        if(opn == 0):
                            cl = -1
                            if(c > l):
                                list_words.append(str_words[l:c] + str_words[c])
                            else:
                                list_words.append(str_words[c])
                            r = c + 1
                        elif(opn > 0):
                            cl = c+1
                            op = p
 
        if(r > 0) or (l > 0) or (C == True):
            for index in range(len(list_words)-1, -1, -1):
                if(list_words[index][0] == Opn) and (list_words[index][-1] == Cls):
                    new_list.append(Opn + self.parse_bracs(list_words[index][1:-1]) + Cls)
                elif(list_words[index][0] == Opn):
                    new_list.append(self.parse_bracs(list_words[index][1:]) + Cls)
                elif(list_words[index][-1] == Cls):
                    new_list.append(Opn + self.parse_bracs(list_words[index][:-1]))
                else:
                    new_list.append(self.parse_bracs(list_words[index]))
            if(len(new_list) > 1):
                return ''.join(new_list)
            elif (len(new_list) > 0):
                return new_list[0]
            else: 
                return str_words
        else:
           return self.revS(str_words) 
    
    def parseAnybrac(self, str_words, brac, n):
        if(n > len(brac)-1):
            return str_words
        l = 0
        r = 0
        opn = 0
        clsd = 0
        cl = -1
        op = -1
        list_words = []
        new_list = []
        L = brac[n][0]
        R = brac[n][1]
        Ls = []
        C = False
        Opn = L
        Cls = R
            
        for c in range(len(str_words)):
            if(c == 0):
                if(str_words[c] == Cls):
                    list_words.append(str_words[c])
                    r = 1
                    C = True
                elif(str_words[c] == Opn):
                    l = 0
                    Ls.append(c)
                    C = True
                    opn = 1
                    
            elif(c == len(str_words) - 1):
                if(opn == 0):
                    if(str_words[c] == Opn):
                        list_words.append(str_words[r:c])
                        list_words.append(str_words[c])
                    else:
                        list_words.append(str_words[r:c+1])
                elif(opn == 1):
                    if(str_words[c] == Opn):
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:c])
                            list_words.append(str_words[c])
                        else:
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:cl])
                            list_words.append(str_words[cl:c])
                            list_words.append(str_words[c])
                    elif(str_words[c] == Cls):
                        list_words.append(str_words[l:c+1])
                    else:
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:c+1])
                        else:
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:c1])    #((XX(X)XX(--
                            list_words.append(str_words[c1:c+1])
                elif(opn > 1):
                    if(str_words[c] == Cls):
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:l1])
                            list_words.append(str_words[l1:c+1])
                        else:             
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:c1])    #((XX(X)XX(--
                            list_words.append(str_words[c1:c+1])
                    elif(str_words[c] == Opn):
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:c])
                            list_words.append(str_words[c])
                        else:
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:cl])
                            list_words.append(str_words[cl:c])
                            list_words.append(str_words[c])
                    else:
                        l1 = Ls[-1]
                        l2 = Ls[0]
                        if(cl == -1):
                            list_words.append(str_words[l:c+1])
                        else:
                            list_words.append(str_words[l:op])
                            list_words.append(str_words[op:cl])
                            list_words.append(str_words[cl:c+1])
            else:
                if(str_words[c] == Opn):
                    
                    Ls.append(c)
                    if(opn == 0):
                        if(c > r):
                            list_words.append(str_words[r:c])
                        l = c
                    opn += 1
                    
                elif(str_words[c] == Cls):
                    opn = opn - 1
                    if(opn < 0):
                        list_words.append(str_words[r:c] + str_words[c])
                        cl = -1
                        r = c + 1
                        opn = 0
                    else:
                        p = Ls.pop
                        if(opn == 0):
                            cl = -1
                            if(c > l):
                                list_words.append(str_words[l:c] + str_words[c])
                            else:
                                list_words.append(str_words[c])
                            r = c + 1
                        elif(opn > 0):
                            cl = c+1
                            op = p
 
        if(r > 0) or (l > 0) or (C == True):
            for index in range(len(list_words)-1, -1, -1):
                if(list_words[index][0] == Opn) and (list_words[index][-1] == Cls):
                    new_list.append(Opn + self.parseAnybrac(list_words[index][1:-1], brac, n) + Cls)
                elif(list_words[index][0] == Opn):
                    new_list.append(self.parseAnybrac(list_words[index][1:], brac, n) + Cls)
                elif(list_words[index][-1] == Cls):
                    new_list.append(Opn + self.parseAnybrac(list_words[index][:-1], brac, n))
                else:
                    new_list.append(self.parseAnybrac(list_words[index], brac, n))
            if(len(new_list) > 1):
                return ''.join(new_list)
            elif (len(new_list) > 0):
                return new_list[0]
            else: 
                return str_words
            
        elif(n < len(brac)-1):
            return self.parseAnybrac(str_words, brac, n+1)
        else:
            return self.num_parser(self.revS(str_words))
               
    def num_parser(self, words):
        fixText = ""
        c = False
        p = False
        d = []
        s =-1
        brackets = ['(', ')', '[', ']', '{', '}']
        plus = ['+', '-']
        for num in range(len(words)):
            if(words[num] == '|'):
                return words
            if(words[num].isdigit() == True) or (not(words[num] in AlefBet+delimiter+punctuation+special_char+operators)):
                c = False
                p = False
                if(s == -1):
                    s = num
                
                if(num == len(words)-1):
                    fixText += self.revS(words[s:num+1])
            elif((c == True)):
                temp = ""
                tempW = words[s:num-1]
                if(p == True):
                    d.pop()
                temp = self.revS(words[s:num-1])
                for x in d:
                    if(x in special_char+plus):
                        if(words[num-1] in brackets):
                            if(temp == ""):
                                temp = words[s:num-1]
                            else:
                                temp = temp
                        else:     
                            if(temp == ""):
                                temp = words[s:num-1]
                            else:
                                temp = temp
                    elif(x in punctuation):
                        if(words[num-1] in brackets):
                            if(temp == ""):
                                 temp = words[s:num-1]
                            else:
                                temp = temp
                        else:     
                            if(temp == ""):
                                 temp = words[s:num-1]
                            else:
                                temp = temp
                    elif(x in delimiter):
                        if(temp == ""):
                            temp = words[s:num-1]
                        else:
                            temp = temp
                    else:
                        if(temp == ""):
                            temp = self.revS(words[s:num-1])
                        else:
                            temp = self.revS(temp)
                fixText = fixText + (temp + words[num-1] + words[num])
                d = []  
                s = -1
                c = False
                p = False
            elif(c == False):
                if(not(s == -1)):
                    if(words[num] in (delimiter+special_char+punctuation+plus)):
                        c = True
                        if(not(words[num] in d)):
                            p = True
                            d.append(words[num])
                    if(num == len(words)-1):
                        fixText += self.revS(words[s:num+1])
                else:
                    fixText += words[num]
        return fixText
        
    def revChar(self, words):
        numWords = ""
        n = 0;
        pre = False
        c = False
        spch = [':', '-']
        brackets = ['(', ')', '[', ']', '{', '}']
        d = []
        for i in range(len(words)):
            if(i > 0):
                if(not(words[i-1] in AlefBet+punctuation+spch)) and (words[i-1].isdigit() == False):
                    pre = True
            if((i+1) < len(words)):
                if((not(words[i+1] in AlefBet+delimiter+spch)) and (words[i+1].isdigit() == False)):
                    c = True
            if(i < len(words)-1) and ((not(words[i] in AlefBet+punctuation+spch)) and (words[i].isdigit() == False) or ((words[i] == ':') and ((c == True)and(pre == True)))):# or (words[i].isdigit() == True):
                if(words[i] in delimiter+punctuation+spch):
                    if(not(words[i] in d)):
                        d.append(words[i])
                n += 1
            else:
                temp = words[i-n:i]
                for x in d:
                    if(x == ':'):
                        index = temp.index(x)
                        if(temp[index] == temp[-1]):
                            temp = temp
                        else:
                            temp = self.rev_wds((temp), x)
                            #index2 = temp.index(x)
                            #temp = (self.revS(temp[:index2]) + temp[index2-1:])
                    elif(x == '-'):
                        temp = self.revS(temp)
                    elif(x == ' '):
                        temp = temp
                    else:
                        temp = temp
                if(words[i] in AlefBet):
                    if(words[i-1] == '-'):
                        numWords += (temp + words[i])
                    else:
                        numWords += (temp + words[i])
                elif(words[i] == ' '):
                    numWords += (temp + words[i])
                elif(words[i] == ':'):
                    numWords += self.revS(temp + words[i])
                else:
                    numWords += temp
                    numWords += words[i]
                n = 0
                d = []
        return str(numWords)
    
    def exclude(self, b, a):
        c = []
        for e in b:
            if(not(e in a)):
                c.append(e)
        return c
        
    def intrsc(self, h, g):
        v = []
        for e in h:
            if(e in g):
                v.append(e)
        return v
        
    def rottate(self, words, delim):
        lst_of_words = words.split()
        reslt_words = ""
        word_lst = []
        for w in lst_of_words:
            word_lst.append(self.rrev_wds(w, delim))  
        reslt_words = ' '.join(word_lst)
        return reslt_words
        
    def rrev_wds(self, Num, d):
        LstNum = Num.split(d)
        rLstNum = []
        FixNum = ""
        end = len(LstNum)-1
        for i in range(len(LstNum)):
            rLstNum.append(self.revS(LstNum[end-i]))
        FixNum = d.join(rLstNum)
        return FixNum
        
    def rev_wds(self, Num, d):
        LstNum = Num.split(d)
        rLstNum = []
        FixNum = ""
        end = len(LstNum)-1
        for i in range(len(LstNum)):
            rLstNum.append(LstNum[end-i])
        FixNum = d.join(rLstNum)
        return FixNum
        
    def revS(self, text):
        revText = ""
        end = len(text)-1
        for i in range(len(text)):
            revText += text[end-i]
        return str(revText)
          
    # check and see if there are final letters at the beginning of word (which should be at the end)
    def check(self, words):
        words = words.split()
        for w in words:
            for i in range(len(punctuation)):
                w = w.strip(punctuation[i])
            if len(w) > 0:
                if w[-1] in finals.values():
                    return True
                if w[0] in finals.values(): # If nonfinal letter is at the beginning then the text is in the correct order
                    return False
                if (not(('\'' in w)or('`' in w)or('\"' in w)or('״' in w))):
                    if w[0] in finals.keys():
                        return True
                    if w[-1] in finals.keys():
                        return False
        return False
    
    
    def clean_vol(self, words):
        words2 = list(words)
        for w in range(len(words)):
            words2[w] = words2[w].replace("וֹ", "ו")
            words2[w] = words2[w].replace("שׁ", "ש")
            words2[w] = words2[w].replace("שׂ", "ש")
            words2[w] = words2[w].replace("ׁ", "")
            words2[w] = words2[w].replace("ׂ", "")
            words2[w] = words2[w].replace("ּ", "")
            words2[w] = words2[w].replace("וּ", "ו")
            words2[w] = words2[w].replace("אָ", "א")
            words2[w] = words2[w].replace("אַ", "א")
            words2[w] = words2[w].replace("בּ", "ב")
            words2[w] = words2[w].replace("גּ", "ג")
            words2[w] = words2[w].replace("דּ", "ד")
            words2[w] = words2[w].replace("הּ", "ה")
            words2[w] = words2[w].replace("זּ", "ז")
            words2[w] = words2[w].replace("טּ", "ט")
            words2[w] = words2[w].replace("יּ", "י")
            words2[w] = words2[w].replace("יִ", "י")
            words2[w] = words2[w].replace("כּ", "כ")
            words2[w] = words2[w].replace("לּ", "ל")
            words2[w] = words2[w].replace("מּ", "מ")
            words2[w] = words2[w].replace("נּ", "נ")
            words2[w] = words2[w].replace("סּ", "ס")
            words2[w] = words2[w].replace("פּ", "פ")
            words2[w] = words2[w].replace("צּ", "צ")
            words2[w] = words2[w].replace("קּ", "ק")
            words2[w] = words2[w].replace("שּׁ", "ש")
            words2[w] = words2[w].replace("שּׂ", "ש")
            words2[w] = words2[w].replace("תּ", "ת")
            
            word = words2[w]
            for l in range(len(word)):
                if(l < len(word)-1) and (l > 0):
                    if(word[l] + word[l+1] == "וֹ")and(word[l-1] in AlefBet):
                        words2[w] = words2[w].replace("וֹ","ו")
                    if(word[l] + word[l+1] == "וֺ")and(word[l-1] in AlefBet):
                        words2[w] = words2[w].replace("וֺ","ו")
                    word = words2[w]

            words2[w] = words2[w].replace("ֹ", "ו") 
            words2[w] = words2[w].replace("ֻ", "ו")
            words2[w] = words2[w].replace("ֹיּ", "י")
            words2[w] = words2[w].replace("ִיַ", "יי")
            words2[w] = words2[w].replace("ֵ", "")
            words2[w] = words2[w].replace("ִ", "")
            words2[w] = words2[w].replace("ַ", "")
            words2[w] = words2[w].replace("ָ", "")
            words2[w] = words2[w].replace("ׇ", "")
            words2[w] = words2[w].replace("ֱ", "")
            words2[w] = words2[w].replace("ֵ", "")
            words2[w] = words2[w].replace("ְ", "")
            words2[w] = words2[w].replace("ֶ", "")
            words2[w] = words2[w].replace("ֲ", "")
            words2[w] = words2[w].replace("ֳ", "")
            words2[w] = words2[w].replace("ֽ", "")
            words2[w] = words2[w].replace("ֺ", "ו")
            
        return words2
    
    def clean(self, words):
        excep = punctuation+delimiter+operators
        words2 = list(words)
        for w in range(len(words)):
            words2[w] = words2[w].replace("וֹ", "ו")
            words2[w] = words2[w].replace("שׁ", "ש")
            words2[w] = words2[w].replace("שׂ", "ש")
            words2[w] = words2[w].replace("ׁ", "")
            words2[w] = words2[w].replace("ׂ", "")
            words2[w] = words2[w].replace("ּ", "")
            words2[w] = words2[w].replace("וּ", "ו")
            words2[w] = words2[w].replace("אָ", "א")
            words2[w] = words2[w].replace("אַ", "א")
            words2[w] = words2[w].replace("בּ", "ב")
            words2[w] = words2[w].replace("גּ", "ג")
            words2[w] = words2[w].replace("דּ", "ד")
            words2[w] = words2[w].replace("הּ", "ה")
            words2[w] = words2[w].replace("זּ", "ז")
            words2[w] = words2[w].replace("טּ", "ט")
            words2[w] = words2[w].replace("יּ", "י")
            words2[w] = words2[w].replace("יִ", "י")
            words2[w] = words2[w].replace("כּ", "כ")
            words2[w] = words2[w].replace("לּ", "ל")
            words2[w] = words2[w].replace("מּ", "מ")
            words2[w] = words2[w].replace("נּ", "נ")
            words2[w] = words2[w].replace("סּ", "ס")
            words2[w] = words2[w].replace("פּ", "פ")
            words2[w] = words2[w].replace("צּ", "צ")
            words2[w] = words2[w].replace("קּ", "ק")
            words2[w] = words2[w].replace("שּׁ", "ש")
            words2[w] = words2[w].replace("שּׂ", "ש")
            words2[w] = words2[w].replace("תּ", "ת")
            
            word = words2[w]
            
            for l in range(len(word)):
                if(l < len(word)-1) and (l > 0):
                    if(word[l] + word[l+1] == "וֹ")and(word[l-1] in AlefBet):
                        words2[w] = words2[w].replace("וֹ","ו")
                    if(word[l] + word[l+1] == "וֺ")and(word[l-1] in AlefBet):
                        words2[w] = words2[w].replace("וֺ","ו")
                    word = words2[w]

            words2[w] = words2[w].replace("ֹ", "ו") 
            words2[w] = words2[w].replace("ֻ", "ו")
            words2[w] = words2[w].replace("ֹיּ", "י")
            words2[w] = words2[w].replace("ִיַ", "יי")
            words2[w] = words2[w].replace("ֵ", "")
            words2[w] = words2[w].replace("ִ", "")
            words2[w] = words2[w].replace("ַ", "")
            words2[w] = words2[w].replace("ָ", "")
            words2[w] = words2[w].replace("ׇ", "")
            words2[w] = words2[w].replace("ֱ", "")
            words2[w] = words2[w].replace("ֵ", "")
            words2[w] = words2[w].replace("ְ", "")
            words2[w] = words2[w].replace("ֶ", "")
            words2[w] = words2[w].replace("ֲ", "")
            words2[w] = words2[w].replace("ֳ", "")
            words2[w] = words2[w].replace("ֽ", "")
            words2[w] = words2[w].replace("ֺ", "ו")
            
        for i in range(len(words2)):
            for j in range(len(excep)):
                words2[i] = words2[i].strip(excep[j])
                    
        for i in range(len(words2)):
            for j in range(len(excep)):
                words2[i] = words2[i].strip(excep[j])
            
        return words2
        

    # Interface for displaying the words found, their diffinition, and some gramatical properties.  
class DisplayWords(GridLayout):
    def __init__(self, instance, **kwargs):
        super(DisplayWords, self).__init__(**kwargs)
        self.cols = 1
        self.readText = TextInput(readonly=True, multiline=True, base_direction='rtl', size_hint=[5, 0.3], focus=True, font_name='data/fonts/times', font_size=Display_Size)
        self.display = TextInput(readonly=True, multiline=True, focus=True, size_hint_x=5, size_hint_y=None, font_name='data/fonts/times', font_size=Display_Size)
        self.display.bind(minimum_height=self.display.setter('height'))
        self.dRoot = ScrollView(size_hint=(5, 1), size=(Window.width, Window.height))
        self.dRoot.add_widget(self.display)
        self.SubPanal = GridLayout(rows=1, size_hint=[5, 0.1])
        self.closeB = Button(text='[color=FFFFFF]Close[color=FFFFFF]', font_name='data/fonts/times', font_size=20, markup=True)
        self.closeB.bind(on_press=instance.closeAction)
        self.topB = Button(text='[color=FFFFFF]Top[color=FFFFFF]', font_name='data/fonts/times', font_size=20, markup=True)
        self.topB.bind(on_press=instance.topAction)
        self.SubPanal.add_widget(self.closeB)
        self.SubPanal.add_widget(self.topB)
        self.add_widget(self.readText)
        self.add_widget(self.dRoot)
        self.add_widget(self.SubPanal)


# Inerface for adding a new word to the dictionary
class AddWord(GridLayout):
    def __init__(self, instance, **kwargs):
        super(AddWord, self).__init__(**kwargs)
        self.cols = 2
        
        self.wLabel = Label(text='[color=3333ff]Word[color=3333ff]', outline_color=black, font_size=30, markup=True)
        self.dLabel = Label(text='[color=3333ff]Diffinition[color=3333ff]', outline_color=black, font_size=30, markup=True)
        self.Word = TextInput(text="", readonly=True, multiline=False, font_name='data/fonts/times', font_size=Display_Size)
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


# top level of app.  
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
        self.Input = CustomInput(readonly=False, multiline=False, base_direction='rtl', font_name='data/fonts/times', font_size=Display_Size)
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
        inputBuff = self.Input.text.replace('-', ' ')
        words = inputBuff.split()
        words = self.clean(words)
        word = '-'.join(words)
        fixedInput = self.revPhWords(word, "-")
        if fixedInput not in self.Dict:
            self.Word.Word.text = word
            self.Word.Definition.text = ""
            self.popup.open()
        
    def editAction(self, instance):
        inputBuff = self.Input.text.replace('-', ' ')
        words = inputBuff.split()
        words = self.clean(words)
        word = '-'.join(words)
        fixedInput = self.revPhWords(word, "-")
        if fixedInput in self.Dict:
            self.Word.Word.text = word
            definition = ",  ".join(self.Dict[fixedInput]["definition"])
            self.Word.Definition.text = definition
            self.popup.title = "Edit Word"
            self.popup.open()
        
    def removeAction(self, instance):
        inputBuff = self.Input.text.replace('-', ' ')
        words = inputBuff.split()
        words = self.clean(words)
        word = '-'.join(words)
        fixedInput = self.revPhWords(word, "-")
        if fixedInput in self.Dict:
            word = fixedInput
            del self.Dict[word]
            self.store.delete(word)
            
    def exitAction(self, instance):
        sys.exit(0)
        
    def closeAction(self, instance):
        self.wordPopup.dismiss()
    
    # scrolls to the beginning of the text input
    def topAction(self, instance):
        self.wordPopup.content.dRoot.scroll_y = 1.0
        
    def cancelAction(self, instance):
        self.popup.dismiss()
    
    def enterAction(self, instance):
        inputBuff = self.Input.text.replace('-', ' ')
        words = inputBuff.split()
        words = self.clean(words)
        word = '-'.join(words)
        self.Word.Word.text = self.revPhWords(word, "-")
        word = {self.Word.Word.text: {"text": self.Word.Word.text, "definition": self.Word.Definition.text.split(",  ")}}
        self.Dict.update(word)
        self.popup.dismiss()
        self.store.put(self.Word.Word.text, text=self.Word.Word.text, definition=self.Word.Definition.text.split(",  "))
        self.Word.Definition.text = ""
    
    def exclude(self, b, a):
        c = []
        for e in b:
            if(not(e in a)):
                c.append(e)
        return c
        
    def intrsc(self, h, g):
        v = []
        for e in h:
            if(e in g):
                v.append(e)
        return v
    
    def clean(self, words):
        words2 = list(words)
        for w in range(len(words)):
            excep = punctuation+delimiter
            words2[w] = words2[w].replace("וֹ", "ו")
            words2[w] = words2[w].replace("שׁ", "ש")
            words2[w] = words2[w].replace("שׂ", "ש")
            words2[w] = words2[w].replace("ׁ", "")
            words2[w] = words2[w].replace("ׂ", "")
            words2[w] = words2[w].replace("ּ", "")
            words2[w] = words2[w].replace("וּ", "ו")
            words2[w] = words2[w].replace("אָ", "א")
            words2[w] = words2[w].replace("אַ", "א")
            words2[w] = words2[w].replace("בּ", "ב")
            words2[w] = words2[w].replace("גּ", "ג")
            words2[w] = words2[w].replace("דּ", "ד")
            words2[w] = words2[w].replace("הּ", "ה")
            words2[w] = words2[w].replace("זּ", "ז")
            words2[w] = words2[w].replace("טּ", "ט")
            words2[w] = words2[w].replace("יּ", "י")
            words2[w] = words2[w].replace("יִ", "י")
            words2[w] = words2[w].replace("כּ", "כ")
            words2[w] = words2[w].replace("לּ", "ל")
            words2[w] = words2[w].replace("מּ", "מ")
            words2[w] = words2[w].replace("נּ", "נ")
            words2[w] = words2[w].replace("סּ", "ס")
            words2[w] = words2[w].replace("פּ", "פ")
            words2[w] = words2[w].replace("צּ", "צ")
            words2[w] = words2[w].replace("קּ", "ק")
            words2[w] = words2[w].replace("שּׁ", "ש")
            words2[w] = words2[w].replace("שּׂ", "ש")
            words2[w] = words2[w].replace("תּ", "ת")
            
            word = words2[w]
            
            for l in range(len(word)):
                if(l < len(word)-1) and (l > 0):
                    if(word[l] + word[l+1] == "וֹ")and(word[l-1] in AlefBet):
                        words2[w] = words2[w].replace("וֹ","ו")
                    if(word[l] + word[l+1] == "וֺ")and(word[l-1] in AlefBet):
                        words2[w] = words2[w].replace("וֺ","ו")
                    word = words2[w]
                        
            words2[w] = words2[w].replace("[", " ")
            words2[w] = words2[w].replace("]", " ")
            words2[w] = words2[w].replace("”", "")
            words2[w] = words2[w].replace("״", "\"")
            words2[w] = words2[w].replace("׳", "\'")
            words2[w] = words2[w].replace("ֹ", "ו") 
            words2[w] = words2[w].replace("ֻ", "ו")
            words2[w] = words2[w].replace("ִיַ", "יי")
            words2[w] = words2[w].replace("ֵ", "")
            words2[w] = words2[w].replace("ִ", "")
            words2[w] = words2[w].replace("ַ", "")
            words2[w] = words2[w].replace("ׇ", "")
            words2[w] = words2[w].replace("ָ", "")
            words2[w] = words2[w].replace("ֱ", "")
            words2[w] = words2[w].replace("ֵ", "")
            words2[w] = words2[w].replace("ְ", "")
            words2[w] = words2[w].replace("ֶ", "")
            words2[w] = words2[w].replace("ֲ", "")
            words2[w] = words2[w].replace("ֳ", "")
            words2[w] = words2[w].replace("ֽ", "")
            words2[w] = words2[w].replace("ֺ", "ו")
            
        for i in range(len(words2)):
            for j in range(len(excep)):
                if(excep[j] =="'"):
                    continue
                else:
                    words2[i] = words2[i].strip(excep[j])
                    
        for i in range(len(words2)):
            for j in range(len(excep)):
                if(excep[j] =="'"):
                    continue
                else:
                    words2[i] = words2[i].strip(excep[j])
        
        return words2

    def findAction(self, instance):
        if len(self.Input.text) == 0:
            return
        self.wText = ''
        inputBuff = self.Input.text.replace('־', '-')
        inputBuff = inputBuff.replace('-', ' ')
        inputBuff = inputBuff.replace('[', ' ')
        inputBuff = inputBuff.replace(']', ' ')
        operator = operators + ['\\']
        for o in operator:
            inputBuff = inputBuff.replace(o, " " + o + " ")
        words = inputBuff.split()
        words = self.clean(words)
        words = self.revWords(words)
        words = self.getPhrase(words)
        tk = len(words)
        
        self.wordPopup.open()
        for i in range(len(words)):
            k = len(words[i].split('-'))
            self.getWList(words, i, tk, k, 0)
            if not(i == len(words)):
                self.wText += '\n'
                self.wText += "*"*160
                self.wText += '\n\n'
        
        # scrolls to the beginning of the text input once all the resalts are displayed
        self.wordPopup.content.dRoot.scroll_y = 1.0
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
        tempWs = words
        Ws2 = words
        k = 0
        end = len(tempWs)
        for i in range(end):
            N = 1
            s = 0
            while (N + i) < (end):
            
                check = SearchWord()
                checkPl = SearchWord()
                checkPre = SearchWord()
                checkSuf = SearchWord()
                checkPrePl = SearchWord()
                checkSufPre = SearchWord()
                checkPlPre = SearchWord()
            
                revPhrase = '-'.join(self.revWords(Ws2[i:(N+i+1)]))
                fixedPhrase = '-'.join(tempWs[i:(N+i+1)])
                
                phraseW = Word(fixedPhrase, "")
                rPhraseW = Word(revPhrase, "")
                self.CurrentWord.equalTo(phraseW)
                self.algorithm(check, phraseW, False)
                if("\"" in phraseW.getText()):
                    phraseW2 = Word("", "")
                    phraseW2.equalTo(phraseW)
                    phraseW2.setText(phraseW.getText().replace("\"", ""))
                    self.algorithm(check, phraseW2, False)
                
                if((check.find(phraseW, self.Dict) == True) or (check.getNumWds() > 0)) and (end > 1):
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
                    check2 = SearchWord()
                    if(tempWs[i+1][p:] in prephrase) and (not (len(tempWs[i+1][:p]) < 2)):
                        prePhrase = tempWs[i] + "-" + tempWs[i+1][p:]
                        prephraseW = Word(prePhrase, "")
                        zPhrasePre = Word(prephraseW, "")
                        zPhrasePre.equalTo(self.prefix(check2, prephraseW, False, False))
                        if (check2.find(prephraseW, self.Dict) == True) or (check2.getNumWds() > 0):
                            tempWs[i] = prePhrase
                            tempWs[i+1] = tempWs[i+1]
                            break                   
        return tempWs[0:(end)]
        
    # This function is responsible for finding and displaying all the diffent possible words that the word, stored in text[i],
    # is derived from.
    def getWList(self, text, i, tk, k, n):
    
        number = ''
        Year = ''
        look = SearchWord()
        check = SearchWord()
        ckYear = SearchWord()
        isVerb = False
        isNoun = False
        yWord = Word(text[i], "")
        confidence = 7
        Skip = False
        Check = False
        tempWord = Word("", "")
        word0 = Word("", "")
        # creating word object with text value of the string at indext 'i' (current index)
        word = Word(text[i], "")
        # initialize 'CurrentWord' variable to the word now being processed
        self.CurrentWord.equalTo(word)
        word0.equalTo(word)
        # checks to see if the text is in the format of a Hebrew year.
        # If so format a string in the 'Year' variable to display that year.
        if yWord.isYear() == True:
            Year = 'Year: ' + str(yWord.getYear()) + ';'
        # otherwise check to see if the text is in the Hebrew year format with a prefix at the beginning of the text
        else:
            preYr = self.smPrefix(ckYear, yWord, False, False)
            if preYr.getLen() > 0:
                if(preYr.isYear() == True) and (not preYr.getText() == ""):
                    Year = "prefix [" + preYr.getPrefixW() + '] ' + 'Year: ' + str(preYr.getYear()) + ';'
        tempWord.equalTo(word)
        #if(Year == ''): #Only if text is not in the Hebrew year format do the following:
        if word.isNumb() == True: #If text in word object is in the format of a Hebrew number, format a string in the 
            #'number' variable to display that number.
            if(not(Year == '')):
                 number = '(#' + str(word.getGemontria()) + ') '
            else:
                number = '#' + str(word.getGemontria()) + ';'
        # otherwise check to see if the text is in the Hebrew number format with a prefix at the beginning of the text
        else:
            preNum = self.smPrefix(check, tempWord, False, False)
            if preNum.getLen() > 0:
                if(preNum.isNumb() == True) and (not preNum.getText() == ""):
                    if(Year == ''):
                        number = "prefix [" + preNum.getPrefixW() + '] ' + '#' + str(preNum.getGemontria()) + ';'
                    else:
                        Year = "prefix [" + preNum.getPrefixW() + '] ' + '(#' + str(preNum.getGemontria()) + ') ' + 'Year: ' + str(preYr.getYear()) + ';' 
        
        # This section of the code is dedicated to context recognition.
        # if the current word is not the first word check the word before it; and if the word
        # before it is one if the Hebrew words below in the if statement, then the current word 
        # is most likely a noun
        rightW = Word("", "")
        if i > 0:
            if((text[i-1] == 'תא') or (text[i-1] == 'תאו')):
                isNoun = True
                self.CurrentWord.setNoun()
                word.setNfactor(confidence)
                word.setVfactor(-confidence)
                if(not(word.getText() == "הוהי")):
                    nounW = Word("", "")
                    nounW.equalTo(word)
                    nounW.setNoun()
                    nounW.setValue(INF)
                    rightW = Word("", "")
                    rightW.equalTo(nounW)
                    look.find(rightW, self.Dict)
                    self.algorithm(look, nounW, False)
                    
        # if the current word is not the last word, and not The Tetragramaton, and not a noun,
        # and the next word is in the list variable 'obj', or is 'תא', there is a good chance
        # that the current word is a verb.
        if(tk > i+1):
            if(not(word.getText() == "הוהי")) and (isNoun == False) and ((text[i+1] in Obj) or (text[i+1] == 'תא')):
                isVerb = True  
                self.CurrentWord.setVerb()
                word.setVfactor(confidence)
                word.setNfactor(-confidence)
                verbW = Word("", "")
                verbW.equalTo(word)
                verbW.setVerb()
                verbW.setValue(INF)
                rightW = Word("", "")  
                rightW.equalTo(verbW)
                rightW.setValue(INF)
                look.find(rightW, self.Dict)
                self.algorithm(look, verbW, False)
                        
        self.wText += '\t\t'*n + ':' + (self.revPhWords(text[i], '-')) + '   ' + number + Year + '\n\n'
         
        # If the current word is The Tetragramaton, then we don't need to process the word any further
        # we already know this is the proper name of G_d and a proper noun.
        if word.getText() == "הוהי":
            word.setNoun()
            look.find(word0, self.Dict)
        else: #If the current word is not The Tetragramaton, then the current word may or may not be set to a noun or a verb
              #based on the resalts from the context recognition part of the code
            if(isVerb == True) or (isNoun == True):
                Check = True
             #   word0.equalTo(rightW)
            #else:
            rightW.equalTo(word0)
            rightW.setValue(INF)
            self.FindHelper(look, rightW, self.Dict, Check)
            self.algorithm(look, rightW, Check) #determines the possible forms of the current word, and searches

            # These three blocks gets rid of any quotation marks just in cases thay interfered with the processing of the word.
            # words must be searched with each single and double quotes missing and with both present (done above).
            sText = word0.getText()
            sText = sText.replace('\"', '')

            if(not (word0.getText() == sText)): #if there are quotation marks in the current word put stripped version in the algorithm
                word0.setText(sText)            #stored in the 'sText' variable.
                self.CurrentWord.setText(sText)
                rightW = Word("", "")
                rightW.equalTo(word0)
                rightW.setValue(INF)
                self.FindHelper(look, rightW, self.Dict, Check)
                self.algorithm(look, rightW, Check)
                
        
            sText2 = word0.getText()
            sText2 = sText2.replace("\'", "")
            
            if(not (word0.getText() == sText2)): #if there are single quotes in the current word put stripped version in the algorithm
                word0.setText(sText2)            #stored in the 'sText2' variable.
                self.CurrentWord.setText(sText2)
                rightW = Word("", "")
                rightW.equalTo(word0)
                rightW.setValue(INF)
                self.FindHelper(look, rightW, self.Dict, Check)
                self.algorithm(look, rightW, Check)
                                    
        look.group()
        WList = look.getWords() #store all the words found in the 'WList' variable
        #WList.sort(key=look.getValue, reverse = True) #store words according to closeness to the word as it appears in the input field
        #based on a formula in the algorithm for calculating the value, which is built in the 'Word' class
        # This block of code is responsible for formatting and displaying the results.                                               
        if(len(look.getWords()) > 0):
            prevW = Word("", "")
            start = True
            for wi in WList:
                w = Word("", "")
                w.equalTo(wi)
                w.setText(self.revPhWords(wi.getText(), '-'))
                val = ""
                OutPut = []
                #if (w.getSuffix() == True) and (w.isVerb() == False):
                   # w.setNoun()
                   # if look.HasWord(w) == True:
                        #w.unSetNoun()
                    
                if((not(prevW.getText() == w.getText())) and (start == False)):
                    self.wText += '\n'
                prevW.equalTo(w)
                
                start = False
                if w.isVerb() == True:
                    if((w.getPrixListEnd() == 'מ') or (w.getPrixListEnd() == 'ל')) and (w.isTense() == False):
                        w.unSetVerb()
                    else:
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
                sf7 = ''
                      
                isR = ""
                ARROW = "  =>  "
                X = ""
                HR = False
                #Val = "[" + str(w.getValue()) + "]"
                #HR = w.hasRoot()
                if(w.isRoot() == True):
                    isR = "(r) "# + Val + " "
                #else:
                    #isR = " " + Val + " "
                if(not(w.getVerbformVal() == -1)) or (not(w.getTenseVal() == -1)) or (not(w.getPersonVal() == -1)) or (not(w.getGenderVal() == -1)) or (w.getPlural() == True) or (w.getModern() == True) or (w.getDual() == True) or (w.getHey1() > 0) or (w.getSuffix() == True) or (w.getPrefix() == True) or (HR == True) or (w.getConstruct() == True):
                    gr = True


                if w.getPlural() == True:
                    pl = "pl."
                if w.getDual() == True:
                    pl = "dual"
                if((w.getTense() == 'Participle') or (w.getTense() == 'Infinitive') or (w.getTense() == 'Infinitive abs.')) and (pl == ""):
                    pl = "sg."
                    
                definition = ", ".join(w.definition)
                if gr == True:
                    prL = '('
                    prR = ')'
                    
                verbform = w.getVerbform()
                #mult = 1
                if(w.getTense() == 'Participle') and (not(w.getPar() == '')):
                    tense = w.getPar() + " " + w.getTense()
                else:
                    tense = w.getTense()
                   # mult = 6
                person = w.getPerson()
                gender = w.getGender()
                
                if w.getPrefix() == True:
                    pr = "prefix [" + w.getPrefixW() + ']'
                    OutPut.append(pr)
                    X += 'x'*math.floor(len(pr)/4)
                    
                if (not(verbform == '')):
                    OutPut.append(verbform)
                    X += 'xxx'
                    
                if (not(tense == "")):
                    OutPut.append(tense)
                    X += 'xxx'
                    
                if (not(person == "")):
                    OutPut.append(person)
                    X += 'xxx'
                    
                if (not((w.getGenderVal() == -1)or(w.getGenderVal() == 2))) and ((not(w.getTenseVal() == -1)) or (w.getPlural() == True) or (w.getDual() == True)):
                    OutPut.append(gender)
                    X += 'xxx'
                    
                if w.getConstruct() == True:
                    contr = "cnstr."
                    OutPut.append(contr)
                    X += 'xxx'
                    
                if(not(pl == "")):
                    OutPut.append(pl)
                    X += 'xx'
                    
                if w.getModern() == True:
                    X += 'xxxxxxxx'
                    suff = "modern suffix:"
                    sf7 = " [" + w.getModernW() + ']'
                    OutPut.append(suff + sf7)
                    
                if w.getHey1() > 0:
                    suff = "suffix"
                    sf7 = " [" + dirHey + ']'
                    OutPut.append(suff + sf7)
                    X += 'x'*math.floor(len(suff + sf7)/4)       
                if w.getSuffix() == True:
                    if w.getHey1() > 0:
                        suff = ""
                    else:
                        suff = "suffix"
                    if w.getHey1() > 0:
                        sf7 = " [" + w.getSuffixW() + ',' + ' ' + dirHey + ']'  
                    else:
                        sf7 = " [" + w.getSuffixW() + ']'
                    X += 'x'*math.floor(len(suff + sf7)/4)
                    OutPut.append(suff + sf7)
                   
                speech = "" 
                speechB = ""
                for t in range(len(OutPut)):
                    speech += OutPut[t]
                    speechB += OutPut[t]
                    if(t < len(OutPut)-1):
                        speech += " "
                        speechB += " "
                
                
                script = TAB2*n + TAB2 + val + prL + speechB + X #(pre) + (s6[:-(preN-1)])*(2) + preSP + (verbform)*2 + s1 + (tense2)*(2) + s2*mult + person + s3 + gender + s4 + s4b + (constr[:-1])*2 + s5 + (suff) + (s7[:-1])*(2) + suffSP + pl*2 
                script+= prR + ARROW + isR + (w.getText()[:-1])*(2) + TAB + '-' + TAB
                spaces = len(script)
                
                self.wText += '\t\t'*n +  '\t\t' + val + prL + speech #pre + s6 + preSP + w.getVerbform() + s1 + tense + s2 + w.getPerson() + s3 + w.getGender() + s4 + s4b + constr + s5 + suff + s7 + suffSP + pl
                self.wText += prR + ARROW + isR + w.getText() + '\t' + '-' + '\t' + self.fixDef(definition, spaces) + ';' + ' gmra. = ' + str(w.getGemontria()) + '\n'
        elif number + Year == "":
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
                    if Lwords[lw] in prefixD:
                        self.wText += '\t\t'*(n+1) + "prefix " + '[' + Lwords[lw] + '-' + " " + prefixD[Lwords[lw]] + ']'
                    else:
                        self.wText += '\t\t'*(n+1) + "prefix " + '[' + Lwords[lw] + ']'
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
        n = 200
        diff = 0
        for i in range(len(words)):
            diff += len(words[i]) + 1
            if ((diff + spaces*0.70) > n):
                fixedL[i] = words[i] + '\n' + (' ')*spaces + (' ')*math.floor(spaces/10)
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
      
    def algorithm(self, look, word, Check):
        if word.getLen() < 2:
            return Word("", "")
        plural = False
    
        self.prefix(look, word, False, Check)
 
        if(not(word.getVerbform() in Hiphil)) and (not(word.getVerbform() == 'Hophal')) and (not(word.getVerbform() in Hithpeal)):
            self.participle(look, word, False)
        
        self.constr(look, word, Check)
        if(word.isVerb() == False):
            self.plural(look, word, Check)
            
        self.suffix(look, word, 2, Check)

        if(word.isVerb() == False):
            #self.plural(look, word, Check)
            self.constr(look, word, Check)
            self.modern(look, word, Check)
            self.dirHey(look, word, Check)
        
        if(word.isNoun() == False):
            self.tense(look, word, True, Check)
        self.verbForms(look, word, Check)
            
        self.pilpel(look, word, Check)
        self.irreg(look, word, Check)
                
    def FindHelper(self, look, w, Dict, Check):
        if Check == True:
            return self.FindHelperCheck(look, w, Dict)
            
        if(((w.getText() == self.CurrentWord.getText()) and (look.findText(w) == True))):
            return False
                
        if((w.getLen() < 3) and ((w.getTense() == 'Participle')or(w.getVerbform() in Hiphil)or(w.getVerbform() in Pual)or((w.getVerbform() in Piel)and(not(w.getVerbform() == 'Pilpel'))))):
            return False
        else:
            return look.find(w, Dict)
            
    def FindHelperCheck(self, look, w, Dict):

        if(look.findText(w) == True):
            return False
                
        if((w.getLen() < 3) and ((w.getTense() == 'Participle')or(w.getVerbform() in Hiphil)or(w.getVerbform() in Pual)or((w.getVerbform() in Piel)and(not(w.getVerbform() == 'Pilpel'))))):
            return False
        else:
            return look.find(w, Dict)
    
    def modern(self, look, word, Check):
        if(word.getLen() < 3) or (word.isPhrase()) or (word.isTense() == True) or (word.getModern() == True) or ((word.isVerbf() == True)and(not(word.getVerbform() == 'Qal'))):
            return Word("", "")
                
        if(word.getPartiVal() == 0):
            return Word("","")
                
        if(word.getLen() > 6):
            if word.lastX(5) in modernL:
                mdrnW = Word("","")
                mdrnW.equalTo(word)
                mdrnW.setText(self.Final(word.getText()[5:]))
                mdrnW.setModern()
                mdrnW.setMdrn(word.lastX(5))
                mdrnW.setNoun()
                self.FindHelper(look, mdrnW, self.Dict, Check)
                self.algorithm(look, mdrnW, Check)
                if(mdrnW.last() == "ת"):
                    mdrnWh = Word("","")
                    mdrnWh.equalTo(mdrnW) 
                    mdrnWh.setText('ה' + mdrnW.getText()[1:])
                    mdrnWh.addToValue(0.5)
                    self.algorithm(look, mdrnWh, Check)
                    self.FindHelper(look, mdrnWh, self.Dict, Check)
                if(not('ה' in word.getSufxList())):
                    mdrnWh = Word("","")
                    mdrnWh.equalTo(mdrnW)
                    mdrnWh.setText('ה' + self.unFinal(mdrnW.getText()))
                    mdrnWh.addToValue(2)
                    self.FindHelper(look, mdrnWh, self.Dict, Check)
                    self.algorithm(look, mdrnWh, Check)
                if(not('ת' in word.getSufxList())):
                    mdrnWt = Word("","")
                    mdrnWt.equalTo(mdrnW)
                    mdrnWt.setText('ת' + self.unFinal(mdrnW.getText()))
                    mdrnWt.addToValue(3)
                    self.FindHelper(look, mdrnWt, self.Dict, Check)
                    self.algorithm(look, mdrnWt, Check)
                return mdrnW
                
        if(word.getLen() > 5):
            if word.lastX(4) in modernL:
                mdrnW = Word("","")
                mdrnW.equalTo(word)
                mdrnW.setText(self.Final(word.getText()[4:]))
                mdrnW.setModern()
                mdrnW.setMdrn(word.lastX(4))
                mdrnW.setNoun()
                self.FindHelper(look, mdrnW, self.Dict, Check)
                self.algorithm(look, mdrnW, Check)
                if(mdrnW.last() == "ת"):
                    mdrnWh = Word("","")
                    mdrnWh.equalTo(mdrnW) 
                    mdrnWh.setText('ה' + mdrnW.getText()[1:])
                    mdrnWh.addToValue(0.5)
                    self.algorithm(look, mdrnWh, Check)
                    self.FindHelper(look, mdrnWh, self.Dict, Check)
                if(not('ה' in word.getSufxList())):
                    mdrnWh = Word("","")
                    mdrnWh.equalTo(mdrnW)
                    mdrnWh.setText('ה' + self.unFinal(mdrnW.getText()))
                    mdrnWh.addToValue(2)
                    self.FindHelper(look, mdrnWh, self.Dict, Check)
                    self.algorithm(look, mdrnWh, Check)
                if(not('ת' in word.getSufxList())):
                    mdrnWt = Word("","")
                    mdrnWt.equalTo(mdrnW)
                    mdrnWt.setText('ת' + self.unFinal(mdrnW.getText()))
                    mdrnWt.addToValue(3)
                    self.FindHelper(look, mdrnWt, self.Dict, Check)
                    self.algorithm(look, mdrnWt, Check)
                if((word.getPlural() == False) or (not(word.getGenderVal() == 1))):
                    mdrnWth = Word("","")
                    mdrnWth.equalTo(mdrnW)
                    mdrnWth.setText('תו' + self.unFinal(mdrnW.getText()))
                    mdrnWth.addToValue(4)
                    self.FindHelper(look, mdrnWth, self.Dict, Check)
                    self.algorithm(look, mdrnWth, Check)
                return mdrnW
                
        if(word.getLen() > 4):
            if word.last3() in modernL:
                #mdrnW = Word("","")
                #mdrnW.equalTo(word)
                #mdrnW.setText(self.Final(word.getText()[2:]))
                #mdrnW.setModern()
                #mdrnW.setMdrn(word.last2())
                #mdrnW.setNoun()
                #self.FindHelper(look, mdrnW, self.Dict, Check)
                mdrnW2 = Word("","")
                mdrnW2.equalTo(word)
                mdrnW2.setText(self.Final(word.getText()[3:]))
                mdrnW2.setModern()
                mdrnW2.setMdrn(word.last3())
                mdrnW2.setNoun()
                self.FindHelper(look, mdrnW2, self.Dict, Check)
                self.algorithm(look, mdrnW2, Check)
                if(mdrnW2.last() == "ת"):
                    mdrnWh = Word("","")
                    mdrnWh.equalTo(mdrnW2) 
                    mdrnWh.setText('ה' + mdrnW.getText()[1:])
                    mdrnWh.addToValue(0.5)
                    self.algorithm(look, mdrnWh, Check)
                    self.FindHelper(look, mdrnWh, self.Dict, Check)
                if(not('ה' in word.getSufxList())):
                    mdrnWh = Word("","")
                    mdrnWh.equalTo(mdrnW2)
                    mdrnWh.setText('ה' + self.unFinal(mdrnW2.getText()))
                    mdrnWh.addToValue(2)
                    self.FindHelper(look, mdrnWh, self.Dict, Check)
                    self.algorithm(look, mdrnWh, Check)
                if(not('ת' in word.getSufxList())):
                    mdrnWt = Word("","")
                    mdrnWt.equalTo(mdrnW2)
                    mdrnWt.setText('ת' + self.unFinal(mdrnW2.getText()))
                    mdrnWt.addToValue(3)
                    self.FindHelper(look, mdrnWt, self.Dict, Check)
                    self.algorithm(look, mdrnWt, Check)
                #return mdrnW2
                
        if(word.getLen() > 3):
            if (word.last2() in modernL):
                mdrnW = Word("","")
                mdrnW.equalTo(word)
                mdrnW.setText(self.Final(word.getText()[2:]))
                mdrnW.setModern()
                mdrnW.setMdrn(word.last2())
                mdrnW.setNoun()
                self.FindHelper(look, mdrnW, self.Dict, Check)
                self.algorithm(look, mdrnW, Check)
                if(mdrnW.last() == "ת"):
                    mdrnWh = Word("","")
                    mdrnWh.equalTo(mdrnW) 
                    mdrnWh.setText('ה' + mdrnW.getText()[1:])
                    mdrnWh.addToValue(0.5)
                    self.algorithm(look, mdrnWh, Check)
                    self.FindHelper(look, mdrnWh, self.Dict, Check)
                if(not('ה' in word.getSufxList())):
                    mdrnWh = Word("","")
                    mdrnWh.equalTo(mdrnW)
                    mdrnWh.setText('ה' + self.unFinal(mdrnW.getText()))
                    mdrnWh.addToValue(2)
                    self.FindHelper(look, mdrnWh, self.Dict, Check)
                    self.algorithm(look, mdrnWh, Check)
                if(not('ת' in word.getSufxList())):
                    mdrnWt = Word("","")
                    mdrnWt.equalTo(mdrnW)
                    mdrnWt.setText('ת' + self.unFinal(mdrnW.getText()))
                    mdrnWt.addToValue(3)
                    self.FindHelper(look, mdrnWt, self.Dict, Check)
                    self.algorithm(look, mdrnWt, Check)
                return mdrnW
            
        if (word.last() in modernL):
            mdrnW = Word("","")
            mdrnW.equalTo(word)
            mdrnW.setText(self.Final(word.getText()[1:]))
            mdrnW.setModern()
            mdrnW.setMdrn(word.last())
            mdrnW.setNoun()
            self.FindHelper(look, mdrnW, self.Dict, Check)
            self.algorithm(look, mdrnW, Check)
            if(mdrnW.last() == "ת"):
                mdrnWh = Word("","")
                mdrnWh.equalTo(mdrnW) 
                mdrnWh.setText('ה' + mdrnW.getText()[1:])
                mdrnWh.addToValue(0.5)
                self.algorithm(look, mdrnWh, Check)
            if(not('ה' in word.getSufxList())):
                mdrnWh = Word("","")
                mdrnWh.equalTo(mdrnW)
                mdrnWh.setText('ה' + self.unFinal(mdrnW.getText()))
                mdrnWh.addToValue(2)
                self.FindHelper(look, mdrnWh, self.Dict, Check)
                self.algorithm(look, mdrnWh, Check)
            if(not('ת' in word.getSufxList())):
                mdrnWt = Word("","")
                mdrnWt.equalTo(mdrnW)
                mdrnWt.setText('ת' + self.unFinal(mdrnW.getText()))
                mdrnWt.addToValue(3)
                self.FindHelper(look, mdrnWt, self.Dict, Check)
                self.algorithm(look, mdrnWt, Check)
                
            return mdrnW
            
        return Word("", "")

    def tense(self, look, word, alg, Check):
        if(word.getLen() < 2) or (word.isPhrase()) or (word.isTense() == True) or ((word.getVerbform() == 'Niphal')or((word.getVerbform() == 'Hophal') and (self.CurrentWord.first() == 'ה'))or((word.getVerbform() in Hiphil) and (self.CurrentWord.first() == 'ה'))) or (word.getHey1() > 0):
            return False
            
        revCW = self.rev(self.CurrentWord.getText())
        posTov = revCW.find("ת", 0, 4)
        if not ((posTov == -1) or (posTov == 0)):
            if(revCW[posTov-1] == 'ה') and (word.getVerbform() in Hithpeal):
                return False
                
        if(not(word.getVerbform() in Hiphil)) and (not(word.getVerbform() == 'Hophal')) and (not(word.getVerbform() in Hithpeal)):
            parti = Word("","")
            parti.equalTo(self.participle(look, word, False))
        
        infin_abs = Word("","")
        infin_abs.equalTo(self.infinitiveAbs(look, word, Check))
            
        if(word.isNoun() == True):
            return False
            
        if(word.getPlural() == True) or (word.getDual() == True) or (word.getConstruct() == True) or (word.getPrixListEnd() == 'מ') or (word.getPrixListEnd() == 'ל') or ('ה' in word.getPrixList()):
            return False
        
        perf = Word("","")
        perf.equalTo(self.perfect(look, word, Check))
        if not (perf.getText() == ""):
            if alg == True:
                self.FindHelper(look, perf, self.Dict, Check)
                #self.algorithm(look, perf)
        
        infin = Word("","")
        if(not((word.getPrixListEnd() == 'מ') or (word.getPrixListEnd() == 'ל') or (word.getPrixListEnd() == 'כ') or ('ה' in word.getPrixList()))) and (not(word.getVerbform() in Hiphil)) and (not(word.getVerbform() == 'Hophal')) and (not(word.getVerbform() in Hithpeal)) and (word.getTenseVal() == -1):
            infin.equalTo(self.infinitive(look, word, Check))
            if not (infin.getText() == ""):
                if alg == True:
                    self.FindHelper(look, infin, self.Dict, Check)
                    #self.algorithm(look, infin)
                    
        imp = Word("","")
        if(not (word.getVerbform() in Hiphil)) and (not(word.getVerbform() == 'Hophal')) and (not(word.getVerbform() in Hithpeal)):
            if(word.isTense() == False):
                imp.equalTo(self.future(look, word, Check))
                if not (imp.getText() == ""):
                    if alg == True:
                        self.FindHelper(look, imp, self.Dict, Check)
                        #self.algorithm(look, imp)
            
        if(word.isTense() == False):
            imper = Word("","")
            imper.equalTo(self.imperative(look, word, Check))
            if not (imper.getText() == ""):
                if alg == True:
                    self.FindHelper(look, imper, self.Dict, Check)
                    self.piel(look, imper, Check)
                
        if(word.isTense() == False):
            cohor = Word("","")
            cohor.equalTo(self.cohortative(look, word, Check))
            if not (cohor.getText() == ""):
                if alg == True:
                    self.FindHelper(look, cohor, self.Dict, Check)
                    #self.algorithm(look, cohor)
                
        if(not(infin.getText() == "")) or (not(perf.getText() == "")) or (not(imp.getText() == "")):
            return True
        else:
            return False

    def verbForms(self, look, word, Check):
        if(word.getLen() < 2) or (word.isPhrase()) or (word.getIrreg() == True):
            return Word("","")

        nifalW = Word("","")
        nifalW.equalTo(self.nifal(look, word, Check))
        if not (nifalW.getText() == ""):
            self.algorithm(look, nifalW, Check)

        pilpelW = Word("","")
        pilpelW.equalTo(self.pilpel(look, word, Check))
        if not (pilpelW.getText() == ""):
            self.algorithm(look, pilpelW, Check)

        pielW = Word("","")
        pielW.equalTo(self.piel(look, word, Check))
        if not (pielW.getText() == ""):
            self.FindHelper(look, pielW, self.Dict, Check)
            #self.algorithm(look, pielW)

        pualW = Word("","")
        pualW.equalTo(self.pual(look, word, Check))
        if not (pualW.getText() == ""):
            self.algorithm(look, pualW, Check)
            
        hifilW = Word("","")
        hifilW.equalTo(self.hifil(look, word, Check))
        if not(hifilW.getText() == ""):
            self.algorithm(look, hifilW, Check)
            
        hufalW = Word("","")
        hufalW.equalTo(self.hufal(look, word, Check))
        if not (hufalW.getText() == ""):
            self.algorithm(look, hufalW, Check)
            
        hitpaelW = Word("","")
        hitpaelW.equalTo(self.hitpael(look, word, Check))
        if not (hitpaelW.getText() == ""):
            self.algorithm(look, hitpaelW, Check)
            
        hishtaphelW = Word("","")
        hishtaphelW.equalTo(self.hishtaphel(look, word, Check))
        if not (hishtaphelW.getText() == ""):
            self.algorithm(look, hishtaphelW, Check)
            
        return Word("", "")

    def pilpel(self, look, word, Check):
    
        rareVerbforms  = {'Qal':8, 'Hithpoel':14}
        
        if(word.getLen() < 3) or ((word.isVerbf() == True) and (not(word.getVerbform() in rareVerbforms))):
            return Word("","")
        
        Stop = False
        tempW = Word("","")
        tempW.equalTo(word)
        tempW.setText(self.unFinal(word.getText()))
        while (tempW.nextToLast() == self.unFinal(tempW.last()) and (Stop == False)):
            if(not(tempW.getRoot()[:2] == tempW.last2())) and (len(tempW.getText()) > 3): 
                Stop = False
            else:
                Stop = True
            tempW.setText(self.Final(tempW.getText()[1:]))
            tempWf = Word("","")
            tempWf.equalTo(tempW)
            
            if(not((tempW.last() == 'י') or (tempW.last() == 'ו') or (tempW.last() == 'ה'))):
                #tempWf.setText(self.Final(tempW.getText()))
                if(word.isVerbf() == False):
                    tempWf.setVerbform(8)
                else:
                    tempWf.setVerbform(rareVerbforms[word.getVerbform()])

            if(tempWf.getLen() < 3):
                Stop = True
                
            self.verbForms(look, tempWf, Check)
            self.irreg(look, tempWf, Check)
            self.FindHelper(look, tempWf, self.Dict, Check)
                
            if(not(tempW.last() == 'י')):
                tempWf2 = Word("","")
                tempWf2.equalTo(tempWf)
                tempWf2.setText('י' + self.unFinal(tempWf.getText()))
                tempWf2.addToValue(4)
                if(tempWf2.getLen() > 2):
                    if(not(tempWf2.hasRoot() and (not(tempWf2.getRoot()[1:] == tempWf2.last3()[1:])))):
                        tempWf2.setRoot(tempWf2.last3())
                self.FindHelper(look, tempWf2, self.Dict, Check)
            if(not(tempW.last() == 'ה')):
                tempWf3 = Word("","")
                tempWf3.equalTo(tempWf)
                tempWf3.setText('ה' + self.unFinal(tempWf.getText()))
                tempWf3.addToValue(3)
                if('ה' in tempWf3.getSufxList()):
                    tempWf3.remSuff();
                if(tempWf3.getLen() > 2):
                    if(not(tempWf3.hasRoot() and (not(tempWf3.getRoot()[1:] == tempWf3.last3()[1:])))):
                        tempWf3.setRoot(tempWf3.last3())
                self.FindHelper(look, tempWf3, self.Dict, Check)
                self.verbForms(look, tempWf3, Check)
            if (not (tempW.nextToLast() == self.unFinal(tempW.last()))) or (len(tempW.getText()) < 3):
                return tempWf
        
        tempW = Word("","")
        tempW.equalTo(word)
        tempW.setText(self.unFinal(word.getText()))
        if tempW.last2() == tempW.getText()[2:4]: 
            tempW.setText(self.Final(tempW.getText()[2:]))
            tempWf = Word("","")
            tempWf.equalTo(tempW)
            tempWf.setText(self.Final(tempW.getText()))
            if(word.isVerbf() == False):
                tempWf.setVerbform(8)
            else:
                tempWf.setVerbform(rareVerbforms[word.getVerbform()])
                    
            self.verbForms(look, tempWf, Check)
             
            if(not(word.getRoot()[:2] == word.last2())): 
                tempWf2 = Word("","")
                tempWf2.equalTo(tempWf)
                tempWf2.setText('י' + self.unFinal(tempWf.getText()))
                tempWf2.addToValue(4)
                if(tempWf2.getLen() > 2):
                    if(not(tempWf2.hasRoot() and (not(tempWf2.getRoot()[1:] == tempWf2.last3()[1:])))):
                        tempWf2.setRoot(tempWf2.last3())
                tempWf3 = Word("","")
                tempWf3.equalTo(tempWf)
                tempWf3.setText('ה' + self.unFinal(tempWf.getText()))
                tempWf3.addToValue(3)
                if('ה' in tempWf3.getSufxList()):
                    tempWf3.remSuff();
                if(tempWf3.getLen() > 2):
                    if(not(tempWf3.hasRoot() and (not(tempWf3.getRoot()[1:] == tempWf3.last3()[1:])))):
                        tempWf3.setRoot(tempWf3.last3())
                self.irreg(look, tempWf, Check)
                self.verbForms(look, tempWf2, Check)
                self.verbForms(look, tempWf3, Check)
                self.FindHelper(look, tempWf, self.Dict, Check)
                self.FindHelper(look, tempWf2, self.Dict, Check)
                self.FindHelper(look, tempWf3, self.Dict, Check)
                return tempWf
            if(tempWf.getLen() == 2) or (word.getRoot()[:2] == word.last2()):
                self.FindHelper(look, tempWf, self.Dict, Check)
                
        return Word("", "")  

    def nifal(self, look, word, Check):

        rareVerbforms  = {'Qal':1}
        
        if(word.getLen() < 3) or (word.getIrreg() == True) or (word.isParticiple() == True) or (word.getTense() == 'Imperfect') or ((word.isVerbf() == True) and (not(word.getVerbform() in rareVerbforms))):
            return Word("","")
                  
        if(word.getTense() == 'Infinitive') or (word.getTense() == 'Infinitive abs.') or (word.getTense() == 'Imperative'):
            if(word.first() == 'ה') and (not(word.getRoot()[-2:] == word.first2())):
                nifalW = Word("","")
                nifalW.equalTo(word)
                if(word.nextToFirst() == 'ו'):
                    nifalW.setText(word.getText()[:-2] + 'י')
                else:
                    nifalW.setText(word.getText()[:-1])
                
                if(nifalW.getLen() > 2):
                    if(not(word.hasRoot() and (not(word.getRoot()[:2] == self.Final(word.firstX(4)[:2]))))):
                        nifalW.setRoot(self.Final(nifalW.first3()))
                
                if(word.isVerbf() == False):
                    nifalW.setVerbform(1)
                else:
                    nifalW.setVerbform(rareVerbforms[word.getVerbform()])
                    
                self.FindHelper(look, nifalW, self.Dict, Check)
                self.algorithm(look, nifalW, Check)
                return nifalW
            if(not(word.getTense() == 'Infinitive abs.')):
                return Word("","")
        
        if(word.first() == 'נ') and (not(word.getRoot()[-2:] == word.first2())):
            nifalW = Word("","")
            nifalW.equalTo(word)
            if(word.nextToFirst() == 'ו'):
                nifalW.setText(word.getText()[:-2] + 'י')
            else:
                nifalW.setText(word.getText()[:-1])
                
            if(nifalW.getLen() > 2):
                if(not(word.hasRoot() and (not(word.getRoot()[:2] == self.Final(word.firstX(4)[:2]))))):
                    nifalW.setRoot(self.Final(nifalW.first3()))
            
            if(word.isVerbf() == False):
                nifalW.setVerbform(1)
            else:
                nifalW.setVerbform(rareVerbforms[word.getVerbform()])
                    
            self.FindHelper(look, nifalW, self.Dict, Check)
            self.perfect(look, nifalW, Check)
            return nifalW
            
        return Word("", "")
    
    def piel(self, look, word, Check):

        rareVerbforms  = {'Qal':2, 'Hithpeal':6, 'Pilpel':10}
        
        if(word.getLen() < 3) or ((word.isVerbf() == True) and (not(word.getVerbform() in rareVerbforms))):
            return Word("","")

        if(word.XtoY(1, 3) == 'יי') and (len(word.getText()) > 4) and (not((word.hasRoot == True) and (not((word.getRootFirst2()  == word.first2()) or (word.getRootFirst2() == word.XtoY(1, 3)) or (word.getRootFirst2() == word.XtoY(2, 4)))))) and (self.num_of_a_roots(word.getText()[:-5]) == 0):
            pielW = Word("","")
            pielW.equalTo(word)
            pielW.setText(word.getText()[:-3] + word.first())
            pielW.setRoot(self.Final(pielW.first3()))
        
            if(word.isVerbf() == False):
                pielW.setVerbform(2)
            else:
                pielW.setVerbform(rareVerbforms[word.getVerbform()])
                
            self.FindHelper(look, pielW, self.Dict, Check)
            self.algorithm(look, pielW, Check)
        
        if(word.nextToFirst() == 'י') and (len(word.getText()) > 3) and (not((word.hasRoot == True) and (not((word.getRootFirst2()  == word.first2()) or (word.getRootFirst2() == word.XtoY(1, 3)))))) and (self.num_of_a_roots(word.getText()[:-4]) == 0):
            pielW = Word("","")
            pielW.equalTo(word)
            pielW.setText(word.getText()[:-2] + word.first())
            pielW.setRoot(self.Final(pielW.first3()))
            
            if(word.isVerbf() == False):
                pielW.setVerbform(2)
            else:
                pielW.setVerbform(rareVerbforms[word.getVerbform()])
                
            self.FindHelper(look, pielW, self.Dict, Check)
            self.algorithm(look, pielW, Check)
        
            return pielW
        
        if(word.nextToFirst() == 'י') and (len(word.getText()) == 3) and (not((word.hasRoot == True) and (not((word.getRootFirst2()  == word.first2()) or (word.getRootFirst2() == word.XtoY(1, 3)))))):
            hollow = Word("","")
            hollow.equalTo(word)
            hollow.setText(word.last() + 'ו' + word.first())
            hollow.addToValue(1)
            hollow.setRoot(self.Final(hollow.getText()))
            
            if(word.isVerbf() == False):
                hollow.setVerbform(2)
            else:
                hollow.setVerbform(rareVerbforms[word.getVerbform()])
                
            self.FindHelper(look, hollow, self.Dict, False)
            self.perfect(look, hollow, False)
        
            return hollow
            
        if(word.third() == 'י') and (word.first() in prefixL) and (len(word.getText()) > 3) and (not((word.hasRoot == True) and (not((word.getRootFirst2()  == word.first2()) or (word.getRootFirst2() == word.XtoY(1, 3)))))):
            hollow = Word("","")
            hollow.equalTo(word)
            hollow.setText(word.getText()[:-3] + 'ו' +  word.nextToFirst() + word.first())
            hollow.addToValue(1)
            
            if(word.isVerbf() == False):
                hollow.setVerbform(2)
            else:
                hollow.setVerbform(rareVerbforms[word.getVerbform()])
                
            if(self.prefixRuls(word, word.first(), False) == True):
                self.prefix(look, hollow, False, Check)
            if(word.first() == 'ל'):
                return self.infinitive(look, hollow, Check)
            if(word.first() == 'מ'):
                return self.participle(look, hollow, False)
        
            return hollow
        
        if(len(word.getText()) > 5) and (word.first() in prefixL) and (word.XtoY(2, 4) == 'יי') and (not((word.hasRoot == True) and (not((word.getRootFirst2()  == word.XtoY(1, 3)) or (word.getRootFirst2() == word.XtoY(2, 4)) or (word.getRootFirst2() == word.XtoY(3, 5)))))) and (self.num_of_a_roots(word.getText()[:-6]) == 0):
            pielW = Word("","")
            pielW.equalTo(word)
            pielW.setText(word.getText()[:-4] + word.nextToFirst() + word.first())
            pielW.setRoot(self.Final(pielW.getText()[-4:-1]))
            
            if(word.isVerbf() == False):
                pielW.setVerbform(2)
            else:
                pielW.setVerbform(rareVerbforms[word.getVerbform()])
                
            self.algorithm(look, pielW, Check)
            if(self.prefixRuls(word, word.first(), False) == True):
                self.prefix(look, pielW, False, Check)
            if(word.first() == 'ל'):
                return self.infinitive(look, pielW, Check)
            if(word.first() == 'מ'):
                return self.participle(look, pielW, False)
            
        if(len(word.getText()) > 4) and (word.first() in prefixL) and (word.third() == 'י') and (not((word.hasRoot == True) and (not((word.getRootFirst2()  == wordword.XtoY(1, 3)) or (word.getRootFirst2() == word.XtoY(2, 4)))))) and (self.num_of_a_roots(word.getText()[:-5]) == 0):
            pielW = Word("","")
            pielW.equalTo(word)
            pielW.setText(word.getText()[:-3] + word.nextToFirst() + word.first())
            pielW.setRoot(self.Final(pielW.getText()[-4:-1]))
            
            if(word.isVerbf() == False):
                pielW.setVerbform(2)
            else:
                pielW.setVerbform(rareVerbforms[word.getVerbform()])
                
            self.algorithm(look, pielW, Check)
            if(self.prefixRuls(word, word.first(), False) == True):
                self.prefix(look, pielW, False, Check)
            if(word.first() == 'ל'):
                return self.infinitive(look, pielW, Check)
            if(word.first() == 'מ'):
                return self.participle(look, pielW, False)
                
        return Word("", "")  
    
    def pual(self, look, word, Check):

        rareVerbforms  = {'Qal':3, 'Pilpel':11, 'Hithpeal':13}
        
        if(word.getLen() < 4) or (word.getPar() == 'Active') or ((word.isVerbf() == True) and (not(word.getVerbform() in rareVerbforms))):
            return Word("","")

        if(word.nextToFirst() == 'ו') and (len(word.getText()) > 3) and (not((word.hasRoot == True) and (not((word.getRootFirst2()  == word.first2()) or (word.getRootFirst2() == word.XtoY(1, 3)))))) and (self.num_of_a_roots(word.getText()[:-4]) == 0):
            pualW = Word("","")
            pualW.equalTo(word)
            pualW.setText(word.getText()[:-2] + word.first())
            pualW.setRoot(self.Final(pualW.first3()))
            
            if(word.isVerbf() == False):
                pualW.setVerbform(3)
            else:
                pualW.setVerbform(rareVerbforms[word.getVerbform()])
                
            self.FindHelper(look, pualW, self.Dict, Check)
            self.algorithm(look, pualW, Check)
        
        if(word.nextToFirst() == 'ו') and (word.third() == 'י') and (not((word.hasRoot == True) and (not((word.getRootFirst2()  == word.first2()) or (word.getRootFirst2() == word.XtoY(1, 3)))))) and (self.num_of_a_roots(word.getText()[:-4]) == 0):
            if(len(word.getText()) == 4):
                hollow = Word("","")
                hollow.equalTo(word)
                hollow.setText(word.getText()[:-3] + word.nextToFirst() + word.first())
                hollow.setRoot(self.Final(hollow.first3()))

                if(word.isVerbf() == False):
                    hollow.setVerbform(3)
                else:
                    hollow.setVerbform(rareVerbforms[word.getVerbform()])
                
                self.FindHelper(look, hollow, self.Dict, Check)
                return hollow
            
            if(word.first() == 'מ') and (len(word.getText()) > 4):
                self.hufal(look, word, Check)
            pualW = Word("","")
            pualW.equalTo(word)
            pualW.setText(word.getText()[:-2] + word.first())
            pualW.setRoot(self.Final(pualW.first3()))

            if(word.isVerbf() == False):
                pualW.setVerbform(3)
            else:
                pualW.setVerbform(rareVerbforms[word.getVerbform()])
            
            self.FindHelper(look, pualW, self.Dict, Check)
            return pualW
            
        if(len(word.getText()) > 4) and (word.third() == 'ו') and (not((word.hasRoot == True) and (not((word.getRootFirst2()  == wordword.XtoY(1, 3)) or (word.getRootFirst2() == word.XtoY(2, 4)))))) and (self.num_of_a_roots(word.getText()[:-5]) == 0):
            pualW = Word("","")
            pualW.equalTo(word)
            pualW.setText(word.getText()[:-3] + word.nextToFirst() + word.first())
            pualW.setRoot(self.Final(pualW.getText()[-4:-1]))
        
            if(word.isVerbf() == False):
                pualW.setVerbform(3)
            else:
                pualW.setVerbform(rareVerbforms[word.getVerbform()])
            if(self.prefixRuls(word, word.first(), False) == True):
                self.prefix(look, pualW, False, Check)
            if(word.first() == 'ל'):
                return self.infinitive(look, pualW, Check)
            if(word.first() == 'מ'):
                return self.participle(look, pualW, False)
            
        return Word("", "")
    
    def hifil(self, look, word, Check):

        rareVerbforms  = {'Qal':4}
        
        if(word.getLen() < 3) or ((word.isVerbf() == True) and (not(word.getVerbform() in rareVerbforms))) or (word.getPartiVal() == 1) or (word.getTenseVal() == 0) or (word.getConstruct() == True):
            return Word("","")
            
        end = False
        word2 = Word("","")
        word2.equalTo(word)
        Rword = Word("","")
        if(word2.getLen() > 3):
            if(word2.third() == 'י' ):
                wordH = Word("","")
                wordH.equalTo(word2)
                if ((wordH.last2() == 'םת') or (wordH.last2() == 'ןת') or (wordH.last2() == 'ית') or (wordH.last2() == 'ונ') or (wordH.last2() == 'הנ')):
                    wordH.setText(self.Final(wordH.getText()[2:]))
                    
                elif ((wordH.last() == 'ת') or (wordH.last() == 'י')):
                    wordH.setText(self.Final(wordH.getText()[1:]))
                    
                if(wordH.getLen() < 5):
                    
                    if(word2.first() == 'מ'):
                        wordNun = Word("","")
                        wordNun.equalTo(word2)
                        wordNun.setText(word2.getText()[:-1] + "נ" + word2.first())
                        self.hifil(look, wordNun, Check)
                        
                        H_hollow = Word("","")
                        H_hollow.equalTo(word2)
                        
                        #word_P = Word("","")
                        #word_P.equalTo(word2)
                        
                        H_hollow.setText(word2.getText()[:-3] + "ו" + word2.first2())
                        H_hollow.addToValue(1)
                        
                        #word_P.setText(word2.getText()[:-3] + word2.first2())
                        #word_P.addToValue(1)
                        
                        
                        if(not(H_hollow.hasRoot() and (H_hollow.getRootFirst2() == H_hollow.first2()))):
                            H_hollow.setRoot(self.Final(H_hollow.getText()[-4:-1]))
                            
                        #if(not(word_P.hasRoot())):
                            #word_P.setRoot(self.Final(word_P.first3()))
                        
                        if(word2.isVerbf() == False):
                            H_hollow.setVerbform(4)
                            #word_P.setVerbform(4)
                        else:
                            H_hollow.setVerbform(rareVerbforms[word2.getVerbform()])
                            #word_P.setVerbform(rareVerbforms[word2.getVerbform()])
                                    
                        self.participle(look, H_hollow, False)
                        #self.participle(look, word_P, Check) 
                        
                        #self.FindHelper(look, word_P, self.Dict Check)
                        return H_hollow
                        
                if(word2.first() == 'ה') and (not(word2.getRoot()[-2:] == word2.first2())):
                    wordNun = Word("","")
                    wordNun.equalTo(word2)
                    wordNun.setText(word2.getText()[:-1] + "נ" + word2.first())
                    self.hifil(look, wordNun, Check)
                    
                    H_hollow = Word("","")
                    H_hollow.equalTo(word2)
                    H_hollow.setText(word2.getText()[:-3] + "ו" + word2.first2()[:-1])
                    H_hollow.addToValue(1)
                    H_hollow.setRoot(self.Final(H_hollow.first3()))
                    
                    if(word2.isVerbf() == False):
                        H_hollow.setVerbform(4)
                    else:
                        H_hollow.setVerbform(rareVerbforms[word2.getVerbform()])
                                
                    self.FindHelper(look, H_hollow, self.Dict, Check)
                    self.perfect(look, H_hollow, Check)
                    self.imperative(look, H_hollow, Check)
                    self.irreg(look, H_hollow, Check)
                    return H_hollow
                        
                if((word2.first() == 'י') or (word2.first() == 'נ' ) or (word2.first() == 'ת' ) or (word2.first() == 'א')):
                    wordNun = Word("","")
                    wordNun.equalTo(word2)
                    wordNun.setText(word2.getText()[:-1] + "נ" + word2.first())
                    self.hifil(look, wordNun, Check)
                    
                    H_hollow = Word("","")
                    H_hollow.equalTo(word2)
                    H_hollow.setText(word2.getText()[:-3] + "ו" + word2.first2())
                    H_hollow.addToValue(1)
                    if(not(H_hollow.hasRoot() and (H_hollow.getRootFirst2() == H_hollow.first2()))):
                        H_hollow.setRoot(self.Final(H_hollow.getText()[-4:-1]))
                        
                    if(word2.first() == 'י'):
                        word_P = Word("","")
                        word_P.equalTo(word2)
                        word_P.setText(word2.getText()[:-3] + word2.first2())
                        word_P.addToValue(1)
                        if(not(word_P.hasRoot())):
                            word_P.setRoot(self.Final(word_P.first3()))
                            
                        if(word2.isVerbf() == False):
                            word_P.setVerbform(4)
                        else:
                            word_P.setVerbform(rareVerbforms[word2.getVerbform()])
                            
                        self.perfect(look, word_P, Check)
                        self.FindHelper(look, word_P, self.Dict, Check)
                        self.irreg(look, word_P, Check)
                        
                    if(word2.first() == 'ת') and (not(word2.getRoot()[-2:] == word2.first2())):
                        T_hollow = Word("","")
                        T_hollow.equalTo(word2)
                        T_hollow.setText(word2.getText()[:-3] + "ו" + word2.first2()[:-1])
                        T_hollow.addToValue(1)
                        if(not(T_hollow.hasRoot() and (not(T_hollow.getRoot()[:2] == self.Final(word2.firstX(4)[:2]))))):
                            T_hollow.setRoot(self.Final(T_hollow.first3()))
                        
                        T_hollow.setVerbform(12)
                        self.perfect(look, T_hollow, Check)
                        self.FindHelper(look, T_hollow, self.Dict, Check)
                        self.irreg(look, T_hollow, Check)
                        
                    if(word2.isVerbf() == False):
                        H_hollow.setVerbform(4)
                    else:
                        H_hollow.setVerbform(rareVerbforms[word2.getVerbform()])
                        
                    if(word2.last() == 'ה') and (word2.getLen() > 4):
                        self.cohortative(look, H_hollow, Check)
                                
                    self.future(look, H_hollow, Check)
                    return H_hollow
                
        if(word2.getLen() > 4):
            if(word2.fourth() == 'י'):
                if(word2.getLen() < 6):
                    if(word2.first() == 'ל') and (word2.second() == 'ה'):
                        hifilW = Word("","")
                        hifilW.equalTo(word2)
                        hifilW.setText(word2.getText()[:-4]   + "ו" +  word2.first3()[:-2] + word2.first())
                        hifilW.addToValue(1)
                        if(not(word2.hasRoot() and ((word2.getRootFirst2() == word2.first2()) or (word2.getRootFirst2() == word2.XtoY(1, 3))))):
                            hifilW.setRoot(self.Final(hifilW.getText()[-4:-1]))
                        if(word2.isVerbf() == False):
                            hifilW.setVerbform(4)
                        else:
                            hifilW.setVerbform(rareVerbforms[word2.getVerbform()])
                                        
                        self.infinitive(look, hifilW, Check)
                        
                    if(word2.first() == 'מ') and (not((word2.hasRoot()) and (not((word2.getRootLast2() == word2.XtoY(2, 4)) or (word2.getRootLast2() == word2.XtoY(3, 5)))))):
                        hifilW = Word("","")
                        hifilW.equalTo(word2)
                        hifilW.setText(word2.getText()[:-4] + word2.first3())
                        hifilW.setRoot(self.Final(hifilW.getText()[-4:-1]))
                            
                        if(word2.isVerbf() == False):
                            hifilW.setVerbform(4)
                        else:
                            hifilW.setVerbform(rareVerbforms[word2.getVerbform()])
                                    
                        self.participle(look, hifilW, False)
                            
                    if(word2.first() in prefixL) and (word2.second() =='ה') and (self.prefixRuls(word2, word2.first(), True) == True) and (not(word2.first() =='ו')) and (not(word2.first() =='ה')) and (not((word2.getRootFirst2() == word2.first2()) or (word2.getRootFirst2() == word2.XtoY(1, 3)))):
                        hifilW = Word("","")
                        hifilW.equalTo(word2)
                        hifilW.setText(word2.getText()[:-4] + "ו" + word2.first3()[:-2] + word2.first())
                        hifilW.addToValue(1)
                        hifilW.setRoot(self.Final(hifilW.getText()[-4:-1]))
                            
                        if(word2.isVerbf() == False):
                            hifilW.setVerbform(4)
                        else:
                            hifilW.setVerbform(rareVerbforms[word2.getVerbform()])
                            
                        return self.smPrefix(look, hifilW, True, Check)
                
                if(word2.nextToFirst() == 'ו'):
                    if(word2.first() == 'ה') and (not(word2.getRootFirst2() == word2.first2())):
                        hifilW2 = Word("","")
                        hifilW2.equalTo(word2)
                        hifilW2.setText(word2.getText()[:-4] + word2.first3()[:-2] + 'י')
                        hifilW2.setRoot(self.Final(hifilW2.first3()))
                        
                        if(word2.isVerbf() == False):
                            hifilW2.setVerbform(4)
                        else:
                            hifilW2.setVerbform(rareVerbforms[word2.getVerbform()])
                                
                        self.FindHelper(look, hifilW2, self.Dict, Check)
                        self.perfect(look, hifilW2, Check)
                        self.imperative(look, hifilW2, Check)
                        return hifilW2
                
                if(word2.first() == 'ה') and (not(word2.getRootFirst2() == word2.first2())) and (not((word2.hasRoot()) and (not((word2.getRootLast2() == word2.XtoY(2, 4)) or (word2.getRootLast2() == word2.XtoY(3, 5)))))):
                    end = True
                    hifilW = Word("","")
                    hifilW.equalTo(word2)
                    hifilW.setText(word2.getText()[:-4]  + word2.first3()[:-1])
                    hifilW.setRoot(self.Final(hifilW.first3()))
                    
                    if(word2.isVerbf() == False):
                        hifilW.setVerbform(4)
                    else:
                        hifilW.setVerbform(rareVerbforms[word2.getVerbform()])
                                
                    self.FindHelper(look, hifilW, self.Dict, Check)
                    self.perfect(look, hifilW, Check)
                    self.imperative(look, hifilW, Check)
                    self.irreg(look, hifilW, Check)
                
                if((word2.first() == 'י') or (word2.first() == 'נ' ) or (word2.first() == 'ת' ) or (word2.first() == 'א')) and (not((word2.hasRoot()) and (not((word2.getRootLast2() == word2.XtoY(2, 4)) or (word2.getRootLast2() == word2.XtoY(3, 5)))))):
                    if(word2.nextToFirst() == 'ו'):# and (not(word2.getRoot()[-2:] == word2.first2())):
                        hifilW2 = Word("","")
                        hifilW2.equalTo(word2)
                        hifilW2.setText(word2.getText()[:-4] + word2.first3()[:-2] + word2.first())
                        hifilW2.setRoot(self.Final(hifilW2.first3()))
                        
                        if(word2.isVerbf() == False):
                            hifilW2.setVerbform(4)
                        else:
                            hifilW2.setVerbform(rareVerbforms[word2.getVerbform()])
                                    
                        if(word2.last() == 'ה') and (word2.getLen() > 5):
                            self.cohortative(look, hifilW2, Check)
                        
                        self.future(look, hifilW2, Check)
                        
                    hifilW = Word("","")
                    hifilW.equalTo(word2)
                    hifilW.setText(word2.getText()[:-4] + word2.first3())
                    hifilW.setRoot(self.Final(hifilW.getText()[-4:-1]))
                        
                    if(word2.first() == 'ת') and (not(word2.getRoot()[-2:] == word2.first2())):
                        tifilW = Word("","")
                        tifilW.equalTo(word2)
                        tifilW.setText(word2.getText()[:-4] + word2.first3()[:-1])
                        tifilW.setRoot(self.Final(tifilW.first3()))
                            
                        tifilW.setVerbform(12)
                        self.perfect(look, tifilW, Check)
                        self.FindHelper(look, tifilW, self.Dict, Check)
                        self.irreg(look, tifilW, Check)
                        
                    if(word2.isVerbf() == False):
                        hifilW.setVerbform(4)
                    else:
                        hifilW.setVerbform(rareVerbforms[word2.getVerbform()])
                                
                    if(word2.last() == 'ה') and (word2.getLen() > 5):
                        self.cohortative(look, hifilW, Check)
                        
                    self.future(look, hifilW, Check)

        if(word2.getLen() > 5):
            if(word2.getX(5) == 'י' ):
                if(word2.getLen() < 7):
                    if(word2.first() == 'ל') and (word2.second() == 'ה') and (not((word2.hasRoot()) and (not((word2.getRootLast2() == word2.XtoY(3, 5)) or (word2.getRootLast2() == word2.XtoY(4, 6)))))):
                        hifilW = Word("","")
                        hifilW.equalTo(word2)
                        hifilW.setText(word2.getText()[:-5]  + word2.firstX(4)[:-2] + word2.first())
                        hifilW.setRoot(self.Final(hifilW.getText()[-4:-1]))
                            
                        if(word2.isVerbf() == False):
                            hifilW.setVerbform(4)
                        else:
                            hifilW.setVerbform(rareVerbforms[word2.getVerbform()])
                                        
                        self.infinitive(look, hifilW, Check)
                                
                    if(word2.first() in prefixL) and (word2.second() =='ה') and (self.prefixRuls(word2, word2.first(), True) == True) and (not(word2.first() =='ו')) and (not(word2.first() =='ה')) and (not(word2.getRootFirst2() == word2.first3()[:-1]) or (word2.getRootLast2() == self.Final(word2.first3()[:-1]))) and (not((word2.hasRoot()) and (not((word2.getRootLast2() == word2.XtoY(3, 5)) or (word2.getRootLast2() == word2.XtoY(4, 6)))))):
                        hifilW = Word("","")
                        hifilW.equalTo(word2)
                        hifilW.setText(word2.getText()[:-5] + word2.firstX(4)[:-2] + word2.first())
                        hifilW.setRoot(self.Final(hifilW.getText()[-4:-1]))
                            
                        if(word2.isVerbf() == False):
                            hifilW.setVerbform(4)
                        else:
                            hifilW.setVerbform(rareVerbforms[word2.getVerbform()])
                                        
                        self.smPrefix(look, hifilW, True, Check)
                    
                if(word2.nextToFirst() == 'י') and (not(word2.getRootFirst2() == word2.first3()[:-1]) or (word2.getRootLast2() == self.Final(word2.first3()[:-1]))) and (not((word2.hasRoot()) and (not((word2.getRootLast2() == word2.XtoY(3, 5)) or (word2.getRootLast2() == word2.XtoY(4, 6)))))):
                    if(word2.first() == 'ה'):
                        hifilW2 = Word("","")
                        hifilW2.equalTo(word2)
                        hifilW2.setText(word2.getText()[:-5]  + word2.firstX(4)[:-2])
                        hifilW2.setRoot(self.Final(hifilW2.first3()))                       
                        hifilW2.setRoot(self.Final(hifilW2.first3()))
                        
                        if(word2.isVerbf() == False):
                            hifilW2.setVerbform(4)
                        else:
                            hifilW2.setVerbform(rareVerbforms[word2.getVerbform()])
                                
                        self.FindHelper(look, hifilW2, self.Dict, Check)
                        self.perfect(look, hifilW2, Check)
                        self.imperative(look, hifilW2, Check)
                        self.irreg(look, hifilW2, Check)
                        
                        return hifilW2
                    
                    if((word2.first() == 'י') or (word2.first() == 'נ' ) or (word2.first() == 'ת' ) or (word2.first() == 'א')) and (not(word2.getRootFirst2() == word2.first3()[:-1]) or (word2.getRootLast2() == self.Final(word2.first3()[:-1]))) and (not((word2.hasRoot()) and (not((word2.getRootLast2() == word2.XtoY(3, 5)) or (word2.getRootLast2() == word2.XtoY(4, 6)))))):
                        hifilW = Word("","")
                        hifilW.equalTo(word2)
                        hifilW.setText(word2.getText()[:-5]  + word2.firstX(4)[:-2] + word2.first())
                        hifilW.setRoot(self.Final(hifilW.getText()[-4:-1]))
                        
                        if(word2.isVerbf() == False):
                            hifilW.setVerbform(4)
                        else:
                            hifilW.setVerbform(rareVerbforms[word2.getVerbform()])
                                    
                        if(word2.last() == 'ה') and (word2.getLen() > 5):
                            self.cohortative(look, hifilW, Check)
                            
                        self.future(look, hifilW, Check)
                        
                    if(word2.first() in prefixL) and (self.prefixRuls(word2, word2.first(), True) == True) and (not(word2.first() =='ה')) and (not(word2.getRootFirst2() == word2.first3()[:-1]) or (word2.getRootLast2() == self.Final(word2.first3()[:-1]))) and (not((word2.hasRoot()) and (not((word2.getRootLast2() == word2.XtoY(3, 5)) or (word2.getRootLast2() == word2.XtoY(4, 6)))))):
                        hifilW = Word("","")
                        hifilW.equalTo(word2)
                        hifilW.setText(word2.getText()[:-5]  + word2.firstX(4)[:-2] + word2.first())
                        hifilW.setRoot(self.Final(hifilW.getText()[-4:-1]))
                            
                        if(word2.isVerbf() == False):
                            hifilW.setVerbform(4)
                        else:
                            hifilW.setVerbform(rareVerbforms[word2.getVerbform()])
                            
                        self.smPrefix(look, hifilW, True, Check)
                    
                        if(word2.first() == 'מ'):
                            hifilW3 = Word("","")
                            hifilW3.equalTo(word2)
                            hifilW3.setText(word2.getText()[:-5]  + word2.firstX(4)[:-2] + word2.first())
                            hifilW3.setRoot(self.Final(hifilW3.getText()[-4:-1]))
                            
                            if(word2.isVerbf() == False):
                                hifilW3.setVerbform(4)
                            else:
                                hifilW3.setVerbform(rareVerbforms[word2.getVerbform()])
                                        
                            return self.participle(look, hifilW3, False)

        if(word2.first2() == 'יה') and (end == False):
            if((word2.last() == 'ת' ) or (word2.last() == 'י' ) or (word2.last2() == 'םת') or (word2.last2() == 'ןת') or (word2.last2() == 'ית') or (word2.last2() == 'ונ') or (word2.last2() == 'הנ') or (word2.getLen() < 5)) and (not(word2.getRootFirst2() == word2.first2())):
                hifilW = Word("","")
                hifilW.equalTo(word2)
                hifilW.setText(word2.getText()[:-2])
                hifilW.addToValue(3)
                Ch = False
                if(hifilW.first() == 'ו'):
                    hifilW.setText(hifilW.getText()[:-1] + 'י')
                    #hifilW.addToValue(1)
                if(word2.isVerbf() == False):
                    hifilW.setVerbform(4)
                else:
                    hifilW.setVerbform(rareVerbforms[word2.getVerbform()])
                    
                if(hifilW.getLen() > 2):  
                    if ((hifilW.last2() == 'םת') or (hifilW.last2() == 'ןת') or (hifilW.last2() == 'ית') or (hifilW.last2() == 'ונ') or (hifilW.last2() == 'הנ')) and (hifilW.getLen() == 4):
                        hifilW.setText(hifilW.getText()[:-1] + 'ו' + hifilW.first())
                        hifilW.addToValue(1)
                    elif (hifilW.last() == 'ת') or (hifilW.last() == 'י') and (hifilW.getLen() == 3):
                        hifilW.setText(hifilW.getText()[:-1] + 'ו' + hifilW.first())
                        hifilW.addToValue(1)
                        
                    else:
                        hifilW.setRoot(self.Final(hifilW.first3()))
                elif hifilW.getLen() == 2:
                    hifilW.setText(hifilW.last() + 'ו' + hifilW.first())
                    hifilW.addToValue(1)
                    Ch = True
                else:
                    return Word("", "")
                    
                if(not(hifilW.hasRoot())):   
                    hifilW.setRoot(self.Final(hifilW.first3()))
                    
                if (Ch == True):
                    self.FindHelper(look, hifilW, self.Dict, Check)
                self.imperative(look, hifilW, Check)
                self.perfect(look, hifilW, Check)
                #self.infinitive(look, hifilW, Check)
                self.infinitiveAbs(look, hifilW, Check)
                self.cohortative(look, hifilW, Check)
                self.irreg(look, hifilW, Check)
                
                return hifilW
                
        if(word2.first() == 'ה') and (end == False):
            if((word2.last() == 'ת' ) or (word2.last() == 'י' ) or (word2.last2() == 'םת') or (word2.last2() == 'ןת') or (word2.last2() == 'ית') or (word2.last2() == 'ונ') or (word2.last2() == 'הנ') or (word2.getLen() < 4)) and (not(word2.getRootFirst2() == word2.first2())):
                hifilW = Word("","")
                hifilW.equalTo(word2)
                hifilW.setText(word2.getText()[:-1])
                hifilW.addToValue(3)
                Ch = False
                if(hifilW.first() == 'ו'):
                    hifilW.setText(hifilW.getText()[:-1] + 'י')
                    #hifilW.addToValue(1)
                if(word2.isVerbf() == False):
                    hifilW.setVerbform(4)
                else:
                    hifilW.setVerbform(rareVerbforms[word2.getVerbform()])
                    
                if(hifilW.getLen() > 2):  
                    if ((hifilW.last2() == 'םת') or (hifilW.last2() == 'ןת') or (hifilW.last2() == 'ית') or (hifilW.last2() == 'ונ') or (hifilW.last2() == 'הנ')) and (hifilW.getLen() == 4):
                        hifilW.setText(hifilW.getText()[:-1] + 'ו' + hifilW.first())
                        hifilW.addToValue(1)
                    elif ((hifilW.last() == 'ת') or (hifilW.last() == 'י')) and (hifilW.getLen() == 3):
                        hifilW.setText(hifilW.getText()[:-1] + 'ו' + hifilW.first())
                        hifilW.addToValue(1)
                    else:
                        hifilW.setRoot(self.Final(hifilW.first3()))
                elif hifilW.getLen() == 2:
                    Ch = True
                    hifilW.setText(hifilW.last() + 'ו' + hifilW.first())
                    hifilW.addToValue(1)
                else:
                    return Word("", "")
                    
                if(not(hifilW.hasRoot())):   
                    hifilW.setRoot(self.Final(hifilW.first3()))
                
                if (Ch == True):
                    self.FindHelper(look, hifilW, self.Dict, Check)
                    
                self.imperative(look, hifilW, Check)
                self.perfect(look, hifilW, Check)
                self.irreg(look, hifilW, Check)
                self.infinitiveAbs(look, hifilW, Check)
                self.cohortative(look, hifilW, Check)
                
                return hifilW
            
        return Word("", "")
    
    def hufal(self, look, word, Check):
    
        rareVerbforms  = {'Qal':5}
        
        if(word.getLen() < 4) or ((word.isVerbf() == True) and (not(word.getVerbform() in rareVerbforms))):
            return Word("","")
            
        if(word.getPartiVal() == 1) or ((word.getTense() == "Imperfect") or (word.getTense() == "Perfect") or (word.getTense() == "Participle")):
            return Word("","")
       
        if(word.nextToFirst() == 'ו') and (not(word.getRoot()[-2:] == word.first3()[:-1]) or (word.getRoot()[:2] == self.Final(word.first3()[:-1]))):
            if(word.first() == 'ה'):
                if(word.getLen() == 4):
                    wordNun = Word("","")
                    wordNun.equalTo(word)
                    wordNun.setText(word.getText()[:-2] + "נ" + word.first2())
                    self.hufal(look, wordNun, Check)
                
                hufalW = Word("","")
                hufalW.equalTo(word)
                hufalW.setText(word.getText()[:-2])
                if(hufalW.getLen() > 2) and (word.isTense() == True) and (not(hufalW.hasRoot() and (not(hufalW.getRoot()[:2] == self.Final(hufalW.first3()[:2]))))):
                    hufalW.setRoot(self.Final(hufalW.first3()))
                
                if(word.isVerbf() == False):
                    hufalW.setVerbform(5)
                else:
                    hufalW.setVerbform(rareVerbforms[word.getVerbform()])
                    
                self.FindHelper(look, hufalW, self.Dict, Check)
                self.imperative(look, hufalW, Check)
                self.perfect(look, hufalW, Check)
                hufalWy = Word("","")
                hufalWy.equalTo(hufalW)
                hufalWy.setText(hufalW.getText() + 'י')
                self.FindHelper(look, hufalWy, self.Dict, Check)
                self.irreg(look, hufalW, Check)
                return hufalW
                
            elif(word.first() == 'מ') and (not(word.getRoot()[-2:] == word.first2())):
                if(word.getLen() == 4):
                    wordNun = Word("","")
                    wordNun.equalTo(word)
                    wordNun.setText(word.getText()[:-2] + "נ" + word.first2())
                    self.hufal(look, wordNun, Check)
                
                hufalW = Word("","")
                hufalW.equalTo(word)
                hufalW.setText(word.getText()[:-2] + word.first())
                if(hufalW.getLen() > 3) and (not(hufalW.hasRoot() and (not(hufalW.getRoot()[:2] == self.Final(hufalW.firstX(4)[:2]))))):
                    hufalW.setRoot(self.Final(hufalW.getText()[-4:-1]))
                
                if(word.isVerbf() == False):
                    hufalW.setVerbform(5)
                else:
                    hufalW.setVerbform(rareVerbforms[word.getVerbform()])
                    
                return self.participle(look, hufalW, False)
       
            elif((word.first() == 'י') or (word.first() == 'נ' ) or (word.first() == 'ת' ) or (word.first() == 'א')) and (not(word.getRoot()[-2:] == word.first2())):
                if(word.getLen() == 4):
                    wordNun = Word("","")
                    wordNun.equalTo(word)
                    wordNun.setText(word.getText()[:-2] + "נ" + word.first2())
                    self.hufal(look, wordNun, Check)
                
                hufalW = Word("","")
                hufalW.equalTo(word)
                hufalW.setText(word.getText()[:-2] + word.first())
                if(hufalW.getLen() > 3) and (not(hufalW.hasRoot() and (not(hufalW.getRoot()[:2] == self.Final(hufalW.firstX(4)[:2]))))):
                    hufalW.setRoot(self.Final(hufalW.getText()[-4:-1]))
                
                if(word.isVerbf() == False):
                    hufalW.setVerbform(5)
                else:
                    hufalW.setVerbform(rareVerbforms[word.getVerbform()])
                    
                return self.future(look, hufalW, Check)
                
        if(word.third() == 'ו') and (not(word.getRoot()[-2:] == word.first3()[:-1]) or (word.getRoot()[:2] == self.Final(word.first3()[:-1]))):
            if(word.second() == 'ה'):
                if(word.first() in prefixL) and (not(word.Ht == False)) and (not(word.first() =='ו')) and (not(word.getRoot()[-2:] == word.first2())):
                    if(word.getLen() == 5):
                        wordNun = Word("","")
                        wordNun.equalTo(word)
                        wordNun.setText(word.getText()[:-3] + "נ" + word.first3())
                        self.hufal(look, wordNun, Check)
                        
                    hufalW = Word("","")
                    hufalW.equalTo(word)
                    hufalW.setText(word.getText()[:-3] + word.first())
                    if(hufalW.getLen() > 3) and (not(hufalW.hasRoot() and (not(hufalW.getRoot()[:2] == self.Final(hufalW.firstX(4)[:2]))))):
                        hufalW.setRoot(self.Final(hufalW.getText()[-4:-1]))
                    if(word.isVerbf() == False):
                        hufalW.setVerbform(5)
                    else:
                        hufalW.setVerbform(rareVerbforms[word.getVerbform()])
                        
                    if(word.first() == 'ל'):
                        self.infinitive(look, hufalW, Check)
                    if(self.prefixRuls(word, word.first(), True) == True):
                        return self.smPrefix(look, hufalW, True, Check)
                    else:
                        return hufalW

        return Word("", "")
    
    def hitpael(self, look, word, Check):
    
        rareVerbforms  = {'Qal':6, 'Niphal':9, 'Pilpel':15}
        
        if(word.getLen()  < 4) or (word.getPartiVal() == 1) or ((word.isVerbf() == True) and (not(word.getVerbform() in rareVerbforms))):
            return Word("","")
                   
        if((word.nextToFirst() == "ש") or (word.nextToFirst() == "ס") or (word.nextToFirst() == "צ")) and ((word.first() in prefixL)or(word.first() == 'א')or(word.first() == 'י')or(word.first() == 'נ')or(word.first() == 'ת')):
            metaW = Word("","")
            metaW.equalTo(self.metathesis(look, word))
            if not (metaW.getText() == ""):
                return self.hitpael(look, metaW, Check)
               
        #This loop checks for any possible assimilation and undoes it.
        if((word.nextToFirst() == "ט") or (word.nextToFirst() == "ד") or (word.nextToFirst() == "נ") or (word.nextToFirst() == "ס")) and ((word.first() in prefixL)or(word.first() == 'א')or(word.first() == 'י')or(word.first() == 'נ')or(word.first() == 'ת')):
            if(word.nextToFirst() == "ט"):
                if(word.third() == "צ"):
                    tempW = Word("","")
                    tempW.equalTo(word)
                    tempW.setText(word.getText()[:-2] + "ת" + word.first())
                    return self.hitpael(look, tempW, Check)
            else:
                tempW = Word("","")
                tempW.equalTo(word)
                tempW.setText(word.getText()[:-1] + "ת" + word.first())
                return self.hitpael(look, tempW, Check)
                
        if(word.first2() == 'תה') and (not(word.Ht == False)) and (not(word.getRoot()[-2:] == word.first3()[:-1]) or (word.getRoot()[:2] == self.Final(word.first3()[:-1]))):
            if(word.getLen() == 4):
                wordNun = Word("","")
                wordNun.equalTo(word)
                wordNun.setText(word.getText()[:-2] + "נ" + word.first2())
                self.hitpael(look, wordNun, Check)
                
            hitpaelW = Word("","") 
            hitpaelW.equalTo(word)
            if(word.third() == 'ו'):
                hitpaelW.setText(word.getText()[:-3] + 'י')
            else:
                hitpaelW.setText(word.getText()[:-2])  
                
            if(hitpaelW.getLen() > 2) and (not(hitpaelW.hasRoot() and (not(hitpaelW.getRoot()[:2] == self.Final(hitpaelW.first3()[:2]))))):
                hitpaelW.setRoot(self.Final(hitpaelW.first3()))
                
            if(word.isVerbf() == False):
                hitpaelW.setVerbform(6)
            else:
                hitpaelW.setVerbform(rareVerbforms[word.getVerbform()])
                
            if(hitpaelW.second() == 'י'):
                hollow = Word("","")
                hollow.equalTo(hitpaelW)
                hollow.setText(hitpaelW.getText()[:-2] + 'ו' + hitpaelW.first())
                hollow.addToValue(1)
                if(hollow.getLen() > 2) and (not(hollow.hasRoot() and (not(hollow.getRoot()[:2] == self.Final(hollow.first3()[:2]))))):
                    hollow.setRoot(self.Final(hollow.first3()))
                
                self.imperative(look, hollow, Check)   
                self.FindHelper(look, hollow, self.Dict, Check)
                
                if(not (hollow.last() == 'ה')) and ((word.getTense() == 'Perfect')and(not(self.CurrentWord.last() == word.last()))):
                    hollowh = Word("","")
                    hollowh.equalTo(hollow)
                    hollowh.setText('ה' + self.unFinal(hollow.getText()))
                    hollowh.addToValue(3)
                    if('ה' in hollowh.getSufxList()):
                        hollow.remSuff();
                    self.FindHelper(look, hollowh, self.Dict, Check)    
            
            self.imperative(look, hitpaelW, Check)
            self.irreg(look, hitpaelW, Check)
            self.FindHelper(look, hitpaelW, self.Dict, Check)
            
            if(not (hitpaelW.last() == 'ה')) and ((word.getTense() == 'Perfect')and(not(self.CurrentWord.last() == word.last()))):
                hitpaelWh = Word("","")
                hitpaelWh.equalTo(hitpaelW)
                hitpaelWh.setText('ה' + self.unFinal(hitpaelW.getText()))
                hitpaelWh.addToValue(3)
                if('ה' in hitpaelWh.getSufxList()):
                    hitpaelWh.remSuff();
                self.FindHelper(look, hitpaelWh, self.Dict, Check)
                self.irreg(look, hitpaelWh, Check)
            return hitpaelW
         
        if(word.third() == 'ת') and (word.second() == 'ה'):
            if(word.first() in prefixL) and (not(word.Ht == False)) and (not(word.first() =='ו')) and (not(word.getRoot()[-2:] == word.first2())):
                if(word.getLen() == 5):
                    wordNun = Word("","")
                    wordNun.equalTo(word)
                    wordNun.setText(word.getText()[:-3] + "נ" + word.first3())
                    self.hitpael(look, wordNun, Check)
                    
                hitpaelW = Word("","")
                hitpaelW.equalTo(word)
                hitpaelW.setText(word.getText()[:-3] + word.first())
                if(hitpaelW.getLen() > 3) and (not(hitpaelW.hasRoot() and (not(hitpaelW.getRoot()[:2] == self.Final(hitpaelW.firstX(4)[:2]))))):
                    hitpaelW.setRoot(self.Final(hitpaelW.getText()[-4:-1]))
                if(word.isVerbf() == False):
                    hitpaelW.setVerbform(6)
                else:
                    hitpaelW.setVerbform(rareVerbforms[word.getVerbform()])
                    
                if(hitpaelW.second() == 'י'):
                    hollow = Word("","")
                    hollow.equalTo(hitpaelW)
                    hollow.setText(hitpaelW.getText()[:-3] + 'ו' + hitpaelW.second() + hitpaelW.first())
                    hollow.addToValue(1)
                    if(hollow.getLen() > 3) and (not(hollow.hasRoot() and (not(hollow.getRoot()[:2] == self.Final(hollow.firstX(4)[:2]))))):
                        hollow.setRoot(self.Final(hollow.first3()[-4:-1]))
                    
                    if(word.first() == 'ל'):
                        self.infinitive(look, hollow, False)
                    self.Prefix(look, hollow, True, Check)
                    
                if(word.first() == 'ל'):
                    self.infinitive(look, hitpaelW, Check)
                if(self.prefixRuls(word, word.first(), True) == True):
                    return self.smPrefix(look, hitpaelW, True, Check)
                else:
                    return hitpaelW
                
        if(word.nextToFirst() == 'ת') and (word.first() == 'מ') and (not(word.first() =='ו')) and (not(word.getRoot()[-2:] == word.first2())):
            if(word.getLen() == 4):
                wordNun = Word("","")
                wordNun.equalTo(word)
                wordNun.setText(word.getText()[:-2] + "נ" + word.first2())
                self.hitpael(look, wordNun, Check)
                
            hitpaelW = Word("","")
            hitpaelW.equalTo(word)
            hitpaelW.setText(word.getText()[:-2] + word.first())
            if(hitpaelW.getLen() > 3) and (not(hitpaelW.hasRoot() and (not(hitpaelW.getRoot()[:2] == self.Final(hitpaelW.firstX(4)[:2]))))):
                hitpaelW.setRoot(self.Final(hitpaelW.getText()[-4:-1]))
            if(word.isVerbf() == False):
                hitpaelW.setVerbform(6)
            else:
                hitpaelW.setVerbform(rareVerbforms[word.getVerbform()])
                
            if(hitpaelW.second() == 'י'):
                hollow = Word("","")
                hollow.equalTo(hitpaelW)
                hollow.setText(hitpaelW.getText()[:-3] + 'ו' + hitpaelW.second() + hitpaelW.first())
                hollow.addToValue(1)
                if(hollow.getLen() > 3) and (not(hollow.hasRoot() and (not(hollow.getRoot()[:2] == self.Final(hollow.firstX(4)[:2]))))):
                    hollow.setRoot(self.Final(hollow.first3()[-4:-1]))
                  
                self.FindHelper(look, hollow, self.Dict, Check)
                self.participle(look, hollow, False)
                  
            return self.participle(look, hitpaelW, False)
            
        if(word.first2() == 'תנ') and (not(word.Ht == False)) and ((word.isVerbf() == False) or (word.getVerbform() == 'Qal')) and (not(word.getRoot()[-2:] == word.first3()[:-1]) or (word.getRoot()[:2] == self.Final(word.first3()[:-1]))):
            if(word.getLen() == 4):
                wordNun = Word("","")
                wordNun.equalTo(word)
                wordNun.setText(word.getText()[:-2] + "נ" + word.first2())
                self.hitpael(look, wordNun, Check)
                
            nithpaelW = Word("","")
            nithpaelW.equalTo(word)
            if(word.third() == 'ו'):
                nithpaelW.setText(word.getText()[:-3] + 'י')
            else:
                nithpaelW.setText(word.getText()[:-2])
            nithpaelW.setVerbform(9)
            
            if(nithpaelW.second() == 'י'):
                hollow = Word("","")
                hollow.equalTo(nithpaelW)
                hollow.setText(nithpaelW.getText()[:-2] + 'ו' + nithpaelW.first())
                hollow.addToValue(1)
                if(hollow.getLen() > 2) and (not(hollow.hasRoot() and (not(hollow.getRoot()[:2] == self.Final(hollow.first3()[:2]))))):
                    hollow.setRoot(self.Final(hollow.first3()))
                self.FindHelper(look, hollow, self.Dict, Check)
                self.imperative(look, hollow, Check)
                if(not (hollow.last() == 'ה')) and ((word.getTense() == 'Perfect')and(not(self.CurrentWord.last() == word.last()))):
                    hollowh = Word("","")
                    hollowh.equalTo(hollow)
                    hollowh.setText('ה' + self.unFinal(hollow.getText()))
                    hollowh.addToValue(3)
                    if('ה' in hollowh.getSufxList()):
                        hollow.remSuff();
                    self.FindHelper(look, hollowh, self.Dict, Check)    
            
            if(nithpaelW.getLen() > 2) and (not(nithpaelW.hasRoot() and (not(nithpaelW.getRoot()[:2] == self.Final(nithpaelW.first3()[:2]))))):
                nithpaelW.setRoot(self.Final(nithpaelW.first3()))
            self.FindHelper(look, nithpaelW, self.Dict, Check)
            self.imperative(look, nithpaelW, Check)
            if(not (nithpaelW.last() == 'ה')) and ((word.getTense() == 'Perfect')and(not(self.CurrentWord.last() == word.last()))):
                nithpaelWh = Word("","")
                nithpaelWh.equalTo(nithpaelW)
                nithpaelWh.setText('ה' + self.unFinal(nithpaelW.getText()))
                nithpaelWh.addToValue(3)
                if('ה' in nithpaelWh.getSufxList()):
                    nithpaelWh.remSuff();
                self.FindHelper(look, nithpaelWh, self.Dict, Check)
            
        if((word.first2() == 'תי') or (word.first2() == 'תת' ) or (word.first2() == 'תא') or (word.first2() == 'תנ')) and (not(word.Ht == False)) and (not(word.getRoot()[-2:] == word.first2())):
            if(word.getLen() == 4):
                wordNun = Word("","")
                wordNun.equalTo(word)
                wordNun.setText(word.getText()[:-2] + "נ" + word.first2())
                self.hitpael(look, wordNun, Check)
                
            hitpaelW = Word("","")
            hitpaelW.equalTo(word)
            hitpaelW.setText(word.getText()[:-2] + word.first())
            if(hitpaelW.getLen() > 3) and (not(hitpaelW.hasRoot() and (not(hitpaelW.getRoot()[:2] == self.Final(hitpaelW.firstX(4)[:2]))))):
                hitpaelW.setRoot(self.Final(hitpaelW.getText()[-4:-1]))
            if(word.isVerbf() == False):
                hitpaelW.setVerbform(6)
            else:
                hitpaelW.setVerbform(rareVerbforms[word.getVerbform()])
                
            if(hitpaelW.second() == 'י'):
                hollow = Word("","")
                hollow.equalTo(hitpaelW)
                hollow.setText(hitpaelW.getText()[:-3] + 'ו' + hitpaelW.second() + hitpaelW.first())
                hollow.addToValue(1)
                if(hollow.getLen() > 3) and (not(hollow.hasRoot() and (not(hollow.getRoot()[:2] == self.Final(hollow.firstX(4)[:2]))))):
                    hollow.setRoot(self.Final(hollow.first3()[-4:-1]))
                  
                self.FindHelper(look, hollow, self.Dict, Check)
                self.future(look, hollow, False)
                if(word.last() == 'ה'):
                    self.cohortative(look, hollow, Check)
                
            if(word.last() == 'ה'):
                self.cohortative(look, hitpaelW, Check)
            return self.future(look, hitpaelW, Check)
            
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
         
    def hishtaphel(self, look, word, Check):
    
        rareVerbforms  = {'Qal':7}
        
        if(word.getLen() < 5) or ((word.isVerbf() == True) and (not(word.getVerbform() in rareVerbforms))):
            return Word("","")
            
        if(word.getPartiVal() == 1):
            return Word("","")
       
        if(word.first3() == 'תשה') and (not('תש' in word.getRoot())):
            if(word.getLen() == 5):
                wordNun = Word("","")
                wordNun.equalTo(word)
                wordNun.setText(word.getText()[:-3] + "נ" + word.first3())
                self.hishtaphel(look, wordNun, Check)
                
            hishtaphelW = Word("","") 
            hishtaphelW.equalTo(word)
            if(word.fourth() == 'ו'):
                hishtaphelW.setText(word.getText()[:-4] + 'י')
            else:
                hishtaphelW.setText(word.getText()[:-3])
            if(hishtaphelW.getLen() > 2) and (not(hishtaphelW.hasRoot() and (not(hishtaphelW.getRoot()[:2] == self.Final(hishtaphelW.first3()[:2]))))):
                hishtaphelW.setRoot(self.Final(hishtaphelW.first3()))
            if(word.isVerbf() == False):
                hishtaphelW.setVerbform(7)
            else:
                hishtaphelW.setVerbform(rareVerbforms[word.getVerbform()])
                
            self.irreg(look, hishtaphelW, Check)
            self.FindHelper(look, hishtaphelW, self.Dict, Check)
            if(not (hishtaphelW.last() == 'ה')) and (not ('ה' in word.getSufxList())):
                hishtaphelWh = Word("","")
                hishtaphelWh.equalTo(hishtaphelW)
                hishtaphelWh.setText('ה' + self.unFinal(hishtaphelW.getText()))
                hishtaphelWh.addToValue(3)
                self.FindHelper(look, hishtaphelWh, self.Dict, Check)
            return hishtaphelW

        if(word.second() == 'ה') and (word.third() == 'ש') and (word.getX(4) == 'ת') and (not('תש' in word.getRoot())):
            if(word.first() in prefixL) and (not(word.Ht == False)) and (not(word.first() =='ו')) and (not(word.getRoot()[-2:] == word.first2())):
                if(word.getLen() == 6):
                    wordNun = Word("","")
                    wordNun.equalTo(word)
                    wordNun.setText(word.getText()[:-4] + "נ" + word.getX(4) + word.first3())
                    self.hishtaphel(look, wordNun, Check)
                
                hishtaphelW = Word("","")
                hishtaphelW.equalTo(word)
                hishtaphelW.setText(word.getText()[:-4] + word.first())
                if(hishtaphelW.getLen() > 3) and (not(hishtaphelW.hasRoot() and (not(hishtaphelW.getRoot()[:2] == self.Final(hishtaphelW.firstX(4)[:2]))))):
                    hishtaphelW.setRoot(self.Final(hishtaphelW.getText()[-4:-1]))
                    
                if(word.isVerbf() == False):
                    hishtaphelW.setVerbform(6)
                else:
                    hishtaphelW.setVerbform(rareVerbforms[word.getVerbform()])
                    
                if(word.first() == 'ל'):
                    self.infinitive(look, hishtaphelW, Check)
                if(self.prefixRuls(word, word.first(), True) == True):
                    return self.smPrefix(look, hishtaphelW, True, Check)
                else:
                    return hishtaphelW

        if(word.nextToFirst() == 'ש') and (word.third() == 'ת') and (word.first() == 'מ') and (not('תש' in word.getRoot())):
            if(word.getLen() == 5):
                wordNun = Word("","")
                wordNun.equalTo(word)
                wordNun.setText(word.getText()[:-3] + "נ" + word.first3())
                self.hishtaphel(look, wordNun, Check)
                
            hishtaphelW = Word("","")
            hishtaphelW.equalTo(word)
            hishtaphelW.setText(word.getText()[:-3] + word.first())
            if(hishtaphelW.getLen() > 3) and (not(hishtaphelW.hasRoot() and (not(hishtaphelW.getRoot()[:2] == self.Final(hishtaphelW.firstX(4)[:2]))))):
                hishtaphelW.setRoot(self.Final(hishtaphelW.getText()[-4:-1]))
            if(word.isVerbf() == False):
                hishtaphelW.setVerbform(7)
            else:
                hishtaphelW.setVerbform(rareVerbforms[word.getVerbform()])
                
            self.participle(look, hishtaphelW, False)
            
        if((word.first3() == 'תשי') or (word.first3() == 'תשת' ) or (word.first3() == 'תשא') or (word.first3() == 'תשנ')) and (not('תש' in word.getRoot())):
            if(word.getLen() == 5):
                wordNun = Word("","")
                wordNun.equalTo(word)
                wordNun.setText(word.getText()[:-3] + "נ" + word.first3())
                self.hishtaphel(look, wordNun, Check)
                
            hishtaphelW = Word("","")
            hishtaphelW.equalTo(word)
            hishtaphelW.setText(word.getText()[:-3] + word.first())
            if(hishtaphelW.getLen() > 3) and (not(hishtaphelW.hasRoot() and (not(hishtaphelW.getRoot()[:2] == self.Final(hishtaphelW.firstX(4)[:2]))))):
                hishtaphelW.setRoot(self.Final(hishtaphelW.getText()[-4:-1]))
            if(word.isVerbf() == False):
                hishtaphelW.setVerbform(7)
            else:
                hishtaphelW.setVerbform(rareVerbforms[word.getVerbform()])       
                
            return self.future(look, hishtaphelW, Check)
            
        return Word("", "")
           
    def rev(self, text):
        revText = ""
        end = len(text)-1
        for i in range(len(text)):
            revText += text[end-i]
        return str(revText)
            
    def perfect(self, look, word, Check):
        if(word.getLen() < 2) or (word.isPhrase()) or (word.isTense() == True) or (word.getVerbform() in Piel) or (word.isNoun() == True) or (word.getHey1() > 0):
            return Word("","")

        if(word.getLen() > 2):
            if(word.last2() == 'ית') and (not((word.getRoot()[:2] == self.Final(word.last3()[1:])) or (word.getRoot()[:2] == word.last2()))):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[2:]))
                perfW.setVerb()
                
                newRT = False
                if(perfW.getLen() > 2):
                    if(not(perfW.hasRoot())):
                        perfW.setRoot(self.Final(perfW.last3()))
                        newRT = True
                
                if(word.getPrixListEnd() == 'ו'):
                    perfW.setTense(1)
                    perfW.setVavSeq()
                else:
                    perfW.setTense(0)
                    
                perfW.setPerson(0)
                perfW.setGender(3)
                
                if(perfW.last() == 'י'):
                    perfIh = Word("","")
                    perfIh.equalTo(perfW)
                    perfIh.setText('ה' + perfW.getText()[1:])
                    perfIh.addToValue(1)
                    if(perfIh.getLen() > 2):
                        if(newRT == True):
                            perfIh.setRoot(self.Final(perfIh.last3()))
                    self.FindHelper(look, perfIh, self.Dict, Check)
                    self.algorithm(look, perfIh, Check)
                    
                if(perfW.last() == 'ת'):
                    perfth = Word("","")
                    perfth.equalTo(perfW)
                    perfth.setText('ה' + perfW.getText()[1:])
                    if(perfth.getLen() > 2):
                        if(newRT == True):
                            perfth.setRoot(self.Final(perfth.last3()))
                    self.FindHelper(look, perfth, self.Dict, Check)
                    self.irreg(look, perfth, Check)
                 
                hollow = Word("","")
                hollow.equalTo(perfW)
                if(not(perfW.getVerbform() == "Qal")):
                    if(perfW.last() == 'ו') and (not(perfW.getRoot()[:2] == perfW.last2())):
                        perfVh = Word("","")
                        perfVh.equalTo(perfW)
                        perfVh.setText(self.Final(perfW.getText()[1:]))
                        if(perfVh.getLen() > 2):
                            #if(newRT == True):
                            if(not((perfVh.hasRoot()) and (perfVh.getRoot()[1:] == perfVh.last2()))):
                                perfVh.setRoot(self.Final(perfVh.last3()))
                        if((perfW.getVerbform() in Hiphil) or (perfW.getVerbform() in Niphal)):
                            self.FindHelper(look, perfVh, self.Dict, False)
                            self.algorithm(look, perfVh, False)
                        else:
                            self.FindHelper(look, perfVh, self.Dict, Check)
                            self.algorithm(look, perfVh, Check)
                        if(perfVh.getLen() == 2):
                            hollow.equalTo(perfVh)
                                    
                if(hollow.getLen() == 2):
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    if((hollow.getVerbform() in Hophal) or (hollow.getVerbform() in Niphal)):
                        self.FindHelper(look, hollow, self.Dict, False)
                    else:
                        self.FindHelper(look, hollow, self.Dict, Check)
                
                f = self.FindHelper(look, perfW, self.Dict, Check)
                self.algorithm(look, perfW, Check)
            
                fh = False
                if(not (perfW.last() == 'ה')) and (not(word.getRoot()[:2] == word.last2())):
                    perfWh = Word("","")
                    perfWh.equalTo(perfW)
                    perfWh.setText('ה' + self.unFinal(perfW.getText()))
                    perfWh.addToValue(3)
                    if('ה' in perfWh.getSufxList()):
                        perfWh.remSuff();
                    if(perfWh.hasRoot()) and (perfWh.getLen() > 2):
                        if(perfWh.getRoot()[1:] == perfWh.last3()[1:]):
                            perfWh.setRoot(perfWh.last3())
                    fh = self.FindHelper(look, perfWh, self.Dict, Check)
                    self.irreg(look, perfWh, Check)
            
                return perfW
                
            if(word.last2() == 'ונ') and (not((word.getRootLast2() == self.Final(word.last3()[1:])) or (word.getRootLast2() == word.last2()))):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[2:]))
                perfW.setVerb()
                
                newRT = False
                if(perfW.getLen() > 2):
                    if(not(perfW.hasRoot())):
                        perfW.setRoot(self.Final(perfW.last3()))
                        newRT = True
           
                if(word.getPrixListEnd() == 'ו'):
                    perfW.setTense(1)
                    perfW.setVavSeq()
                else:
                    perfW.setTense(0)
                    
                perfW.setPerson(1)
                perfW.setGender(2)
                
                if(perfW.last() == 'י'):
                    perfIh = Word("","")
                    perfIh.equalTo(perfW)
                    perfIh.setText('ה' + perfW.getText()[1:])
                    perfIh.addToValue(1)
                    if(perfIh.getLen() > 2):
                        if(newRT == True):
                            perfIh.setRoot(self.Final(perfIh.last3()))
                    self.FindHelper(look, perfIh, self.Dict, Check)
                    self.algorithm(look, perfIh, Check)
                    
                if(perfW.last() == 'ת'):
                    perfth = Word("","")
                    perfth.equalTo(perfW)
                    perfth.setText('ה' + perfW.getText()[1:])
                    perfth.addToValue(0.5)
                    if(perfth.getLen() > 2):
                        if(newRT == True):
                            perfth.setRoot(self.Final(perfth.last3()))
                    self.FindHelper(look, perfth, self.Dict, Check)
                    self.irreg(look, perfth, Check)

                hollow = Word("","")
                hollow.equalTo(perfW)
                if(not(perfW.getVerbform() == "Qal")):
                    if(perfW.last() == 'ו') and (not(perfW.getRoot()[:2] == perfW.last2())):
                        perfVh = Word("","")
                        perfVh.equalTo(perfW)
                        perfVh.setText(self.Final(perfW.getText()[1:]))
                        if(perfVh.getLen() > 2):
                            if(not((perfVh.hasRoot()) and (perfVh.getRoot()[1:] == perfVh.last2()))):
                                perfVh.setRoot(self.Final(perfVh.last3()))
                        if((perfW.getVerbform() in Hiphil) or (perfW.getVerbform() in Niphal)):
                            self.FindHelper(look, perfVh, self.Dict, False)
                            self.algorithm(look, perfVh, False)
                        else:
                            self.FindHelper(look, perfVh, self.Dict, Check)
                            self.algorithm(look, perfVh, Check)
                        if(perfVh.getLen() == 2):
                            hollow.equalTo(perfVh)

                if(hollow.getLen() == 2):
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    if((hollow.getVerbform() in Hophal) or (hollow.getVerbform() in Niphal)):
                        self.FindHelper(look, hollow, self.Dict, False)
                    else:
                        self.FindHelper(look, hollow, self.Dict, Check)
                
                f = self.FindHelper(look, perfW, self.Dict, Check)
                self.algorithm(look, perfW, Check)
            
                fh = False
                if(not (perfW.last() == 'ה')) and (not(word.getRoot()[:2] == word.last2())):
                    perfWh = Word("","")
                    perfWh.equalTo(perfW)
                    perfWh.setText('ה' + self.unFinal(perfW.getText()))
                    perfWh.addToValue(3)
                    if(perfWh.hasRoot()) and (perfWh.getLen() > 2):
                        if(perfWh.getRoot()[1:] == perfWh.last3()[1:]):
                            perfWh.setRoot(perfWh.last3())
                    fh = self.FindHelper(look, perfWh, self.Dict, Check)
                    self.irreg(look, perfWh, Check)
                
                #return perfW
                
            if(word.getVerbform() == 'Niphal') and (word.last3() == 'ונת') and ((not((word.getRoot()[:2] == self.Final(word.lastX(4)[2:])) or (word.getRoot()[-2:] == word.lastX(4)[2:]) or (word.getRoot() == word.last3())))):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[3:]))
                perfW.setVerb()
                
                newRT = False
                if(perfW.getLen() > 2):
                    if(not(perfW.hasRoot())):
                        perfW.setRoot(self.Final(perfW.last3()))
                        newRT = True
                    
                if(word.getPrixListEnd() == 'ו'):
                    perfW.setTense(1)
                    perfW.setVavSeq()
                else:
                    perfW.setTense(0)
                    
                perfW.setPerson(1)
                perfW.setGender(2)
                
                if(perfW.last() == 'י'):
                    perfIh = Word("","")
                    perfIh.equalTo(perfW)
                    perfIh.setText('ה' + perfW.getText()[1:])
                    perfIh.addToValue(1)
                    if(perfIh.getLen() > 2):
                        if(newRT == True):
                            perfIh.setRoot(self.Final(perfIh.last3()))
                    self.FindHelper(look, perfIh, self.Dict, Check)
                    self.algorithm(look, perfIh, Check)
                    
                if(perfW.last() == 'ת'):
                    perfth = Word("","")
                    perfth.equalTo(perfW)
                    perfth.setText('ה' + perfW.getText()[1:])
                    perfth.addToValue(0.5)
                    if(perfth.getLen() > 2):
                        if(newRT == True):
                            perfth.setRoot(self.Final(perfth.last3()))
                    self.FindHelper(look, perfth, self.Dict, Check)
                    self.irreg(look, perfth, Check)
                
                hollow = Word("","")
                hollow.equalTo(perfW)
                if(perfW.getLen() == 2):
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    if((hollow.getVerbform() in Hiphil) or (hollow.getVerbform() in Niphal)):
                        self.FindHelper(look, hollow, self.Dict, False)
                    else:
                        self.FindHelper(look, hollow, self.Dict, Check)
   
                f = self.FindHelper(look, perfW, self.Dict, Check)
                self.algorithm(look, perfW, Check)
            
                fh = False
                if(not (perfW.last() == 'ה')) and (not((word.getRoot()[:2] == self.Final(word.last3()[1:])) or (word.getRoot()[-2:] == word.last3()[1:]))):
                    perfWh = Word("","")
                    perfWh.equalTo(perfW)
                    perfWh.setText('ה' + self.unFinal(perfW.getText()))
                    perfWh.addToValue(3)
                    if(perfWh.hasRoot()) and (perfWh.getLen() > 2):
                        if(perfWh.getRoot()[1:] == perfWh.last3()[1:]):
                            perfWh.setRoot(perfWh.last3())
                    fh = self.FindHelper(look, perfWh, self.Dict, Check)
                    self.irreg(look, perfWh, Check)
                
                #return perfW
                
            if(word.last2() == 'םת') and (not((word.getRoot()[:2] == self.Final(word.last3()[1:])) or (word.getRoot()[:2] == word.last2()))):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[2:]))
                perfW.setVerb()
                
                newRT = False
                if(perfW.getLen() > 2):
                   if(not(perfW.hasRoot())):
                       perfW.setRoot(self.Final(perfW.last3()))
                       newRT = True
                
                if(word.getPrixListEnd() == 'ו'):
                    perfW.setTense(1)
                    perfW.setVavSeq()
                else:
                    perfW.setTense(0)
                    
                perfW.setPerson(3)
                perfW.setGender(0)
                
                if(perfW.last() == 'י'):
                    perfIh = Word("","")
                    perfIh.equalTo(perfW)
                    perfIh.setText('ה' + perfW.getText()[1:])
                    perfIh.addToValue(1)
                    if(perfIh.getLen() > 2):
                        if(newRT == True):
                            perfIh.setRoot(self.Final(perfIh.last3()))
                    self.FindHelper(look, perfIh, self.Dict, Check)
                    self.algorithm(look, perfIh, Check)
                    
                if(perfW.last() == 'ת'):
                    perfth = Word("","")
                    perfth.equalTo(perfW)
                    perfth.setText('ה' + perfW.getText()[1:])
                    perfth.addToValue(0.5)
                    if(perfth.getLen() > 2):
                        if(newRT == True):
                            perfth.setRoot(self.Final(perfth.last3()))
                    self.FindHelper(look, perfth, self.Dict, Check)
                    self.irreg(look, perfth, Check)
                
                hollow = Word("","")
                hollow.equalTo(perfW)
                if(not(perfW.getVerbform() == "Qal")):
                    if(perfW.last() == 'ו') and (not(perfW.getRoot()[:2] == perfW.last2())):
                        perfVh = Word("","")
                        perfVh.equalTo(perfW)
                        perfVh.setText(self.Final(perfW.getText()[1:]))
                        if(perfVh.getLen() > 2):
                            if(not((perfVh.hasRoot()) and (perfVh.getRoot()[1:] == perfVh.last2()))):
                                perfVh.setRoot(self.Final(perfVh.last3()))
                        if((perfW.getVerbform() in Hiphil) or (perfW.getVerbform() in Niphal)):
                            self.FindHelper(look, perfVh, self.Dict, False)
                            self.algorithm(look, perfVh, False)
                        else:
                            self.FindHelper(look, perfVh, self.Dict, Check)
                            self.algorithm(look, perfVh, Check)
                        if(perfVh.getLen() == 2):
                            hollow.equalTo(perfVh)
                
                if(hollow.getLen() == 2):
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    if((hollow.getVerbform() in Hophal) or (hollow.getVerbform() in Niphal)):
                        self.FindHelper(look, hollow, self.Dict, False)
                    else:
                        self.FindHelper(look, hollow, self.Dict, Check)
                
                f = self.FindHelper(look, perfW, self.Dict, Check)
                self.algorithm(look, perfW, Check)
            
                fh = False
                if(not (perfW.last() == 'ה')) and (not(word.getRoot()[:2] == word.last2())):
                    perfWh = Word("","")
                    perfWh.equalTo(perfW)
                    perfWh.setText('ה' + self.unFinal(perfW.getText()))
                    perfWh.addToValue(3)
                    if(perfWh.hasRoot()) and (perfWh.getLen() > 2):
                        if(perfWh.getRoot()[1:] == perfWh.last3()[1:]):
                            perfWh.setRoot(perfWh.last3())
                    fh = self.FindHelper(look, perfWh, self.Dict, Check)
                    self.irreg(look, perfWh, Check)
            
                return perfW 
                
            if(word.last2() == 'ןת') and (not((word.getRoot()[:2] == self.Final(word.last3()[1:])) or (word.getRoot()[-2:] == word.last3()[1:]))):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[2:]))
                perfW.setVerb()
                
                newRT = False
                if(perfW.getLen() > 2):
                    if(not(perfW.hasRoot())):
                        perfW.setRoot(self.Final(perfW.last3()))
                        newRT = True
                
                if(word.getPrixListEnd() == 'ו'):
                    perfW.setTense(1)
                    perfW.setVavSeq()
                else:
                    perfW.setTense(0)
                    
                perfW.setPerson(3)
                perfW.setGender(1)
                
                if(perfW.last() == 'י'):
                    perfIh = Word("","")
                    perfIh.equalTo(perfW)
                    perfIh.setText('ה' + perfW.getText()[1:])
                    perfIh.addToValue(1)
                    if(perfIh.getLen() > 2):
                        if(newRT == True):
                            perfIh.setRoot(self.Final(perfIh.last3()))
                    self.FindHelper(look, perfIh, self.Dict, Check)
                    self.algorithm(look, perfIh, Check)
                            
                if(perfW.last() == 'ת'):
                    perfth = Word("","")
                    perfth.equalTo(perfW)
                    perfth.setText('ה' + perfW.getText()[1:])
                    perfth.addToValue(0.5)
                    if(perfth.getLen() > 2):
                        if(newRT == True):
                            perfth.setRoot(self.Final(perfth.last3()))
                    self.FindHelper(look, perfth, self.Dict, Check)
                    self.irreg(look, perfth, Check)
                
                hollow = Word("","")
                hollow.equalTo(perfW)
                if(not(perfW.getVerbform() == "Qal")):
                    if(perfW.last() == 'ו') and (not(perfW.getRoot()[:2] == perfW.last2())):
                        perfVh = Word("","")
                        perfVh.equalTo(perfW)
                        perfVh.setText(self.Final(perfW.getText()[1:]))
                        if(perfVh.getLen() > 2):
                            if(not((perfVh.hasRoot()) and (perfVh.getRoot()[1:] == perfVh.last2()))):
                                perfVh.setRoot(self.Final(perfVh.last3()))
                        if((perfW.getVerbform() in Hiphil) or (perfW.getVerbform() in Niphal)):
                            self.FindHelper(look, perfVh, self.Dict, False)
                            self.algorithm(look, perfVh, False)
                        else:
                            self.FindHelper(look, perfVh, self.Dict, Check)
                            self.algorithm(look, perfVh, Check)
                        if(perfVh.getLen() == 2):
                            hollow.equalTo(perfVh)
                
                if(hollow.getLen() == 2):
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    if((hollow.getVerbform() in Hophal) or (hollow.getVerbform() in Niphal)):
                        self.FindHelper(look, hollow, self.Dict, False)
                    else:
                        self.FindHelper(look, hollow, self.Dict, Check)
                
                f = self.FindHelper(look, perfW, self.Dict, Check)
                self.algorithm(look, perfW, Check)
            
                fh = False
                if(not (perfW.last() == 'ה')) and (not(word.getRoot()[:2] == word.last2())):
                    perfWh = Word("","")
                    perfWh.equalTo(perfW)
                    perfWh.setText('ה' + self.unFinal(perfW.getText()))
                    perfWh.addToValue(3)
                    if(perfWh.hasRoot()) and (perfWh.getLen() > 2):
                        if(perfWh.getRoot()[1:] == perfWh.last3()[1:]):
                            perfWh.setRoot(perfWh.last3())
                    fh = self.FindHelper(look, perfWh, self.Dict, Check)
                    self.irreg(look, perfWh, Check)
            
                return perfW 
        
        if(word.getLen() > 2):
            if(word.last() == 'ו') and (not(word.getRoot()[:2] == word.last2())):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[1:]))
                perfW.setVerb()
                
                newRT = False
                if(perfW.getLen() > 2):
                    if(not(perfW.hasRoot())):
                        perfW.setRoot(self.Final(perfW.last3()))
                        newRT = True
                
                if(word.getPrixListEnd() == 'ו'):
                    perfW.setTense(1)
                    perfW.setVavSeq()
                else:
                    perfW.setTense(0)
                    
                perfW.setPerson(5)
                perfW.setGender(2)
                
                if(perfW.last() == 'י'):
                    perfIh = Word("","")
                    perfIh.equalTo(perfW)
                    perfIh.setText('ה' + perfW.getText()[1:])
                    perfIh.addToValue(1)
                    if(perfIh.getLen() > 2):
                        if(newRT == True):
                            perfIh.setRoot(self.Final(perfIh.last3()))
                    self.FindHelper(look, perfIh, self.Dict, Check)
                    self.algorithm(look, perfIh, Check)
                            
                if(perfW.last() == 'ת'):
                    perfth = Word("","")
                    perfth.equalTo(perfW)
                    perfth.setText('ה' + perfW.getText()[1:])
                    perfth.addToValue(0.5)
                    if(perfth.getLen() > 2):
                        if(newRT == True):
                            perfth.setRoot(self.Final(perfth.last3()))
                    self.FindHelper(look, perfth, self.Dict, Check)
                    self.irreg(look, perfth, Check)
                
                hollow = Word("","")
                hollow.equalTo(perfW)
                if(hollow.getLen() == 2):
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    if((hollow.getVerbform() in Hophal) or (hollow.getVerbform() in Niphal)):
                        self.FindHelper(look, hollow, self.Dict, False)
                    else:
                        self.FindHelper(look, hollow, self.Dict, Check)
                
                f = self.FindHelper(look, perfW, self.Dict, Check)
                self.algorithm(look, perfW, Check)
            
                fh = False
                if(not (perfW.last() == 'ה')):
                    perfWh = Word("","")
                    perfWh.equalTo(perfW)
                    perfWh.setText('ה' + self.unFinal(perfW.getText()))
                    perfWh.addToValue(3)
                    if(perfWh.hasRoot()) and (perfWh.getLen() > 2):
                        if(perfWh.getRoot()[1:] == perfWh.last3()[1:]):
                            perfWh.setRoot(perfWh.last3())
                    fh = self.FindHelper(look, perfWh, self.Dict, Check)
                    self.irreg(look, perfWh, Check)
                    
                return perfW
                
            if(word.last() == 'ת') and (not(word.getRoot()[:2] == word.last2())):
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[1:]))
                perfW.setVerb()
                
                newRT = False
                if(perfW.getLen() > 2):
                    if(not(perfW.hasRoot())):
                        newRT = True
                        perfW.setRoot(self.Final(perfW.last3()))
                
                if(word.getPrixListEnd() == 'ו'):
                    perfW.setTense(1)
                    perfW.setVavSeq()
                else:
                    perfW.setTense(0)
                    
                perfW.setPerson(2)
                perfW.setGender(2)
                
                if(perfW.last() == 'י'):
                    perfIh = Word("","")
                    perfIh.equalTo(perfW)
                    perfIh.setText('ה' + perfW.getText()[1:])
                    perfIh.addToValue(1)
                    if(perfIh.getLen() > 2):
                        if(newRT == True):
                            perfIh.setRoot(self.Final(perfIh.last3()))
                    self.FindHelper(look, perfIh, self.Dict, Check)
                    self.algorithm(look, perfIh, Check)
                 
                if(perfW.last() == 'ת'):
                    perfth = Word("","")
                    perfth.equalTo(perfW)
                    perfth.setText('ה' + perfW.getText()[1:])
                    perfth.addToValue(0.5)
                    if(perfth.getLen() > 2):
                        if(newRT == True):
                            perfth.setRoot(self.Final(perfth.last3()))
                    self.FindHelper(look, perfth, self.Dict, Check)
                    self.irreg(look, perfth, Check)
                
                hollow = Word("","")
                hollow.equalTo(perfW)
                if(not(perfW.getVerbform() == "Qal")):
                    if(perfW.last() == 'ו') and (not(perfW.getRoot()[:2] == perfW.last2())):
                        perfVh = Word("","")
                        perfVh.equalTo(perfW)
                        perfVh.setText(self.Final(perfW.getText()[1:]))
                        if(perfVh.getLen() > 2):
                            if(not((perfVh.hasRoot()) and (perfVh.getRoot()[1:] == perfVh.last2()))):
                                perfVh.setRoot(self.Final(perfVh.last3()))
                        if((perfW.getVerbform() in Hiphil) or (perfW.getVerbform() in Niphal)):
                            self.FindHelper(look, perfVh, self.Dict, False)
                            self.algorithm(look, perfVh, False)
                        else:
                            self.FindHelper(look, perfVh, self.Dict, Check)
                            self.algorithm(look, perfVh, Check)
                        if(perfVh.getLen() == 2):
                            hollow.equalTo(perfVh)
                
                if(hollow.getLen() == 2):
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    if((hollow.getVerbform() in Hophal) or (hollow.getVerbform() in Niphal)):
                        self.FindHelper(look, hollow, self.Dict, False)
                    else:
                        self.FindHelper(look, hollow, self.Dict, Check)
                
                f = self.FindHelper(look, perfW, self.Dict, Check)
                self.algorithm(look, perfW, Check)
            
                fh = False
                if(not (perfW.last() == 'ה')):
                    perfWh = Word("","")
                    perfWh.equalTo(perfW)
                    perfWh.setText('ה' + self.unFinal(perfW.getText()))
                    perfWh.addToValue(3)
                    if(perfWh.hasRoot()) and (perfWh.getLen() > 2):
                        if(perfWh.getRoot()[1:] == perfWh.last3()[1:]):
                            perfWh.setRoot(perfWh.last3())
                    fh = self.FindHelper(look, perfWh, self.Dict, Check)
                    self.algorithm(look, perfWh, Check)
                  
                if(word.getSuffix() == False):
                    return perfW
                
            #may have to be changed later upon further knowledge    
            if(((word.last() == 'ה') and (self.CurrentWord.last() == 'ה')) or ((word.last() == 'ת')and(word.getSuffix() == True))) and (not(word.getRoot()[:2] == word.last2())):
                f = False
                newRT = False 
                perfW = Word("","")
                perfW.equalTo(word)
                perfW.setText(self.Final(word.getText()[1:]))
                perfW.setVerb()
                if(perfW.getLen() > 2):
                    if(not(perfW.hasRoot())):
                        perfW.setRoot(self.Final(perfW.last3()))
                        newRT = True
                
                if(word.getPrixListEnd() == 'ו'):
                    perfW.setTense(1)
                    perfW.setVavSeq()
                else:
                    perfW.setTense(0)
                    
                perfW.setPerson(4)
                perfW.setGender(1)
                
                if(perfW.last() == 'י'):
                    perfIh = Word("","")
                    perfIh.equalTo(perfW)
                    perfIh.setText('ה' + perfW.getText()[1:])
                    perfIh.addToValue(1)
                    if(perfIh.getLen() > 2):
                        if(newRT == True):
                            perfIh.setRoot(self.Final(perfIh.last3()))
                    self.FindHelper(look, perfIh, self.Dict, Check)
                    self.algorithm(look, perfIh, Check)
                        
                hollow = Word("","")
                hollow.equalTo(perfW)
                if(not(perfW.getVerbform() == "Qal")):
                    if(perfW.last() == 'ו') and (not(perfW.getRoot()[:2] == perfW.last2())):
                        perfVh = Word("","")
                        perfVh.equalTo(perfW)
                        perfVh.setText(self.Final(perfW.getText()[1:]))
                        if(perfVh.getLen() > 2):
                            if(not((perfVh.hasRoot()) and (perfVh.getRoot()[1:] == perfVh.last2()))):
                                perfVh.setRoot(self.Final(perfVh.last3()))
                        if((perfW.getVerbform() in Hiphil) or (perfW.getVerbform() in Niphal)):
                            self.FindHelper(look, perfVh, self.Dict, False)
                            self.algorithm(look, perfVh, False)
                        else:
                            self.FindHelper(look, perfVh, self.Dict, Check)
                            self.algorithm(look, perfVh, Check)
                        if(perfVh.getLen() == 2):
                            hollow.equalTo(perfVh)
                
                if(hollow.getLen() == 2):
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    if((hollow.getVerbform() in Hophal) or (hollow.getVerbform() in Niphal)):
                        self.FindHelper(look, hollow, self.Dict, False)
                    else:
                        self.FindHelper(look, hollow, self.Dict, Check)
                         
                f = self.FindHelper(look, perfW, self.Dict, Check)
                self.algorithm(look, perfW, Check)

                fh = False
                if(perfW.last() == 'ת') and (not(perfW.getRoot()[:2] == perfW.last2())):
                    irreg = Word("","")
                    irreg.equalTo(perfW)
                    irreg.setText(self.Final(perfW.getText()[1:]))
                    self.irreg(look, irreg, Check)
                    
                if(perfW.last() == 'ת'):
                    perfth = Word("","")
                    perfth.equalTo(perfW)
                    perfth.setText('ה' + perfW.getText()[1:])
                    perfth.addToValue(0.5)
                    if(perfth.getLen() > 2):
                        if(newRT == True):
                            perfth.setRoot(self.Final(perfth.last3()))
                    self.FindHelper(look, perfth, self.Dict, Check)
                    self.irreg(look, perfth, Check)
                    
                    fh = False
                    if(not ('ה' in word.getSufxList())):
                        perfWh = Word("","")
                        perfWh.equalTo(perfW)
                        perfWh.setText('ה' + perfW.getText()[1:])
                        perfWh.addToValue(3)
                        if(perfWh.hasRoot()) and (perfWh.getLen() > 2):
                            if(perfWh.getRoot()[1:] == perfWh.last3()[1:]):
                                perfWh.setRoot(perfWh.last3())
                        fh = self.FindHelper(look, perfWh, self.Dict, Check)
                        self.algorithm(look, perfWh, Check)
                
                    return perfW
                    
        if(word.getLen() == 3) and (word.second() == 'י'):
            hollow = Word("","")
            hollow.equalTo(word)
            if(word.getPrixListEnd() == 'ו'):
                hollow.setTense(1)
                hollow.setVavSeq()
            else:
                hollow.setTense(0)
            hollow.setPerson(4)
            hollow.setVerb()
            hollow.setGender(0)
            self.FindHelper(look, hollow, self.Dict, False)
            self.piel(look, hollow, Check)
            
        if(word.getLen() == 4) and (word.second() == 'ו') and (word.third() == 'י'):
            hollow = Word("","")
            hollow.equalTo(word)
            if(word.getPrixListEnd() == 'ו'):
                hollow.setTense(1)
                hollow.setVavSeq()
            else:
                hollow.setTense(0)
            hollow.setPerson(4)
            hollow.setVerb()
            hollow.setGender(0)
            self.FindHelper(look, hollow, self.Dict, False)
            self.pual(look, hollow, Check)
            
        if(word.getLen() == 2):
            if(not(word.getVerbform() in Pual)):
                hollow = Word("","")
                hollow.equalTo(word)
                hollow.setText(word.last() + 'ו' + word.first())
                if(word.getPrixListEnd() == 'ו'):
                    hollow.setTense(1)
                    hollow.setVavSeq()
                else:
                    hollow.setTense(0)
                hollow.setVerb()
                hollow.setPerson(4)
                hollow.setGender(0)
                hollow.setRoot(hollow.getText())
                if((hollow.getVerbform() in Hophal) or (hollow.getVerbform() in Niphal)):
                    self.FindHelper(look, hollow, self.Dict, False)
                else:
                    self.FindHelper(look, hollow, self.Dict, Check)
                    
                self.irreg(look, word, True)
        return Word("", "")
                      
    def future(self, look, word, Check):
        if(word.getLen() < 2) or ((word.getLen() < 3) and(not('ו' in word.getPrixList()))) or (word.isPhrase()) or (word.isTense() == True) or (word.getVerbform() in Piel) or (word.isNoun() == True) or (word.getVerbform() in Niphal) or (word.getVerbform() in Pual) or (word.getVerbform() in Piel) or (word.getHey1() > 0):
            return Word("","")

        if(word.getLen() > 3):
            if((word.first() == 'ת')and(word.last2() == 'הנ')) and (self.imperRules(word, 'ת') == True) and (not(word.getRootFirst2() == word.first2())) and (not((word.getRootLast2() == self.Final(word.last3()[1:])) or (word.getRootLast2() == word.last2()))):
                holl = True
                full2 = False
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(self.Final(word.getText()[2:-1]))
                if(futurW.first() == 'ו'):
                    futurW.setText(futurW.getText()[:-1] + 'י')
                if(futurW.getLen() > 2):
                    if(not(futurW.hasRoot() and (not(futurW.getRootLast2() == self.Final(futurW.first3()[:2]))))):
                        futurW.setRoot(self.Final(futurW.first3()))
                    
                futurW.setVerb()
                
                if(word.getPrixListEnd() == 'ו') and (futurW.first() == 'ו'):
                    if(futurW.getLen() > 6):
                        futurW.setText(futurW.getText()[:-1])
                        full2 = True
                    futurW.setTense(0)
                    futurW.setVavSeq()
                else:
                    futurW.setTense(1)
                futurW.setPerson(3)
                futurW.setGender(1)
                
                TfuturW = Word("","")
                if(futurW.getLen() > 2):
                    if(not((futurW.hasRoot()) and (not((futurW.getRootLast2() == self.Final(futurW.last3()[1:])) or (futurW.getRootLast2() == futurW.last2()))))):
                        if((futurW.nextToLast() == 'ו') and (not((futurW.getVerbform() == 'Qal') and (not(futurW.third() == 'ו'))))) and (self.num_of_p_roots(futurW.getText()[:-4]) == 0) and ((futurW.isVerbf() == False) or (futurW.getVerbform() == 'Qal')):
                            futurW.setText(futurW.last() + futurW.getText()[2:])
                            holl = False
                            if(futurW.getLen() > 2):
                                futurW.setRoot(futurW.last3())
                   
                    if(word.second() == 'ו'):
                        TfuturW.equalTo(futurW)
                        TfuturW.setText(word.getText()[2:-2] + 'ת')
                        TfuturW.addToValue(1)
                        if(holl == False):
                            TfuturW.setText(TfuturW.last() + TfuturW.getText()[2:])
                        if(TfuturW.getLen() > 2):
                            TfuturW.setRoot(TfuturW.last3())
                        if(full2 == False) and (word.getPrixListEnd() == 'ו'):
                            futurW.setText(futurW.getText()[:-1])
                            if(futurW.getLen() > 2):
                                futurW.setRoot(futurW.first3())
                            
                        if(TfuturW.last() == 'ת'):
                            TfuturWh = Word("","")
                            TfuturWh.equalTo(TfuturW)
                            TfuturWh.setText('ה' + TfuturW.getText()[1:])
                            TfuturWh.addToValue(-1)
                            
                            if(TfuturWh.hasRoot()) and (TfuturWh.getLen() > 2):
                                if(TfuturWh.getRoot()[1:] == TfuturWh.last3()[1:]):
                                    TfuturWh.setRoot(TfuturWh.last3())
                                    
                            self.FindHelper(look, TfuturWh, self.Dict, Check)
                            self.irreg(look, TfuturWh, Check)
                                    
                        self.FindHelper(look, TfuturW, self.Dict, Check)
                        self.algorithm(look, TfuturW, Check)
                        
                    hollow = Word("","")
                    hollow.equalTo(futurW)
                    if(not(futurW.getVerbform() == "Qal")):
                        if(futurW.last() == 'י'):
                            futurWI = Word("","")
                            futurWI.equalTo(futurW)
                            futurWI.setText(self.Final(futurW.getText()[1:]))
                            futurWI.addToValue(1)
                            if(futurWI.getLen() > 2):
                                if(not((futurWI) and (futurWI.getRoot()[1:] == futurWI.last2()))):
                                    futurWI.setRoot(self.Final(futurWI.last3()))
                            self.FindHelper(look, futurWI, self.Dict, Check)
                            self.algorithm(look, futurWI, Check)
                            if(futurWI.getLen() == 2):
                                hollow.equalTo(futurWI)
                                            
                        if(futurW.getLen() == 2) and (holl == True):
                            hollow.setText(hollow.last() + 'ו' + hollow.first())
                            hollow.addToValue(1)
                            hollow.setRoot(hollow.getText())
                            self.FindHelper(look, hollow, self.Dict, Check)
                            
                        if(futurW.getLen() > 2):
                            futurW.setRoot(futurW.last3())
                    f = self.FindHelper(look, futurW, self.Dict, Check)
                    self.algorithm(look, futurW, Check)
                    
                    if(futurW.last() == 'ת'):
                        futurWh2 = Word("","")
                        futurWh2.equalTo(futurW)
                        futurWh2.setText('ה' + futurW.getText()[1:])
                        futurWh2.addToValue(-1)
                    
                        if(futurWh2.hasRoot()) and (futurWh2.getLen() > 2):
                            if(futurWh2.getRoot()[1:] == futurWh2.last3()[1:]):
                                futurWh2.setRoot(futurWh2.last3())
                    
                        self.FindHelper(look, futurWh2, self.Dict, Check)
                        self.irreg(look, futurWh2, Check)
                        
                    fh = False
                    if(not (futurW.last() == 'ה')) and (not ('ה' in word.getSufxList())):
                        futurWh = Word("","")
                        futurWh.equalTo(futurW)
                        futurWh.setText('ה' + self.unFinal(futurW.getText()))
                        futurWh.addToValue(3)
                        if(futurWh.hasRoot()) and (futurWh.getLen() > 2):
                            if(futurWh.getRoot()[1:] == futurWh.last3()[1:]):
                                futurWh.setRoot(futurWh.last3())
                        fh = self.FindHelper(look, futurWh, self.Dict, Check)
                        self.irreg(look, futurWh, Check)
                elif 'ו' in word.getPrixList():
                    self.irreg(look, futurW, Check)
                
                if(not('ונ' in word.getSufxList())) and (not('ןכ' in word.getSufxList())) and (not('ןה' in word.getSufxList())) and (not('ן' in word.getSufxList())) and (not('ינ' in word.getSufxList())) and (not('הנ' in word.getSufxList())):
                    imperwNun = Word("","")
                    imperwNun.equalTo(futurW)
                    imperwNun.setText('ן' + self.unFinal(futurW.getText()))
                    imperwNun.addToValue(5)
                    self.irreg(look, imperwNun, Check)
                
                futurW2 = Word("","")
                futurW2.equalTo(word)
                futurW2.setText(futurW.getText())
                futurW2.setRoot(futurW.getRoot())
                futurW2.setVerb()
                 
                if(futurW.isVavSeq() == True):
                    futurW2.setTense(0)
                    futurW2.setVavSeq()
                else:
                    futurW2.setTense(1)
                futurW2.setPerson(5)
                futurW2.setGender(1)
                
                if(futurW2.getLen() > 1): 
                    f2 = self.FindHelper(look, futurW2, self.Dict, Check)
                    self.algorithm(look, futurW2, Check)
                    
                    if(not(TfuturW == Word("",""))):
                        TfuturW2 = Word("","")
                        TfuturW2.equalTo(futurW2)
                        TfuturW2.setText(TfuturW.getText())
                        TfuturW2.setRoot(TfuturW.getRoot())
                        self.FindHelper(look, TfuturW2, self.Dict, False)
                        self.algorithm(look, TfuturW2, False)
                        
                        if(TfuturW.last() == 'ת'):
                            TfuturWh = Word("","")
                            TfuturWh.equalTo(TfuturW2)
                            TfuturWh.setText('ה' + TfuturW.getText()[1:])
                            TfuturWh.addToValue(-1)
                            
                            if(TfuturWh.hasRoot()) and (TfuturWh.getLen() > 2):
                                if(TfuturWh.getRoot()[1:] == TfuturWh.last3()[1:]):
                                    TfuturWh.setRoot(TfuturWh.last3())
                                    
                            self.FindHelper(look, TfuturWh, self.Dict, Check)
                            self.irreg(look, TfuturWh, Check)
                        
                    if(futurW2.last() == 'ת'):
                        futurWh2 = Word("","")
                        futurWh2.equalTo(futurW2)
                        futurWh2.setText('ה' + futurW2.getText()[1:])
                        futurWh2.addToValue(-1)
                    
                        if(futurWh2.hasRoot()) and (futurWh2.getLen() > 2):
                            if(futurWh2.getRoot()[1:] == futurWh2.last3()[1:]):
                                futurWh2.setRoot(futurWh2.last3())
                        
                        self.FindHelper(look, futurWh2, self.Dict, Check)
                        self.irreg(look, futurWh2, Check)
                        
                    if(not(futurW2.getVerbform() == "Qal")):
                        if(futurW2.last() == 'י'):
                            futurWI2 = Word("","")
                            futurWI2.equalTo(futurW2)
                            futurWI2.setText(self.Final(futurW2.getText()[1:]))
                            futurWI2.addToValue(1)
                            if(futurWI2.getLen() > 2):
                                if(not((futurWI2) and (futurWI2.getRoot()[1:] == futurWI2.last2()))):
                                    futurWI2.setRoot(self.Final(futurWI2.last3()))
                            self.FindHelper(look, futurWI2, self.Dict, Check)
                            self.algorithm(look, futurWI2)
                            if(futurWI2.getLen() == 2):
                                futurW2.equalTo(futurWI2)  
                    f2h = False
                    if(not (futurW2.last() == 'ה')) and (not ('ה' in word.getSufxList())):
                        futurW2h = Word("","")
                        futurW2h.equalTo(futurW2)
                        futurW2h.setText('ה' + self.unFinal(futurW2.getText()))
                        futurW2h.addToValue(3)
                        if(futurW2h.hasRoot()) and (futurWh.getLen() > 2):
                            if(futurW2h.getRoot()[1:] == futurW2h.last3()[1:]):
                                futurW2h.setRoot(futurW2h.last3())
                        f2h = self.FindHelper(look, futurW2h, self.Dict, Check)
                        self.irreg(look, futurW2h, Check)
                    return futurW2
                elif 'ו' in word.getPrixList():
                    return self.irreg(look, futurW2, Check)
                    
                if(not('ונ' in word.getSufxList())) and (not('ןכ' in word.getSufxList())) and (not('ןה' in word.getSufxList())) and (not('ן' in word.getSufxList())) and (not('ינ' in word.getSufxList())) and (not('הנ' in word.getSufxList())):
                    imperwNun = Word("","")
                    imperwNun.equalTo(futurW2)
                    imperwNun.setText('ן' + self.unFinal(futurW2.getText()))
                    imperwNun.addToValue(5)
                    self.irreg(look, imperwNun, Check)
                    
            if(word.getPrixListEnd() == 'ו') and(((word.first2() == 'וי') and (word.last() == 'ו') and (self.imperRules(word, 'וי') == True)) or ((word.first2() == 'יי') and (word.last() == 'ו') and (self.imperRules(word, 'יי') == True))) and (not(word.getRoot()[-2:] == word.first3()[:-1]) or (word.getRoot()[:2] == self.Final(word.first3()[:-1]))) and (not(word.getRoot()[:2] == word.last2())):
                futurW = Word("","")                                                                                                                                                                                                                                                                                      
                futurW.equalTo(word)
                futurW.setText(word.getText()[1:-2])
                futurW.setVerb()
                 
                futurW.setTense(0)
                futurW.setPerson(5)
                futurW.setGender(0)
                futurW.setVavSeq()
                holl2 = True
                if(futurW.getLen() > 2):
                    if(not((futurW.hasRoot()) and (not((futurW.getRootLast2() == self.Final(futurW.last3()[1:])) or (futurW.getRootLast2() == futurW.last2()))))):
                        if((futurW.nextToLast() == 'ו') and (not((futurW.getVerbform() == 'Qal') and (not(futurW.third() == 'ו'))))) and (self.num_of_p_roots(futurW.getText()[:-4]) == 0) and ((futurW.isVerbf() == False) or (futurW.getVerbform() == 'Qal')):
                            futurW.setText(futurW.last() + futurW.getText()[2:])
                            holl2 = False
                            if(futurW.getLen() > 2):
                                futurW.setRoot(futurW.last3())
                    if(futurW.getLen() == 2) and (holl2 == True):
                        hollow = Word("","")
                        hollow.equalTo(futurW)
                        hollow.setText(hollow.last() + 'ו' + hollow.first())
                        hollow.addToValue(1)
                        hollow.setRoot(hollow.getText())
                        self.FindHelper(look, hollow, self.Dict, Check)
                    if(futurW.getLen() > 2):
                        futurW.setRoot(futurW.last3())
                    f = self.FindHelper(look, futurW, self.Dict, Check)
                    self.algorithm(look, futurW, Check)
                        
                    fh = False
                    if(not (futurW.last() == 'ה')) and (not ('ה' in word.getSufxList())):
                        futurWh = Word("","")
                        futurWh.equalTo(futurW)
                        futurWh.setText('ה' + self.unFinal(futurW.getText()))
                        futurWh.addToValue(3)
                        if(futurWh.hasRoot()) and (futurWh.getLen() > 2):
                            if(futurWh.getRoot()[1:] == futurWh.last3()[1:]):
                                futurWh.setRoot(futurWh.last3())
                        fh = self.FindHelper(look, futurWh, self.Dict, Check)
                        self.irreg(look, futurWh, Check)
                    if (word.first2() == 'וי'):
                        return futurW
                        
                self.irreg(look, futurW, Check)
                if (word.first2() == 'וי'):
                    return futurW
               
        if(word.getLen() > 2):
            if ('ו' in word.getPrixList()) and ((word.first2() == 'וי') and (self.imperRules(word, 'וי') == True) or (word.getPrixListEnd() == 'ו')and(word.first2() == 'יי') and (self.imperRules(word, 'יי') == True)) and (not(word.getRoot()[-2:] == word.first3()[:-1]) or (word.getRoot()[:2] == self.Final(word.first3()[:-1]))):
                holl = True
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(word.getText()[:-2])
                futurW.setVerb()
                 
                futurW.setTense(0)
                futurW.setPerson(4)
                futurW.setGender(0)
                futurW.setVavSeq()
                
                if(futurW.getLen() > 2):
                    if((futurW.nextToLast() == 'ו') and (not((futurW.getVerbform() == 'Qal') and (not(futurW.third() == 'ו'))))) and (self.num_of_p_roots(futurW.getText()[:-4]) == 0) and ((futurW.isVerbf() == False) or (futurW.getVerbform() == 'Qal')) and (not((futurW.hasRoot()) and (not((futurW.getRootLast2() == self.Final(futurW.last3()[1:])) or (futurW.getRootLast2() == futurW.last2()))))):
                        futurW.setText(futurW.last() + futurW.getText()[2:])
                        if(futurW.getLen() > 2):
                            futurW.setRoot(futurW.last3())
                    elif(futurW.getLen() == 2):
                        hollow = Word("","")
                        hollow.equalTo(futurW)
                        hollow.setText(hollow.last() + 'ו' + hollow.first())
                        hollow.setRoot(hollow.getText())
                        hollow.addToValue(1)
                        self.FindHelper(look, hollow, self.Dict, Check)
                    if(futurW.getLen() > 2)and(word.getSuffix() == True):
                        futurW.setRoot(futurW.last3())
                    
                    f = self.FindHelper(look, futurW, self.Dict, Check)
                    self.algorithm(look, futurW, Check)
                    fh = False
                    if(not ('ה' in word.getSufxList())):
                        futurWh = Word("","")
                        futurWh.equalTo(futurW)
                        futurWh.setText('ה' + self.unFinal(futurW.getText()))
                        futurWh.addToValue(3)
                        fh = self.FindHelper(look, futurWh, self.Dict, Check)
                        self.irreg(look, futurWh, Check)
                    if (word.first2() == 'וי'):
                        return futurW
                self.irreg(look, futurW, Check)
                if (word.first2() == 'וי'):
                    return futurW
              
            if((word.first() == 'ת')and(word.last() == 'ו') and (self.imperRules(word, 'ת') == True)) and (not(word.getRoot()[-2:] == word.first2())) and (not(word.getRoot()[:2] == word.last2())):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(self.Final(word.getText()[1:-1]))
                futurW.setVerb()
                full = False
                full2 = False
            
                if(word.getPrixListEnd() == 'ו'):
                    if(futurW.first() == 'ו')and(word.getLen() > 6):
                        futurW.setText(futurW.getText()[:-1])
                        full2 = True
                    futurW.setTense(0)
                    futurW.setVavSeq()
                else:
                    futurW.setTense(1)
                futurW.setPerson(3)
                futurW.setGender(0)
                holl2 = True
                if(futurW.first() == 'ו'):
                    futurW.setText(futurW.getText()[:-1] + 'י')
                if(futurW.getLen() > 2):
                    futurW.setRoot(self.Final(futurW.first3()))
                
                if(futurW.getLen() > 2):
                    if((futurW.nextToLast() == 'ו') and (not((futurW.getVerbform() == 'Qal') and (not(futurW.third() == 'ו'))))) and (self.num_of_p_roots(futurW.getText()[:-4]) == 0) and ((futurW.isVerbf() == False) or (futurW.getVerbform() == 'Qal')) and (not((futurW.hasRoot()) and (not((futurW.getRootLast2() == self.Final(futurW.last3()[1:])) or (futurW.getRootLast2() == futurW.last2()))))):
                        futurW.setText(futurW.last() + futurW.getText()[2:])
                        holl2 = False
                        full = True
                        if(futurW.getLen() > 2):
                            futurW.setRoot(futurW.last3())
                            
                if(word.second() == 'ו'):
                    TfuturW = Word("","")
                    TfuturW.equalTo(futurW)
                    TfuturW.setText(word.getText()[1:-2] + 'ת')
                    TfuturW.addToValue(1)
                    if(full == True):
                        TfuturW.setText(TfuturW.last() + TfuturW.getText()[2:])
                    if(TfuturW.getLen() > 2):
                        TfuturW.setRoot(TfuturW.last3())
                    if(full2 == False) and (word.getPrixListEnd() == 'ו'):
                        futurW.setText(futurW.getText()[:-1])
                        if(futurW.getLen() > 2):
                            futurW.setRoot(futurW.first3())
                            
                    if(TfuturW.last() == 'ת'):
                        TfuturWh = Word("","")
                        TfuturWh.equalTo(TfuturW)
                        TfuturWh.setText('ה' + TfuturW.getText()[1:])
                        TfuturWh.addToValue(-1)
                                
                        if(TfuturWh.hasRoot()) and (TfuturWh.getLen() > 2):
                            if(TfuturWh.getRoot()[1:] == TfuturWh.last3()[1:]):
                                TfuturWh.setRoot(TfuturWh.last3())
                                
                        self.FindHelper(look, TfuturWh, self.Dict, Check)
                        self.irreg(look, TfuturWh, Check)
                                
                    self.FindHelper(look, TfuturW, self.Dict, Check)
                    self.algorithm(look, TfuturW, Check)
                            
                if(futurW.getLen() == 2) and (holl2 == True):
                    hollow = Word("","")
                    hollow.equalTo(futurW)
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    self.FindHelper(look, hollow, self.Dict, Check)
                if(not(word.getRoot()[:2] == word.last2()))and(futurW.getLen() > 2):
                    futurW.setRoot(futurW.last3())
                    
                if(futurW.last() == 'ת'):
                    futurWh2 = Word("","")
                    futurWh2.equalTo(futurW)
                    futurWh2.setText('ה' + futurW.getText()[1:])
                    futurWh2.addToValue(-1)
                    
                    if(futurWh2.hasRoot()) and (futurWh2.getLen() > 2):
                        if(futurWh2.getRoot()[1:] == futurWh2.last3()[1:]):
                            futurWh2.setRoot(futurWh2.last3())
                    
                    self.FindHelper(look, futurWh2, self.Dict, Check)
                    self.irreg(look, futurWh2, Check)
                    
                f = self.FindHelper(look, futurW, self.Dict, Check)
                self.algorithm(look, futurW, Check)
                fh = False
                if(not ('ה' in word.getSufxList())):
                    futurWh = Word("","")
                    futurWh.equalTo(futurW)
                    futurWh.setText('ה' + self.unFinal(futurW.getText()))
                    futurWh.addToValue(1)
                    if(futurWh.hasRoot()) and (futurWh.getLen() > 2):
                        if(futurWh.getRoot()[1:] == futurWh.last3()[1:]):
                            futurWh.setRoot(futurWh.last3())
                    fh = self.FindHelper(look, futurWh, self.Dict, Check)
                    self.irreg(look, futurWh, Check)

                elif 'ו' in word.getPrixList():
                    self.irreg(look, futurW, Check)

            if((word.first() == 'ת')and(word.last() == 'י') and (self.imperRules(word, 'ת') == True))and (not(word.getRoot()[-2:] == word.first2())) and (not(word.getRoot()[:2] == word.last2())):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(self.Final(word.getText()[1:-1]))
                futurW.setVerb()
                full = False
                full2 = False
            
                if(word.getPrixListEnd() == 'ו'):
                    if(futurW.first() == 'ו')and(word.getLen() > 6):
                        futurW.setText(futurW.getText()[:-1])
                        full2 = True
                    futurW.setTense(0)
                    futurW.setVavSeq()
                else:
                    futurW.setTense(1)
                futurW.setPerson(2)
                futurW.setGender(1)
                
                if(futurW.first() == 'ו'):
                    futurW.setText(futurW.getText()[:-1] + 'י')
                if(futurW.getLen() > 2):
                    futurW.setRoot(self.Final(futurW.first3()))
                    
                if(word.second() == 'ו'):
                    TfuturW = Word("","")
                    TfuturW.equalTo(futurW)
                    TfuturW.setText(word.getText()[1:-2] + 'ת')
                    TfuturW.addToValue(1)
                    if(full == True):
                        TfuturW.setText(TfuturW.last() + TfuturW.getText()[2:])
                    if(TfuturW.getLen() > 2):
                        TfuturW.setRoot(TfuturW.last3())
                    if(full2 == False) and (word.getPrixListEnd() == 'ו'):
                        futurW.setText(futurW.getText()[:-1])
                        if(futurW.getLen() > 2):
                            futurW.setRoot(futurW.first3())
                                
                    if(TfuturW.last() == 'ת'):
                        TfuturWh = Word("","")
                        TfuturWh.equalTo(TfuturW)
                        TfuturWh.setText('ה' + TfuturW.getText()[1:])
                        TfuturWh.addToValue(-1)
                        
                        if(TfuturWh.hasRoot()) and (TfuturWh.getLen() > 2):
                            if(TfuturWh.getRoot()[1:] == TfuturWh.last3()[1:]):
                                TfuturWh.setRoot(TfuturWh.last3())
                                
                        self.FindHelper(look, TfuturWh, self.Dict, Check)
                        self.irreg(look, TfuturWh, Check)
                                
                    self.FindHelper(look, TfuturW, self.Dict, Check)
                    self.algorithm(look, TfuturW, Check)
                    
                if(futurW.getLen() == 2):
                    hollow = Word("","")
                    hollow.equalTo(futurW)
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    self.FindHelper(look, hollow, self.Dict, Check)
                if(not(word.getRoot()[:2] == word.last2()))and(futurW.getLen() > 2):
                    futurW.setRoot(futurW.last3())
                    
                if(futurW.last() == 'ת'):
                    futurWh2 = Word("","")
                    futurWh2.equalTo(futurW)
                    futurWh2.setText('ה' + futurW.getText()[1:])
                    futurWh2.addToValue(-1)
                    
                    if(futurWh2.hasRoot()) and (futurWh2.getLen() > 2):
                        if(futurWh2.getRoot()[1:] == futurWh2.last3()[1:]):
                            futurWh2.setRoot(futurWh2.last3())
                    
                    self.FindHelper(look, futurWh2, self.Dict, Check)
                    self.irreg(look, futurWh2, Check)
                
                f = self.FindHelper(look, futurW, self.Dict, Check)
                self.algorithm(look, futurW, Check)
                fh = False
                if(not ('ה' in word.getSufxList())):
                    futurWh = Word("","")
                    futurWh.equalTo(futurW)
                    futurWh.setText('ה' + self.unFinal(futurW.getText()))
                    futurWh.addToValue(3)
                    if(futurWh.hasRoot()) and (futurWh.getLen() > 2):
                        if(futurWh.getRoot()[1:] == futurWh.last3()[1:]):
                            futurWh.setRoot(futurWh.last3())
                    fh = self.FindHelper(look, futurWh, self.Dict, Check)
                    self.irreg(look, futurWh, Check)
                elif 'ו' in word.getPrixList():
                    self.irreg(look, futurW, Check)
                    
            if((word.first() == 'י') and (word.last()== 'ו') and (self.imperRules(word, 'י') == True)) and (not(word.getRoot()[-2:] == word.first2())) and (not(word.getRoot()[:2] == word.last2())):
                futurW = Word("","")
                futurW.equalTo(word)
                futurW.setText(self.Final(word.getText()[1:-1]))
                futurW.setVerb()
                 
                futurW.setTense(1)
                futurW.setPerson(5)
                futurW.setGender(0)
                
                if(futurW.first() == 'ו'):
                    futurW.setText(futurW.getText()[:-1] + 'י')
                if(futurW.getLen() > 2):
                    futurW.setRoot(self.Final(futurW.first3()))
                        
                if(futurW.getLen() == 2):
                    hollow = Word("","")
                    hollow.equalTo(futurW)
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    self.FindHelper(look, hollow, self.Dict, Check)
                if(not(word.getRoot()[:2] == word.last2()))and(futurW.getLen() > 2):
                    futurW.setRoot(futurW.last3())
                
                if(futurW.last() == 'ת'):
                    futurWh2 = Word("","")
                    futurWh2.equalTo(futurW)
                    futurWh2.setText('ה' + futurW.getText()[1:])
                    futurWh2.addToValue(-1)
                    
                    if(futurWh2.hasRoot()) and (futurWh2.getLen() > 2):
                        if(futurWh2.getRoot()[1:] == futurWh2.last3()[1:]):
                            futurWh2.setRoot(futurWh2.last3())
                    
                    self.FindHelper(look, futurWh2, self.Dict, Check)
                    self.irreg(look, futurWh2, Check)
                
                f = self.FindHelper(look, futurW, self.Dict, Check)
                self.algorithm(look, futurW, Check)
                fh = False
                if(not ('ה' in word.getSufxList())):
                    futurWh = Word("","")
                    futurWh.equalTo(futurW)
                    futurWh.setText('ה' + self.unFinal(futurW.getText()))
                    futurWh.addToValue(3)
                    if(word.getPrixListEnd() == 'ו'):
                        futurWh.setTense(0)
                        futurWh.setVavSeq()
                        if(not(futurWh.hasRoot())) and (futurWh.getLen() > 2):
                            futurWh.setRoot(futurWh.last3())
                    if(futurWh.hasRoot()) and (futurWh.getLen() > 2):
                        if(futurWh.getRoot()[1:] == futurWh.last3()[1:]):
                            futurWh.setRoot(futurWh.last3())
                    fh = self.FindHelper(look, futurWh, self.Dict, Check)
                    self.irreg(look, futurWh, Check)
                    
                elif 'ו' in word.getPrixList():
                    self.irreg(look, futurW, Check)

        if(word.first() == 'א') and (self.imperRules(word, 'א') == True) and (not(word.getRoot()[-2:] == word.first2())):
            futurW = Word("","")
            futurW.equalTo(word)
            futurW.setText(word.getText()[:-1])
            futurW.setVerb()
            full = False
             
            if(word.getPrixListEnd() == 'ו'):
                if(word.second() == 'ו'):
                    if(word.nextToLast == 'ו'):
                        if(word.getLen() > 5):
                            futurW.setText(futurW.getText()[:-1])
                    else:
                        if(not(word.second() == 'ו')):
                            if(word.getLen() > 4):
                                futurW.setText(futurW.getText()[:-1])
                        
                futurW.setTense(0)
                futurW.setVavSeq()
            else:
                futurW.setTense(1)
            futurW.setPerson(0)
            futurW.setGender(2)
            
            if(futurW.first() == 'ו'):
                futurW.setText(futurW.getText()[:-1] + 'י')
            if(futurW.getLen() > 2):
                if(not(futurW.hasRoot() and (not(futurW.getRoot()[:2] == self.Final(futurW.first3()[:2]))))):
                    futurW.setRoot(self.Final(futurW.first3()))
        
            if(futurW.getLen() > 1):
                if(futurW.getLen() > 3):
                    if((futurW.nextToLast() == 'ו') and (not((futurW.getVerbform() == 'Qal') and (not(futurW.third() == 'ו'))))) and (self.num_of_p_roots(futurW.getText()[:-4]) == 0) and ((futurW.isVerbf() == False) or (futurW.getVerbform() == 'Qal')) and (not((futurW.hasRoot()) and (not((futurW.getRootLast2() == self.Final(futurW.last3()[1:])) or (futurW.getRootLast2() == futurW.last2()))))):
                        futurW.setText(futurW.last() + futurW.getText()[2:])
                        full = True
                        if(futurW.getLen() > 2):
                            futurW.setRoot(futurW.last3())
                            
                if(word.second() == 'ו'):
                    AfuturW = Word("","")
                    AfuturW.equalTo(futurW)
                    AfuturW.setText(word.getText()[:-2] + 'א')
                    AfuturW.addToValue(1)
                    if(full == True):
                        AfuturW.setText(AfuturW.last() + AfuturW.getText()[2:])
                    if(AfuturW.getLen() > 2):
                        AfuturW.setRoot(AfuturW.last3()) 
                                
                    self.FindHelper(look, AfuturW, self.Dict, Check)
                    self.algorithm(look, AfuturW, Check)
                            
                if(futurW.getLen() == 2) and (full == False):
                    hollow = Word("","")
                    hollow.equalTo(futurW)
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    self.FindHelper(look, hollow, self.Dict, Check)
                if(not(futurW.hasRoot()))and(futurW.getLen() > 2)and(word.getSuffix() == True):
                    futurW.setRoot(futurW.last3())
                    
                f = self.FindHelper(look, futurW, self.Dict, Check)
                self.algorithm(look, futurW, Check)
                fh = False
                if(not ('ה' in word.getSufxList())):
                    futurWh = Word("","")
                    futurWh.equalTo(futurW)
                    futurWh.setText('ה' + self.unFinal(futurW.getText()))
                    futurWh.addToValue(3)
                    if(word.getPrixListEnd() == 'ו'):
                        futurWh.setTense(0)
                        futurWh.setVavSeq()
                    fh = self.FindHelper(look, futurWh, self.Dict, Check)
                    self.irreg(look, futurWh, Check)
                return futurW
            elif 'ו' in word.getPrixList():
                return self.irreg(look, futurW, Check)
            
        if(word.first() == 'י') and (self.imperRules(word, 'י') == True) and (not(word.getRoot()[-2:] == word.first2())):
            futurW = Word("","")
            futurW.equalTo(word)
            futurW.setText(word.getText()[:-1])
            futurW.setVerb()
            full = False
             
            if 'ו' in word.getPrixList():
                futurW.setTense(0)
            else:
                futurW.setTense(1)
            futurW.setPerson(4)
            futurW.setGender(0)
            
            if(futurW.first() == 'ו'):
                futurW.setText(futurW.getText()[:-1] + 'י')
            if(futurW.getLen() > 2):
                futurW.setRoot(self.Final(futurW.first3()))
        
            if(futurW.getLen() > 1):
                if(futurW.getLen() > 2):
                    if((futurW.nextToLast() == 'ו') and (not((futurW.getVerbform() == 'Qal') and (not(futurW.third() == 'ו'))))) and (self.num_of_p_roots(futurW.getText()[4:]) == 0) and ((futurW.isVerbf() == False) or (futurW.getVerbform() == 'Qal')) and (not((futurW.hasRoot()) and (not((futurW.getRootLast2() == self.Final(futurW.last3()[1:])) or (futurW.getRootLast2() == futurW.last2()))))):
                        futurW.setText(futurW.last() + futurW.getText()[2:])
                        full = True
                        if(futurW.getLen() > 2):
                            futurW.setRoot(futurW.last3())
                if(futurW.getLen() == 2) and (full == False):
                    hollow = Word("","")
                    hollow.equalTo(futurW)
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    self.FindHelper(look, hollow, self.Dict, Check)
                if(not(futurW.hasRoot()))and(futurW.getLen() > 2)and(word.getSuffix() == True):
                    futurW.setRoot(futurW.last3())
                    
                f = self.FindHelper(look, futurW, self.Dict, Check)
                self.algorithm(look, futurW, Check)
              
                fh = False
                if(not ('ה' in word.getSufxList())):
                    futurWh = Word("","")
                    futurWh.equalTo(futurW)
                    futurWh.setText('ה' + self.unFinal(futurW.getText()))
                    futurWh.addToValue(3)
                    if(word.getPrixListEnd() == 'ו'):
                        futurWh.setTense(0)
                        futurWh.setVavSeq()
                        if(not(futurWh.hasRoot())) and (futurWh.getLen() > 2):
                            futurWh.setRoot(futurWh.last3())
                    fh = self.FindHelper(look, futurWh, self.Dict, Check)
                    self.irreg(look, futurWh, Check)
                return futurW
            elif 'ו' in word.getPrixList():
                self.irreg(look, futurW, Check)
                
            return futurW
  
        if(word.first() == 'ת') and (self.imperRules(word, 'ת') == True) and (not(word.getRoot()[-2:] == word.first2())):
            futurW = Word("","")
            futurW.equalTo(word)
            futurW.setText(word.getText()[:-1])
            futurW.setVerb()
            full = False
            full2 = False
            
            if(word.getPrixListEnd() == 'ו'):
                if(futurW.first() == 'ו')and(word.getLen() > 5):
                    futurW.setText(futurW.getText()[:-1])
                    full2 = True
                futurW.setTense(0)
                futurW.setVavSeq()
            else:
                futurW.setTense(1)
            futurW.setPerson(2)
            futurW.setGender(0)
            
            if(futurW.first() == 'ו'):
                futurW.setText(futurW.getText()[:-1] + 'י')
                #futurW.addToValue(1)
            if(futurW.getLen() > 2):
                if(not(futurW.hasRoot() and (not(futurW.getRoot()[:2] == self.Final(futurW.first3()[:2]))))):
                    futurW.setRoot(self.Final(futurW.first3()))
            
            TfuturW = Word("","")
            if(futurW.getLen() > 1):
                if(futurW.getLen() > 2):
                    if((futurW.nextToLast() == 'ו') and (not((futurW.getVerbform() == 'Qal') and (not(futurW.third() == 'ו'))))) and (self.num_of_p_roots(futurW.getText()[4:]) == 0) and ((futurW.isVerbf() == False) or (futurW.getVerbform() == 'Qal')) and (not((futurW.hasRoot()) and (not((futurW.getRootLast2() == self.Final(futurW.last3()[1:])) or (futurW.getRootLast2() == futurW.last2()))))):
                        futurW.setText(futurW.last() + futurW.getText()[2:])
                        full = True
                        if(futurW.getLen() > 2):
                            #if(not(futurW.hasRoot() and (not((futurW.getRoot()[1:] == futurW.last3()[1:])or(futurW.getRoot()[:1] + futurW.getRoot()[-1:] == futurW.last2()))))):
                            futurW.setRoot(futurW.last3())
                     
                if(word.second() == 'ו'):
                    TfuturW.equalTo(futurW)
                    TfuturW.setText(word.getText()[:-2] + 'ת')
                    TfuturW.addToValue(1)
                    if(full == True):
                        TfuturW.setText(TfuturW.last() + TfuturW.getText()[2:])
                    if(TfuturW.getLen() > 2):
                        TfuturW.setRoot(TfuturW.last3())
                    if(full2 == False) and (word.getPrixListEnd() == 'ו'):
                        futurW.setText(futurW.getText()[:-1])
                        if(futurW.getLen() > 2):
                            futurW.setRoot(futurW.first3())
                                
                    self.FindHelper(look, TfuturW, self.Dict, Check)
                    self.algorithm(look, TfuturW, Check)
                            
                if(futurW.getLen() == 2) and (full == False):
                    hollow = Word("","")
                    hollow.equalTo(futurW)
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    self.FindHelper(look, hollow, self.Dict, Check)
                if(not(futurW.hasRoot()))and(futurW.getLen() > 2)and(word.getSuffix() == True):
                    futurW.setRoot(futurW.last3())
                    
                f = self.FindHelper(look, futurW, self.Dict, Check)
                self.algorithm(look, futurW, Check)
                fh = False
                if(not ('ה' in word.getSufxList())):
                    futurWh = Word("","")
                    futurWh.equalTo(futurW)
                    futurWh.setText('ה' + self.unFinal(futurW.getText()))
                    futurWh.addToValue(3)
                    if(word.getPrixListEnd() == 'ו'):
                        futurWh.setTense(0)
                        futurWh.setVavSeq()
                    fh = self.FindHelper(look, futurWh, self.Dict, Check)
                    self.irreg(look, futurWh, Check)
            elif 'ו' in word.getPrixList():
                self.irreg(look, futurW, Check)
                
            futurW2 = Word("","")
            futurW2.equalTo(word)
            futurW2.setText(futurW.getText())
            futurW2.setRoot(futurW.getRoot())
            futurW2.setVerb()
             
            if(futurW.isVavSeq() == True):
                futurW2.setTense(0)
                futurW2.setVavSeq()
            else:
                futurW2.setTense(1)
            futurW2.setPerson(4)
            futurW2.setGender(1)
            
            if(not(TfuturW == Word("",""))):
                TfuturW2 = Word("","")
                TfuturW2.equalTo(futurW2)
                TfuturW2.setText(TfuturW.getText())
                TfuturW2.setRoot(TfuturW.getRoot())
                self.FindHelper(look, TfuturW2, self.Dict, False)
                self.algorithm(look, TfuturW2, False)
            
            if(futurW2.getLen() == 2):
                hollow = Word("","")
                hollow.equalTo(futurW2)
                hollow.setText(hollow.last() + 'ו' + hollow.first())
                hollow.addToValue(1)
                hollow.setRoot(hollow.getText())
                self.FindHelper(look, hollow, self.Dict, False)
            
            if(futurW2.getLen() > 1):
                f2 = self.FindHelper(look, futurW2, self.Dict, False)
                self.algorithm(look, futurW2, False)
                fh = False
                if(not ('ה' in word.getSufxList())):
                    futurW2h = Word("","")
                    futurW2h.equalTo(futurW2)
                    futurW2h.setText('ה' + self.unFinal(futurW2.getText()))
                    futurW2h.addToValue(3)
                    if(word.getPrixListEnd() == 'ו'):
                        futurW2h.setTense(0)
                        futurW2h.setVavSeq()
                    fh = self.FindHelper(look, futurW2h, self.Dict, False)
                    self.irreg(look, futurW2h, Check)
            elif 'ו' in word.getPrixList():
                self.irreg(look, futurW2, Check)
            return futurW2
  
        if(word.first() == 'נ') and (self.imperRules(word, 'נ') == True)and (not(word.getRoot()[-2:] == word.first2())):
            futurW = Word("","")
            futurW.equalTo(word)
            futurW.setText(word.getText()[:-1])
            futurW.setVerb()
            full = False
            full2 = False
             
            if(word.getPrixListEnd() == 'ו')and(futurW.first() == 'ו'):
                if(futurW.getLen() > 4):
                    futurW.setText(futurW.getText()[:-1])
                    full2 = True
                futurW.setTense(0)
                futurW.setVavSeq()
            else:
                futurW.setTense(1)
            futurW.setPerson(1)
            futurW.setGender(2)
            
            if(futurW.first() == 'ו'):
                futurW.setText(futurW.getText()[:-1] + 'י')
            if(futurW.getLen() > 2):
                if(not(futurW.hasRoot() and (not(futurW.getRoot()[:2] == self.Final(futurW.first3()[:2]))))):
                    futurW.setRoot(self.Final(futurW.first3()))
              
            if(futurW.getLen() > 1):
                if(futurW.getLen() > 2):
                    if((futurW.nextToLast() == 'ו') and (not((futurW.getVerbform() == 'Qal') and (not(futurW.third() == 'ו'))))) and (self.num_of_p_roots(futurW.getText()[4:]) == 0) and ((futurW.isVerbf() == False) or (futurW.getVerbform() == 'Qal')) and (not((futurW.hasRoot()) and (not((futurW.getRootLast2() == self.Final(futurW.last3()[1:])) or (futurW.getRootLast2() == futurW.last2()))))):
                        futurW.setText(futurW.last() + futurW.getText()[2:])
                        full = True
                        if(futurW.getLen() > 2):
                            futurW.setRoot(futurW.last3())
                            
                if(not(futurW.first() == 'נ')) and ((futurW.getLen() == 2)or(word.second() == 'ו')):
                    NfuturW = Word("","")
                    NfuturW.equalTo(futurW)
                    if(word.second() == 'ו'):
                        NfuturW.setText(word.getText()[:-2] + 'נ')
                    else:
                        NfuturW.setText(futurW.getText() + 'נ')
                    NfuturW.addToValue(3)
                    if(NfuturW.getLen() > 2):
                        NfuturW.setRoot(NfuturW.first3())
                    self.FindHelper(look, NfuturW, self.Dict, Check)
                    
                    if(full2 == False) and (word.getPrixListEnd() == 'ו'):
                        futurW.setText(futurW.getText()[:-1])
                        if(futurW.getLen() > 2):
                            futurW.setRoot(futurW.first3())
                            
                if(futurW.getLen() == 2) and (full == False):
                    hollow = Word("","")
                    hollow.equalTo(futurW)
                    hollow.setText(hollow.last() + 'ו' + hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    self.FindHelper(look, hollow, self.Dict, Check)
                if(not(futurW.hasRoot()))and(futurW.getLen() > 2)and(word.getSuffix() == True):
                    futurW.setRoot(futurW.last3())
                    
                f = self.FindHelper(look, futurW, self.Dict, Check)
                self.algorithm(look, futurW, Check)
                fh = False
                if(not ('ה' in word.getSufxList())):
                    futurWh = Word("","")
                    futurWh.equalTo(futurW)
                    futurWh.setText('ה' + self.unFinal(futurW.getText()))
                    futurWh.addToValue(3)
                    if(futurWh.hasRoot()) and (futurWh.getLen() > 2):
                        if(futurWh.getRoot()[1:] == futurWh.last3()[1:]):
                            futurWh.setRoot(futurWh.last3())
                    if(word.getPrixListEnd() == 'ו'):
                        futurWh.setTense(0)
                        futurWh.setVavSeq()
                    fh = self.FindHelper(look, futurWh, self.Dict, Check)
                    self.irreg(look, futurWh, Check)
                return futurW
            elif 'ו' in word.getPrixList():
                self.irreg(look, futurW, Check)

        return Word("", "")
    
    def imperRules(self, word, l):
        if (('ה' in word.getPrixList()) or (word.getPrixListEnd() == 'ל') or (word.getPrixListEnd() == 'מ') or (word.getVerbform() in Piel) or (word.getPrixListEnd() == 'ב')):
            return False
        return True
        
    def impertvRules(self, word, l):
        if (('ה' in word.getPrixList()) or ('ל' in word.getPrixList()) or ('כ' in word.getPrixList()) or ('מ' in word.getPrixList()) or ('ש' in word.getPrixList()) or ('ב'in word.getPrixList())):
            return False
        return True
    
    def imperative(self, look, word, Check):
        if(word.getLen() < 2) or (word.isPhrase()) or (self.impertvRules(word, word.last()) == False) or (not(word.getTenseVal() == -1)) or (word.isNoun() == True) or (word.getVerbform() in Hophal) or (word.getVerbform() in Piel) or (word.getVerbform() in Niphal) or (word.getModern == True):
            return Word("","")
        
        if(word.getLen() < 3):
            imperW = Word("","")
            imperW.equalTo(word)
            imperW.setVerb()
            imperW.setTense(4)
            imperW.setPerson(2)
            imperW.setGender(0)
            self.irreg(look, imperW, Check)
       
            hollow = Word("","")
            hollow.equalTo(imperW)
            hollow.setText(imperW.last() + 'ו' + imperW.first())
            hollow.addToValue(1)
            hollow.setTense(4)
            hollow.setVerb()
            hollow.setGender(0)
            hollow.setPerson(2)
            hollow.setRoot(hollow.getText())
            self.FindHelper(look, hollow, self.Dict, Check)
            
        if(word.getLen() == 3) and (word.getVerbform() in Hithpeal):
            piel = Word("","")
            piel.equalTo(word)
            piel.addToValue(1)
            piel.setTense(4)
            piel.setGender(0)
            piel.setPerson(2)
            piel.setVerb()
            piel.setRoot(piel.getText())
            self.FindHelper(look, piel, self.Dict, Check)
            if(word.second() == 'י'):
                self.piel(look, piel, Check)
            
        if(word.getRoot()[:2] == word.last2()):
            return Word("","")
            
        if word.last() == 'ו':
            imperW = Word("","")
            imperW.equalTo(word)
            imperW.setText(self.Final(word.getText()[1:]))
            imperW.setVerb()
            imperW.setTense(4)
            imperW.setPerson(3)
            imperW.setGender(0)
            
            singleW = Word("","")
            singleW.equalTo(imperW)
            singleW.setText('ה' + self.unFinal(imperW.getText()))
            singleW.addToValue(1)
            self.FindHelper(look, singleW, self.Dict, Check)
            
            if(imperW.first() == 'ה') and ((imperW.isVerbf() == False) or (imperW.getVerbformVal() == 0)):
                if(imperW.getLen() < 3):
                    return self.nifal(look, imperW, Check)
                self.nifal(look, imperW, Check)
                
            self.FindHelper(look, imperW, self.Dict, Check)
            self.verbForms(look, imperW, Check)
            self.irreg(look, imperW, Check)
            return imperW
            
        if (word.last() == 'י') and (word.getPlural() == False):
            imperW = Word("","")
            imperW.equalTo(word)
            imperW.setText(self.Final(word.getText()[1:]))
            imperW.setVerb()
            imperW.setTense(4)
            imperW.setPerson(2)
            imperW.setGender(1)
            
            singleW = Word("","")
            singleW.equalTo(imperW)
            singleW.setText('ה' + self.unFinal(imperW.getText()))
            singleW.addToValue(1)
            self.FindHelper(look, singleW, self.Dict, Check)
            
            if(imperW.first() == 'ה') and ((imperW.isVerbf() == False) or (imperW.getVerbformVal() == 0)):
                if(imperW.getLen() < 3):
                    return self.nifal(look, imperW, Check)
                self.nifal(look, imperW, Check)
                
            self.FindHelper(look, imperW, self.Dict, Check)
            self.verbForms(look, imperW, Check)
            self.irreg(look, imperW, Check)
            return imperW
        
        if(word.getLen() > 2) and (not((word.getRoot()[:2] == self.Final(word.last3()[1:])) or (word.getRoot()[-2:] == word.last3()[1:]))):
            if word.last2() == 'הנ':
                imperW = Word("","")
                imperW.equalTo(word)
                imperW.setText(self.Final(word.getText()[2:]))
                imperW.setVerb()
                imperW.setTense(4)
                imperW.setPerson(3)
                imperW.setGender(1)
                if(imperW.getLen() > 3):
                    if(imperW.nextToLast() == 'ו') and (self.num_of_p_roots(imperW.getText()[4:]) == 0) and (not((imperW.hasRoot()) and (not((imperW.getRootLast2() == self.Final(imperW.last3()[1:])) or (imperW.getRootLast2() == imperW.last2()))))):
                        imperW.setText(imperW.last() + imperW.getText()[2:])
                        #imperW.addToValue(-2)
                        #if(imperW.hasRoot() and (not((imperW.getRoot()[1:] == imperW.last3()[1:])or(imperW.getRoot()[:1] + imperW.getRoot()[-1:] == imperW.last2())))):
                            #imperW.setText(self.Final(word.getText()[2:]))
                        #else:
                        imperW.setRoot(imperW.last3())
                    if(not(imperW.hasRoot())):
                        imperW.setRoot(imperW.last3())
                        
                    if(imperW.first() == 'ה') and ((imperW.isVerbf() == False) or (imperW.getVerbformVal() == 0)):
                        if(imperW.getLen() < 3):
                            return self.nifal(look, imperW, Check)
                        self.nifal(look, imperW, Check)
                        
                singleW = Word("","")
                singleW.equalTo(imperW)
                singleW.setText('ה' + self.unFinal(imperW.getText()))
                singleW.addToValue(1)
                self.FindHelper(look, singleW, self.Dict, Check)
                        
                self.FindHelper(look, imperW, self.Dict, Check)
                self.verbForms(look, imperW, Check)
                if(imperW.getLen() == 3):
                    imperW.setRoot(imperW.getText())
                elif(imperW.getLen() == 2):
                    hollow = Word("","")
                    hollow.equalTo(imperW)
                    hollow.setText(imperW.last() + 'ו' + imperW.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    self.FindHelper(look, hollow, self.Dict, Check)
                
                if(not('ונ' in word.getSufxList())) and (not('ןכ' in word.getSufxList())) and (not('ןה' in word.getSufxList())) and (not('ן' in word.getSufxList())) and (not('ינ' in word.getSufxList())) and (not('הנ' in word.getSufxList())):
                    imperwNun = Word("","")
                    imperwNun.equalTo(imperW)
                    imperwNun.setText('ן' + self.unFinal(imperW.getText()))
                    imperwNun.addToValue(5)
                    self.irreg(look, imperwNun, Check)
                return imperW
            if(word.getLen() > 3):
                if(word.nextToLast() == 'ו') and (self.num_of_p_roots(word.getText()[4:]) == 0) and (not((word.hasRoot()) and (not((word.getRootLast2() == self.Final(word.last3()[1:])) or (word.getRootLast2() == word.last2()))))):
                    imperW = Word("","")
                    imperW.equalTo(word)
                    imperW.setText(word.last() + word.getText()[2:])
                    #imperW.addToValue(-2)
                    #if(not(imperW.hasRoot() and (not((imperW.getRoot()[1:] == imperW.last3()[1:])or(imperW.getRoot()[:1] + imperW.getRoot()[-1:] == imperW.last2()))))):
                    imperW.setRoot(imperW.last3())
                    imperW.setVerb()
                    imperW.setTense(4)
                    imperW.setPerson(2)
                    imperW.setGender(0)
                    if(imperW.first() == 'ה') and ((imperW.isVerbf() == False) or (imperW.getVerbformVal() == 0)):
                        if(imperW.getLen() < 3):
                            return self.nifal(look, imperW, Check)
                        self.nifal(look, imperW, Check)
                        
                    self.FindHelper(look, imperW, self.Dict, Check)
                    self.verbForms(look, imperW, Check)
                    return imperW
     
        return Word("", "")
        
    def infinitive(self, look, word, Check):
        if((word.getLen() < 3) or (word.isPhrase()) or (word.getPrixListEnd() == 'מ') or (word.getVerbform() in Hophal) or (word.getPrixListEnd() == 'ל') or ('ה' in word.getPrixList()) or (word.isTense() == True) or (word.isNoun() == True) or (word.getVerbform() in Niphal) or (word.getVerbform() in Pual)):# or (word.getVerbform() in Piel)):
            return Word("","")
        
        singleW2 = Word("","")
        if(not((word.last2() == 'תו') and (word.getLen() < 5))):
            if(word.first() == 'ל') and (not(word.getRoot()[-2:] == word.first2())):
                infW = Word("","")
                infW.equalTo(word)
                infW.setText(word.getText()[:-1])
                infW.setVerb()
                infW.setTense(3)
                infW.setGender(0)
                if(infW.getLen() > 3):
                    if(infW.nextToLast() == 'ו') and (self.num_of_p_roots(infW.getText()[4:]) == 0) and (not((infW.hasRoot()) and (not((infW.getRootLast2() == self.Final(infW.last3()[1:])) or (infW.getRootLast2() == infW.last2()))))):
                        infW.setText(infW.last() + infW.getText()[2:])
                        #if(infW.hasRoot() and (not(((infW.getRoot()[1:] == infW.last3()[1:]))or(infW.getRoot()[:1] + infW.getRoot()[-1:] == infW.last2())))):
                            #infW.setText(word.getText()[:-1])
                        #else:
                        infW.setRoot(infW.last3())
                        #infW.addToValue(-2)
                    if(not(infW.hasRoot()))and(word.getSuffix() == True):
                        infW.setRoot(infW.last3())
                    self.FindHelper(look, infW, self.Dict, Check)
                    self.algorithm(look, infW, Check)
                elif(infW.getLen() == 3):
                    infW.setRoot(infW.getText())
                    self.irreg(look, infW, Check)
                if(infW.getLen() > 1):
                    self.FindHelper(look, infW, self.Dict, Check)
                    self.algorithm(look, infW, Check)
                else:
                    self.irreg(look, infW, Check)
                if(infW.getLen() > 1) and (infW.first() == 'ה'):
                    singleW2 = Word("","")
                    singleW2.equalTo(infW)
                    singleW2.setText(infW.getText()[:-1] + 'י')
                    singleW2.addToValue(1)
                    self.FindHelper(look, singleW2, self.Dict, Check)
                    self.irreg(look, singleW2, Check)
                    
        if(word.getLen() > 3):
            if((word.first() == 'ל') and (word.last2() == 'תו')) and (not(word.getRoot()[-2:] == word.first2())) and (not((word.getRoot()[:2] == self.Final(word.last3()[1:])) or (word.getRoot()[:2] == word.last2()))):
                infW = Word("","")
                infW.equalTo(word)
                infW.setText(self.Final(word.getText()[2:-1]))
                infW.setVerb()
                infW.setTense(3)
                infW.setPlural()
                infW.setGender(1)
                if(infW.getLen() == 3) or (infW.getLen() == 2):
                    if(infW.nextToLast() == 'ו') and (not((infW.hasRoot()) and (not((infW.getRootLast2() == self.Final(infW.last3()[1:])) or (infW.getRootLast2() == infW.last2()))))):
                        #infW.setText(infW.getText()[1:])
                        infW.setText(infW.last() + infW.getText()[2:])
                        #if(infW.hasRoot()):
                            #infW.setText(self.Final(word.getText()[2:-1]))
                        #else:
                        #infW.addToValue(2)
                      
                    singleW = Word("","")
                    singleW.equalTo(infW)
                    singleW.setText('ה' + self.unFinal(infW.getText()))
                    singleW.addToValue(-2)
                    if(singleW.getLen() == 3):
                        singleW.setRoot(singleW.last3())
                    self.FindHelper(look, singleW, self.Dict, Check)
                    if(singleW.first() == 'ה') and ((singleW.isVerbf() == False) or (singleW.getVerbformVal() == 0)):
                        self.nifal(look, singleW, Check)
                    
                    if(infW.getLen() > 1):
                        self.FindHelper(look, infW, self.Dict, Check)
                        self.algorithm(look, infW, Check)
                    else:
                        self.irreg(look, infW, Check)
                    
                    if(singleW.getLen() < 4):
                        return singleW
                    else:
                        self.algorithm(look, singleW, Check)
                            
                if(infW.getLen() > 3):
                    if(infW.nextToLast() == 'ו') and (self.num_of_p_roots(infW.getText[4:]) == 0) and (not((infW.hasRoot()) and (not((infW.getRootLast2() == self.Final(infW.last3()[1:])) or (infW.getRootLast2() == infW.last2()))))):
                        infW.setText(infW.last() + infW.getText()[2:])
                        #if(infW.hasRoot() and (not((infW.getRoot()[1:] == infW.last3()[1:])or(infW.getRoot()[:1] + infW.getRoot()[-1:] == infW.last2())))):
                            #infW.setText(self.Final(word.getText()[2:-1]))
                        #else:
                        infW.setRoot(infW.last3())
                        #infW.addToValue(-2)
                    
                    if(infW.getLen() > 1):
                        self.FindHelper(look, infW, self.Dict, Check)
                        self.algorithm(look, infW, Check)
                    else:
                        self.irreg(look, infW, Check)
                            
                    singleW = Word("","")
                    singleW.equalTo(infW)
                    singleW.setText('ה' + self.unFinal(infW.getText()))
                    singleW.addToValue(-2)
                    if(singleW.hasRoot()) and (singleW.getLen() > 2):
                        if(singleW.getRoot()[1:] == singleW.last3()[1:]):
                            singleW.setRoot(singleW.last3())
                    self.FindHelper(look, singleW, self.Dict, Check)
                    if(singleW.first() == 'ה') and ((singleW.isVerbf() == False) or (singleW.getVerbformVal() == 0)):
                        self.nifal(look, singleW, Check)
                    
                    if(infW.getLen() > 1) and (infW.first() == 'ה'):
                        singleW2 = Word("","")
                        singleW2.equalTo(infW)
                        singleW2.setText(infW.getText()[:-1] + 'י')
                        singleW2.addToValue(1)
                        self.FindHelper(look, singleW2, self.Dict, Check)
                        self.irreg(look, singleW2, Check)
                        
                    if(singleW.getLen() < 4):
                        return singleW
                    else:
                        self.algorithm(look, singleW, Check)
                        
                if(infW.getLen() == 2):
                    hollow = Word("","")
                    hollow.equalTo(infW)
                    hollow.setText(infW.last() + 'ו' + infW.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    self.FindHelper(look, hollow, self.Dict, Check)
                    self.irreg(look, hollow, Check)
                    
        if(word.getLen() > 2):
            if((word.first() == 'ל') and (word.last() == 'ת')) and (not(word.getRoot()[-2:] == word.first2())) and (not(word.getRoot()[:2] == word.last2())):
                infW = Word("","")
                infW.equalTo(word)
                infW.setText(self.Final(word.getText()[1:-1]))
                infW.setVerb()
                infW.setTense(3)
                infW.setGender(1)
                if(infW.getLen() > 3):
                    if(infW.nextToLast() == 'ו') and (self.num_of_p_roots(infW.getText()[4:]) == 0) and (not((infW.hasRoot()) and (not((infW.getRootLast2() == self.Final(infW.last3()[1:])) or (infW.getRootLast2() == infW.last2()))))):
                        infW.setText(infW.last() + infW.getText()[2:])
                        #if(infW.hasRoot() and (not((infW.getRoot()[1:] == infW.last3()[1:])or(infW.getRoot()[:1] + infW.getRoot()[-1:] == infW.last2())))):
                            #infW.setText(self.Final(word.getText()[1:-1]))
                        #else:
                        infW.setRoot(infW.last3())
                        #infW.addToValue(-2)
                    if(not(infW.hasRoot())):
                        infW.setRoot(infW.last3())
                            
                    if(infW.getLen() > 1):
                        self.FindHelper(look, infW, self.Dict, Check)
                        self.algorithm(look, infW, Check)
                    else:
                        self.irreg(look, infW, Check)
                            
                    singleW = Word("","")
                    singleW.equalTo(infW)
                    singleW.setText('ה' + self.unFinal(infW.getText()))
                    singleW.addToValue(-2)
                    if(singleW.hasRoot()) and (singleW.getLen() > 2):
                        if(singleW.getRoot()[1:] == singleW.last3()[1:]):
                            singleW.setRoot(singleW.last3())
                    self.FindHelper(look, singleW, self.Dict, Check)
                    if(singleW.first() == 'ה') and ((singleW.isVerbf() == False) or (singleW.getVerbformVal() == 0)):
                        self.nifal (look, singleW, Check)
                
                    if(infW.getLen() > 1) and (infW.first() == 'ה'):
                        singleW2 = Word("","")
                        singleW2.equalTo(infW)
                        singleW2.setText(infW.getText()[:-1] + 'י')
                        singleW2.addToValue(1)
                        self.FindHelper(look, singleW2, self.Dict, Check)
                        self.irreg(look, singleW2, Check)

                    if(singleW.getLen() < 4):
                        return singleW
                    else:
                        self.algorithm(look, singleW, Check)
                        
                elif(infW.getLen() == 3) or (infW.getLen() == 2):
                    if(infW.last() == 'ו'):
                        infW.setText(infW.getText()[1:])
                        if(infW.hasRoot()):
                            infW.setText(self.Final(word.getText()[2:-1]))
                        else:
                            infW.addToValue(5)
                            
                    singleW = Word("","")
                    singleW.equalTo(infW)
                    singleW.setText('ה' + self.unFinal(infW.getText()))
                    singleW.addToValue(-2)
                    singleW.setGender(1)
                    if(singleW.getLen() == 3):
                        singleW.setRoot(singleW.last3())
                    self.FindHelper(look, singleW, self.Dict, Check)
                    if(singleW.first() == 'ה') and ((singleW.isVerbf() == False) or (singleW.getVerbformVal() == 0)):
                        self.nifal(look, singleW, Check)
                    
                    if(infW.getLen() > 1):
                        self.FindHelper(look, infW, self.Dict, Check)
                        self.algorithm(look, infW, Check)
                    else:
                        self.irreg(look, infW, Check)
                    
                    if(singleW.getLen() < 4):
                        return singleW
                    else:
                        self.algorithm(look, singleW, Check)

                if(infW.getLen() == 2):
                    hollow = Word("","")
                    hollow.equalTo(infW)
                    hollow.setText(infW.last() + 'ו' + infW.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    self.FindHelper(look, hollow, self.Dict, Check)
                    self.irreg(look, hollow, Check)
                    
                    self.FindHelper(look, infW, self.Dict, Check)
                    self.algorithm(look, infW, Check)
                return infW
            
        return Word("", "")
        
    def infinitiveAbs(self, look, word, Check):
        if((word.getLen() < 3)  or ('-' in word.getText()) or (word.getVerbform() == 'Niphal') or (word.isTense() == True) or (word.getPrixListEnd() == 'מ') or (word.getPrixListEnd() == 'ל') or ('ה' in word.getPrixList())):
            return Word("","")
        
        infWp = Word("","")
        infWp.equalTo(word)
        if(word.last2() == 'תו') and (not((word.getRoot()[:2] == word.last3()[1:]) or (word.getRoot()[-2:] == word.last3()[1:]))):
            infWp.setText(self.Final(word.getText()[2:]))
            infWp.setPlural2()
            infWp.setGender(1)
            infWp.addToValue(2)
            
        
        if(infWp.getLen() > 3):
            if(infWp.isVerbf() == False) or (infWp.getVerbform() in Qal) or (infWp.getVerbform() in Niphal) or (infWp.getVerbform() in Piel) or (infWp.getVerbform() in Pual):
                if((infWp.nextToLast() == 'ו') and (not((infWp.getVerbform() == 'Qal') and (not(infWp.third() == 'ו'))))) and (self.num_of_p_roots(infWp.getText()[4:]) == 0) and (not((infWp.hasRoot()) and (not((infWp.getRootLast2() == self.Final(infWp.last3()[1:])) or (infWp.getRootLast2() == infWp.last2()))))):
                    infW = Word("","")
                    infW.equalTo(infWp)
                    infW.setText(infWp.last() + infWp.getText()[2:])
                    #infW.addToValue(-2)
                    #if(infW.hasRoot() and (not((infW.getRoot()[1:] == infW.last3()[1:])or(infW.getRoot()[:1] + infW.getRoot()[-1:] == infW.last2())))):
                        #return Word("","")
                    #else:
                    infW.setRoot(infW.last3())
                    infW.setTense(6)
                    infW.setVerb()
                    if(infW.first() == 'ה'):
                        if(infW.getLen() < 3):
                            return self.nifal(look, infW, Check)
                        self.nifal(look, infW, Check)
                    self.FindHelper(look, infW, self.Dict, Check)
                    self.algorithm(look, infW, Check)
                    if(not (infWp.last() == 'ה')) and (not('ה' in infWp.getSufxList())) and (not(infWp.getHey1() > 0)):
                        singleW2 = Word("","") 
                        singleW2.equalTo(infW)
                        singleW2.setText('ה' + self.unFinal(infW.getText()))
                        if(word.last2() == 'תו'):
                            singleW2.addToValue(-4)
                        else:
                            singleW2.addToValue(1.5)
                        if(singleW2.first() == 'ה'):
                            if(singleW2.getLen() < 3):
                                return self.nifal(look, singleW2, Check)
                            self.nifal(look, singleW2, Check)
                        self.FindHelper(look, singleW2, self.Dict, Check)
                        return singleW2
                    
                    return infW
                
        return Word("", "")

    def cohortative(self, look, word, Check):
        if((word.getLen() < 3) or (word.getPrixListEnd() == 'ל') or ('ה' in word.getPrixList()) or (word.getVerbform() in Hophal) or (word.isPhrase()) or (word.isTense() == True) or (word.isNoun() == True) or (word.getVerbform() in Niphal) or (word.getRoot()[:2] == word.last2()) or (word.getRoot()[-2:] == word.first2()) or (word.getVerbform() in Pual) or (word.getVerbform() in Piel)):
            return Word("","")
            
        if(word.getLen() > 3):   
            if((word.first() == 'א')and(word.last() == 'ה')and(self.CurrentWord.last() == 'ה')):
                cohorW = Word("","")
                cohorW.equalTo(word)
                if(word.nextToFirst() == 'ו'):
                    cohorW.setText(word.getText()[1:-2] + 'י')
                    #cohorW.addToValue(1)
                else:
                    cohorW.setText(self.Final(word.getText()[1:-1]))
                cohorW.setVerb()
                if(cohorW.getLen() > 2):
                    if(not(cohorW.hasRoot() and (not(cohorW.getRoot()[:2] == self.Final(cohorW.first3()[:2]))))):
                        cohorW.setRoot(self.Final(cohorW.first3()))
               
                cohorW.setTense(5)
                cohorW.setPerson(0)
                cohorW.setGender(2)
                
                if(cohorW.getLen() > 1):
                    if(cohorW.getLen() > 2):
                        if((cohorW.nextToLast() == 'ו') and (not((cohorW.getVerbform() == 'Qal') and (not(cohorW.third() == 'ו'))))) and ((cohorW.isVerbf() == False) or (cohorW.getVerbform() == 'Qal')) and (not((cohorW.hasRoot()) and (not((cohorW.getRootLast2() == self.Final(cohorW.last3()[1:])) or (cohorW.getRootLast2() == cohorW.last2()))))) and (self.num_of_p_roots(cohorW.getText()[4:]) == 0):
                            cohorW.setText(cohorW.last() + cohorW.getText()[2:])
                            #cohorW.addToValue(-2)
                            if(cohorW.getLen() > 2):
                                #if(cohorW.hasRoot() and (not((cohorW.getRoot()[1:] == cohorW.last3()[1:])or(cohorW.getRoot()[:1] + cohorW.getRoot()[-1:] == cohorW.last2())))): 
                                    #cohorW.setText(self.Final(word.getText()[1:-1]))
                                #else:
                                cohorW.setRoot(cohorW.last3())
                        if(not(cohorW.hasRoot())) and (cohorW.getLen() > 2):
                            cohorW.setRoot(cohorW.last3())
                            
                    if(not(cohorW.first() == 'א')) and (word.second() == 'ו'):
                        AcohorrW = Word("","")
                        AcohorrW.equalTo(cohorW)
                        if(word.second() == 'ו'):
                            AcohorrW.setText(word.getText()[1:-2] + 'א')
                        else:
                            AcohorrW.setText(cohorW.getText() + 'א')
                        AcohorrW.addToValue(3)
                        if(AcohorrW.getLen() > 2):
                            AcohorrW.setRoot(AcohorrW.first3())
                        self.FindHelper(look, AcohorrW, self.Dict, Check)
                        self.verbForms(look, AcohorrW, Check)
                        
                        if(AcohorrW.last() == 'ת'):
                            AcohorrWh2 = Word("","")
                            AcohorrWh2.equalTo(AcohorrW)
                            AcohorrWh2.setText('ה' + AcohorrW.getText()[1:])
                            AcohorrWh2.addToValue(-1)
                            
                            if(AcohorrWh2.hasRoot()) and (AcohorrWh2.getLen() > 2):
                                if(AcohorrWh2.getRoot()[1:] == AcohorrWh2.last3()[1:]):
                                    AcohorrWh2.setRoot(AcohorrWh2.last3())
                            
                            self.FindHelper(look, AcohorrWh2, self.Dict, Check)
                            self.irreg(look, AcohorrWh2, Check)
                        
                    
                    if(cohorW.last() == 'ת'):
                        cohorWh2 = Word("","")
                        cohorWh2.equalTo(cohorW)
                        cohorWh2.setText('ה' + cohorW.getText()[1:])
                        cohorWh2.addToValue(-1)
                        
                        if(cohorWh2.hasRoot()) and (cohorWh2.getLen() > 2):
                            if(cohorWh2.getRoot()[1:] == cohorWh2.last3()[1:]):
                                cohorWh2.setRoot(cohorWh2.last3())
                        
                        self.FindHelper(look, cohorWh2, self.Dict, Check)
                        self.irreg(look, cohorWh2, Check)
                        
                    self.verbForms(look, cohorW, Check)
                    self.FindHelper(look, cohorW, self.Dict, Check)
                    return cohorW          
                elif 'ו' in word.getPrixList():
                    return self.irreg(look, cohorW, Check)
                
                return Word("","")
                    
        if((word.first() == 'נ')and(word.last() == 'ה')and(self.CurrentWord.last() == 'ה')):
            cohorW = Word("","")
            cohorW.equalTo(word)
            if(word.nextToFirst() == 'ו'):
                cohorW.setText(word.getText()[1:-2] + 'י')
                #addToValue(1)
            else:
                cohorW.setText(self.Final(word.getText()[1:-1]))
            cohorW.setVerb()
            if(cohorW.getLen() > 2):
                if(not(cohorW.hasRoot() and (not(cohorW.getRoot()[:2] == self.Final(cohorW.first3()[:2]))))):
                    cohorW.setRoot(self.Final(cohorW.first3()))
           
            cohorW.setTense(5)
            cohorW.setPerson(1)
            cohorW.setGender(2)
            
            if(cohorW.getLen() > 1):
                if(cohorW.getLen() > 2):
                    if((cohorW.nextToLast() == 'ו') and (not((cohorW.getVerbform() == 'Qal') and (not(cohorW.third() == 'ו')))))and (self.num_of_p_roots(cohorW.getText()[4:]) == 0) and ((cohorW.isVerbf() == False) or (cohorW.getVerbform() == 'Qal')) and (not((cohorW.hasRoot()) and (not((cohorW.getRootLast2() == self.Final(cohorW.last3()[1:])) or (cohorW.getRootLast2() == cohorW.last2()))))):
                        cohorW.setText(cohorW.last() + cohorW.getText()[2:])
                        #cohorW.addToValue(-2)
                        if(cohorW.getLen() > 2):
                            #if(cohorW.hasRoot() and (not((cohorW.getRoot()[1:] == cohorW.last3()[1:])or(cohorW.getRoot()[:1] + cohorW.getRoot()[-1:] == cohorW.last2())))): 
                                #cohorW.setText(self.Final(word.getText()[1:-1]))
                            #else:
                            cohorW.setRoot(cohorW.last3()) 
                    
                    if(cohorW.getLen() > 2):
                        cohorW.setRoot(cohorW.last3())
                        
                if(not(cohorW.first() == 'נ')) and ((cohorW.getLen() == 2)or(word.second() == 'ו')):
                    NcohorrW = Word("","")
                    NcohorrW.equalTo(cohorW)
                    if(word.second() == 'ו'):
                        NcohorrW.setText(word.getText()[1:-2] + 'נ')
                    else:
                        NcohorrW.setText(cohorW.getText() + 'נ')
                    NcohorrW.addToValue(3)
                    if(NcohorrW.getLen() > 2):
                        NcohorrW.setRoot(NcohorrW.first3())
                    self.FindHelper(look, NcohorrW, self.Dict, Check)
                    self.verbForms(look, NcohorrW, Check)
                    
                    if(NcohorrW.last() == 'ת'):
                        NcohorrWh2 = Word("","")
                        NcohorrWh2.equalTo(NcohorrW)
                        NcohorrWh2.setText('ה' + NcohorrW.getText()[1:])
                        NcohorrWh2.addToValue(-1)
                        
                        if(NcohorrWh2.hasRoot()) and (NcohorrWh2.getLen() > 2):
                            if(NcohorrWh2.getRoot()[1:] == NcohorrWh2.last3()[1:]):
                                NcohorrWh2.setRoot(NcohorrWh2.last3())
                        
                        self.FindHelper(look, NcohorrWh2, self.Dict, Check)
                        self.irreg(look, NcohorrWh2, Check)
                        
                if(cohorW.last() == 'ת'):
                    cohorWh2 = Word("","")
                    cohorWh2.equalTo(cohorW)
                    cohorWh2.setText('ה' + cohorW.getText()[1:])
                    cohorWh2.addToValue(-1)
                    
                    if(cohorWh2.hasRoot()) and (cohorWh2.getLen() > 2):
                        if(cohorWh2.getRoot()[1:] == cohorWh2.last3()[1:]):
                            cohorWh2.setRoot(cohorWh2.last3())
                    
                    self.FindHelper(look, cohorWh2, self.Dict, Check)
                    self.irreg(look, cohorWh2, Check)
                        
                self.verbForms(look, cohorW, Check)
                self.FindHelper(look, cohorW, self.Dict, Check)
                return cohorW
            elif 'ו' in word.getPrixList():
                return self.irreg(look, cohorW, Check)
                
            return Word("","")
                    
        return Word("", "")
        
    def wFinal(self, text):
        if text[0] in finals.keys():
            return finals.get(text[0]) + text[1:]
        return text
        
    def FinalChain(self, text):
        inputL = text.split()
        if len(inputL) > 1:
            for i in range(len(inputL)):
                inputL[i] = self.wFinal(inputL[i])
            text =  " ".join(inputL)  
        else:
            text = self.wFinal(text)
        return text
        
    def lstChain(self, text, end):
        temp = text.replace("-", " ")
        inputL = temp.split()
        s = len(end)
        count = 0
        if len(inputL) > 1:
            for i in range(len(inputL)):
                if(inputL[i][0:s] == end):
                    count = count + 1
                    if(len(inputL[i]) < s+1):
                        return -1
        return count      
        
    def sizChain(self, phrase, size):
        text = phrase.getText()
        temp = text.replace("-", " ")
        inputL = temp.split()
        if len(inputL) > 1:
            for i in range(len(inputL)):
                if(len(inputL[i]) < size):
                    return False
        return True
        
    def sizChainSub(self, phrase, suffix):
        text = phrase.getText()
        temp = text.replace("-", " ")
        inputL = temp.split()
        if len(inputL) > 1:
            for i in range(len(inputL)):
                if len(inputL[i]) >= len(suffix):
                    if inputL[i][0:len(suffix)] == suffix:
                        inputL[i] = inputL[i][2:]
                    if(len(inputL[i]) < 2):
                        return False
        return True
            
    def plural(self, look, word, Check):
        if(word.getGrstphLen() < 3) or (word.isVerb() == True) or (word.getVerbform() in Piel) or ((word.getPlural() == True)and(not((word.getConstruct() == True)and(word.getSuffix() == True)))) or (word.getDual() == True) or ((word.getConstruct() == True)and(not((word.getPlural() == True)and(word.getSuffix() == True)))) or (word.getModern == True) or ((word.getRoot()[:2] == self.Final(word.last3()[1:])) or (word.getRoot()[-2:] == word.last3()[1:])) or (word.getPluralVal() > 3*word.plFactor):
            return Word("", "")
            
        cPhrasePl = Word("","")
        cPhrasePl.equalTo(word)
        cPhrasePl.setText(self.revPhWords(word.getText(), "-"))
        
        if(word.getPluralVal() > 3*word.plFactor):
            return Word("", "")

        if (self.sizChainSub(cPhrasePl, "םיי")):
            change = self.lstChain(cPhrasePl.getText(), "םיי")
            if((cPhrasePl.isPhrase()) and (change > -1)) and (cPhrasePl.getExphLen() > 3):
                plW = Word("","")
                plW.equalTo(cPhrasePl)
                plW.setText(plW.getText().replace("-םיי", " "))
                plW.setText(self.FinalChain(plW.getText()))
                plW.setText(plW.getText().replace(" ", "-"))
                plWt = Word("","")
                plWt.equalTo(plW)
                if(change > 0):
                    plWt.setDual()
                    if(not(word.getTense() == 'Participle')):
                        plWt.setNoun()
                    plWt.setText(self.revPhWords(plWt.getText(), "-"))
                    if (self.FindHelper(look, plWt, self.Dict, Check) == True):
                        return plWt
                
                changC = self.lstChain(cPhrasePl.getText(), "יי")
                if(changC > -1):
                    plWc = Word("","")
                    plWc.equalTo(cPhrasePl)
                    plWc.setText(plWc.getText().replace("-יי", " "))
                    plWc.setText(self.FinalChain(plWc.getText()))
                    plWc.setText(plWc.getText().replace(" ", "-"))
                    if(changC > 0):
                        if(not(word.getTense() == 'Participle')):
                            plWc.setNoun()
                        plWc.setDual()
                        #plWc.setConstruct()
                        plWc.setText(self.revPhWords(plWc.getText(), "-"))
                        if(self.FindHelper(look, plWc, self.Dict, Check) == True):
                            return plWc
                    
                plWh = Word("","")
                plWh.equalTo(cPhrasePl)
                plWh.setText(plWh.getText().replace("-םיי", "-ה"))
                plWh.addToValue(1)
                if(change > 0):
                    if(not(word.getTense() == 'Participle')):
                        plWh.setNoun()
                    plWh.setDual2()
                    plWh.setText(self.revPhWords(plWh.getText(), "-"))
                    if(self.FindHelper(look, plWh, self.Dict, Check) == True):
                        return plWh
            
            plural = False
            cPhrasePl2 = Word("","")
            cPhrasePl2.equalTo(cPhrasePl)
            if(cPhrasePl.getSuffix() == True) or (cPhrasePl.getHeyDir() == True):
                if(cPhrasePl.last2() == 'יי') and (cPhrasePl.getLstLen() > 3) and (not (cPhrasePl.getTense() == 'Perfect')) and (not((cPhrasePl.getRootLast2() == self.Final(cPhrasePl.last3()[1:])) or (cPhrasePl.getRootLast2() == cPhrasePl.last2()))):
                    plural = True
                    plW = Word("","")
                    plW.equalTo(cPhrasePl)
                    plW.setText(self.Final(cPhrasePl.getText()[2:]))
                    cPhrasePl2.equalTo(plW)
                    if(not(word.getTense() == 'Participle')):
                        plW.setNoun()
            else:
                if(cPhrasePl.last3() == 'םיי') and (cPhrasePl.getLstLen() > 4) and (not (cPhrasePl.getTense() == 'Perfect')):
                    plural = True
                    plW = Word("","")
                    plW.equalTo(cPhrasePl)
                    plW.setText(self.Final(cPhrasePl.getText()[3:]))
                    if(not(word.getTense() == 'Participle')):
                        plW.setNoun()
                        
            if plural == True:
                singleW = Word("","")
                singleW.equalTo(plW)
                    
                plW.setDual()
                change2 = self.lstChain(cPhrasePl.getText(), cPhrasePl.last3())
                if((cPhrasePl.isPhrase()) and (change2 > -1)):
                    plW.setText(plW.getText().replace("-םיי", " "))
                    plW.setText(self.FinalChain(plW.getText()))
                    plW.setText(plW.getText().replace(" ", "-"))
                    plWt = Word("","")
                    plWt.equalTo(plW)
                    plWt.setText(self.revPhWords(plWt.getText(), "-"))
                    if (self.FindHelper(look, plWt, self.Dict, Check) == True):
                        return plWt
                        
                    if(plW.getLstLen() > 1):
                        if(plW.last() == "ת"):
                            plWth = Word("","")
                            plWth.equalTo(plW) 
                            plWth.setText('ה' + plW.getText()[1:])
                            plWth.addToValue(0.5)
                            plWth.setText(self.revPhWords(plWth.getText(), "-"))
                            self.FindHelper(look, plWth, self.Dict, Check)
                     
                    changeC2 = self.lstChain(cPhrasePl.getText(), "יי")
                    if(changeC2 > -1) and (cPhrasePl.getLstLen() > 2):
                        plWc = Word("","")
                        plWc.equalTo(cPhrasePl)
                        if(cPhrasePl.getSuffix() == True) or (cPhrasePl.getHeyDir() == True):
                            plWc.setText(self.Final(cPhrasePl.getText()[2:]))
                        elif cPhrasePl.getLstLen() > 3:
                            plWc.setText(self.Final(cPhrasePl.getText()[3:]))
                        plWc.setText(plWc.getText().replace("-יי", " "))
                        plWc.setText(self.FinalChain(plWc.getText()))
                        plWc.setText(plWc.getText().replace(" ", "-"))
                        if(not(word.getTense() == 'Participle')):
                            plWc.setNoun()
                        plWc.setDual()
                        
                        if(plWc.getLen() > 1):
                            if(plWc.last() == "ת"):
                                plWch = Word("","")
                                plWch.equalTo(plWc) 
                                plWch.setText('ה' + plWc.getText()[1:])
                                plWch.addToValue(0.5)
                                plWch.setText(self.revPhWords(plWch.getText(), "-"))
                                self.FindHelper(look, plWch, self.Dict, Check)
                                
                        if(changeC2 > 0):
                            #plWc.setConstruct()
                            plWc.setText(self.revPhWords(plWc.getText(), "-"))
                            if(self.FindHelper(look, plWc, self.Dict, Check) == True):
                                return plWc
                        
                    plWh = Word("","")
                    plWh.equalTo(cPhrasePl)
                    if(cPhrasePl.getLstLen() > 2) and ((cPhrasePl.getSuffix() == True) or (cPhrasePl.getHeyDir() == True)):
                        plWh.setText('ה' + cPhrasePl.getText()[2:])
                    elif cPhrasePl.getLstLen() > 3:
                        plWh.setText('ה' + cPhrasePl.getText()[3:])
                    plWh.setText(plWh.getText().replace("-םיי", "-ה"))
                    plWh.addToValue(1)
                    if(not(word.getTense() == 'Participle')):
                        plWh.setNoun()
                    plWh.setDual2()
                    plWh.setText(self.revPhWords(plWh.getText(), "-"))
                    self.algorithm(look, plWh, Check)
                    if(change2 > 0):
                        if(self.FindHelper(look, plWh, self.Dict, Check) == True):
                            return plWh
                else:
                    Go2 = False
                    if((cPhrasePl2.getLen() > 2) and ((cPhrasePl2.getSuffix() == True) or (cPhrasePl2.getHeyDir() == True))):
                        Go2 = True
                    if(cPhrasePl2.getLen() > 3):               
                        if((not((cPhrasePl2.getRoot()[:2] == self.Final(cPhrasePl2.lastX(4)[2:])) or (cPhrasePl2.getRoot()[-2:] == cPhrasePl2.lastX(4)[2:]) or (cPhrasePl2.getRoot() == cPhrasePl2.last3())))):
                            Go2 = True
                            
                    if(Go2 == True):
                        plW2 = Word("","")
                        plW2.equalTo(plW)
                        plW2.setText(self.revPhWords(plW2.getText(), "-"))
                        self.FindHelper(look, plW2, self.Dict, Check)
                        self.algorithm(look, plW2, Check)
                        
                        if(plW.getLen() > 1):
                            if(plW.last() == "ת"):
                                plWWh = Word("","")
                                plWWh.equalTo(plW) 
                                plWWh.setText('ה' + plW.getText()[1:])  
                                plWWh.addToValue(0.5)
                                if(plWWh.hasRoot()) and (plWWh.getLen() > 2):
                                    if(plWWh.getRoot()[1:] == plWWh.last3()[1:]):
                                        plWWh.setRoot(plWWh.last3())
                                plWWh.setText(self.revPhWords(plWWh.getText(), "-"))
                                self.FindHelper(look, plWWh, self.Dict, Check)
                                    
                    if((cPhrasePl2.getLen() > 3) or ((cPhrasePl2.getLen() > 2) and ((cPhrasePl2.getSuffix() == True) or (cPhrasePl2.getHeyDir() == True)))):
                        if(not((cPhrasePl2.getRoot()[:2] == self.Final(cPhrasePl2.last3()[1:])) or (cPhrasePl2.getRoot()[-2:] == cPhrasePl2.last3()[1:]))):
                            singleW.setText('ה' + self.unFinal(plW.getText()))
                            singleW.setDual2()
                            singleW.addToValue(1)
                            if(singleW.hasRoot()) and (singleW.getLen() > 2):
                                if(singleW.getRoot()[1:] == singleW.last3()[1:]):
                                    singleW.setRoot(singleW.last3())
                            singleW.setText(self.revPhWords(singleW.getText(), "-"))
                            self.FindHelper(look, singleW, self.Dict, Check)
                            self.algorithm(look, singleW, Check)
                            tempWf2 = Word("","")
                            tempWf2.equalTo(plW)
                            tempWf2.setText('י' + self.unFinal(plW.getText()))
                            tempWf2.addToValue(1)
                            if(tempWf2.hasRoot()) and (tempWf2.getLen() > 2):
                                if(tempWf2.getRoot()[1:] == tempWf2.last3()[1:]):
                                    tempWf2.setRoot(tempWf2.last3())
                            tempWf2.setText(self.revPhWords(tempWf2.getText(), "-"))
                            self.FindHelper(look, plW, self.Dict, Check)
                            self.FindHelper(look, tempWf2, self.Dict, Check)
                    
                plW.setText(self.revPhWords(plW.getText(), "-"))
                #return plW

        if(self.sizChainSub(cPhrasePl, "םי")):
            change3 = self.lstChain(cPhrasePl.getText(), "םי")
            if((cPhrasePl.isPhrase()) and (change3 > -1)) and (cPhrasePl.getExphLen() > 2):
                plW = Word("","")
                plW.equalTo(cPhrasePl)
                plW.setText(plW.getText().replace("-םי", " "))
                plW.setText(self.FinalChain(plW.getText()))
                plW.setText(plW.getText().replace(" ", "-"))
                plWt = Word("","")
                plWt.equalTo(plW)
                if(change3 > 0):
                    plWt.setPlural()
                    plWt.setGender(0)
                    if(not(word.getTense() == 'Participle')):
                        plWt.setNoun()
                    plWt.setText(self.revPhWords(plWt.getText(), "-"))
                    if(self.FindHelper(look, plWt, self.Dict, Check) == True):
                        return plWt
                
                change3C = self.lstChain(cPhrasePl.getText(), "י")
                if(change3C > -1):
                    plWc = Word("","")
                    plWc.equalTo(cPhrasePl)
                    plWc.setText(plWc.getText().replace("-י", " "))
                    plWc.setText(self.FinalChain(plWc.getText()))
                    plWc.setText(plWc.getText().replace(" ", "-"))
                    if(change3C > 0):
                        if(not(word.getTense() == 'Participle')):
                            plWc.setNoun()
                        plWc.setPlural()
                        plWc.setGender(0)
                        plWc.setText(self.revPhWords(plWc.getText(), "-"))
                        if(self.FindHelper(look, plWc, self.Dict, Check) == True):
                            return plWc
                        
                plWh = Word("","")
                plWh.equalTo(cPhrasePl)
                plWh.setText(plWh.getText().replace("-םי", "-ה"))
                plWh.addToValue(1)
                if(change3 > 0):
                    if(not(word.getTense() == 'Participle')):
                        plWh.setNoun()
                    plWh.setPlural2()
                    plWh.setGender(0)
                    plWh.setText(self.revPhWords(plWh.getText(), "-"))
                    if(self.FindHelper(look, plWh, self.Dict, Check) == True):
                        return plWh
            
            plural = False
            cPhrasePl2 = Word("","")
            cPhrasePl2.equalTo(cPhrasePl)
            if((cPhrasePl.getSuffix() == True) or (cPhrasePl.getHeyDir() == True)):
                if(cPhrasePl.last() == 'י') and (not((cPhrasePl.nextToLast() + cPhrasePl.thirdFromLast()) == 'תו')) and (cPhrasePl.getLstLen() > 2) and (not (cPhrasePl.getTense() == 'Perfect')) and (not(cPhrasePl.getRootLast2() == cPhrasePl.last2())):
                    plural = True
                    plW = Word("","")
                    plW.equalTo(cPhrasePl)
                    plW.setText(self.Final(cPhrasePl.getText()[1:]))
                    cPhrasePl2.equalTo(plW)
                    if(not(word.getTense() == 'Participle')):
                        plW.setNoun()
            else:            
                if(cPhrasePl.getLstLen() > 2) and (cPhrasePl.last2() == 'םי') and (not (cPhrasePl.getTense() == 'Perfect')):
                    plural = True
                    plW = Word("","")
                    plW.equalTo(cPhrasePl)
                    plW.setText(self.Final(cPhrasePl.getText()[2:]))
                    if(not(word.getTense() == 'Participle')):
                        plW.setNoun()
                
            if plural == True:                
                singleW = Word("","")
                singleW.equalTo(plW)
                    
                plW.setPlural()
                change4 = self.lstChain(cPhrasePl2.getText(), cPhrasePl2.last2())
                if(((cPhrasePl2.isPhrase()) and ((change4) > -1)) and ((cPhrasePl2.getExphLen() > 2) or ((cPhrasePl2.getExphLen() > 1) and ((cPhrasePl2.getSuffix() == True) or (cPhrasePl2.getHeyDir() == True))))):
                    plW.setText(plW.getText().replace("-םי", " "))
                    plW.setText(self.FinalChain(plW.getText()))
                    plW.setText(plW.getText().replace(" ", "-"))
                    plWt = Word("","")
                    plWt.equalTo(plW)
                    plWt.setGender(0)
                    plWt.setText(self.revPhWords(plWt.getText(), "-"))
                    if(self.FindHelper(look, plWt, self.Dict, Check) == True) and (cPhrasePl.getSuffix() == False) and (cPhrasePl.getHeyDir() == False):
                        return plWt
                        
                    if(plW.getLstLen() > 1):
                        if(plW.last() == "ת"):
                            plWth = Word("","")
                            plWth.equalTo(plW)
                            plWth.setText('ה' + plW.getText()[1:])
                            plWth.addToValue(0.5)
                            plWth.setText(self.revPhWords(plWth.getText(), "-"))
                            self.FindHelper(look, plWth, self.Dict, Check)
                    
                    changeC4 = self.lstChain(cPhrasePl.getText(), "י")
                    if(changeC4 > -1) and (cPhrasePl.getLstLen() > 1):
                        plWc = Word("","")
                        plWc.equalTo(cPhrasePl)
                        if(cPhrasePl.getSuffix() == True) or (cPhrasePl.getHeyDir() == True):
                            plWc.setText(self.Final(cPhrasePl.getText()[1:]))
                        elif cPhrasePl.getLstLen() > 2:
                            plWc.setText(self.Final(cPhrasePl.getText()[2:]))
                        plWc.setText(plWc.getText().replace("-י", " "))
                        plWc.setText(self.FinalChain(plWc.getText()))
                        plWc.setText(plWc.getText().replace(" ", "-")) 
                        if(not(word.getTense() == 'Participle')):
                            plWc.setNoun()
                        plWc.setPlural()
                        
                        if(plWc.getLstLen() > 1):
                            if(plWc.last() == "ת"):
                                plWch = Word("","")
                                plWch.equalTo(plWc) 
                                plWch.setText('ה' + plWc.getText()[1:])
                                plWch.addToValue(0.5)
                                plWch.setText(self.revPhWords(plWch.getText(), "-"))
                                self.FindHelper(look, plWch, self.Dict, Check)
                        
                        if(changeC4 > 0):
                            #plWc.setConstruct()
                            plWc.setGender(0)
                            plWc.setText(self.revPhWords(plWc.getText(), "-"))
                            if(self.FindHelper(look, plWc, self.Dict, Check) == True) and (cPhrasePl.getSuffix() == False) and (cPhrasePl.getHeyDir() == False):
                                return plWc
                            
                    plWh = Word("","")
                    plWh.equalTo(cPhrasePl)
                    if(cPhrasePl.getLstLen() > 1) and ((cPhrasePl.getSuffix() == True) or (cPhrasePl.getHeyDir() == True)):
                        plWh.setText('ה' + cPhrasePl.getText()[1:])
                        plWh.addToValue(1)
                    elif cPhrasePl.getLstLen() > 2:
                        plWh.setText('ה' + cPhrasePl.getText()[2:])
                    plWh.setText(plWh.getText().replace("-םי", "-ה"))
                    plWh.addToValue(1)
                    plWh.setPlural2()
                    if(not(word.getTense() == 'Participle')):
                        plWh.setNoun()
                    plWh.setGender(0)
                    plWh.setText(self.revPhWords(plWh.getText(), "-"))
                    self.algorithm(look, plWh, Check)
                    if(change4 > 0):
                        if(self.FindHelper(look, plWh, self.Dict, Check) == True) and (cPhrasePl.getSuffix() == False) and (cPhrasePl.getHeyDir() == False):
                            return plWh
                else:
                    Go = False
                    if((cPhrasePl2.getLen() > 1) and ((cPhrasePl2.getSuffix() == True) or (cPhrasePl2.getHeyDir() == True))):
                        Go = True
                    if(cPhrasePl2.getLen() > 2):               
                        if(not((cPhrasePl2.getRoot()[:2] == self.Final(cPhrasePl2.last3()[1:])) or (cPhrasePl2.getRoot()[-2:] == cPhrasePl2.last3()[1:]))):
                            Go = True
                            
                    if(Go == True):
                        plW2 = Word("","")
                        plW2.equalTo(plW)
                        plW2.setGender(0)
                        plW2.setText(self.revPhWords(plW2.getText(), "-"))
                        self.FindHelper(look, plW2, self.Dict, Check)
                        self.algorithm(look, plW2, Check)
                        if(plW.getLstLen() > 1):
                            if(plW.last() == "ת"):
                                plWWh = Word("","")
                                plWWh.equalTo(plW) 
                                plWWh.setText('ה' + plW.getText()[1:])   
                                plWWh.addToValue(0.5)
                                if(plWWh.hasRoot()) and (plWWh.getLen() > 2):
                                    if(plWWh.getRoot()[1:] == plWWh.last3()[1:]):
                                        plWWh.setRoot(plWWh.last3())
                                plWWh.setText(self.revPhWords(plWWh.getText(), "-"))
                                self.FindHelper(look, plWWh, self.Dict, Check)
                        
                    if((cPhrasePl2.getLen() > 2) or ((cPhrasePl2.getLen() > 1) and ((cPhrasePl2.getSuffix() == True) or (cPhrasePl2.getHeyDir() == True)))):
                        if(not(cPhrasePl2.getRoot()[:2] == cPhrasePl2.last2())):
                            singleW.setText('ה' + self.unFinal(plW.getText()))
                            singleW.addToValue(1)
                            singleW.setPlural2()
                            if(singleW.hasRoot()) and (singleW.getLstLen() > 2):
                                if(singleW.getRoot()[1:] == singleW.last3()[1:]):
                                    singleW.setRoot(singleW.last3())
                            singleW.setText(self.revPhWords(singleW.getText(), "-"))
                            self.FindHelper(look, singleW, self.Dict, Check)
                            self.algorithm(look, singleW, Check)
                            tempWf2 = Word("","")
                            tempWf2.equalTo(plW)
                            tempWf2.setText('י' + self.unFinal(plW.getText()))
                            tempWf2.addToValue(1)
                            if(tempWf2.hasRoot()) and (tempWf2.getLstLen() > 2):
                                if(tempWf2.getRoot()[1:] == tempWf2.last3()[1:]):
                                    tempWf2.setRoot(tempWf2.last3())
                            tempWf2.setText(self.revPhWords(tempWf2.getText(), "-"))
                            self.FindHelper(look, tempWf2, self.Dict, Check)
                plW.setText(self.revPhWords(plW.getText(), "-"))
                if(cPhrasePl.getSuffix() == False) and (cPhrasePl.getHeyDir() == False):
                    return plW
            
            cPhrasePl2 = Word("","")
            cPhrasePl2.equalTo(cPhrasePl)
            if(cPhrasePl.getLen() > 3) and (cPhrasePl.getLstLen() > 2):
                if((cPhrasePl.getSuffix() == True) or (cPhrasePl.getHeyDir() == True)) and (cPhrasePl.last() == 'י') and ((cPhrasePl.nextToLast() + cPhrasePl.thirdFromLast()) == 'תו') and (not(cPhrasePl.getRoot()[:2] == cPhrasePl.last2())):
                    cPhrasePl2.setText(self.Final(cPhrasePl.getText()[1:]))
                    cPhrasePl2.setText(self.revPhWords(cPhrasePl2.getText(), "-"))
                    self.FindHelper(look, cPhrasePl2, self.Dict, Check)
                    cPhrasePl2 = Word("","")
                    cPhrasePl2.equalTo(cPhrasePl)
                    cPhrasePl2.setText(self.Final(cPhrasePl.getText()[1:]))
                    
            changef = self.lstChain(cPhrasePl2.getText(), "תו")

            if((cPhrasePl2.isPhrase()) and (changef > -1)) and (cPhrasePl2.getExphLen() > 2):
                plW = Word("","")
                plW.equalTo(cPhrasePl2)
                plW.setText(plW.getText().replace("-תו", " "))
                plW.setText(self.FinalChain(plW.getText()))
                plW.setText(plW.getText().replace(" ", "-"))
                if(changef > 0):
                    if(not(word.getTense() == 'Participle')):
                        plW.setNoun()
                    plW.setPlural2()
                    plW.setGender(1)
                    plW.setText(self.revPhWords(plW.getText(), "-"))
                    self.algorithm(look, plW, Check)
                    if(self.FindHelper(look, plW, self.Dict, Check) == True):
                        return plW
                
                plW.equalTo(cPhrasePl2)
                plW.setText(plW.getText().replace("-תו", "-ה"))
                plW.addToValue(-0.5)
                if(changef > 0):
                    if(not(word.getTense() == 'Participle')):
                        plW.setNoun()
                    plW.setPlural()
                    plW.setGender(1)
                    plW.setText(self.revPhWords(plW.getText(), "-"))
                    self.algorithm(look, plW, Check)
                    if(self.FindHelper(look, plW, self.Dict, Check) == True):
                        return plW
                       
                plW.equalTo(cPhrasePl2)
                plW.setText(plW.getText().replace("-תו", "-ת"))
                if(changef > 0):
                    if(not(word.getTense() == 'Participle')):
                        plW.setNoun()
                    plW.setGender(1)
                    plW.setPlural()
                    plW.setText(self.revPhWords(plW.getText(), "-"))
                    self.algorithm(look, plW, Check)
                    if(self.FindHelper(look, plW, self.Dict, Check) == True):
                        return plW       
                
            if(cPhrasePl2.last2() == 'תו') and (not (cPhrasePl2.getTense() == 'Perfect')) and (not(cPhrasePl2.getTense() == 'Imperfect')) and (not(cPhrasePl2.getTense() == 'Imperative')) and (not(cPhrasePl2.getTense() == 'Infinitive')):
                changef2 = self.lstChain(cPhrasePl2.getText(), cPhrasePl2.last2())
                if((cPhrasePl2.isPhrase()) and (changef2 > -1)) and (cPhrasePl2.getLstLen() > 2):
                    plW = Word("","")
                    plW.equalTo(cPhrasePl2)
                    plW.setText(self.Final(plW.getText()[2:]))
                    plW.setText(plW.getText().replace("-תו", " "))
                    plW.setText(self.FinalChain(plW.getText()))
                    plW.setText(plW.getText().replace(" ", "-"))
                    if(not(word.getTense() == 'Participle')):
                        plW.setNoun()
                    plW.setPlural2()
                    plW.setGender(1)
                    plW.setText(self.revPhWords(plW.getText(), "-"))
                    self.algorithm(look, plW, Check)
                    if(self.FindHelper(look, plW, self.Dict, Check) == True):
                        return plW
                    
                    plW = Word("","")
                    plW.equalTo(cPhrasePl2)
                    plW.setText('ה' + cPhrasePl2.getText()[2:])
                    plW.setText(plW.getText().replace("-תו", "-ה"))
                    if(not(word.getTense() == 'Participle')):
                        plW.setNoun()
                    plW.setPlural()
                    plW.setGender(1)
                    plW.addToValue(-0.5)
                    plW.setText(self.revPhWords(plW.getText(), "-"))
                    self.algorithm(look, plW, Check)
                    if(self.FindHelper(look, plW, self.Dict, Check) == True):
                        return plW
                        
                    plW.equalTo(cPhrasePl2)
                    plW.setText('ת' + cPhrasePl2.getText()[2:])
                    plW.addToValue(0.5)
                    plW.setText(plW.getText().replace("-תו", "-ת"))
                    if(not(word.getTense() == 'Participle')):
                        plW.setNoun()
                    plW.setPlural()
                    plW.setGender(1)
                    plW.setText(self.revPhWords(plW.getText(), "-"))
                    self.algorithm(look, plW, Check)
                    if(self.FindHelper(look, plW, self.Dict, Check) == True):
                        return plW
                elif cPhrasePl2.getLstLen() > 2:
                    plW = Word("","")
                    plW.equalTo(cPhrasePl2)
                    plW.setText(cPhrasePl2.Final(cPhrasePl2.getText()[2:]))
                    plW.setPlural()
                    plW.setGender(1)
                    if(not(word.getTense() == 'Participle')):
                        plW.setNoun()
                        
                    singleW = Word("","")
                    singleW.equalTo(plW)
                    
                    singleWt = Word("","")
                    singleWt.equalTo(plW)
                    
                    plW.setPlural2()
                    if(not((cPhrasePl2.getRoot()[:2] == self.Final(cPhrasePl2.last3()[1:])) or (cPhrasePl2.getRoot()[-2:] == cPhrasePl2.last3()[1:]))):
                        plW2 = Word("","")
                        plW2.equalTo(plW)
                        plW2.setText(self.revPhWords(plW2.getText(), "-"))
                        self.FindHelper(look, plW2, self.Dict, Check)
                        self.algorithm(look, plW2, Check)
                    
                    if(not(cPhrasePl2.getRoot()[:2] == cPhrasePl2.last2())):
                        singleW.setText('ה' + self.unFinal(plW.getText()))
                        #singleW.setPlural()
                        singleW.addToValue(-0.5)
                        if(singleW.hasRoot()) and (singleW.getLen() > 2):
                            if(singleW.getRoot()[1:] == singleW.last3()[1:]):
                                singleW.setRoot(singleW.last3())
                        singleW.setText(self.revPhWords(singleW.getText(), "-"))
                        
                        singleWt.setText('ת' + self.unFinal(plW.getText()))
                        singleWt.setPlural()
                        if(singleWt.hasRoot()) and (singleWt.getLen() > 2):
                            if(singleWt.getRoot()[1:] == singleWt.last3()[1:]):
                                singleWt.setRoot(singleWt.last3())
                        singleWt.setText(self.revPhWords(singleWt.getText(), "-"))
                        
                        self.FindHelper(look, singleW, self.Dict, Check)
                        self.FindHelper(look, singleWt, self.Dict, Check)
                        self.algorithm(look, singleW, Check)
                    if(cPhrasePl2.getLen() > 3) and (not((cPhrasePl2.getRoot()[:2] == self.Final(cPhrasePl2.last3()[1:])) or (cPhrasePl2.getRoot()[-2:] == cPhrasePl2.last3()[1:]))):
                        if(plW.last() == 'י') and (plW.getLstLen() > 1):
                            if(not(plW.getRoot()[:2] == plW.last2())):
                                plW2 = Word("","")
                                plW2.equalTo(plW)
                                plW2.setText(cPhrasePl2.Final(plW.getText()[1:]))
                                plW2.setText(self.revPhWords(plW2.getText(), "-"))
                                self.FindHelper(look, plW2, self.Dict, Check)
                                self.algorithm(look, plW2, Check)
                                plW2.setText(self.revPhWords(plW2.getText(), "-"))
                            singleW2 = Word("","")
                            singleW2.equalTo(plW)
                            singleW2.setText('ה' + plW.getText()[1:])
                            singleW2.addToValue(1)
                            if(singleW2.hasRoot()) and (singleW2.getLen() > 2):
                                if(singleW2.getRoot()[1:] == singleW2.last3()[1:]):
                                    singleW2.setRoot(singleW2.last3())
                            singleW2.setText(self.revPhWords(singleW2.getText(), "-"))
                            self.FindHelper(look, singleW2, self.Dict, Check)
                            self.algorithm(look, singleW2, Check)
                            return singleW2
        
        if(cPhrasePl.isPhrase()):
            return Word("","")
            
        constr = Word("","")
        constr.equalTo(self.constr(look, cPhrasePl, Check))
        if not (constr.getText() == ""):
            self.algorithm(look, constr, Check)
        #return constr
        return Word("","")
            
    def prefixRuls(self, word, p, h):
        cPhraseSuf2 = Word("","")
        cPhraseSuf2.equalTo(self.CurrentWord)
        cPhraseSuf2.setText(self.revPhWords(self.CurrentWord.getText(), "-"))
        if(word.getVerbform() in Pual) or (word.getVerbform() in Niphal) or (word.getVerbform() in Piel) or (word.getPartiVal() == 1):
            return False
        if(word.getVerbform() in Piel) or ((word.getPrefix() == True) and (h == False) and ((word.getVerbform() in Hithpeal)or(word.getVerbform() in Hiphil)or(word.getVerbform() in Hophal))) or (word.getRoot()[-2:] == word.first2()):
            return False
            
        prep = ['מ', 'ב', 'ל']
        
        revCW = self.rev(cPhraseSuf2.getText())
        posTov = revCW.find("ת", 0, 4)
        if not ((posTov == -1) or (posTov == 0)):
            if(revCW[posTov-1] == 'ה') and (word.getVerbform() in Hithpeal):
                return False
        if (word.isTense() == True) or (word.getTense() == 'Infinitive') or (word.getVerbform in Niphal) or ((word.getVerbform() in Hophal) and (cPhraseSuf2.first() == 'ה'))or((word.getVerbform() in Hiphil) and (cPhraseSuf2.first() == 'ה')): #((word.getTense() == 'Perfect') and ('ו' in word.getPrixList())) or 
            return False
        if ((word.getHey1() > 0) and (p in prep)):
            return False
        if (p in word.getPrixList()):
            return False
        if ((p in prep) and (word.getPrixListEnd() in prep)) and (not((p == 'ב')and(word.getPrixListEnd() == 'מ'))): 
            return False
        if (word.isVavSeq() == True):
            return False
        if ((p == 'ו') and (word.getPrefix() == True)):
            return False
        if ((not(p == 'תת')) and (word.getPrixListEnd() == 'תת')):
            return False
        if (('ה' in word.getPrixList()) and (not(p == 'תת'))):
            return False
        if (word.getPrixListEnd() == p):
            return False
        if (p == 'כ') and (('ל' in word.getPrixList()) or ('כ' in word.getPrixList()) or (word.getPrixListEnd() == 'ש') or (word.getPrixListEnd() == 'מ')):
            return False
        if (p == 'ה') and (word.isVerb() == True):
            return False
        #if(word.getLen() > 2):
           # if(word.second() == 'ו') and (not (word.XtoY(1, 3) == "וו")) and (not (word.XtoY(1, 3) == "וי")) and (h == False):
           #     return False
        return True
            
    def prefix(self, look, word, h, Check):
        if(word.getLen() < 2):
            return Word("","")
        
        if not (word.isPhrase()):
            return self.smPrefix(look, word, h, Check)
            
        cPhrasePre = Word("","")
        cPhrasePre.equalTo(word)
        cPhrasePre = Word("","")
        cPhrasePre.equalTo(word)
          
        preChain1 = Word("","")
        preChain1.equalTo(self.prexChain(look, cPhrasePre, Check))
        if (not(preChain1.getText() == "")):
            return preChain1
        
        cPhrasePre.setText(self.revPhWords(cPhrasePre.getText(), "-"))

        if(cPhrasePre.getFrsLen() > 3): 
            if (cPhrasePre.first2() in prefixL) and (self.prefixRuls(cPhrasePre, cPhrasePre.first2(), False) == True):
                preW = Word("","")
                preW.equalTo(cPhrasePre)
                preW.setText(cPhrasePre.getText()[:-2])
                preW.setPrefixN(prefixV[cPhrasePre.first2()])
                preW.addPre(cPhrasePre.first2())
                preW.setText(self.revPhWords(preW.getText(), "-"))
                
                self.FindHelper(look, preW, self.Dict, Check) 
                self.plural(look, preW, Check)
                self.suffix(look, preW, 1, Check)
                preWend = Word("","")
                preWend.equalTo(self.prefix(look, preW, False, Check))
                if preWend.getText() == "":
                    return preW
                else:
                    return preWend
                    
        if(cPhrasePre.getFrsLen() > 2):
            if (cPhrasePre.first() in prefixL) and (self.prefixRuls(cPhrasePre, cPhrasePre.first(), False) == True):
                preW = Word("","")
                preW.equalTo(cPhrasePre)
                preW.setText(cPhrasePre.getText()[:-1])
                preW.setPrefixN(prefixV[cPhrasePre.first()])
                preW.addPre(cPhrasePre.first())
                preW.setText(self.revPhWords(preW.getText(), "-"))
                
                self.FindHelper(look, preW, self.Dict, Check) 
                self.plural(look, preW, Check)
                self.suffix(look, preW, 1, Check)
                preWend = Word("","")
                preWend.equalTo(self.prefix(look, preW, False, Check))
                if preWend.getText() == "":
                    return preW
                else:
                    return preWend
                
        return Word("", "")
    
    def prexChain(self, look, word, Check):
        if(word.getLen() < 2):
            return Word("", "")
              
        temp1 = Word("", "")
        temp1.equalTo(word)
        temp1.setText(self.revPhWords(temp1.getText(), "-"))
        
        if(temp1.getFrsLen() < 2) or (temp1.last2() == "ה-") or ("-ה-" in temp1.getText()):
            return Word("", "")
            
        s = temp1.getText().count("ה-")
        if s == 0:
            return Word("", "")
        
        for i in range(1, s + 1):
            temp2 = Word("", "")
            temp2.equalTo(temp1)
            temp2.setText(temp1.getText().replace("ה-", "-", i))
            if(not('ה' in temp2.getPrixList())):
                temp2.setPrefixN(temp2.heyVal)
                temp2.addPre('ה')
                
            temp2.setText(self.revPhWords(temp2.getText(), "-"))
            if self.FindHelper(look, temp2, self.Dict, Check) == True:
                return temp2
                
            self.plural(look, temp2, Check)
            self.suffix(look, temp2, 1, Check)
            
        return Word("", "")

    def smPrefix(self, look, word, h, Check):
        if(word.getLen() < 2) or (not((self.CurrentWord.first() in prefixL) or (self.CurrentWord.first2() in prefixL))) or (word.isPhrase()): #or (word.getModern == True):
            return Word("","")
            
        if(word.getLen() > 2):
            if(word.first2() in prefixL):
                preW = Word("","")
                preW.equalTo(word)
                if(word.third() == 'ו') and (not((word.isVerbf() == False)or(word.getVerbform() in Qal))):
                    preW.setText(word.getText()[:-3] + 'י')
                    if(preW.getLen() > 3):
                        if(not(preW.hasRoot() and (not(preW.getRoot()[:2] == self.Final(preW.firstX(4)[:2]))))):
                            preW.setRoot(self.Final(preW.first3()))
                else:
                    preW.setText(word.getText()[:-2])
                    
                preW.setPrefixN(prefixV[word.first2()])
                preW.addPre(word.first2())
                self.FindHelper(look, preW, self.Dict, Check)
                self.algorithm(look, preW, Check)
                return preW
                
        
        if(word.first() in prefixL) and (self.prefixRuls(word, word.first(), h) == True):
            preW = Word("","")
            preW.equalTo(word)
            if(word.nextToFirst() == 'ו') and (not((word.isVerbf() == False)or(word.getVerbform() in Qal))):
                preW.setText(word.getText()[:-2] + 'י')
                if(preW.getLen() > 2):
                    if(not(preW.hasRoot() and (not(preW.getRoot()[:2] == self.Final(preW.first3()[:2]))))):
                        preW.setRoot(self.Final(preW.first3()))
            else:
                preW.setText(word.getText()[:-1])
                
            if(word.first() == 'ה') or word.first() == 'ל':
                if word.isVerb() == False:
                    preW.setNoun()
                else:
                    return Word("","")
            preW.setPrefixN(prefixV[word.first()])
            preW.addPre(word.first())
            self.FindHelper(look, preW, self.Dict, Check)
            self.algorithm(look, preW, Check)
            return preW
        return Word("", "")  
    
    def suffix(self, look, word, p, Check):
        if(word.getLen() < 3) or (word.getConstruct() == True) or (word.getModern() == True) or ('ה' in word.getPrixList()) or ((word.isVerb() == True)and(self.CurrentWord.isVerb() == False)) or (word.getVerbform() in Piel) or (word.getSuffix() == True) or (word.getPlural() == True) or (word.getDual() == True) or (not (word.getTenseVal() == -1)) or (word.getModern == True) or (word.getPartiVal() == 0) or (word.getVerbform() in Pual):
            return Word("","")
            
        suff1 = Word("","")
        suff2 = Word("","")
        suff1 = self.suffix1(look, word, Check)
        suff2 = self.suffix2(look, word, Check)
        
        self.suffix3(look, word, Check)

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
        
    def dirHey(self, look, word, Check):
        if(word.getLen() < 2) or (word.getHeyDir() == True) or ('ב' in word.getPrixList())or (word.getModern() == True) or (word.getVerbform() in Piel) or ('ל' in word.getPrixList()) or ('מ' in word.getPrixList()) or (word.isVerb() == True) or (word.getSuffix() == True) or (word.getPlural() == True) or (word.getDual() == True) or (word.getConstruct() == True) or (word.getTense() == 'Participle'):
            return Word("","")
            
        cPhraseHey1 = Word("","")
        cPhraseHey1.equalTo(word)
        cPhraseHey1.setText(self.revPhWords(word.getText(), "-"))
        
        cPhraseHey2 = Word("","")
        cPhraseHey2.equalTo(self.CurrentWord)
        cPhraseHey2.setText(self.revPhWords(word.getText(), "-"))
        
        if(cPhraseHey1.getLstLen() < 3) and (word.isPhrase()):
            return Word("", "")
        if(word.hasRoot() == True):
            if(word.getRoot()[:2] == word.last2()):
                return Word("", "")
        
        if(cPhraseHey2.last() == cPhraseHey1.last()) and (cPhraseHey1.last() == 'ה'):
            hey1W = Word("","")
            hey1W.equalTo(cPhraseHey1)
            hey1W.setText(self.Final(cPhraseHey1.getText()[1:]))
            hey1W.setHey1()
            hey1W.setNoun()

            if(hey1W.getLstLen() > 1):
                last_eq = False
                if(hey1W.hasRoot() == True):
                    if(not (hey1W.getRoot()[:2] == hey1W.last2())):
                        last_eq = True
                        
                if(hey1W.last() == "ת") and (last_eq == False):
                    hey1Wh = Word("","")
                    hey1Wh.equalTo(hey1W) 
                    hey1Wh.setText('ה' + hey1W.getText()[1:])
                    hey1Wh.addToValue(0.5)
                    hey1Wh.setText(self.revPhWords(hey1Wh.getText(), "-"))
                    self.FindHelper(look, hey1Wh, self.Dict, Check)
                    self.algorithm(look, hey1Wh, Check)
                    
            hey1W.setText(self.revPhWords(hey1W.getText(), "-"))
            self.FindHelper(look, hey1W, self.Dict, Check)
            self.algorithm(look, hey1W, Check)
            if(cPhraseHey1.isPhrase()):
                return hey1W

            if(not(hey1W.last() == 'ה')) and (not(cPhraseHey1.last() == 'ה')):
                hey1Wh = Word("","")
                hey1Wh.equalTo(hey1W)
                hey1Wh.setText('ה' + cPhraseHey1.getText()[1:])
                hey1Wh.addToValue(1)
                self.FindHelper(look, hey1Wh, self.Dict, Check)
                self.prefix(look, hey1Wh, False, Check)
                self.verbForms(look, hey1Wh, Check)
                return hey1Wh
                
            return hey1W
                
        return Word("","")
            
    def suffix1(self, look, word, Check):
        if(word.getLstLen() < 2) or ((word.isVerb() == True)and(self.CurrentWord.isVerb() == False)) or (word.getSuffix() == True) or (word.getPlural() == True) or (word.getDual() == True) or (word.getConstruct() == True) or (word.getModern == True) or (word.getPartiVal() == 0) or (word.getVerbform() in Pual):
            return Word("","")
                
        cPhraseSuf = Word("","")
        cPhraseSuf.equalTo(word)
        cPhraseSuf.setText(self.revPhWords(word.getText(), "-"))
        cPhraseSuf2 = Word("","")
        cPhraseSuf2.equalTo(self.CurrentWord)
        cPhraseSuf2.setText(self.revPhWords(self.CurrentWord.getText(), "-"))
        
        if(cPhraseSuf.getLstLen() < 3):
            return Word("", "")
        
        if((cPhraseSuf.last() == 'ה') and (cPhraseSuf.getPlural() == True)) or (cPhraseSuf.getLen() < 3) or (word.getRoot()[:2] == word.last2()):
            return Word("","")
  
        if ((cPhraseSuf2.last() == cPhraseSuf.last()) or (word.getHeyDir() == True)) and (cPhraseSuf.last() in suffix) and (not((cPhraseSuf2.nextToLast() == "י")and(cPhraseSuf.getVerbform() in Hiphil))):
            suffW = Word("","")
            suffW.equalTo(cPhraseSuf)
            suffW.setText(self.Final(cPhraseSuf.getText()[1:]))
            suffW.setSuffixX(cPhraseSuf.last())
            suffW.addSuff(cPhraseSuf.last())
            if(suffW.getLstLen() > 1):
                if(suffW.last() == "ת"):
                    suffWh = Word("","")
                    suffWh.equalTo(suffW) 
                    suffWh.setText('ה' + suffW.getText()[1:])
                    suffWh.addToValue(0.5)
                    suffWh.setGender(1)
                    if(suffWh.hasRoot()) and (suffWh.getLen() > 2):
                        if(suffWh.getRoot()[1:] == suffWh.last3()[1:]):
                            suffWh.setRoot(suffWh.last3())
                    suffWh.setText(self.revPhWords(suffWh.getText(), "-"))
                    self.FindHelper(look, suffWh, self.Dict, Check)
                    self.algorithm(look, suffWh, Check)
                if(suffW.getLen() == 2) and (not(cPhraseSuf.isPhrase())):
                    hollow  = Word("","")
                    hollow.equalTo(suffW)
                    hollow.setText(hollow.last() + 'ו' +  hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    self.FindHelper(look, hollow, self.Dict, Check)
            suffW.setText(self.revPhWords(suffW.getText(), "-"))
            self.FindHelper(look, suffW, self.Dict, Check)
            self.algorithm(look, suffW, Check)
            if(cPhraseSuf.isPhrase()):
                return suffW

            if(suffW.getLen() > 1):
                if(not(cPhraseSuf.last() == 'ה')):
                    suffWh2 = Word("","")
                    suffWh2.equalTo(suffW)
                    suffWh2.setText('ה' + cPhraseSuf.getText()[1:])
                    suffWh2.addToValue(1)
                    if(suffWh2.hasRoot()) and (suffWh2.getLen() > 2):  
                        if(suffWh2.getRoot()[1:] == suffWh2.last3()[1:]):
                            suffWh2.setRoot(suffWh2.last3())
                    self.FindHelper(look, suffWh2, self.Dict, Check)
                    self.prefix(look, suffWh2, False, Check)
                    self.verbForms(look, suffWh2, Check)
                    self.participle(look, suffWh2, False)
                    return suffWh2
                
        return Word("","")

    def suffix2(self, look, word, Check):
        if(word.getLstLen() < 3) or ((word.isVerb() == True)and(self.CurrentWord.isVerb() == False)) or (word.getSuffix() == True) or (word.getPlural() == True) or (word.getDual() == True) or (word.getConstruct() == True) or (word.getModern == True) or (word.getPartiVal() == 0) or (word.getVerbform() in Pual):
            return Word("","")

        cPhraseSuf = Word("","")
        cPhraseSuf.equalTo(word)
        cPhraseSuf.setText(self.revPhWords(word.getText(), "-"))
        cPhraseSuf2 = Word("","")
        cPhraseSuf2.equalTo(self.CurrentWord)
        cPhraseSuf2.setText(self.revPhWords(self.CurrentWord.getText(), "-"))
        
        if(cPhraseSuf.getLstLen() < 4):
            return Word("", "")
            
        if ((cPhraseSuf2.last2() == cPhraseSuf.last2()) or (word.getHeyDir() == True)) and (cPhraseSuf.last2() in suffix) and (not((cPhraseSuf2.nextToLast() == "י")and(cPhraseSuf.getVerbform() in Hiphil))):
            suffW = Word("","")
            suffW.equalTo(cPhraseSuf)
            suffW.setText(self.Final(cPhraseSuf.getText()[2:]))
           
            suffW.setSuffixX(cPhraseSuf.last2())
            suffW.addSuff(cPhraseSuf.last2())    
            if(not((word.getRoot()[:2] == self.Final(word.last3()[1:])) or (word.getRoot()[-2:] == word.last3()[1:]))):
                if(suffW.getLstLen() > 1):
                    if(suffW.last() == "ת"):
                        suffWh = Word("","")
                        suffWh.equalTo(suffW) 
                        suffWh.setText('ה' + suffW.getText()[1:])
                        suffWh.addToValue(0.5)
                        suffWh.setGender(1)
                        if(suffWh.hasRoot()) and (suffWh.getLen() > 2):
                            if(suffWh.getRoot()[1:] == suffWh.last3()[1:]):
                                suffWh.setRoot(suffWh.last3())
                        suffWh.setText(self.revPhWords(suffWh.getText(), "-"))
                        self.FindHelper(look, suffWh, self.Dict, Check)
                        self.algorithm(look, suffWh, Check)
                    if(suffW.getLen() == 2) and (not(cPhraseSuf.isPhrase())):
                        hollow  = Word("","")
                        hollow.equalTo(suffW)
                        hollow.setText(hollow.last() + 'ו' +  hollow.first())
                        hollow.addToValue(1)
                        hollow.setRoot(hollow.getText())
                        self.FindHelper(look, hollow, self.Dict, Check)
                suffW.setText(self.revPhWords(suffW.getText(), "-"))
                self.FindHelper(look, suffW, self.Dict, Check)
                self.algorithm(look, suffW, Check)
                if(cPhraseSuf.isPhrase()):
                    return suffW           
                
                if(suffW.getLen() > 1):
                    if(not(cPhraseSuf.last3()[2:] == 'ה')) and (not ('ה' in cPhraseSuf.getSufxList())) and (not(cPhraseSuf.getRoot()[:2] == cPhraseSuf.last2())):
                        suffWh2 = Word("","")
                        suffWh2.equalTo(suffW)
                        suffWh2.setText('ה' + cPhraseSuf.getText()[2:])
                        suffWh2.addToValue(1)
                        if(suffWh2.hasRoot()) and (suffWh2.getLen() > 2):
                            if(suffWh2.getRoot()[1:] == suffWh2.last3()[1:]):
                                suffWh2.setRoot(suffWh2.last3())
                        self.FindHelper(look, suffWh2, self.Dict, Check)
                        self.prefix(look, suffWh2, False, Check)
                        self.verbForms(look, suffWh2, Check)
                        self.participle(look, suffWh2, False)
                        return suffWh2

        return Word("","")
        
    def suffix3(self, look, word, Check):
        if(word.getLstLen() < 4) or ((word.isVerb() == True)and(self.CurrentWord.isVerb() == False)) or (word.getSuffix() == True) or (word.getPlural() == True) or (word.getDual() == True) or (word.getConstruct() == True) or (word.getModern == True) or (word.getPartiVal() == 0) or (word.getVerbform() in Pual):
            return Word("","")

        cPhraseSuf = Word("","")
        cPhraseSuf.equalTo(word)
        cPhraseSuf.setText(self.revPhWords(word.getText(), "-"))
        cPhraseSuf2 = Word("","")
        cPhraseSuf2.equalTo(self.CurrentWord)
        cPhraseSuf2.setText(self.revPhWords(self.CurrentWord.getText(), "-"))
        
        if(cPhraseSuf.getLstLen() < 5):
            return Word("", "")
            
        if ((cPhraseSuf2.last3() == cPhraseSuf.last3()) or (word.getHeyDir() == True)) and (cPhraseSuf.last3() in suffix) and (not(((cPhraseSuf2.thirdFromLast() == "י")or(cPhraseSuf2.fourthFromLast() == "י"))and(cPhraseSuf.getVerbform() in Hiphil))):
            suffW = Word("","")
            suffW.equalTo(cPhraseSuf)
            suffW.setText(self.Final(cPhraseSuf.getText()[3:]))
            
            suffW.setSuffixX(cPhraseSuf.last3())
            suffW.addSuff(cPhraseSuf.last3())
            if(not((self.unFinal(cPhraseSuf.getRoot()[:2]) == cPhraseSuf.lastX(4)[2:]) or (self.unFinal(cPhraseSuf.getRoot()[:2]) == cPhraseSuf.last3()[1:]) or (cPhraseSuf.getRoot()[:2] == cPhraseSuf.last2()))):
                
                if(suffW.getLstLen() > 1):
                    if(suffW.last() == "ת"):
                        suffWh = Word("","")
                        suffWh.equalTo(suffW) 
                        suffWh.setText('ה' + suffW.getText()[1:])
                        suffWh.addToValue(0.5)
                        suffWh.setGender(1)
                        if(suffWh.hasRoot()) and (suffWh.getLen() > 2):
                            if(suffWh.getRoot()[1:] == suffWh.last3()[1:]):
                                suffWh.setRoot(suffWh.last3())
                        suffWh.setText(self.revPhWords(suffWh.getText(), "-"))
                        self.FindHelper(look, suffWh, self.Dict, Check)
                        self.algorithm(look, suffWh, Check)
                 
                    if(suffW.getLen() == 2) and (not(cPhraseSuf.isPhrase())):
                        hollow  = Word("","")
                        hollow.equalTo(suffW)
                        hollow.setText(hollow.last() + 'ו' +  hollow.first())
                        hollow.addToValue(1)
                        hollow.setRoot(hollow.getText())
                        self.FindHelper(look, hollow, self.Dict, Check)
                suffW.setText(self.revPhWords(suffW.getText(), "-"))
                self.FindHelper(look, suffW, self.Dict, Check)
                self.algorithm(look, suffW, Check)
                if(cPhraseSuf.isPhrase()):
                    return suffW
                   
                if(suffW.getLen() > 1):
                    if(not(cPhraseSuf.lastX(4)[3:] == 'ה')) and (not ('ה' in cPhraseSuf.getSufxList())) and (not((cPhraseSuf.getRoot()[:2] == self.Final(cPhraseSuf.last3()[1:])) or (cPhraseSuf.getRoot()[-2:] == cPhraseSuf.last3()[1:]))):
                        suffWh2 = Word("","")
                        suffWh2.equalTo(suffW)
                        suffWh2.setText('ה' + cPhraseSuf.getText()[3:])
                        suffWh2.addToValue(1)
                        if(suffWh2.hasRoot()) and (suffWh2.getLen() > 2):
                            if(suffWh2.getRoot()[1:] == suffWh2.last3()[1:]):
                                suffWh2.setRoot(suffWh2.last3())
                        self.FindHelper(look, suffWh2, self.Dict, Check)
                        self.prefix(look, suffWh2, False, Check)
                        self.verbForms(look, suffWh2, Check)
                        self.participle(look, suffWh2, False)
                        return suffWh2
                
        return Word("","")
        
    def participle(self, look, word, Check):
        if(word.getLen() < 2) or (word.isPhrase() == True) or (word.isTense() == True):
            return Word("","")
          
        #if(not(word.getVerbform() in Pual)):
        hollow = Word("","")
        hollow.equalTo(word)
        hollow.setTense(2)
        #hollow.setGender(2)
        Holl = False
        
        if(word.getLen() == 2):
            if((not(word.last() == 'ה')) and (not(word.last() == 'ת')) and (not('ה' in word.getSufxList())) and (not('ת' in word.getSufxList()))): 
                hollow.setGender(0)
            else:
                hollow.setGender(1)
            Holl = True
        else:
            if(word.last3() == 'םיי') and (word.getLen() > 4) and (word.getPlural() == False) and ((word.getSuffix() == False) and (word.getHeyDir() == False)):
                if((not((word.getRoot()[:2] == self.Final(word.lastX(4)[2:])) or (word.getRoot()[-2:] == word.lastX(4)[2:]) or (word.getRoot() == word.last3())))):
                    hollow.setText(hollow.Final(hollow.getText()[3:]))
                    hollow.setDual()
                    if(hollow.getLen() > 2):
                        hollow.setRoot(hollow.last3())
                    Holl = True
            elif(word.last2() == 'םי') and (word.getLen() > 3) and (word.getPlural() == False) and ((word.getSuffix() == False) and (word.getHeyDir() == False)):
                if(not((word.getRoot()[:2] == self.Final(word.last3()[1:])) or (word.getRoot()[-2:] == word.last3()[1:]))):
                    hollow.setText(hollow.Final(hollow.getText()[2:]))
                    hollow.setPlural()
                    if(hollow.getLen() > 2):
                        hollow.setRoot(hollow.last3())
                    hollow.setGender(0)
                    Holl = True
            elif(word.last2() == 'תו') and (word.getLen() > 3) and (word.getPlural() == False):
                if(not((word.getRoot()[:2] == self.Final(word.last3()[1:])) or (word.getRoot()[-2:] == word.last3()[1:]))):
                    hollow.setText(hollow.Final(hollow.getText()[2:]))
                    hollow.setPlural()
                    if(hollow.getLen() > 2):
                        hollow.setRoot(hollow.last3())
                    hollow.setGender(1)
                    Holl = True
            elif((word.last() == 'ת')or(word.last() == 'ה')) and (word.getLen() > 2) and (word.getPlural() == False):
                if(not(word.getRoot()[:2] == word.last2())):
                    hollow.setText(hollow.Final(hollow.getText()[1:])) 
                    hollow.addToValue(-2)
                    if(hollow.getLen() > 2):
                        hollow.setRoot(hollow.last3())
                    hollow.setGender(1)
                    Holl = True
                    
        if(hollow.getVerbform() in Niphal):
            if(hollow.getLen() == 3):
                hollow.setRoot(hollow.getText())
                hollow.setPar(0)
                self.FindHelper(look, hollow, self.Dict, Check)

        if((Holl == True) or (hollow.first() == "מ")):
            if(hollow.getLen() == 2):
                hollow2 = Word("","")
                hollow2.equalTo(hollow)
                hollow2.setText(hollow.last() + 'ו' +  hollow.first())
                hollow2.addToValue(1) 
                hollow2.setRoot(hollow2.first3())
                hollow2.setPar(1)
                if(hollow2.isVerbf() == False):
                    hollow2.setVerbform(0)
                self.FindHelper(look, hollow2, self.Dict, Check)
                if(word.last2() == 'תו') and (hollow.getPlural() == True):
                    hollow2.setText('ה' + self.unFinal(hollow2.getText()))
                    hollow2.addToValue(-2)
                    self.FindHelper(look, hollow2, self.Dict, Check)
            elif((word.getVerbform() in Piel) or (word.getVerbform() in Hiphil)):
                if(hollow.getLen() > 3) and (hollow.first() == "מ"):
                    hollow3 = Word("","")
                    hollow3.equalTo(hollow)
                    if(not(hollow.getRoot()[-2:] == hollow.first2())):
                        hollow3.setText(hollow3.getText()[:-1])
                        hollow3.setRoot(hollow3.first3())
                        hollow3.addToValue(1)
                        hollow3.setPar(1)
                        if(hollow3.getLen() > 2):
                            hollow3.setRoot(hollow3.first3())
                        self.FindHelper(look, hollow3, self.Dict, Check)
                        if(word.last2() == 'תו') and (hollow3.getPlural() == True):
                            hollow3.setText('ה' + self.unFinal(hollow3.getText()))
                            hollow3.addToValue(-2)
                            self.FindHelper(look, hollow3, self.Dict, Check)
            elif((word.getVerbform() in Hophal) or (word.getVerbform() in Pual) or (word.getVerbform() in Hithpeal)):
                if(hollow.getLen() > 2) and (hollow.first() == "מ"):
                    hollow4 = Word("","")
                    hollow4.equalTo(hollow)
                    if(hollow.getLen() == 3):
                        hollow4.setText(hollow.last() + 'ו' +  hollow.first2())
                        hollow4.addToValue(1)
                        if(not(hollow.getRoot()[-2:] == hollow.first2())):
                            hollow4.setText(hollow4.getText()[:-1])
                            hollow4.setRoot(hollow4.first3())
                            hollow4.setPar(0)
                            if(hollow4.getLen() > 2):
                                hollow4.setRoot(hollow4.first3())
                            self.FindHelper(look, hollow4, self.Dict, Check)
                            if(word.last2() == 'תו') and (hollow4.getPlural() == True):
                                hollow4.setText('ה' + self.unFinal(hollow4.getText()))
                                hollow4.addToValue(-2)
                                self.FindHelper(look, hollow4, self.Dict, Check)
        
        if(word.getLen() < 3):
            return Word("","")
            
        uther = False
        isPar = False
        
        if("מ" in word.getText()) and (not(word.last() == "מ")):
            rVcW = Word("", "")
            rVcW.setText(self.rev(self.CurrentWord.getText()))
            if ('מ' in word.getPrixList()): 
                frsM = rVcW.getText().index("מ")
                iM = rVcW.getText()[frsM+1:].index("מ") + frsM + 1
            else:
                iM = rVcW.getText().index("מ")
                
            if(rVcW.getText()[iM + 1] == "י"):
                uther = True
        
        if(word.last() == 'ת') and (not((word.third() == 'ו')and(not(word.first() == 'מ')))) and (not(word.getConstruct() == True)) and (not(word.getPlural() == True)) and (not(word.getRoot()[:2] == word.last2())) and (word.getLen() > 4):
            fimW = Word("","")
            fimW.equalTo(word)
            yod = False
            fimW.setText(self.Final(word.getText()[1:]))
            #if(word.getGenderVal() == -1):
            fimW.addToValue(2)
            fimW.setGender(1)
            pfimW = Word("","")
            
            if(fimW.first() == 'מ') and (not(fimW.getRoot()[-2:] == fimW.first2())):
                if(fimW.nextToFirst() == 'ו'):
                    fimW.setText(fimW.getText()[:-2] + 'י' + fimW.first())
                    #fimW.addToValue(1)
                    yod = True
                    if(fimW.getLen() < 5):
                        pYad = Word("","")
                        pYad.equalTo(fimW)
                        pYad.setText(fimW.getText()[:-1])
                        if(pYad.getLen() > 2):
                            if(not(pYad.hasRoot() and ((pYad.getRoot()[1:] == pYad.first2())))):
                                pYad.setRoot(self.Final(pYad.first3()))
                            pYad.setTense(2)
                            if((pYad.getVerbform() in Hophal) or (pYad.getVerbform() in Pual) or (pYad.getVerbform() in Hithpeal)):
                                pYad.setPar(0)
                            else:
                                pYad.setPar(1)
                            self.FindHelper(look, pYad, self.Dict, Check)
                if(fimW.getLen() > 4):# and ((fimW.isVerbf() == False) or (fimW.getVerbform() == 'Qal')):
                    if(fimW.third() == 'ו') and (self.num_of_a_roots(fimW.getText()[:-5]) == 0) and (not(fimW.getRootFirst2()  == fimW.first2())) and (not((fimW.hasRoot == True) and (not((fimW.getRootFirst2()  == fimW.first3()[:-1]) or (fimW.getRootFirst2() == fimW.XtoY(2, 4)))))):
                        pfimW.equalTo(fimW)
                        pfimW.setText(fimW.getText()[:-3] + fimW.nextToFirst())
                        #pfimW.addToValue(-2) 
                        if(pfimW.getLen() > 2):
                            #if(not(pfimW.hasRoot() and (not((pfimW.getRoot()[:-1] == self.Final(pfimW.first3()[:-1]))or(self.unFinal(pfimW.getRoot()[:1] + pfimW.getRoot()[-1:]) == pfimW.first2()))))):
                            pfimW.setRoot(self.Final(pfimW.first3()))
                            if fimW.first() == 'ת':
                                pfimW.Ht = False
                            pfimW.setTense(2)
                            if((word.getVerbform() in Hophal) or (word.getVerbform() in Pual) or (word.getVerbform() in Hithpeal)):
                                pfimW.setPar(0)
                            else:
                                pfimW.setPar(1)
                            if((pfimW.getPlural() == True) or (pfimW.getDual() == True)) and (not(('ה' in pfimW.getPrixList())or('ל' in pfimW.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                                pfimW.unSetNoun()
                            pfimWh = Word("","")
                            pfimWh.equalTo(pfimW)
                            pfimWh.setText('ה' + self.unFinal(pfimW.getText()))
                            pfimWh.addToValue(-4)
                            self.FindHelper(look, pfimW, self.Dict, Check)
                            self.FindHelper(look, pfimWh, self.Dict, Check)
                            self.algorithm(look, pfimW, Check)
                            if word.getVerbform() == '':
                                return pfimW
                                
                    if((fimW.nextToLast() == 'ו') and (fimW.getX(4) == 'ו')) and (self.num_of_p_roots(fimW.getText()[4:]) == 0) and (not(fimW.last() == 'י')) and (not(fimW.last() == 'ו')) and (fimW.getLen() > 4) and (not(fimW.getRootFirst2()  == fimW.first2())) and (not((fimW.hasRoot()) and (not((fimW.getRootLast2() == self.Final(fimW.last3()[1:])) or (fimW.getRootLast2() == fimW.last2()))))):
                        isPar = True
                        pfimW2 = Word("","")
                        pfimW2.equalTo(fimW)
                        
                        pfimW2.setText(fimW.last() + fimW.getText()[2:-1])
                        pfimW2.addToValue(-2) 
                        if(pfimW2.getLen() > 2):
                            #if(not(pfimW2.hasRoot() and (not((pfimW2.getRoot()[1:] == pfimW2.first2())or(self.unFinal(pfimW2.getRoot()[:1] + pfimW2.getRoot()[-1:]) == pfimW2.first3()[:-1]))))):
                            pfimW2.setRoot(self.Final(pfimW2.last3()))
                            pfimW2.setTense(2)
                            if((word.getVerbform() in Piel) or (word.getVerbform() in Hiphil)):
                                pfimW2.setPar(1)
                            else:
                                pfimW2.setPar(0)
                            if((pfimW2.getPlural() == True) or (pfimW2.getDual() == True)) and (not(('ה' in pfimW2.getPrixList())or('ל' in pfimW2.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                                pfimW2.unSetNoun()
                            pfimWh = Word("","")
                            pfimWh.equalTo(pfimW2)
                            pfimWh.setText('ה' + self.unFinal(pfimW2.getText()))
                            pfimWh.addToValue(-4)
                            self.FindHelper(look, pfimW2, self.Dict, Check)
                            self.FindHelper(look, pfimWh, self.Dict, Check)
                            #self.algorithm(look, pfimW2, Check) 
                            if word.getVerbform() == '':
                                return pfimW2
                    
                if((fimW.getLen() > 3) and (((word.getVerbform() in Piel) and (uther == False)) or (word.getVerbform() in Hiphil)) or (yod == True)) and (not(fimW.getRootFirst2()  == fimW.first2())):
                    isPar = True
                    pfimW2 = Word("","")
                    pfimW2.equalTo(fimW)
                    pfimW2.setText(fimW.getText()[:-1])
                    #if(not(pfimW2.hasRoot() and (not(pfimW2.getRootLast2() == self.Final(pfimW2.first3()[:2]))))):
                    pfimW2.setRoot(self.Final(pfimW2.first3()))
                    pfimW2.setTense(2)
                    pfimW2.setPar(1)
                    if((pfimW2.getPlural() == True) or (pfimW2.getDual() == True)) and (not(('ה' in pfimW2.getPrixList())or('ל' in pfimW2.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                        pfimW2.unSetNoun()
                    pfimWh = Word("","")
                    pfimWh.equalTo(pfimW2)
                    pfimWh.setText('ה' + self.unFinal(pfimW2.getText()))
                    pfimWh.addToValue(-4)
                    self.FindHelper(look, pfimW2, self.Dict, Check)
                    self.FindHelper(look, pfimWh, self.Dict, Check)
                    self.algorithm(look, pfimW2, Check) 
                    return pfimW2
                    
                if(fimW.getLen() > 3) and ((word.getVerbform() in Hophal) or (word.getVerbform() in Pual) or (word.getVerbform() in Hithpeal)) and (not(fimW.getRootFirst2()  == fimW.first2())):
                    isPar = True
                    pfimW2 = Word("","")
                    pfimW2.equalTo(fimW)
                    pfimW2.setText(fimW.getText()[:-1])
                    if(not(pfimW2.hasRoot() and (not(pfimW2.getRoot()[:2] == self.Final(pfimW2.first3()[:2]))))):
                        pfimW2.setRoot(self.Final(pfimW2.first3()))
                        pfimW2.setTense(2)
                        pfimW2.setPar(0)
                        if((pfimW2.getPlural() == True) or (pfimW2.getDual() == True)) and (not(('ה' in pfimW2.getPrixList())or('ל' in pfimW2.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                            pfimW2.unSetNoun()
                        pfimWh = Word("","")
                        pfimWh.equalTo(pfimW2)
                        pfimWh.setText('ה' + self.unFinal(pfimW2.getText()))
                        pfimWh.addToValue(-4)
                        self.FindHelper(look, pfimW2, self.Dict, Check)
                        self.FindHelper(look, pfimWh, self.Dict, Check)
                        self.algorithm(look, pfimW2, Check) 
                        return pfimW2
                        
                elif(fimW.getLen() > 3) and (not((fimW.getVerbform() in Qal)or(fimW.getVerbform() in Niphal))) and (not(fimW.getRootFirst2()  == fimW.first2())):
                    isPar = True
                    pfimW2 = Word("","")
                    pfimW2.equalTo(fimW)
                    pfimW2.setText(fimW.getText()[:-1])
                    if(not(pfimW2.hasRoot() and (not(pfimW2.getRoot()[:2] == self.Final(pfimW2.first3()[:2]))))):
                        pfimW2.setRoot(self.Final(pfimW2.first3()))
                        pfimW2.setTense(2)
                        pfimW2.setPar(2)
                        pfimW2.setVerbform(17)
                        if((pfimW2.getPlural() == True) or (pfimW2.getDual() == True)) and (not(('ה' in pfimW2.getPrixList())or('ל' in pfimW2.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                            pfimW2.unSetNoun()
                        pfimWh = Word("","")
                        pfimWh.equalTo(pfimW2)
                        pfimWh.setText('ה' + self.unFinal(pfimW2.getText()))
                        pfimWh.addToValue(-4)
                        pfimWh.setGender(1)
                        self.FindHelper(look, pfimW2, self.Dict, Check)
                        self.FindHelper(look, pfimWh, self.Dict, Check)
                        self.algorithm(look, pfimW2, Check) 
                        return pfimW2
                return fimW
                
            if(fimW.getLen() > 3) and (word.isVerbf() == False) or (word.getVerbform() in Qal) or (word.getVerbform() in Niphal):
                if(fimW.nextToFirst() == 'ו') and ((word.isVerbf() == False) or (word.getVerbform() in Qal)) and (self.num_of_a_roots(fimW.getText()[:-4]) == 0) and (not((fimW.hasRoot == True) and (not((fimW.getRootFirst2()  == fimW.first2()) or (fimW.getRootFirst2() == fimW.XtoY(1, 3)))))):
                    isPar = True
                    pfimW.equalTo(fimW)
                    pfimW.setText(fimW.getText()[:-2] + fimW.first())
                    #pfimW.addToValue(-2)
                    if(pfimW.getLen() > 2):
                        #if(not(pfimW.hasRoot() and (not((pfimW.getRoot()[:-1] == self.Final(pfimW.first3()[:-1]))or(self.unFinal(pfimW.getRoot()[:1] + pfimW.getRoot()[-1:]) == pfimW.first2()))))):
                        pfimW.setRoot(self.Final(pfimW.first3()))
                        if fimW.first() == 'ת':
                            pfimW.Ht = False
                        pfimW.setTense(2)
                        pfimW.setPar(1)
                        if((pfimW.getPlural() == True) or (pfimW.getDual() == True)) and (not(('ה' in pfimW.getPrixList())or('ל' in pfimW.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                            pfimW.unSetNoun()
                        pfimWh = Word("","")
                        pfimWh.equalTo(pfimW)
                        pfimWh.setText('ה' + self.unFinal(pfimW.getText()))
                        pfimWh.addToValue(-4)
                        self.FindHelper(look, pfimW, self.Dict, Check)
                        self.FindHelper(look, pfimWh, self.Dict, Check)
                        self.algorithm(look, pfimW, Check)        
                if((fimW.nextToLast() == 'ו') and (fimW.third() == 'ו')) and (not((fimW.hasRoot()) and (not((fimW.getRootLast2() == self.Final(fimW.last3()[1:])) or (fimW.getRootLast2() == fimW.last2()))))) and (self.num_of_p_roots(fimW.getText()[4:]) == 0):# and (not(fimW.last() == 'י')) and (not(fimW.last() == 'ו')) and (fimW.getLen() > 3):
                    isPar = True
                    pfimW2 = Word("","")
                    pfimW2.equalTo(fimW)
                    pfimW2.setText(fimW.last() + fimW.getText()[2:])
                    #pfimW2.addToValue(-2)
                    if(pfimW2.getLen() > 2):
                        #if(pfimW2.hasRoot() and (not((pfimW2.getRoot()[1:] == pfimW2.last3()[1:])or(pfimW2.getRoot()[:1] + pfimW2.getRoot()[-1:] == pfimW2.last2())))):
                        pfimW2.setRoot(self.Final(pfimW2.last3()))
                        pfimW2.setTense(2)
                        pfimW2.setPar(0)
                        if((pfimW2.getPlural() == True) or (pfimW2.getDual() == True)) and (not(('ה' in pfimW2.getPrixList())or('ל' in pfimW2.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                            pfimW2.unSetNoun()
                        pfimWh = Word("","")
                        pfimWh.equalTo(pfimW2)
                        pfimWh.setText('ה' + self.unFinal(pfimW2.getText()))
                        pfimWh.addToValue(-4)
                        self.FindHelper(look, pfimW2, self.Dict, Check)
                        self.FindHelper(look, pfimWh, self.Dict, Check)
                       #self.algorithm(look, pfimW2, Check)
                        return pfimW2
            return fimW    
        else:
            pword = Word("","")
            pword.equalTo(word)
            d = 0
            if (word.getSuffix1() == True) or (word.getHey1() > 0):
                d = 1
            if word.getSuffix2() == True:
                d = 2
            if(word.first() == 'מ') and (not(word.getRoot()[-2:] == word.first2())):
                word2 = Word("","")
                word2.equalTo(pword)
                if(word2.getLen() > 5) and (word2.last() == 'ה') and (not((word.second() == 'ו')and(not(word.first() == 'מ')))):
                    word2.setText(self.Final(word2.getText()[1:]))
                    word2.addToValue(2)
                    word2.setGender(1)
                elif(not(word.getGenderVal() == 1)):
                    word2.setGender(0)
                if(word2.nextToFirst() == 'ו'):
                    word2.setText(word2.getText()[:-2] + 'י' + word2.first())
                    if(word2.getLen() < 5):
                        pYad = Word("","")
                        pYad.equalTo(word2)
                        pYad.setText(word2.getText()[:-1])
                        if(pYad.getLen() > 2):
                            if(not(pYad.hasRoot() and ((pYad.getRoot()[1:] == pYad.first2())))):
                                pYad.setRoot(self.Final(pYad.first3()))
                            pYad.setTense(2)
                            if((word.getVerbform() in Hophal) or (word.getVerbform() in Pual) or (word.getVerbform() in Hithpeal)):
                                pYad.setPar(0)
                            else:
                                pYad.setPar(1)
                            self.FindHelper(look, pYad, self.Dict, Check)
                if(word2.getLen() > 4):# and ((word2.isVerbf() == False) or (word2.getVerbform() == 'Qal')):
                    if((word2.nextToLast() == 'ו') and (word2.getX(4) == 'ו')) and (self.num_of_p_roots(word2.getText()[4:]) == 0) and (not(word2.getRootFirst2()  == word2.first2())) and (not((word2.hasRoot()) and (not((word2.getRootLast2() == self.Final(word2.last3()[1:])) or (word2.getRootLast2() == word2.last2()))))):
                        isPar = True
                        pword.equalTo(word2)
                        pword.setText(word2.last() + word2.getText()[2:-1])
                        if(pword.getLen() > 2):
                            #if(not(pword.hasRoot() and (not((pword.getRoot()[1:] == pword.first2())or(self.unFinal(pword.getRoot()[:1] + pword.getRoot()[-1:]) == pword.first3()[:-1]))))):
                            pword.setRoot(self.Final(pword.last3()))
                            pword.setTense(2)
                            if((word.getVerbform() in Piel) or (word.getVerbform() in Hiphil)):
                                pword.setPar(1)
                            else:
                                pword.setPar(0)
                            if(not(self.CurrentWord.last() == 'י')):
                                pword.resetConstruct()
                            if((pword.getPlural() == True) or (pword.getDual() == True)) and (not(('ה' in pword.getPrixList())or('ל' in pword.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                                pword.unSetNoun()
                            if word2.first() == 'ת':
                                pword.Ht = False
                            self.FindHelper(look, pword, self.Dict, Check)
                            self.algorithm(look, pword, Check)
                            if word.getVerbform() == '':
                                return pword
                                
                    if(word2.third() == 'ו') and (word2.getLen() > 4) and (self.num_of_a_roots(word2.getText()[:-5]) == 0) and (not(word2.getRootFirst2()  == word2.first2())) and (not((word2.hasRoot == True) and (not((word2.getRootFirst2()  == word2.first3()[:-1]) or (word2.getRootFirst2() == word2.XtoY(2, 4)))))):
                        isPar = True
                        pword2 = Word("","")
                        pword2.equalTo(word2)
                        pword2.setText(word2.getText()[:-3] + word2.nextToFirst())
                        if(pword2.getLen() > 2):
                            #if(not(pword2.hasRoot() and (not((pword2.getRoot()[:-1] == self.Final(pword2.first3()[:-1]))or(self.unFinal(pword2.getRoot()[:1] + pword2.getRoot()[-1:]) == pword2.first2()))))):
                            pword2.setRoot(pword2.first3())
                            pword2.setTense(2)
                            if((word.getVerbform() in Hophal) or (word.getVerbform() in Pual) or (word.getVerbform() in Hithpeal)):
                                pword2.setPar(0)
                            else:
                                pword2.setPar(1)
                            if(not(self.CurrentWord.last() == 'י')):
                                pword2.resetConstruct()
                            if((pword2.getPlural() == True) or (pword2.getDual() == True)) and (not(('ה' in pword2.getPrixList())or('ל' in pword2.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                                pword2.unSetNoun()
                            self.FindHelper(look, pword2, self.Dict, Check)
                            self.algorithm(look, pword2, Check)
                            if word.getVerbform() == '':
                                return pword2
                
                if(word2.getLen() > 3) and (((word.getVerbform() in Piel) and (uther == False)) or (word.getVerbform() in Hiphil)) and (not(word2.getRootFirst2()  == word2.first2())):
                    isPar = True
                    pword2 = Word("","")
                    pword2.equalTo(word2)
                    pword2.setText(word2.getText()[:-1])
                    #if(not(pword2.hasRoot() and (not(pword2.getRoot()[:2] == self.Final(pword2.first3()[:2]))))):
                    pword2.setRoot(self.Final(pword2.first3()))
                    pword2.setTense(2)
                    pword2.setPar(1)
                    if(not(self.CurrentWord.last() == 'י')):
                        pword2.resetConstruct()
                    if((pword2.getPlural() == True) or (pword2.getDual() == True)) and (not(('ה' in pword2.getPrixList())or('ל' in pword2.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                        pword2.unSetNoun()
                    self.FindHelper(look, pword2, self.Dict, Check)
                    self.algorithm(look, pword2, Check) 
                    return pword2
                    
                if(word2.getLen() > 3) and ((word.getVerbform() in Hophal) or (word.getVerbform() in Pual) or (word.getVerbform() in Hithpeal)) and (not(word2.getRootFirst2() == word2.first2())):
                    isPar = True
                    pword2 = Word("","")
                    pword2.equalTo(word2)
                    pword2.setText(word2.getText()[:-1])
                    pword2.setRoot(self.Final(pword2.first3()))
                    pword2.setTense(2)
                    pword2.setPar(0)
                    if(not(self.CurrentWord.last() == 'י')):
                        pword2.resetConstruct()
                    if((pword2.getPlural() == True) or (pword2.getDual() == True)) and (not(('ה' in pword2.getPrixList())or('ל' in pword2.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                        pword2.unSetNoun()
                    self.FindHelper(look, pword2, self.Dict, Check)
                    self.algorithm(look, pword2, Check) 
                    return pword2
                    
                elif(word2.getLen() > 3) and (not((word2.getVerbform() in Qal)or(word2.getVerbform() in Niphal))) and (not(word2.getRootFirst2() == word2.first2())):
                    isPar = True
                    pword2 = Word("","")
                    pword2.equalTo(word2)
                    pword2.setText(word2.getText()[:-1])
                    pword2.setRoot(self.Final(pword2.first3()))
                    pword2.setTense(2)
                    pword2.setPar(2)
                    pword2.setVerbform(17)
                    if(not(self.CurrentWord.last() == 'י')):
                        pword2.resetConstruct()
                    if((pword2.getPlural() == True) or (pword2.getDual() == True)) and (not(('ה' in pword2.getPrixList())or('ל' in pword2.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                        pword2.unSetNoun()
                    self.FindHelper(look, pword2, self.Dict, Check)
                    self.algorithm(look, pword2, Check) 
                    return pword2
                return word2
                    
            if(word.isVerbf() == False) or (word.getVerbform() in Qal) or (word.getVerbform() in Niphal):
                word3 = Word("","")
                word3.equalTo(word)
                if(word.getLen() > 4) and ((word.last() == 'ת') or (word.last() == 'ה')) and (not(word.getPlural() == True)):
                    word3.setText(self.Final(word.getText()[1:]))
                    word3.addToValue(1)
                    word3.setGender(1)
                    
                elif(not(word.getGenderVal() == 1)):
                    word3.setGender(0)
                if(word3.nextToFirst() == 'ו') and ((word.isVerbf() == False) or (word.getVerbform() in Qal)) and (self.num_of_a_roots(word3.getText()[:-4]) == 0) and (not((word3.hasRoot == True) and (not((word3.getRootFirst2()  == word3.first2()) or (word3.getRootFirst2() == word3.XtoY(1, 3)))))): 
                    isPar = True
                    pword.equalTo(word3)
                    pword.setText(word3.getText()[:-2] + word3.first())
                    if(pword.getLen() > 2):
                        #if(not(pword.hasRoot() and (not((pword.getRoot()[:-1] == self.Final(pword.first3()[:-1]))or(self.unFinal(pword.getRoot()[:1] + pword.getRoot()[-1:]) == pword.first2()))))):
                        pword.setRoot(self.Final(pword.first3()))
                        pword.setTense(2)
                        pword.setPar(1)
                        if(not(self.CurrentWord.last() == 'י')):
                            pword.resetConstruct()
                        if((pword.getPlural() == True) or (pword.getDual() == True)) and (not(('ה' in pword.getPrixList())or('ל' in pword.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                            pword.unSetNoun()
                        if word3.first() == 'ת':
                            pword.Ht = False
                        if(not(word.last() == 'ה')):
                            pwordh = Word("","")
                            pwordh.equalTo(pword)
                            pwordh.setText('ה' + self.unFinal(pword.getText()))
                            if(word.last() == 'ת'):
                                pwordh.addToValue(-4)
                            else:
                                pwordh.addToValue(1)
                            self.FindHelper(look, pwordh, self.Dict, Check)
                        self.FindHelper(look, pword, self.Dict, Check)
                        if(not(word3.getVerbform() in Qal)):
                            self.algorithm(look, pword, Check)      
                if((word3.nextToLast() == 'ו') and (word3.third() == 'ו')) and (not((word3.hasRoot()) and (not((word3.getRootLast2() == self.Final(word3.last3()[1:])) or (word3.getRootLast2() == word3.last2()))))) and (self.num_of_p_roots(word3.getText()[4:]) == 0):# and (not(word3.last() == 'י')) and (not(word3.last() == 'ו')):
                    isPar = True
                    pword2 = Word("","")
                    pword2.equalTo(word3)
                    pword2.setText(word3.last() + word3.getText()[2:])
                    if(pword2.getLen() > 2):
                        #if(not(pword2.hasRoot() and (not((pword2.getRoot()[1:] == pword2.last3()[1:])or(pword2.getRoot()[:1] + pword2.getRoot()[-1:] == pword2.last2()))))): 
                        pword2.setRoot(pword2.last3())
                        pword2.setTense(2)
                        pword2.setPar(0)
                        if(not(self.CurrentWord.last() == 'י')):
                            pword2.resetConstruct()
                        if((pword2.getPlural() == True) or (pword2.getDual() == True)) and (not(('ה' in pword2.getPrixList())or('ל' in pword2.getPrixList()))) and (self.CurrentWord.isNoun() == False):
                            pword2.unSetNoun()
                        if(not(word.last() == 'ה')):   
                            pword2h = Word("","")
                            pword2h.equalTo(pword2)
                            pword2h.setText('ה' + self.unFinal(pword2.getText()))
                            if(word.last() == 'ת'):
                                pword2h.addToValue(-4)
                            else:
                                pword2h.addToValue(1)
                            self.FindHelper(look, pword2h, self.Dict, Check)
                        self.FindHelper(look, pword2, self.Dict, Check)
                        #self.algorithm(look, pword2, Check)
                        return pword2
            if isPar == True:
                return pword
        return Word("", "")
     
    def constr(self, look, word, Check):
        if(word.getLen() < 2) or (word.getConstruct() == True) or (word.getVerbform() in Piel) or (word.isVerb() == True) or (word.getTense() == 'Perfect') or (word.getTense() == 'Imperfect') or (word.getTense() == 'Imperative') or (word.getTense() == 'Infinitive') or (word.getPartiVal() == 0) or ((not(word.getPartiVal() == 2))and(word.last() == 'ת')) or (word.getRoot()[:2] == word.last2()):
            return Word("", "")
    
        if(word.isPhrase()):
            return self.phCostr(look, word, Check)
        Rt = False
        if(word.getLen() > 2):
            if(word.last() == 'י') and ((self.CurrentWord.last() == 'י')or(word.getSuffix() == True)or(word.getHeyDir() == True)) and (not('ם' in word.getSufxList())) and (not(word.getPlural() == True)) and (not(word.getDual() == True)) and (not (word.getRoot()[:2] == word.last2())):
                constW = Word("","")
                constW.equalTo(word)
                constW.setText(self.Final(constW.getText()[1:]))
                constW.setGender(0)
                if(word.last2() == 'יי'):
                    if(word.getSuffix() == False) and (word.getHeyDir() == False) and (not((word.getRoot()[:2] == self.Final(word.last3()[1:])) or (word.getRoot()[-2:] == word.last3()[1:]))):
                        dualW = Word("","")
                        dualW.equalTo(word)
                        dualW.setText(self.Final(constW.getText()[1:]))
                        dualW.setDual()
                        dualW.setConstruct()
                        dualW.setNoun()
                        if(dualW.last() == 'ת'):
                            dualWt = Word("", "")
                            dualWt.equalTo(dualW)
                            dualWt.setText('ה' + dualW.getText()[1:])
                            dualWt.addToValue(1)
                            self.FindHelper(look, dualWt, self.Dict, Check)
                        if(dualW.getLen() == 2):
                            hollow  = Word("","")
                            hollow.equalTo(dualW)
                            hollow.setText(hollow.last() + 'ו' +  hollow.first())
                            hollow.addToValue(1)
                            hollow.setRoot(hollow.getText())
                            self.FindHelper(look, hollow, self.Dict, Check)
                            if(hollow.last() == 'ת'):
                                hollowt = Word("", "")
                                hollowt.equalTo(hollow)
                                hollowt.setText('ה' + hollowt.getText()[1:])
                                hollowt.addToValue(1)
                                self.FindHelper(look, hollowt, self.Dict, Check)
                        self.FindHelper(look, dualW, self.Dict, Check)
                        self.algorithm(look, dualW, Check)
                    
                    dualW2 = Word("","")
                    dualW2.equalTo(word)
                    dualW2.setText('ם' + word.getText())
                    if(word.getSuffix() == False) and (word.getHeyDir() == False):
                        dualW2.setConstruct()
                    dualW2.addToValue(1)
                    dualW2.setNoun()
                    self.FindHelper(look, dualW2, self.Dict, Check)
                    self.participle(look, dualW2, False)
                    
                    if(not(word.getRoot()[:2] == word.last2())):
                        dualW3 = Word("", "")
                        dualW3.equalTo(word)
                        dualW3.setText('ה' + constW.getText()[1:])
                        dualW3.addToValue(1)
                        dualW3.setConstruct2()
                        dualW3.setDual()
                        if(dualW3.hasRoot()) and (dualW3.getLen() > 2):
                            if(dualW3.getRoot()[1:] == dualW3.last3()[1:]):
                                dualW3.setRoot(dualW3.last3())
                        self.FindHelper(look, dualW3, self.Dict, Check)
                        #self.algorithm(look, dualW3, Check)
                        self.participle(look, dualW3, False)
                    
                else:  
                    if(word.getSuffix() == False) and (word.getHeyDir() == False) and (not(word.getRoot()[:2] == word.last2())):
                        constW.setPlural()
                        constW.setConstruct()                     
                        constW.setNoun()
                        Rt = True
                        if(constW.last() == 'ת'):
                            constWt = Word("", "")
                            constWt.equalTo(constW)
                            constWt.setText('ה' + constW.getText()[1:])
                            constWt.addToValue(1)
                            self.FindHelper(look, constWt, self.Dict, Check)
                        if(constW.getLen() == 2):
                            hollow  = Word("","")
                            hollow.equalTo(constW)
                            hollow.setText(hollow.last() + 'ו' +  hollow.first())
                            hollow.addToValue(1)
                            hollow.setRoot(hollow.getText())
                            self.FindHelper(look, hollow, self.Dict, Check)
                            if(hollow.last() == 'ת'):
                                hollowt = Word("", "")
                                hollowt.equalTo(hollow)
                                hollowt.setText('ה' + hollowt.getText()[1:])
                                hollowt.addToValue(1)
                                self.FindHelper(look, hollowt, self.Dict, Check)
                        self.FindHelper(look, constW, self.Dict, Check)
                        self.algorithm(look, constW, Check)
                    
                    constW2 = Word("","")
                    constW2.equalTo(word)
                    constW2.setText('ם' + word.getText())
                    constW2.addToValue(1)
                    constW2.setGender(0)
                    if(word.getSuffix() == False) and (word.getHeyDir() == False):  
                        constW2.setConstruct()
                    constW2.setNoun()
                    self.FindHelper(look, constW2, self.Dict, Check)   
                    if(word.getSuffix() == False) and (word.getHeyDir() == False):
                        constW3 = Word("", "")
                        constW3.equalTo(word)
                        constW3.setText('ה' + word.getText()[1:])
                        constW3.addToValue(1)
                        constW3.setConstruct2()
                        constW3.setPlural()
                        if(constW3.hasRoot()) and (constW3.getLen() > 2):
                            if(constW3.getRoot()[1:] == constW3.last3()[1:]):
                                constW3.setRoot(constW3.last3())
                        self.FindHelper(look, constW3, self.Dict, Check)
                        self.participle(look, constW3, False)
                    
                    if Rt == True:
                        return constW
                
        if(word.getLen() > 2) and (word.last() == 'ת') and (self.CurrentWord.last() == 'ת'):
            if(not(word.getRoot()[:2] == word.last2())):
                constW = Word("","")
                constW.equalTo(word)
                constW.setText(self.Final(word.getText()[1:]))
                constW.setNoun()
                if(word.getPlural() == False):
                    constW.setConstruct2()
                    constW.setGender(1)
                if(constW.getLen() == 2):
                    hollow  = Word("","")
                    hollow.equalTo(constW)
                    hollow.setText(hollow.last() + 'ו' +  hollow.first())
                    hollow.addToValue(1)
                    hollow.setRoot(hollow.getText())
                    self.FindHelper(look, hollow, self.Dict, Check)
                    
                self.FindHelper(look, constW, self.Dict, Check)
                self.participle(look, constW, False)
                self.irreg(look, constW, Check)
                
            constW2 = Word("", "")
            constW2.equalTo(word)
            constW2.setText('ה' + word.getText()[1:])
            constW2.setNoun()
            constW2.addToValue(-1)
            constW2.setGender(1)
            if(constW2.hasRoot()) and (constW2.getLen() > 2):
                if(constW2.getRoot()[1:] == constW2.last3()[1:]):
                    constW2.setRoot(constW2.last3())
            if(word.getPlural() == False):
                constW2.setConstruct()
            self.FindHelper(look, constW2, self.Dict, Check)
            self.algorithm(look, constW2, Check)
            return constW2
        return Word("", "") 
                
    def phCostr(self, look, word, Check):
    
        PhraseCostr = Word("","")
        PhraseCostr.equalTo(word)
        PhraseCostr.setText(self.revPhWords(word.getText(), "-"))
        
        PhraseCurrent = Word("","")
        PhraseCurrent.equalTo(self.CurrentWord)
        PhraseCurrent.setText(self.revPhWords(self.CurrentWord.getText(), "-"))
    
        if(word.getLstLen() > 2):
            if (PhraseCostr.last() == 'י') and ((PhraseCurrent.last() == 'י')or(PhraseCostr.getSuffix() == True)or(word.getHey1() > 0)) and (not('ם' in PhraseCostr.getSufxList())):
                constW = Word("","")
                constW.equalTo(PhraseCostr)
                constW.setText(self.Final(constW.getText()[1:]))
                constW.setGender(0)
                if(PhraseCostr.last2() == 'יי'):
                    dualW = Word("","")
                    dualW.equalTo(PhraseCostr)
                    dualW.setText(self.Final(constW.getText()[1:]))
                    dualW.setDual()
                    dualW.setNoun()
                    
                    dualW3 = Word("", "")
                    dualW3.equalTo(dualW)
                    
                    dualW.setConstruct()
                    dualW.setText(self.revPhWords(dualW.getText(), "-"))
                    self.FindHelper(look, dualW, self.Dict, Check)
                    self.algorithm(look, dualW, Check)
                    
                    dualW2 = Word("","")
                    dualW2.equalTo(PhraseCostr)
                    dualW2.setText('ם' + PhraseCostr.getText())
                    dualW2.setConstruct()
                    dualW2.addToValue(1)
                    dualW2.setNoun()
                    dualW2.setText(self.revPhWords(dualW2.getText(), "-"))
                    self.FindHelper(look, dualW2, self.Dict, Check)
                    
                    dualW3.setText('ה' + constW.getText()[1:])
                    dualW3.addToValue(1)
                    dualW.setConstruct2()
                    dualW3.setText(self.revPhWords(dualW3.getText(), "-"))
                    self.FindHelper(look, dualW3, self.Dict, Check)
                    self.algorithm(look, dualW3, Check)
                    
                else:   
                    constW.setPlural()
                    constW.setNoun()
                    constW.setText(self.revPhWords(constW.getText(), "-"))
                    
                    constW3 = Word("", "")
                    constW3.equalTo(constW)
                    
                    constW.setConstruct()
                    
                    self.FindHelper(look, constW, self.Dict, Check)
                    self.algorithm(look, constW, Check)
                    
                    constW2 = Word("","")
                    constW2.equalTo(PhraseCostr)
                    constW2.setText('ם' + PhraseCostr.getText())
                    constW2.addToValue(1)
                    constW2.setConstruct()
                    constW2.setGender(0)
                    constW2.setNoun()
                    constW2.setText(self.revPhWords(constW2.getText(), "-"))
                    self.FindHelper(look, constW2, self.Dict, Check)
                    #self.algorithm(look, constW2, Check)
                    constW3.setText('ה' + PhraseCostr.getText()[1:])
                    constW3.addToValue(1)
                    constW3.setConstruct2()
                    constW3.chanGender(2)
                    constW3.setText(self.revPhWords(constW3.getText(), "-"))
                    self.FindHelper(look, constW3, self.Dict, Check)
                    self.algorithm(look, constW3, Check)
                    
                    return constW
                    
        if(word.getLstLen() > 2) and (PhraseCostr.last() == 'ת') and (not (PhraseCostr.getTense() == 'Perfect')) and (not(PhraseCostr.getTense() == 'Imperfect')) and (not(PhraseCostr.getTense() == 'Imperative')) and (not(PhraseCostr.getTense() == 'Infinitive')):
            if('-' in PhraseCostr.getText()):
                plW = Word("","")
                plW.equalTo(PhraseCostr)
                plW.setText(PhraseCostr.Final(PhraseCostr.getText()[1:]))
                plW.setNoun()
                plW.setConstruct2()
                plW.setGender(1)
                plW.setText(self.revPhWords(plW.getText(), "-"))
                self.algorithm(look, plW, Check)
                if(self.FindHelper(look, plW, self.Dict, Check) == True):
                    return plW
                
                plW.equalTo(PhraseCostr)
                plW.setText('ה' + PhraseCostr.getText()[1:])
                plW.addToValue(-2)
                plW.setNoun()
                plW.setConstruct()
                plW.setGender(1)
                plW.setText(self.revPhWords(plW.getText(), "-"))
                self.algorithm(look, plW, Check)
                if(self.FindHelper(look, plW, self.Dict, Check) == True):
                    return plW
                        
        return Word("", "") 
        
    def irreg(self, look, word, Check):
        if(word.getLen() < 1) or (word.isPhrase()) or (word.getIrregVal() > 15):
            return Word("", "")
        
        if(word.getLen() > 1):
            if(not(word.first() == 'נ'))  and (word.getPrefix() == True) and (not (word.getVerbform()in Niphal)) and (not((word.getVerbform() in Pual) or (word.getVerbform() in Piel) or (word.getPartiVal() == 1))):
                irregW5 = Word("","")
                irregW5.equalTo(word)
                irregW5.setText(word.getText() + 'נ')
                irregW5.setIrreg()
                self.FindHelperCheck(look, irregW5, self.Dict)
                self.irreg(look, irregW5, Check)
                
        if((self.CurrentWord.first() == word.first()) or ((self.CurrentWord.second() == word.first())and(word.getPrixListEnd() == self.CurrentWord.first())and(len(word.getPrixList()) == 1))) and (word.getTense() == 'Imperative'):
            if(not (word.last() == 'ה')):
                irreghW = Word("","")
                irreghW.equalTo(word)
                irreghW.setText('ה' + self.unFinal(word.getText()))
                if('ה' in irreghW.getSufxList()):
                    irreghW.remSuff();
                irreghW.setIrreg()
                if(irreghW.getLen() > 2) and (self.CurrentWord.getLen() > 2):
                    if(not(irreghW.last3() == self.CurrentWord.last3())):
                        self.FindHelperCheck(look, irreghW, self.Dict)
                        self.irreg(look, irreghW, Check)
                elif(not(irreghW.last2() == self.CurrentWord.last2())):
                    self.FindHelperCheck(look, irreghW, self.Dict)
                    self.irreg(look, irreghW, Check)
                    
            if(not (word.first() == 'ה')) and (not(word.getVerbform() in Piel)) and (not(word.getVerbform() in Pual)):
                irregipW = Word("","")
                irregipW.equalTo(word)
                irregipW.setText(word.getText() + 'ה')
                irregipW.setIrreg()
                self.FindHelperCheck(look, irregipW, self.Dict)
                self.irreg(look, irregipW, Check)
            
            if(not (word.first() == 'י')) and (not(word.getVerbform() in Piel)) and (not(word.getVerbform() in Pual)):
                irregipW2 = Word("","")
                irregipW2.equalTo(word)
                irregipW2.setText(word.getText() + 'י')
                irregipW2.setIrreg()
                self.FindHelperCheck(look, irregipW2, self.Dict)
                self.irreg(look, irregipW2, Check)
                
            if(not (word.first() == 'נ')) and (not(word.getVerbform() in Piel)) and (not(word.getVerbform() in Pual)) and (not (word.getVerbform() == 'Niphal')):
                irregipW3 = Word("","")
                irregipW3.equalTo(word)
                irregipW3.setText(word.getText() + 'נ')
                irregipW3.setIrreg()
                self.FindHelperCheck(look, irregipW3, self.Dict)
                self.irreg(look, irregipW3, Check)
            if(word.getLen() > 1):
                if(word.last() == 'י') and (not(word.getConstruct() == True)) and (not(self.CurrentWord.last() == 'י')) and (not(word.getRoot()[:2] == word.last2())) and (not(word.getPartiVal() == 0)):
                    irregW6 = Word("","")
                    irregW6.equalTo(word)
                    irregW6.setText('ה' + word.getText()[1:])
                    irregW6.setIrreg()
                    self.FindHelperCheck(look, irregW6, self.Dict)
                    self.irreg(look, irregW6, Check)
                    if(irregW6.getLen() > 2):
                        if(irregW6.nextToLast() == 'י') or (irregW6.nextToLast() == 'ו')  and (not(irregW6.getRoot()[:2] == irregW6.last2())):
                            irregW7 = Word("","")
                            irregW7.equalTo(word)
                            irregW7.setText('ה' + word.getText()[2:])
                            irregW7.setIrreg()
                            self.FindHelperCheck(look, irregW7, self.Dict)
                            self.irreg(look, irregW7, Check)
                      
        if ((word.getLen() == 1) or ((word.getLen() == 2)and(word.last() == 'ת'))) and ((word.isTense() == True) or (word.getPrefix() == True)): #and (not(word.getTense() == 'Imperfect')and(word.getPerson() == '1st, pl.')) and (not (word.getVerbform() == 'Niphal')):
            irregW = Word("","")
            irregW.equalTo(word)
            if(word.getLen() == 2):
                if(not(word.first() == 'נ')) and (not(word.getVerbform() in Niphal)) and (not(word.getRoot()[:2] == word.last2())):
                    irregW.setText(self.Final(word.getText()[1:]) + 'נ')
                    irregW.setIrreg()
            elif ((word.getPrefix() == True) or (word.getTense() == 'Infinitive') or (word.getTense() == 'Imperfect') or (word.getTense() == 'Cohortative')) and (not(word.getPartiVal() == 0)) and (not(word.getVerbform() == 'Pual')):
                irregW.setText(word.getText() + 'נ')
                irregW.setIrreg()
                irregWNN = Word("","")
                irregWNN.equalTo(irregW)

                if(not('ן' in word.getSufxList())):
                    irregWNN.setText('ן' + self.unFinal(irregW.getText()))
                    if('ן' in irregWNN.getSufxList()):
                        irregWNN.remSuff();
                irregWNN.setIrreg()
                self.FindHelperCheck(look, irregWNN, self.Dict)
            if(not(word.last() == 'ה')) and ((word.isVavSeq() == True) or (word.getSuffix() == True)or(word.getHey1() > 0)) and (not(('ה' in word.getSufxList()) or (word.getHey1() > 0))) and (not((word.isVavSeq() == True)and(word.getTense() == 'Imperfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))) and (not((word.isVavSeq() == False)and(word.getTense() == 'Perfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))):   
                irregWh = Word("","")
                irregWh.equalTo(irregW)
                irregWh.setText('ה' + self.unFinal(word.getText()))
                irregWh.setIrreg()
                 
                if(word.last() == 'ת') and (word.isNoun() == True):
                    irregWh.setConstruct()  
                self.FindHelperCheck(look, irregWh, self.Dict)
            self.FindHelperCheck(look, irregW, self.Dict)
            
            if(not(word.last() == 'ן')):
                irregWNN = Word("","")
                irregWNN.equalTo(irregW)
                irregWNN.setText('ן' + self.unFinal(irregW.getText()))
                if('ן' in irregWNN.getSufxList()):
                    irregWNN.remSuff();
                irregWNN.setIrreg()
                self.FindHelper(look, irregWNN, self.Dict, Check)
            if word.getLen() == 1:
                return Word("", "")
        
        if(word.getLen() == 2):
            if(not(word.getTense() == 'Participle')) and (not(word.getVerbform() in Pual)):
                irreg1 = Word("","")
                irreg1.equalTo(word)
                irreg1.setText(word.last() + 'ו' + word.first())
                if irreg1.getTenseVal() == 2:
                    irreg1.setTense(-1)
                irreg1.setIrreg()
                self.FindHelperCheck(look, irreg1, self.Dict)
            
            if(not(word.getVerbform() in Piel)) and (not(word.getTense() == "Participle")):
                irreg2 = Word("","")
                irreg2.equalTo(word)
                irreg2.setText(word.last() + 'י' + word.first())
                irreg2.setIrreg()
                self.FindHelperCheck(look, irreg2, self.Dict)
                
            if(word.isVerb() == True) and (not('ן' in word.getSufxList())) and (not(word.last() == 'ן')):
                irregWN = Word("","")
                irregWN.equalTo(word)
                irregWN.setText('ן' + self.unFinal(word.getText()))
                irregWN.setIrreg()
                self.FindHelperCheck(look, irregWN, self.Dict)
                
        if(word.getLen() > 2):
            if(word.nextToFirst() == 'נ') and (not((word.getVerbform() in Pual) or (word.getVerbform() in Piel) or (word.getVerbform() in Hiphil) or (word.isParticiple() == True))) and (not(word.getRoot()[-2:] == word.first2())):
                irregWN = Word("","")
                irregWN.equalTo(word)
                irregWN.setText(word.getText()[:-2] + word.first())
                irregWN.setIrreg()
                self.FindHelper(look, irregWN, self.Dict, False)
                self.irreg(look, irregWN, Check)
                
            #if(word.nextToLast() == 'י') and (word.getPlural() == False) and (not(word.last2() in suffix)):
            #        irreg3 = Word("","")
            #        irreg3.equalTo(word)
            #        irreg3.setText(word.last() + word.getText()[2:])
           #         irreg3.setIrreg()
           #         self.FindHelperCheck(look, irreg3, self.Dict)
            
        if(word.getLen() == 3):
            if(not(word.getTense() == "Participle")) and ((word.nextToLast() == 'ו') or (word.nextToLast() == 'י')) and (not((word.last() == 'ה')and(not(self.CurrentWord.last() == 'ה')))) and (not (word.getRoot()[:2] == word.last2())):
                hollow = Word("","")
                hollow.equalTo(word)
                hollow.setText(word.last() + word.first())
                hollow.setIrreg()
                self.FindHelperCheck(look, hollow, self.Dict)
        
        if(word.isVerb() == True) and (not('ן' in word.getSufxList())) and (((word.getTense() == "Infinitive")and(word.getLen() < self.CurrentWord.getLen()-len(word.getPrixList()) - 1)and(not(self.CurrentWord.last() == word.last()))) or ((word.getTense() == "Imperfect")and((word.isVavSeq() == True))and(word.getLen() < self.CurrentWord.getLen()-len(word.getPrixList())-1)and(not(self.CurrentWord.last() == word.last()))) or ((word.getTense() == "Perfect")and((word.isVavSeq() == False))and(word.getLen() < self.CurrentWord.getLen()-len(word.getPrixList())-1)and(not(self.CurrentWord.last() == word.last())))) and (not(word.last() == 'ן')):
            irregWN = Word("","")
            irregWN.equalTo(word)
            irregWN.setText('ן' + self.unFinal(word.getText()))
            irregWN.setIrreg()
            self.FindHelperCheck(look, irregWN, self.Dict)
 
        # checking to see if any tavs or hays have been removed form the end of the word, or if any extra vawls have been added within the word
        if (word.getLen() > 3) and (not(word.getPartiVal() == 0)) and ((word.getSuffix() == True) or (word.getHey1() > 0) or (not (word.last3() == self.CurrentWord.last3()))) and (('ו' in word.getPrixList()) or (word.getTense() == "Perfect") or (word.getTense() == "Imperfect") or (word.getTense() == "Imperative") or (word.getTense() == "Infinitive")):
            if((not(((word.getConstruct() == True) and (((word.getPlural() == True)and(self.CurrentWord.getX(self.CurrentWord.getLen() - 2) == word.last())) or ((word.getDual() == True)and(self.CurrentWord.getX(self.CurrentWord.getLen() - 3) == word.last())))) or ((word.getConstruct() == False) and (((word.getPlural() == True)and(self.CurrentWord.getX(self.CurrentWord.getLen() - 3) == word.last())) or ((word.getDual() == True)and(self.CurrentWord.getX(self.CurrentWord.getLen() - 4) == word.last())))))) and (not((word.getConstruct() == True)and((word.getPlural() == False)and(word.getDual() == False)) and (self.CurrentWord.last2()[-1:] == word.last()))) or ((word.getTense() == "Imperfect")and(word.isVavSeq() == True)) or ((word.getTense() == "Perfect")and(word.isVavSeq() == False))) and (word.getSuffix() == True) and (not ('ה' in word.getSufxList())):
                if(not(word.last() == 'ה')) and (not(('ה' in word.getSufxList()) or (word.getHey1() > 0))) and (not((word.isVavSeq() == True)and(word.getTense() == 'Imperfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))):
                    irregW = Word("","")
                    irregW.equalTo(word)
                    irregW.setText('ה' + self.unFinal(word.getText()))
                    irregW.setIrreg()
                    self.FindHelperCheck(look, irregW, self.Dict)
            #elif (word.getTense() == "Imperative") and (not(word.last() == 'ה')) and (not ('ה' in word.getSufxList())) and (not ('ה' in word.getSufxList())) and (not((word.isVavSeq() == True)and(word.getTense() == 'Imperfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))) and (not((word.isVavSeq() == False)and(word.getTense() == 'Perfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))):
            #    irregW = Word("","")
            #    irregW.equalTo(word)
            #    irregW.setText('ה' + self.unFinal(word.getText()))
            #    irregW.setIrreg()
            #    self.FindHelperCheck(look, irregW, self.Dict)
            #elif (word.getTense() == "Perfect") and (not(self.CurrentWord.last3() == word.last3())):
            #    if((word.last3() == 'יוו') or (word.last3() == 'ווי') or (word.last3() == 'ויו')):
            #        irregWa = Word("","")
            #        irregWa.equalTo(word)
            #        irregWa.setText('ה' + word.getText()[3:])
            #        irregWa.setIrreg()
            #        self.FindHelperCheck(look, irregWa, self.Dict)
            #    elif((word.last2() == 'וי') or (word.last2() == 'יו') or (word.last2() == 'וו')):
            #        irregWb = Word("","")
            #        irregWb.equalTo(word)
            #        irregWb.setText('ה' + word.getText()[2:])
            #        irregWb.setIrreg()
            #        self.FindHelperCheck(look, irregWb, self.Dict)
            #    elif(word.last() == 'י'):
            #        irregWc = Word("","")
            #        irregWc.equalTo(word)
            #        irregWc.setText('ה' + word.getText()[1:])
            #        irregWc.setIrreg()
            #        self.FindHelperCheck(look, irregWc, self.Dict)
            #elif (word.getTense() == "Imperfect") and (not(self.CurrentWord.last3() == (word.last3()))):
            #    if(word.getLen() > 3) and ((word.last3() == 'יוו') or (word.last3() == 'ווי') or (word.last3() == 'ויו')):
            #        irregWa = Word("","")
            #        irregWa.equalTo(word)
            #        irregWa.setText('ה' + word.getText()[3:])
            #        irregWa.setIrreg()
            #        self.FindHelperCheck(look, irregWa, self.Dict)
            #    elif(word.getLen() > 2) and ((word.last2() == 'וי') or (word.last2() == 'יו') or (word.last2() == 'וו')):
            #        irregWb = Word("","")
            #        irregWb.equalTo(word)
            #        irregWb.setText('ה' + word.getText()[2:])
            #        irregWb.setIrreg()
            #        self.FindHelperCheck(look, irregWb, self.Dict)
            #    elif(word.last() == 'י'):
            #        irregWc = Word("","")
            #        irregWc.equalTo(word)
            #        irregWc.setText('ה' + word.getText()[1:])
            #        irregWc.setIrreg()
            #        self.FindHelperCheck(look, irregWc, self.Dict)
         
        # checking to see if any letters have been assimilated from the beginning of the word.
        if ((word.getPrefix() == True) or (word.getTense() == 'Infinitive') or (word.getTense() == 'Imperfect') or (word.getTense() == 'Cohortative')) and (not(word.getPartiVal() == 1)) and (not(word.getVerbform() in Pual)):
            if (not((word.getVerbform() in Hophal)or(word.getVerbform() in Hiphil)or(word.getVerbform() in Hithpeal))) and (not(word.getIrregVal() > 0)) and ((not ('ה' in word.getPrixList())) and (not (self.CurrentWord.first() == 'ה')) and (not (word.first() == 'ה'))) and (not(word.getVerbform() in Piel)):
                irregW = Word("","")
                irregW.equalTo(word)
                irregW.setText(word.getText() + 'ה')
                irregW.setIrreg()
                self.FindHelper(look, irregW, self.Dict, False)
                self.irreg(look, irregW, Check)
                
            if(not(word.getVerbform() == 'Niphal')) and (not ((word.first() == 'נ') and (word.getIrregVal() > 0))) and (not(word.getVerbform() in Piel)) and (not(word.getPartiVal() == 0)):
                irregW2 = Word("","")
                irregW2.equalTo(word)
                irregW2.setText(word.getText() + 'נ')
                irregW2.setIrreg()
                self.FindHelper(look, irregW2, self.Dict, False)
                self.irreg(look, irregW2, Check)
                if(not('ה' in word.getSufxList())) and (not(word.last() == 'ה')) and (not (self.CurrentWord.last() == 'ה')) and (not((word.isVavSeq() == True)and(word.getTense() == 'Imperfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))) and (not((word.isVavSeq() == False)and(word.getTense() == 'Perfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))):
                    irregWh = Word("","")
                    irregWh.equalTo(irregW2)
                    irregWh.setText('ה' + self.unFinal(irregW2.getText()))
                    irregWh.setIrreg()
                    self.FindHelperCheck(look, irregWh, self.Dict)
            if(not((word.first() == 'י') and (word.getIrregVal() > 0))) and (not(word.getVerbform() in Piel)) and (not(word.getPartiVal() == 0)):
                irregW3 = Word("","")
                irregW3.equalTo(word)
                irregW3.setText(word.getText() + 'י')
                irregW3.setIrreg()
                self.FindHelperCheck(look, irregW3, self.Dict)
                if(not('ה' in word.getSufxList())) and (not(word.last() == 'ה')) and (not (self.CurrentWord.last() == 'ה')) and (not((word.isVavSeq() == True)and(word.getTense() == 'Imperfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))) and (not((word.isVavSeq() == False)and(word.getTense() == 'Perfect')and(word.getPerson() == '3rd, sg.')and(word.getGender() == 'f.'))):
                    irregWi = Word("","")
                    irregWi.equalTo(irregW3)
                    irregWi.setText('ה' + self.unFinal(irregW3.getText()))
                    irregWi.setIrreg()
                    self.FindHelperCheck(look, irregWi, self.Dict)
                        
        return Word("", "")
        
    def build(self):
        # collecting user words form Json file (the database)
        self.store = JsonStore("data/WordsFinalFixed.json")
        
        # Building .kv file
        #with open('hebrewdictionary2.kv', encoding='utf8') as f:
            #root_widget = builder.Builder.load_string(f.read())
            
        return self.startInterface()

 
if __name__ == '__main__':
    HebrewDictionary().run()