#!/usr/bin/env python
# coding: utf-8

# In[48]:


import nltk 
import string

#capitalization error
def capitalizationError(capWords):
    if capWords[0].islower():
        return True
    return False

#verb form error
def modalError(tags):
    if tags[2].startswith('V') and tags[2] != 'VB':
        if tags[1] == 'MD':
            return True
        elif (tags[0] == 'MD') and (not tags[1].startswith('V')):
            return True
        if tags[1] == 'TO':
            return True
        elif (tags[0] == 'TO') and (not tags[1].startswith('V')):
            return True  
    return False

#subject-verb agreement error
def agreementError1(tags):
    if tags[2] == 'VBZ':
        if (tags[0] == 'NNS') and (not tags[1].startswith('N')):
            return True
    elif tags[2] == 'VBP':
        if tags[1] == 'NNP':
            return True
    return False

#subject-verb agreement error(Personal Pronoun)
def agreementError2(subject, tags):
    if tags == 'VBZ':
        if subject in ['I','you','we','they','You','We','They']:
            return True    
    elif tags == 'VBP' or tags == 'VB':
        if subject in ['he','she','it','He','She','It']:
            return True
    return False
    
fileName = 'error.txt'

wnl = nltk.WordNetLemmatizer()
wordlist = nltk.corpus.words.words()
wordlist.insert(0,'Jingjing')

f = open(fileName)

text = f.read()
sents = nltk.sent_tokenize(text)

for sent in sents:
    words = nltk.word_tokenize(sent)
    tagged_words = nltk.pos_tag(words)
    
    print(sent)
    
    capitalizationWord = words[0]        
    if capitalizationError(capitalizationWord):
            print('** Capitalization error:', capitalizationWord) 
    
    prevWord = '<start>'
    curTags = ['<tag>', '<tag>', '<tag>']
    
    verbNum = 0
    
    for tagged_word in tagged_words:
        
        curWord = tagged_word[0]
        curPOS = tagged_word[1]
        
        curTags.pop(0)
        curTags.append(curPOS)
        
        #verb form error
        if modalError(curTags):
            print('** Verb form error:', curWord)
        
        #subject-verb agreement error
        if agreementError1(curTags):
            print('** Subject-verb agreement error:', curWord)
        
        if agreementError2(prevWord,curPOS):
            print('** Subject-verb agreement error:', curWord)
        
        
        #spelling error
        curWordLow = curWord.lower()
        lemma = wnl.lemmatize(curWordLow)
        
        if curPOS.startswith('V'):
            lemma = wnl.lemmatize(curWordLow, 'v')
        
        if curPOS.startswith('N'):
            lemma = wnl.lemmatize(curWord,'n')
        
        if (not lemma in wordlist) and (not lemma in string.punctuation):
            print('** Spelling error:', curWord)
    
        #fragment error
        if curPOS.startswith('V'):
            verbNum += 1
        
        prevWord = curWord
            
    if verbNum == 0:
        print('** Fragment error')
              
f.close()

