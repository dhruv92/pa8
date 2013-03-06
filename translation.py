# -*- coding: utf-8 -*-
import collections
import nltk
import string
import re


def swap(words, key, val, index_key):
     temp = val
     words[index_key+1]=key
     words[index_key]=temp


def apply_rules(english, translation, english_adjectives):
    english_new=''
    pos= collections.defaultdict(lambda: ('a', 'b'))
    words = english.split(' ')
  
    for x in range (len(words)-2):
        tag = nltk.pos_tag((words [x], words [x+1]))
        first_word = tag[0]
        second_word = tag[1]

        exclude = set(string.punctuation)
        second_no_punc = ''.join(ch for ch in second_word[0] if ch not in exclude)
        first_word_punc=first_word[0]

        # Swap consecutive nouns and adjectives since French and English have a different ordering for these
        if "NN" in first_word[1] and second_no_punc in english_adjectives:
          if ('.' in second_word[0]):
            first_word_punc+='.'
          swap(words, first_word_punc,  second_no_punc, x )

        # Add 'ly' to an adjective that ends a sentence. In French, the adverb and the adjectif form is the 
        # same. Therefore 'se défendent mal' translates to 'defend themselves bad' or 'defend themselves badly', 
        #altough only the second version is correct in english. We therefore need to transform the adjectif to an
        #adverb. 
        if ('!' in second_word[0] or '?' in second_word[0]) and second_no_punc in english_adjectives:
             char_list=list(second_word[0])
             char_list.insert(len(char_list)-1, 'ly')
             second_no_punc = "".join(char_list)
             words[x+1]=second_no_punc

         #rule for indeterminate plural noun following 'the' -> need to remove 'the' (as in "we are lucky that women defend themselves")
         #instead of "we are lucky that the women defend themselves"
        if second_word[1]=='NNS' and first_word[0]=='the':
            words[x]=''

        # In french, the preposition comes before the verb, so it would be "to me save" instead of 'to save me'
        if first_word[0] =='me' and second_word[1]=='VBP':
            swap(words, first_word[0], second_word[0],x)

        #negation in french is always 'ne...pas' so it would always translate to 'not'. However, in English
        # if the word after the 'not' is a verb, then the negation becomes 'cannot' (for example here, 'I cannot imagine'
        # is correct, whereas "I not imagine" is incorrect. 
        if first_word[0]=='not' and second_word[1]=='VBP':
            words[x]= 'cannot'

        #Resolve the French ambiguity with the preposition 'de', which can mean 'to' ( as in 'surprised to see me') or
        # of like ('made of wood')
        if first_word[1]=='VBD' and second_word[0]=='of':
            if words [x+2]== 'the':
                words[x+1]=''
            else : 
                words[x+1]='to'

        # In French, the word 'pour' is ambiguous, and can mean either 'to' or 'for' depending on 
        #the word that follows . 
        if first_word[0]=='for' and (second_word[1] == 'NN' or second_word[1]=='VBP'):
            words [x]= 'to'

        # The reflexive 'se' is the same for everything in French (male / female/ singular/ plural)
        # And is attached to the verb as opposed to the subject, as in english. This yields a translation of 
        # 'les femmes se défendent' as 'women self defend' instead of 'women defend themselves'. This rule fixes that.
        if first_word[0]== 'self' and second_word[1]=='VBP':
            if x:
              french_subject = [key for key, value in translation.iteritems() if value ==words[x-1] ][0]
              if french_subject.endswith('e'):
                swap(words,second_word[0],'herself', x)
              elif french_subject.endswith('s'):
                swap(words,second_word[0], 'themselves', x)
              else:
                swap(words,second_word[0], 'himself',x)
         
        if first_word[0]=='not':
            words[x]= 'do not'

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


def read_files(my_translations,text,adjectives, english_adjectives):
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

    for line in open('eng_adj.txt', 'r'):
        line=line.lower()
        line= line.replace ('\n', '')
        english_adjectives.append(line)

def main():

    my_translations=collections.defaultdict(lambda:'My default')
    text=[]
    adjectives=[]
    english_adjectives=[]
    
    read_files(my_translations,text, adjectives, english_adjectives)

    english_text=''

    english_text= apply_rules_french(text,my_translations, adjectives)
    english_text= apply_rules(english_text, my_translations, english_adjectives)
  
    print english_text


if __name__ == '__main__':
    main()
