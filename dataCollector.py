import json
import requests
from pprint import pprint
from random import randint

databaseURL = 'https://8ddbdd99-b1ed-4834-98f5-254e9cb261df-bluemix' + \
              '.cloudant.com/politicos/'
documentId = 'f25a916a5a971d22928ebefba91bc5d5'
dbHeaders = {'Content-Type': 'application/json'}

appToken = 'UmC2Xc1q3qjJ'

verbose = True
showOutput = True
overwritedb = True
amountToGenerate = 32
attributeAmount = 5
jsonFileName = 'dbFile.json'


def main():
    print('Running the data collector...')
    data = makeData()
    json_text = json.dumps(data)
    saveToJsonFile(json_text)
    if overwritedb:
        postToDatabase(json_text)

    if showOutput:
        pprint(data)


def makeData():
    log('Generating data...')
    data = {}
    data['_id'] = documentId
    if overwritedb:
        data['_rev'] = getDocumentRevision()
    data['size'] = amountToGenerate
    data['politicians'] = []
    data['politicians'].append(processCandidate(1556321)) # Tiririca
    data['politicians'].append(processCandidate(1536940)) # Aecio
    data['politicians'].append(processCandidate(1549993)) # Marcelo Crivella
    data['politicians'].append(processCandidate(1538644)) # Reguffe
    data['politicians'].append(processCandidate(1540356)) # Ronaldo Caiado
    data['politicians'].append(processCandidate(1553259)) # José Serra
    data['politicians'].append(processCandidate(1547943)) # Romário
    data['politicians'].append(processCandidate(1541067)) # Roberto Rocha
    data['politicians'].append(processCandidate(1552319)) # Lasier Martins
    data['politicians'].append(processCandidate(1538723)) # Izalci
    data['politicians'].append(processCandidate(1537726)) # Fraga
    data['politicians'].append(processCandidate(1538344)) # ÉRIKA KOKAY
    data['politicians'].append(processCandidate(1538030)) # Rogerio Rosso
    data['politicians'].append(processCandidate(1538630)) # Ronaldo Fonseca
    data['politicians'].append(processCandidate(1536938)) # Aloisio Ferreira
    data['politicians'].append(processCandidate(1554099)) # Andres Sanchez
    data['politicians'].append(processCandidate(1553846)) # Antonio Bulhoes
    data['politicians'].append(processCandidate(1556235)) # Arlindo Chinaglia
    data['politicians'].append(processCandidate(1556459)) # Arnaldo Faria
    data['politicians'].append(processCandidate(1556265)) # Beto Mansur
    data['politicians'].append(processCandidate(1555985)) # Bruna Furlan
    data['politicians'].append(processCandidate(1555562)) # Carlos Sampaio
    data['politicians'].append(processCandidate(1555980)) # Celso Russomano
    data['politicians'].append(processCandidate(1555458)) # Dr Sinval Medeiros
    data['politicians'].append(processCandidate(1554826)) # Duarte Nogueira
    data['politicians'].append(processCandidate(1547943)) # Romario
    data['politicians'].append(processCandidate(1546673)) # Alvaro Dias
    data['politicians'].append(processCandidate(1546851)) # Alex
    data['politicians'].append(processCandidate(1547071)) # Assis do Couto
    data['politicians'].append(processCandidate(1546920)) # Cristiane
    data['politicians'].append(processCandidate(1550012)) # Jean Willis
    data['politicians'].append(processCandidate(1548184)) # Jair Bolsonaro
    # data['politicians'].append(processCandidate(1546260)) # DELEGADO FRANCISCHINI
    # data['politicians'].append(processCandidate(1546680)) # DIRCEL
    # data['politicians'].append(processCandidate(1546261)) # GIACOBO
    # data['politicians'].append(processCandidate(1546575)) # HERMES FRANGÃO PARCIANELLO"
    # data['politicians'].append(processCandidate(1546933)) # JOAO ARRUDA
    # data['politicians'].append(processCandidate(1537300)) # Eunicio
    # data['politicians'].append(processCandidate(1537281)) # Taisso
    # data['politicians'].append(processCandidate(1537282)) # Andre Figueiredo
    # data['politicians'].append(processCandidate(1537437)) # Danilo Forte
    # data['politicians'].append(processCandidate(1537147)) # Domingos Neto
    # data['politicians'].append(processCandidate(1537295)) # Genecias Noronha




    completeDataWithRandomData(data)
    log('Successfully generated data!')
    return data


def processCandidate(candidateId):
    headers = {'Content-Type': 'application/json', 'App-Token':appToken}
    url = 'http://api.transparencia.org.br:80/sandbox/v1/candidatos/' + str(candidateId)
    r = requests.get(url, headers=headers)
    if not r.ok:
        print('Error on candidate ' + str(candidateId) + ': ' + r.text)
        return None
    else:
        data = json.loads(r.text)
        politician = {}
        politician['name'] = data['apelido'] + ' - ' + data['partido']
        politician['attributes'] = processAttributes(candidateId)
        return politician


def processAttributes(candidateId):
    headers = {'Content-Type': 'application/json', 'App-Token':appToken}
    url = 'http://api.transparencia.org.br:80/sandbox/v1/candidatos/' + str(candidateId) + '/estatisticas'
    r = requests.get(url, headers=headers)
    if not r.ok:
        print('Error on attributes of candidate ' + str(candidateId) + ': ' + r.text)
        return None
    else:
        data = json.loads(r.text)
        attributes = []
        attributes.append(float(data[0]['faltasPlenario']))
        attributes.append(float(data[0]['mediaPlenario']))
        attributes.append(float(data[0]['evolucao']))
        attributes.append(float(data[0]['emendas']))
        attributes.append(float(data[0]['mediaEmendas']))
        return attributes


def completeDataWithRandomData(data):
    for i in range(len(data['politicians']), amountToGenerate):
        politician = {}
        politician['name'] = "Político #" + str(i)
        politician['attributes'] = []
        for j in range(0, attributeAmount):
            politician['attributes'].append(randint(0, 100))
        data['politicians'].append(politician)


def getDocumentRevision():
    log('Trying to get the document revision value...')
    r = requests.get(databaseURL + documentId)
    data = json.loads(r.text)
    log('Revision value was obtained successfully!')
    log(data['_rev'])
    return data['_rev']


def saveToJsonFile(json_text):
    log('Saving json file locally...')
    with open(jsonFileName, 'w') as fileOut:
        fileOut.write(json_text)
    if verbose:
        print('Successfully saved the local json file!')


def postToDatabase(json_text):
    log('Trying to post to database...')
    r = requests.post(databaseURL, headers=dbHeaders, data=json_text)
    if r.ok:
        print('Successfully posted to database')
    else:
        print(r.text)


def log(msg):
    if verbose:
        print(msg)

if __name__ == '__main__':
    main()
