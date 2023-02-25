import pandas as pd
import json
import demjson
import jsonlike
f = open("./data.txt","r",encoding="utf-8") 
string = f.read()


def findmovie(name):
    start_pos = string.find(name)
    res = {}
    i = string.find("poster", start_pos)
    i += 10
    j = i
    while string[j] != '\'':
        j += 1
    poster = string[i:j]
    res['img'] = poster
    i = string.find("genre",i)
    i += 9
    j = i
    while string[j] != '\'':
        j += 1
    genre = string[i:j]
    res['movieType'] = genre
    i = string.find("description",i)
    i += 15
    j = i
    while string[j] != '\'':
        j += 1
    description = string[i:j]
    res['desc'] = description
    i = string.find("doubanRating",i)
    i += 16
    j = i
    while string[j] != '\'':
        j += 1
    doubanRating = string[i:j]
    res['averageScore'] = doubanRating
    i = string.find("doubanVoters",i)
    i += 16
    j = i
    while string[j] != '\'':
        j += 1
    doubanVoters = string[i:j]
    res['numberOfParticipants'] = doubanVoters
    i = string.find("dateReleased",i)
    i += 16
    j = i
    while string[j] != '\'':
        j += 1
    dateReleased = string[i:j]
    res['releaseTime'] = dateReleased
    return res
    

print(findmovie("Now and Then"))


