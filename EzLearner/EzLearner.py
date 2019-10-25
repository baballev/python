# coding: utf8
import os
import random
import sys

# EzLearner 0.2
# By Baballevincent

#TODO:
# 1) Main menu - Modes: Version / Thème
# 2) fichier de sauvegarde de pondération des probas.

## MENU
def menu():
    print(" ______     ______     __         ______     ______     ______     __   __     ______     ______    ")
    print('/\  ___\   /\___  \   /\ \       /\  ___\   /\  __ \   /\  == \   /\ "-.\ \   /\  ___\   /\  == \   ')
    print("\ \  __\   \/_/  /__  \ \ \____  \ \  __\   \ \  __ \  \ \  __<   \ \ \-.  \  \ \  __\   \ \  __<   ")
    print(' \ \_____\   /\_____\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \_\\"\_\  \ \_____\  \ \_\ \_\ ')
    print("  \/_____/   \/_____/   \/_____/   \/_____/   \/_/\/_/   \/_/ /_/   \/_/ \/_/   \/_____/   \/_/ /_/ ")
    print("                                                                                                    ")


## SETUP
# Path to txt file containing words
path = "E:/Programmation/Python/projets/anglais vocab.txt"
config_path = "E:/Programmation/Python/projets/config.txt"
translate_delimiter = ' -> '
meaning_delimiter = ', '
#save_ path = ""
pondering_dict = {}
raw_file = open(path, mode='r', encoding='utf8')
raw = raw_file.readlines()

def load(): # Loads config file
    dico = {} # Words and their translation are stocked in the dico dictionary
            # An english word is a key, all translations are a stocked as a list which is accessible through dico[key]-
    for line in raw:
        if "->" in line:
            tmp = line.split(translate_delimiter)
            if meaning_delimiter in tmp[1]:
                dico[tmp[0]] = [tmp[1].split(meaning_delimiter), 1]
            else:
                dico[tmp[0]] = [[tmp[1]], 1.0]
    for cle in dico:
        dico[cle][0][-1] = dico[cle][0][-1].split("\n")[0]

    # Load / create config file:
    if os.path.exists(config_path):  # If there is already a config file
        print("Config file detected, Loading ...")
        try:
            config = open(config_path, 'r')
            i = 0
            for line in config:
                i+=1
                if (i>len(dico)):
                    print(" i = " + i)
                    raise Exception("The config file is too long compared to the vocabulary file.")
                content = line.split(':')
                key = content[0]
                value = content[1].split("\n")[0]
                pondering_dict[key] = value
            print("Succesfully loaded config file")
        except Exception as e:
            print(e)
            print("Try deleting config file to reset it, it might have been corrupted.")
            sys.exit()
        finally:
            print(pondering_dict)
    else: # Else, create a config file.
        print("No config file detected, Creating one at " + config_path)
        try:
            config = open(config_path, mode='w+')
            for key in dico.keys():
                config.write(key + ":1\n")
                pondering_dict[key] = 1
        except Exception as e:
            print(e)
            print("An error occured while creating the config file. Please check your word list or the code(lol)")
        finally:
            config.close()

def save(): # Saves config file
    try:
        new_config = open(config_path, mode='w')
        for key in pondering_dict.keys():
            new_config.write(key + ":" + pondering_dict[key]+"\n")
    except Exception as e:
        print(e)
    finally:
        new_config.close()

## USEFUL FUNCTIONS
def string_compare(input_word, output_word):
     # DO: Returns the number of different characters between 2 strings
     # If not the same amount of words -> FAIL
     # If the same amount of words:
        # Compare each word: measure the length of each word and add the difference to the count
        # Count each different characters for each word between input and output
        # NB: the so called "output" is the reference string

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
    if input.startswith(" "):
        input = input[1:]
        length -=1
    elif input.endswith(" "):
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
    keep_playing = True
    while keep_playing:
        n = 0 # Somme totale des pondérations
        for v in dic.values():
            n += v[1]
        r = int(round(random.random()*n))
        # TODO: Trouver un moyen de changer la proba et de la sauvegarder dans un fichier de sauvegarde cf début du code
        print(list(dic.keys())[r])
        trad = input("Traduction: ")
        keep_playing = smartcheck(trad, dic[list(dic.keys())[r]][0])
        if keep_playing:
            print("Bonne réponse!")
        else:
            print("Mauvaise réponse!")
            if len(dic[list(dic.keys())[r]][0]) >= 2:
                print("Les bonnes réponses possibles étaient: " + str(dic[list(dic.keys())[r]][0]))
            else:
                print("La bonne réponse était: " + str(dic[list(dic.keys())[r]][0][0]))

## EXEC
load()
menu()
play(dico)
save()



