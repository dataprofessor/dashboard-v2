import configparser
import bidi.algorithm as bidialg
import arabic_reshaper

from datetime import datetime
# from helper.jalali import Persian

def correctPersianText(wrongPersianText):
    text = arabic_reshaper.reshape(wrongPersianText)
    reshaped_text = bidialg.get_display(text)
    return reshaped_text

def persianNumberToEnglish(persianNumber):
    EnglishNumber = ''
    numberSign = 1
    for i in persianNumber:
        if i == '/' or i == ')':
            pass
        if i == '(':
            numberSign = -1
        elif i == ',':
            pass
        elif i == '۰':
            EnglishNumber += '0'
        elif i == '۱':
            EnglishNumber += '1'
        elif i == '۲':
            EnglishNumber += '2'
        elif i == '۳':
            EnglishNumber += '3'
        elif i == '۴':
            EnglishNumber += '4'
        elif i == '۵':
            EnglishNumber += '5'
        elif i == '۶':
            EnglishNumber += '6'
        elif i == '۷':
            EnglishNumber += '7'
        elif i == '۸':
            EnglishNumber += '8'
        elif i == '۹':
            EnglishNumber += '9'
        elif i == '.':
            EnglishNumber += '.'

    return numberSign*float(EnglishNumber)