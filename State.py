import requests


class State:

    def __init__(self):
        self.date = "00-00-0000"
        self.name = "Unknown"
        self.cases = -1
        self.deaths = -1


listState = []
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv'
r = requests.get(url, allow_redirects=True)
open('us-states.csv', 'wb').write(r.content)

covidStateCases = open("us-states.csv", 'r')

Lines = covidStateCases.readlines()
Lines.pop(0)

count = 0
for line in Lines:
    line = Lines[count].split(',')
    s1 = State()
    s1.date = line[0]
    s1.name = line[1]
    s1.cases = line[3]
    s1.deaths = line[4]

    listState.append(s1)
    count += 1


