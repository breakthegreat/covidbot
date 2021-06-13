import requests

url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us.csv'

r = requests.get(url, allow_redirects=True)
open('us.csv', 'wb').write(r.content)

covidCases = open("us.csv", 'r')

Lines = covidCases.readlines()

line = Lines[1].split(',')

date = line[0]
cases = line[1]
deaths = line[2]
confirmed_cases = line[3]
confirmed_deaths = line[4]


def getDate():
    return date


def getCases():
    return cases


def getDeaths():
    return deaths
