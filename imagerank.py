import os
import random
import itertools

NUM_FILES = 10
NUM_PARTITIONS = 5
DIRNAME = 'ranked/'

class Ranker():
    def __init__(self, folder):
        self._folder = folder + '/'
        filenames = [f for f in os.listdir(folder + '/.') if not os.path.isdir(f)]
        
        self._chosenfiles = set(random.choices(filenames, k=NUM_FILES))
        self._combinations = list(itertools.combinations(self._chosenfiles, 2))
        self._dist = [int((i+1) * (100 / NUM_PARTITIONS))
                        for i in range(NUM_PARTITIONS)]
    
    def query(self):
        random.shuffle(self._combinations)
        return self._combinations
    
    def process(self, scores):
        scoredict = {filename: 0 for filename in self._chosenfiles}
        
        for scorecomp in zip(self._combinations, scores):
            scoredict[scorecomp[0][0]] += scorecomp[1][0]
            scoredict[scorecomp[0][1]] += scorecomp[1][1]
        
        sortedscores = sorted(scoredict, key=scoredict.get, reverse=True)
        l = int(len(sortedscores) / NUM_PARTITIONS)
        chunks = self.partitions(sortedscores, l)
        
        if not os.path.isdir(self._folder + DIRNAME):
            self.makedirs()
        
        for obj in zip(chunks, self._dist):
            print(obj)
            for f in obj[0]:
                src = self._folder + f
                dst = self._folder + DIRNAME + str(obj[1]) + '/' + f
                os.rename(src, dst)
        
    def partitions(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i+n]
    
    def makedirs(self):
        os.mkdir(self._folder + DIRNAME)
        for d in self._dist:
            os.mkdir(self._folder + DIRNAME + '/' + str(d))