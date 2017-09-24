# Code written by Billy Mihalarias

import discord
import asyncio
import json
import os.path

from google import search  # google search library

client = discord.Client()

class SearchData:
    def __init__(self, site='', header='Unknown Source: ', requiredTerms={}):
        self.site = site
        self.prefix = header
        self.requiredTerms = requiredTerms

    def getFinalSearchTerm(self, term):  # format the text for a google search
        return self.prefix + ' ' + term

    def formatText(self, result):  # format the text to be posted
        return self.prefix + result + '\n'

defaults = []  # if defaults need to be hard wired

searchTerms = defaults

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    importCustomTerms()
    for item in searchTerms:
        print(item.site)


@client.event
async def on_message(message):
    if message.content.startswith('!ping'):
        await client.send_message(message.channel, 'Pong!')
    if message.content.startswith('!drugInfo'):
        await client.send_message(message.channel, "searching... :thinking:")
        await client.send_message(message.channel, searchAll(stripCommand(message.content)))

def importCustomTerms():  # imports search terms from a json file in the same directory as this file
    if not os.path.isfile('CustomSearches.json'):
        return

    with open('CustomSearches.json') as file:
        data = json.load(file)

    for item in data:
        searchTerms.append(buildNewSearchTerm(item))

    return

def searchAll(term):  # will use the given term and search all the search locations from "search terms"
    text = ''

    for searchData in searchTerms:
        text += searchData.formatText(imFeelingLucky(searchData.getFinalSearchTerm(term)))

    return text

def stripCommand(val):  # used to remove the !search from the string
    return val.split(' ', 1)[1]


def imFeelingLucky(term): # grabs the 1st url from the google search
    val = ""
    for url in search(term, stop=1, num=1):
        val = url
        break

    return val

def buildNewSearchTerm(jsonData): # creates a search term object from json data
    site = "site:" + jsonData['site']
    prefix = "null: " + jsonData['prefix']
    required = jsonData['requiredTerms']

    if required:
        for item in required:
            site += ' "' + item + '"'

    return SearchData(site, prefix)

client.run('MzYwNTkyNDEwMDc5NjU3OTg5.DKi0Vw.QiPozT9kNYLsvZ_1r08S53ej02k')
