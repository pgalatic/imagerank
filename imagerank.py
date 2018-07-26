import os
import random
import itertools
from elo import elo
from PIL import Image

NUM_FILES = 30
NUM_PARTITIONS = 5
DIRNAME = 'ranked/'
COMPARE_FACTOR = 0.15

class Ranker():
    def __init__(self, folder):
        self._folder = folder + '/'
        filenames = [f for f in os.listdir(folder + '/.') if f.endswith('.png') or f.endswith('.jpg')]
        
        self._chosenfiles = set(random.choices(filenames, k=NUM_FILES))
        self._combinations = list(itertools.combinations(self._chosenfiles, 2))
        self._dist = [int((i+1) * (100 / NUM_PARTITIONS))
                        for i in range(NUM_PARTITIONS)]
        self._scoredict = {filename: 1000 for filename in self._chosenfiles}
        self._counter = 0
        
        random.shuffle(self._combinations)
    
    def query(self):
        valid = False
        
        while not valid:
            if self._counter >= len(self._combinations):
                return None, None
        
            nameA = self._combinations[self._counter][0]
            nameB = self._combinations[self._counter][1]
            
            scoreA = self._scoredict[nameA]
            scoreB = self._scoredict[nameB]
            # skip comparisons that are of no contest
            if abs(elo.expected(scoreA, scoreB) - 0.5) < COMPARE_FACTOR:
                print(abs(elo.expected(scoreA, scoreB)))
                valid = True
            else:
                print('SKIP: %s vs %s' % (nameA, nameB))
            
            self._counter += 1
            
        return nameA, nameB
    
    def process(self, winner, loser):        
        scoreA = self._scoredict[winner]
        scoreB = self._scoredict[loser]
        
        expA = elo.expected(scoreA, scoreB)
        expB = elo.expected(scoreB, scoreA)
        
        newA = elo.elo(scoreA, expA, 1)
        newB = elo.elo(scoreB, expB, 0)
        
        self._scoredict[winner] = newA
        self._scoredict[loser] = newB
                
    def finish(self):
        sortedscores = sorted(
            self._scoredict, key=self._scoredict.get, reverse=True)
        l = max(int(len(sortedscores) / NUM_PARTITIONS), 1)
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