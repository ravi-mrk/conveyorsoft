import random
import os
import sys

class Input:
#This class defines the properties of items from Input side from where A and B items are emitted

    def __init__(self, items):
        self.items = items

# Since items are randomly generated, taking a random generator to generate A, B items randomly
    def new(self):
        return random.choice(self.items)


class Stat:
#Passing values by reference

    def __init__(self, val):
        self.val = val

class Belt:
# This class takes in the properties - state of conveyor(stats),Input item on container, workers and computes
    def __init__(self, input, computes, stats=3):
        self.stats = [Stat('')] * stats
        self.input = input
        self.workers = Belt.prod_unit(self.stats)
        self.computes = computes

    @staticmethod
    def prod_unit(stats):
# This function defines the worker action on conveyor belt returning 2 workers per stage
        workers = {}
        for i, _ in enumerate(stats):
# Two workers on either side of the conveyor belts
            workers[i] = Staff('R_Pair%d' % i, ['A', 'B'], 3, Staff('L_Pair%d' % i, ['A', 'B'], 3))
        return workers

    def edge(self, t):
# Printing the item at the out edge of the conveyor belt
        print('step %d: %s' % (t, ' | '.join([s.val for s in self.stats])))

    def start(self, limit=100):
        for t in range(limit):
            print('\n')
# Moving the belt position
            self.stats = [Stat(self.input.new())] + self.stats[:-1]
# Print the belt position
            self.edge(t+1)
# for each stat, invoke start for the workers
            for i, s in enumerate(self.stats):
                self.workers[i].start(s)
# print the belt
            self.edge(t+1)
# Now aggregating
            self.computes.start(self.stats[-1])
            print('\n')
        self.computes.report()

class Computes:
#Computing the output

    def __init__(self):
        self.data = {'P': 0, 'A': 0, 'B': 0}

    def start(self, out):
         if len(out.val) > 0:
            key = out.val[0]
            self.data[key] += 1

    def report(self):
        print('Total Products: %d' % self.data['P'])
        print('Total Unpicked: %d' % (self.data['A'] + self.data['B']))

class Staff:
    '''
    This class defines properties of workers at conveyor.
    worker: Worker at a conveyor belt
    co_worker: Co-worker on the same conveyor belt (Initially considering as None for ease)
    tot_time: total time to deliver a finished product
    all_parts: Required parts for making the product
    '''

    def __init__(self, worker, all_parts, tot_time, co_worker=None):
        self.worker = worker
        self.co_worker = co_worker
        self.tot_time = tot_time
        self.all_parts = all_parts
        self.available = []
        self.exc = tot_time

#This function is called by the belt throughout the execution time.
    def start(self, stat):
        if all([i in self.available for i in self.all_parts]):
            if self.exc <= 0:
                print('<%s> P is ready.' % self.worker)
                if stat.val == '':
                    self.available = []
                    self.exc = self.tot_time
                    print('<%s> Putting P.' % self.worker)
                    stat.val = 'P (%s)' % self.worker
                else:
                    if self.co_worker: self.co_worker.start(stat)
            else:
                self.exc -= 1
                if self.co_worker: self.co_worker.start(stat)
# From here, we scan for parts
        else:
            if stat.val not in self.available and stat.val in self.all_parts:
# Adding new item to the current workers availability list
                print('<%s> Picking up %s.' % (self.worker, stat.val))
                self.available.append(stat.val)
                stat.val = ''
            else:
                if self.co_worker: self.co_worker.start(stat)

def main():
#Inputs to Conveyor belt are A, B and Nil items. Nil / None is taken as '' in here
    Belt(Input(['A', 'B', '']), Computes(), stats=3).start()


if __name__ == "__main__":
    main()
