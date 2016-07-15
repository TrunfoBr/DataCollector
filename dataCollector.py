import json
import requests
from pprint import pprint
from random import randint

databaseURL = 'https://8ddbdd99-b1ed-4834-98f5-254e9cb261df-bluemix.cloudant.com/politicos/'
documentId = 'f25a916a5a971d22928ebefba91bc5d5'
headers = {'Content-Type': 'application/json'}

amountToGenerate = 100
verbose = True
showOutput = False
attributeAmount = 5
jsonFileName = 'dbFile.json'


def main():
    print('Running the data collector...')
    data = makeData()
    json_text = json.dumps(data)
    saveToJsonFile(json_text)
    postToDatabase(json_text)

    if (showOutput):
        pprint(data)
        print(json_text)

def makeData():
    if (verbose):
        print('Generating data...')
    data = {}
    data['_id'] = documentId
    data['_rev'] = getDocumentRevision()
    data['size'] = amountToGenerate
    data['politicians'] = []
    for i in range(0, amountToGenerate):
        politician = {}
        politician['name'] = "politico #" + str(i)
        politician['attributes'] = []
        for j in range(0, attributeAmount):
            politician['attributes'].append(randint(0, 100))
        data['politicians'].append(politician)
    if (verbose):
        print('Successfully generated data!')
    return data


def getDocumentRevision():
    if (verbose):
        print('Trying to get the document revision value...')
    r = requests.get(databaseURL + documentId)
    data = json.loads(r.text)
    if (verbose):
        print('Revision value was obtained successfully!')
        print(data['_rev'])
    return data['_rev']


def saveToJsonFile(json_text):
    if (verbose):
        print('Saving json file locally...')
    with open(jsonFileName, 'w') as fileOut:
        fileOut.write(json_text)
    if (verbose):
        print('Successfully saved the local json file!')


def postToDatabase(json_text):
    if (verbose):
        print('Trying to post to database...')
    r = requests.post(databaseURL, headers = headers, data = json_text);
    if r.ok:
        print('Successfully posted to database')
    else:
        print(r.text)

if (__name__ == '__main__'):
    main()
