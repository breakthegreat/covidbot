import requests


class USCovid:
    def __init__(self):
        url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us.csv'
        r = requests.get(url, allow_redirects=True)
        open('us.csv', 'wb').write(r.content)

        covidCases = open("us.csv", 'r')

        Lines = covidCases.readlines()

        line = Lines[1].split(',')
        self.date = line[0]
        self.cases = line[1]
        self.deaths = line[2]

print("============================================ US_General.py loaded ============================================")

# def getDate():
#     return date
#
#
# def getCases():
#     return cases
#
#
# def getDeaths():
#     return deaths
