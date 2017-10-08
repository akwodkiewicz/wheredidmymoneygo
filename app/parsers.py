from abc import ABC, abstractmethod
import csv
import datetime
import os
import sys
from pprint import pprint

class Parser(ABC):

    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def prepare_csv(self):
        pass

    @abstractmethod
    def parse(self):
        pass



class INGParser(Parser):

    indices = {
        'account': 14,
        'amount': 8,
        'date': 0,
        'title': 3,
        'to': 2
    }

    def prepare_csv(self):
        self.prepared = os.path.splitext(self.filename)[0]+"_prepared.csv"
        with open(self.filename, 'r') as f_in, \
                open(self.prepared, 'w', newline='') as f_out:
            reader = csv.reader(f_in, delimiter=';')
            writer = csv.writer(f_out, delimiter=',')
            counter = 0
            for row in reader:
                counter += 1
                if counter >= 22 and len(row) > 10:
                    writer.writerow(row)

    def parse(self):
        self.transactions = []
        with open(self.prepared, 'r') as f:
            for row in csv.reader(f, delimiter=','):
                transaction = {}
                for k, v in self.indices.items():
                    transaction[k] = row[v]
                self.transactions.append(transaction)

    def print_data(self):
        print(self)
        print(40*'=')
        pprint(self.transactions)
