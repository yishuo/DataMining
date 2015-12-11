#coding=utf-8
import operator
from math import log
import time
import matplotlib.pyplot as plt


FILENAME = "bank.csv"


def splitLine(line):
    """Return a dict object containing all infos of a person"""
    ar = line.split(';')
    categories = ["age", "job", "marital", "education", 
                  "default", "balance", "housing", "loan", 
                  "contact", "day", "month", "duration", 
                  "campaign", "pdays", "previous", "poutcome", "y" ]
    person = {}
                  
    for i in range(len(ar)):
        person[categories[i]] = ar[i].replace('"', '').replace('\n', '')
        
    return person


def calcul(filename):
    with open(filename) as f:
        next(f)
        yesNumber=0
        noNumber=0
        number=0
        for line in f:
            person = splitLine(line)
            default = 0 if person["default"] == 'no' else 1
            housing = 0 if person["housing"] == 'no' else 1
            loan    = 0 if person["loan"] == 'no' else 1
            Debts = '-'+str(default)+str(housing)+str(loan)+'-'
            if((person['poutcome'] == 'success')
               & (Debts!='-000-')
#               & (int(person['duration'])>480)
               & (person['contact']=='telephone')):
                number+=1
                if(person['y']=='yes'):
                    yesNumber += 1
                else:
                    noNumber += 1
#    print(number)
    print('Number: '+str(number)+'\n'+'yes: '+str(yesNumber)+'\n'+'no: '+str(noNumber)
          +'\n'+'yes%: '+ "{0:.2f}".format(yesNumber/number))
          
                            
def main():
    calcul(FILENAME)
if __name__=='__main__':
    main()
