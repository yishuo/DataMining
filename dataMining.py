#!/usr/bin/env python3
import datetime
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
    

def classAge(filename):
    """Return the average age of people who said 'yes' and group answers"""
    averageAge = nbPeople = totalPeople = 0
    MIN_AGE =   0
    MAX_AGE = 120
    STEP    =   5
    ageGroup = [0] * ((MAX_AGE - MIN_AGE) // STEP)
    
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)
            totalPeople += 1
            
            if person['y'] == 'yes':
                age = int(person['age'])
                
                averageAge += age
                nbPeople += 1
                ageGroup[(age - MIN_AGE) // STEP] += 1
            
    averageAge /= nbPeople
    print('Average age: ', "{0:.3f}".format(averageAge))
    print('Succes rate: ', "{0:.3f}".format(nbPeople/totalPeople), '(%d/%d)' % (nbPeople, totalPeople))
    
    for i in range(len(ageGroup)):
        print(MIN_AGE + STEP * i, '-', MIN_AGE + STEP * (i+1), ':', ageGroup[i])
            

def classJob(filename):
    """Group people who said 'yes' by their job"""
    nbPeople = 0
    # there is a typo in the dataset, admin. is a category
    categories = { "admin.":0, "blue-collar":0, "entrepreneur":0,
                   "housemaid":0, "management":0, "retired":0,
                   "self-employed":0, "services":0, "student":0,
                   "technician":0, "unemployed":0, "unknown":0,
                   }
                   
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)
            
            if person['y'] == 'yes':
                job = person['job']
                nbPeople += 1

                if job in categories:
                    categories[job] += 1
       
    for cat, val in categories.items():
        print(cat, ':', val,'-',  "{0:.2f}".format(val/nbPeople))
            

def classMarital(filename):
    """Group people who said 'yes' by their marital status"""
    nbPeople = 0
    status = { "divorced":0, "married":0, "single":0, "unknown":0,
                   }
                   
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)
            
            if person['y'] == 'yes':
                marital = person['marital']
                nbPeople += 1

                if marital in status:
                    status[marital] += 1
       
    for sts, val in status.items():
        print(sts, ':', val,'-',  "{0:.2f}".format(val/nbPeople))
        
        
def classEducation(filename):
    """Group people who said 'yes' by their education"""
    nbPeople = 0
    # categories in the datasset are not the same as described
    levels = { "primary":0, "secondary":0, "tertiary":0, "unknown":0
                }
                   
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)
            
            if person['y'] == 'yes':
                education = person['education']
                nbPeople += 1

                if education in levels:
                    levels[education] += 1
                else:
                    print(education)
                
    for lvl, val in levels.items():
        print(lvl, ':', val,'-',  "{0:.2f}".format(val/nbPeople))
        

def classDebts(filename):
    """Group people by their debts (credit default, housing/personal loan)"""
    nbPeople = nbUnknown = 0
    res = [0] * 8 # 3 binary values -> 8 cells
    
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)
            
            #~ if person['y'] ==  'yes':
            if "unknown" in (person["default"], person["housing"], person["loan"]):
                nbUnknown += 1
            else:
                default = 0 if person["default"] == 'no' else 1
                housing = 0 if person["housing"] == 'no' else 1
                loan    = 0 if person["loan"] == 'no' else 1
                res[default*4 + housing*2 + loan] += 1
                nbPeople += 1
                
    print("Default  Housing  Loan")
    for i in range(8):
        print(format(i, '03b'), ':', "{0:.2f}".format(res[i]/nbPeople))
        
    print(nbPeople)
    
    
############################ C ###############################
############################ C ###############################
############################ C ###############################

def classCampaign(filename):
    """Group people who said 'yes' by the number of contacts performed during the campaign"""
    nbPeople = 0
    totalCampaign = {}
    
    with open(filename) as f:        
        next(f) # skip first line
        for line in f:
            person = splitLine(line)            
            if person['y'] == 'yes':
                nbrCampaign = int(person["campaign"])
                nbPeople += 1
                
                if nbrCampaign in totalCampaign:
                    totalCampaign[nbrCampaign] += 1
                else:
                    totalCampaign[nbrCampaign] = 1
                    
    for key, val in totalCampaign.items():
        print("{:2d} : {:3d} - {:.2f}".format(key, val, val/nbPeople))


