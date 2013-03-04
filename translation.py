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

    # Swap consecutive nouns and adjectives since French and English have a different ordering for these 
    for key, val in pos.items():
        if "NN" in key[1] and val[1]=='JJ':
          swap(words, key[0],  val[0])

    for word in words : 
        if word =='i':
            word= 'I'
        english_new+= word+ ' '

    return english_new

def apply_rules_french(text, my_translations, adjectives):
    english_text=''
    for x in range (0, len(text)):
        word = text[x]
        if word in my_translations.keys():
            translation= my_translations[word]

            # Since otherwise we get double negation in English. We need to account for the fact that 'ne pas' is actually
            #one negation, and not two separate negations. 
            if not word =='pas':

                if x < len(text)-1:

                    next_word= text[x+1]

                    exclude = set(string.punctuation)
                    next_word = ''.join(ch for ch in next_word if ch not in exclude)
                    
                    #make the difference between conditional si ('if') and comparative si ('so').
                    # determines whether preposition 'si' is being used as
                    #conditional or as comparative ( difference between translating to 'if' or to 'so').
                    # If followed by an adjective, it is the comparative 'so', and if not, it is the conditional 'if'
                    if word == 'si' and next_word in adjectives:
                        translation='so'

                english_text+=translation + ' '
    return english_text


def read_files(my_translations,text,adjectives):
    for line in open ('adjectives.txt', 'r'):
        line=line.lower()
        line= line.replace ('\n', '')
        adjectives.append(line)

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

def main():

    my_translations=collections.defaultdict(lambda:'My default')
    text=[]
    adjectives=[]

    
    read_files(my_translations,text, adjectives)

    english_text=''

    english_text= apply_rules_french(text,my_translations, adjectives)
    english_text= apply_rules(english_text)
  


if __name__ == '__main__':
    main()
