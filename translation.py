# -*- coding: utf-8 -*-
import collections
import nltk
import string


def swap( words, key, val):
     temp = val
     index_key = words.index(key)
     words[index_key+1]=key
     words[index_key]=temp


def apply_rules(english):
    pos= collections.defaultdict(lambda: ('a', 'b'))
    words = english.split(' ')
  
    for x in range (len(words)-1):
        tag = nltk.pos_tag((words [x], words [x+1]))
        first_word = tag[0]
        second_word = tag[1]
        pos[first_word]=second_word

    english_new=''

    for key, val in pos.items():
        if "NN" in key[1] and val[1]=='JJ':
          swap(words, key[0],  val[0])

    for word in words : 
        if word =='i':
            word= 'I'
        english_new+= word+ ' '

    return english_new


def main():

    my_translations=collections.defaultdict(lambda:'My default')
    text=[]
    for line in open('liaisons.txt', 'r'):
            line=line.lower()
            line=line.split(' ')
       
            for word in line:
                text.append(word)
                
   
    for line in open('dictionary.txt', 'r'):
        line=line.lower()
        line = line.split('-')
        french = line[0]
        line[1]=line[1].replace('\n','')
        english=line[1]
        my_translations[french]=english

    english_text=''

    for word in text:
        if word in my_translations.keys():
            translation= my_translations[word]
            if not word.startswith(' '):
                english_text+= ' ' + translation
            else : 
                english_text+=translation

    english_text= apply_rules(english_text)
    print english_text

   


if __name__ == '__main__':
    main()
