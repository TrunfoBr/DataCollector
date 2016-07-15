import json
from pprint import pprint
from random import randint

databaseKey = 'urnoopiestortsintlesedow'
databasePassword = 'f93fd3bb40a8c04e69a2be826870e6dc076a4911'
databaseURL = 'https://8ddbdd99-b1ed-4834-98f5-254e9cb261df-bluemix.cloudant.com/politicos/f25a916a5a971d22928ebefba91bc5d5'

amountToGenerate = 100
showOutput = False

def main():
    print('Running the data collector')
    data = makeData()
    json_text = json.dumps(data)
    saveToJsonFile(json_text)
    if (showOutput):
        pprint(data);
        print(json_text)

def makeData():
    data = {}
    data['size'] = amountToGenerate
    data['politicians'] = []
    for i in range(0,amountToGenerate):
        politician = {}
        politician['name'] = "politico #" + str(i)
        politician['attributes'] = []
        for j in range(0,5):
            politician['attributes'].append(randint(0,100))
        data['politicians'].append(politician)
    return data

def saveToJsonFile(json_text):
    with open('dbFile.json','w') as fileOut:
        fileOut.write(json_text)

if (__name__ == '__main__'):
    main()

    # {"size":2,"politicians":[{"name":"Fulaninho - PHC","attributes":[34,23,0,12,45]},
    #                          {"name":"Beltraninho - PHC","attributes":[50,10,15,32,7]}]}