def classPDays(filename):
    """Return the average pDays of people who said 'yes' and group answers"""
    averagePDays = nbPeople = totalPeople = notContacted = 0
    MIN_PDAYS =    0
    MAX_PDAYS = 1000
    STEP    = 100
    pDaysGroup = [0] * ((MAX_PDAYS - MIN_PDAYS) // STEP)
    
    with open(filename) as f:        
        next(f) # skip first line
        for line in f:
            person = splitLine(line)
            totalPeople += 1            
            if person['y'] == 'yes':
              pDays = int(person["pdays"])
              if pDays == -1:
                  notContacted += 1
              else:
                  averagePDays += pDays
                  nbPeople += 1
                  pDaysGroup[(pDays - MIN_PDAYS) // STEP] += 1
            
    averagePDays /= nbPeople
    print('Average pDays: ', "{0:.3f}".format(averagePDays))
    print('Succes rate: ', "{0:.3f}".format(nbPeople/totalPeople), '(%d/%d)' % (nbPeople, totalPeople))
    print('Number of people whose was not previously contacted : ' + str(notContacted))
    for i in range(len(pDaysGroup)):
        print(MIN_PDAYS + STEP * i, '-', MIN_PDAYS + STEP * (i+1), ':', pDaysGroup[i])


def classPrevious(filename):
    """Group people who said 'yes' by the number of contacts performed during the campaign"""
    nbPeople = notContacted = 0
    totalPrevious = {}
    
    with open(filename) as f:        
        next(f) # skip first line
        for line in f:
            person = splitLine(line)            
            if person['y'] == 'yes':
                nbrPrevious = int(person["previous"])
                nbPeople += 1
                
                if nbrPrevious in totalPrevious:
                    totalPrevious[nbrPrevious] += 1
                else:
                    totalPrevious[nbrPrevious] = 1
                    
    for key, val in totalPrevious.items():
        print("{:2d} : {:3d} - {:.2f}".format(key, val, val/nbPeople))
        

def classPOutcome(filename):
    """Group people who said 'yes' by their marital status"""
    nbPeople = 0
    status = { "failure":0, "success":0, "other":0, "unknown":0 }
                   
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)
            
            if person['y'] == 'yes':
                pOutcome = person['poutcome']
                nbPeople += 1

                if pOutcome in status:
                    status[pOutcome] += 1
       
    for sts, val in status.items():
        print(sts, ':', val,'-',  "{0:.2f}".format(val/nbPeople))

############################ C ###############################
############################ C ###############################
############################ C ###############################
############################ C ###############################

def viewYear(filename):
    nbPeople = 0
    beginYear = 2008
    previousMonth = ""
    months = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6,
              'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12
              }
              
    dayOfWeek = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
    countDay  = [0] * 7
    
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            nbPeople += 1
            person = splitLine(line)
            day = person['day']
            month = person['month'].lower()
            
            if previousMonth == 'dec' and month == 'jan':
                beginYear += 1
                
            previousMonth = month
            
            
            weekday = datetime.datetime(beginYear, months[month], int(day)).weekday()
            #~ print(day, month, beginYear, dayOfWeek[weekday])
            countDay[weekday] += 1
            
    for i in range(7):
        print(dayOfWeek[i], "{0:4d} {1:.4f}".format(countDay[i], countDay[i]/nbPeople))
 
def main():
    print('\n' + '*'*20 +'\n')
    classAge(FILENAME)
    print('\n' + '*'*20 +'\n')
    classJob(FILENAME)
    print('\n' + '*'*20 +'\n')
    classMarital(FILENAME)
    print('\n' + '*'*20 +'\n')
    classEducation(FILENAME)
    print('\n' + '*'*20 +'\n')
    classDebts(FILENAME)
    print('\n' + '*'*20 +'\n')
    classCampaign(FILENAME)
    print('\n' + '*'*20 +'\n')
    classPDays(FILENAME)
    print('\n' + '*'*20 +'\n')
    classPrevious(FILENAME)
    print('\n' + '*'*20 +'\n')
    classPOutcome(FILENAME)
    print('\n' + '*'*20 +'\n')
    viewYear(FILENAME)
    
if __name__ == '__main__':
    main()
