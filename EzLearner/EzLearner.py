# coding: utf8
import os
import random
import sys

# NB: Working with dictionaries was a big mistake x) [...]. If you read this please don't judge me, it was done for personal use only and I just wanted it to work.

# EzLearner 0.2
# By Baballevincent

# m = number of words in the vocabulary list.

#TODO:
# 1) Main menu - Modes: Version / Thème

## MENU
def menu():
    print(" ______     ______     __         ______     ______     ______     __   __     ______     ______    ")
    print('/\  ___\   /\___  \   /\ \       /\  ___\   /\  __ \   /\  == \   /\ "-.\ \   /\  ___\   /\  == \   ')
    print("\ \  __\   \/_/  /__  \ \ \____  \ \  __\   \ \  __ \  \ \  __<   \ \ \-.  \  \ \  __\   \ \  __<   ")
    print(' \ \_____\   /\_____\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \_\\\ \_\  \ \_____\  \ \_\ \_\ ')
    print("  \/_____/   \/_____/   \/_____/   \/_____/   \/_/\/_/   \/_/ /_/   \/_/ \/_/   \/_____/   \/_/ /_/ ")
    print("                                                                                                    ")
# Waow, that's some fancy ASCII art

## SETUP
# Path to txt file containing words
path = "E:\Programmation\Python\projets\EzLearner\\anglais vocab.txt"
config_path = "E:\Programmation\Python\projets\EzLearner\\config.txt"
translate_delimiter = ' -> ' # Please include spaces if necessary
meaning_delimiter = ', '     # Please include spaces if necessary
#save_ path = ""
raw_file = open(path, mode='r', encoding='utf8')
raw = raw_file.readlines()

def load(): # Loads config file
    dico = {} # Words and their translation are stocked in the dico dictionary
              # An english word is a key, all translations are a stocked as a list which is accessible through dico[key]-
    for line in raw:
        if "->" in line:
            tmp = line.split(translate_delimiter)
            if meaning_delimiter in tmp[1]:
                dico[tmp[0]] = [tmp[1].split(meaning_delimiter), 1.0] # 1 Is the default pondering value
            else:
                dico[tmp[0]] = [[tmp[1]], 1.0]
    for cle in dico:
        dico[cle][0][-1] = dico[cle][0][-1].split("\n")[0]

    # Load / create config file:
    if os.path.exists(config_path):  # If there is already a config file
        print("Config file detected, Loading ...")
        try:
            config = open(config_path, 'r', encoding='utf8')
            i = 0
            for line in config:
                i+=1
                if (i>len(dico)):
                    raise Exception("The config file is too long compared to the vocabulary file.")
                content = line.split(':')
                key = content[0]
                value = float(content[1].split("\n")[0])
                dico[key][1] = value
            print("Succesfully loaded config file")
        except Exception as e:
            print(e)
            print("Try deleting config file to reset it, it might have been corrupted.")
            sys.exit()
        finally:
            config.close()

    else: # Else, create a config file.
        print("No config file detected, Creating one at " + config_path)
        try:
            config = open(config_path, mode='w', encoding='utf8')
            for key in dico.keys():
                config.write(key + ":1\n")
                # the value is set to 1 by default earlier so no need to change it.
        except Exception as e:
            print(e)
            print("An error occured while creating the config file. Please check your word list or the code(lol)")
        finally:
            config.close()
    return dico

def save(dic): # Saves config file
    try:
        new_config = open(config_path, 'w', encoding='utf8')
        for key in dic.keys():
            new_config.write(key + ":" + str(dico[key][1]) + "\n")
    except Exception as e:
        print(e)
    finally:
        new_config.close()

## TOOLS (MENU)
def convertToStandard(file_path, new_file_path): # O(m)
    try:
        file = open(file_path, 'r')
        new_file = open(new_file_path, 'w')
        for line in file:
            pass

        print("Successfuly created new file at " + new_file_path)
    except Exception as e:
        print(e)
    finally:
        file.close()
        new_file.close()

## USEFUL FUNCTIONS
def string_compare(input_word, output_word):
     # DO: Returns the number of different characters between 2 strings
     # If not the same amount of words -> FAIL
     # If the same amount of words:
        # Compare each word: measure the length of each word and add the difference to the count
        # Count each different characters for each word between input and output
        # NB: the so called "output" is the reference string
    if output_word.startswith(" "):
        output_word = output_word[1:]
    elif output_word.endswith(" "):
        output_word = output_word[:-1]

    new_input = input_word.split(" ")
    new_output = output_word.split(" ")
    if len(new_input) != len(new_output):
        return 127 # Not the same amount of words -> FAIL
    else:
        edit_distance = 0
        for k in range(len(new_input)):
            edit_distance += abs(len(new_input[k]) - len(new_output[k]))
            l = min(len(new_input[k]), len(new_output[k]))
            for i in range(l):
                if new_input[k][i] != new_output[k][i]:
                    if new_input[k][i:] in new_output[k]:
                        break
                    else:
                        edit_distance +=1
    return edit_distance

def  smartcheck(input, output_list):
    # DO: compare two strings (case insensitive)
    # return True if the words are similar
    # input is a string and output_list is a list of strings (reference)
    # Check if the string is empty or filled with space first
    # Check if there was a space added at the end or the begining
    if input.isspace() or input == '':
        return False

    input = input.lower()
    length = len(input)
    if input.startswith(" ") or input.startswith("\"") or input.startswith("\'"):
        input = input[1:]
        length -=1
    elif input.endswith(" ") or input.endswith("\"") or input.endswith("\'"):
        input = input[:length-1]
        length -= 1

    test = False
    for element in output_list:
        robustesse = len(element.split(" "))
        distance = string_compare(input, element)
        if distance <= robustesse:
            test = True
    return test

## MAIN

def play(dic): # Fontion comprenant la boucle principale de jeu
    keys = list(dic.keys())
    keep_playing = True
    while keep_playing:
        n = 0 # Somme totale des pondérations
        for v in dic.values(): # O(m)
            n += v[1]
        r = random.random()*n  # Pick a number in ]0, n[, with n being the sum of the frequence config value
        i = -1
        while r>0:
            i+=1
            r-= dico[keys[i]][1]

        print(list(keys)[i])
        trad = input("Traduction: ")
        keep_playing = smartcheck(trad, dic[keys[i]][0])
        if keep_playing:
            print("Bonne réponse!")
            dic[keys[i]][1] /= 2  # Divise by two the probability when good answer
        else:
            print("Mauvaise réponse!")
            dic[keys[i]][1] *= 2 # Multiply by two the probability when bad answer
            if len(dic[keys[i]][0]) >= 2:
                print("Les bonnes réponses possibles étaient: " + str(dic[keys[i]][0]))
            else:
                print("La bonne réponse était: " + str(dic[keys[i]][0][0]))

    print(n)
## EXEC
dico = load()
menu()
play(dico)
save(dico)




