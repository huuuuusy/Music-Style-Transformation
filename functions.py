import music21
from music21 import  *
import shutil
from collections import Counter, defaultdict
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import sys, re, itertools, random, os

def ReadMidi(file_path):
    file = converter.parse(file_path)
    components = []
    for element in file.recurse():
        components.append(element)
    return components

def TransferMidToChordTxt(file_path):
    try:
        components = readMidiFile(file_path=file_path)
        startPiano = True 
        printRatio = True
        printHighest = True
        printColumns = True
        output = ""
        notes = ""
        chords = ""
        for component in components:
            if startPiano and type(component) is music21.chord.Chord:
                tmp = component.fullName + "," + component.pitchedCommonName + "," + str(component.quarterLength) + "," + str(
                    component.offset)
                output += tmp + "\n"
                #print(tmp)
            elif type(component) is music21.meter.TimeSignature and printRatio:
                tmp = str(component.ratioString)
                output += tmp + "\n"
                #print(tmp)
                printRatio = False
            elif type(component) is music21.stream.Score and printHighest:
                tmp = component.highestTime
                output += str(tmp) + "\n"
                #print(tmp)
                printHighest = False
            elif not printHighest and not printRatio and printColumns:
                tmp = "FullName,CommonName,Len,Offset"
                output += tmp + "\n"
                #print(tmp)
                printColumns = False
        with open((file_path.split(".mid")[0] + "_chord.txt"), 'w') as f:
            f.write(output)
    except:
        pass

def ExtractNodeAndChord(file_path, split_length,out_node_path,out_chord_path):
    read_data = None
    full_name = ""
    common_name = ""
    count_length = 0
    with open(file_path, 'r') as f:
        read_data = f.readlines()
    for line in read_data[1:]:
        if line == "" or "{" not in line:
            continue
        count_length += 1
        sl = line.split(",")
        i  = sl[0].index("{")
        j  = sl[0].index("}")
        full_name += sl[0][i:j+1].replace(" ", "_") + " "
        temp = sl[1].split(" ")[0] + " "
        common_name += sl[1].split(" ")[0].split("-")[0] + " "
        if split_length is not None and count_length == split_length:
            full_name += "\n"
            common_name += "\n"
            count_length = 0

    if full_name.endswith("\n"):
        full_name = full_name[:-1]
    if common_name.endswith("\n"):
        common_name = common_name[:-1]
    #print ("--------This is tpye.node--------")
    #print (full_name)
    #print ("\n")
    #print ("--------This is type.chord--------")
    #print (common_name)
    with open(out_node_path, 'a') as f:
        f.write(full_name + '\n')
    with open(out_chord_path, 'a') as f:
        f.write(common_name + '\n')


def RemoveDuplicateVocab(vocabFile):
    words = []
    num = 0
    with open(vocabFile, 'r') as f:
        for line in f:
            line = line.strip()
            if line not in words:
                words.append(line)
            else:
                num += 1
        f.close()
    try:
        os.remove(vocabFile)
    except OSError:
        pass
    with open(vocabFile, 'w') as f:
        for word in words:
            f.write(word +'\n')
        f.close()
    print("Remove",num ,"duplicate words!")

def RemoveEmptyLine(file_path):
    lines = []
    num = 0
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                num += 1
                continue
            else:
                lines.append(line)
        f.close()
    try:
        os.remove(file_path)
    except OSError:
        pass
    with open(file_path, 'w') as f:
        for line in lines:
            f.write(line+'\n')
        f.close()
    print("Remove",num ,"empty lines!")

def PrintNumLines(file_path,num):
    lines = []
    i = 1
    with open(file_path,'r') as f:
        for line in f:
            line = line.strip()
            if i <= num:
                print(line)
                i += 1
                continue
        f.close()
