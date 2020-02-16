import json


# Таблица рекордов
class ScoresClass:
    def __init__(self, file_name, records_limit):
        self.scores = []
        self.scores.append({
            'score': '9959',
            'name': 'Test player',
        })
        self.file_name = file_name
        self.limit = records_limit
        self.readFile()

    def readFile(self):
        # Читаем рекорды из файла
        try:
            with open(self.file_name) as json_file:
                self.scores = json.load(json_file)
        # Если файла нет, то создаем
        except:
            with open(self.file_name, 'w') as outfile:
                json.dump(self.scores, outfile)

        self.sortScores()

    def addScore(self, name, score):
        self.scores.append({
            'score': str(score),
            'name': name,
        })
        self.sortScores()

    def writeFile(self):
        with open(self.file_name, 'w') as outfile:
            json.dump(self.scores, outfile)

    def sortKey(self, key):
        return key['score']

    def sortScores(self):
        self.scores.sort(reverse = False, key = self.sortKey)
        # Если список больше лимита, то режем его в лимит
        if len(self.scores) > self.limit:
            newscores = []
            for i in self.scores[:self.limit]:
                newscores.append({
                    'score': i['score'],
                    'name': i['name'],
                })
            self.scores = newscores

    def printScores(self):
        print('NAME', ' ' * 25, 'TIME')
        for i in self.scores:
            print('{:_<30}{:02}:{:02}'.format(i['name'], int(i['score'][0:2]), int(i['score'][2:4])))



