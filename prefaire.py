#!/usr/bin/env python3
import datetime
import csv

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

def RWcsv(filename):
    dataSet=[]
    csvfile = open('csv_test.csv', 'w')
    writer = csv.writer(csvfile)
    beginYear = 2008
    previousMonth = ""
    months = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6,
              'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12
              }
    with open(filename) as f:
        next(f)
        for line in f:
            data = []
            person = splitLine(line)
            age = int(person['age'])
            xAge = int(age/5)
            data.append(str(5*xAge)+'-'+str(5*(xAge+1)))

            data.append(person['job'])

            data.append(person['marital'])

            data.append(person['education'])


            default = 0 if person["default"] == 'no' else 1
            housing = 0 if person["housing"] == 'no' else 1
            loan    = 0 if person["loan"] == 'no' else 1
#                res[default*4 + housing*2 + loan] += 1
            Debts = str(default)+str(housing)+str(loan)
#            print(str(default)+str(housing)+str(loan))
            
            data.append('-'+Debts+'-')

            data.append(person['contact'])

            data.append(person['month'])

#            day = person['day']
#            month = person['month'].lower()
#            if previousMonth == 'dec' and month == 'jan':
#                beginYear += 1
#            previousMonth = month
#            weekday = datetime.datetime(beginYear, months[month], int(day)).weekday()
#            data.append(weekday)

            duration = int(person['duration'])
            xDuration = int(duration/60)
            data.append(str(60*xDuration)+'-'+str(60*(xDuration+1)))
           
            data.append(int(person['campaign']))

            #-1的情况是什么.
            pdays = int(person['pdays'])
            xPdays = int(pdays/100)
            data.append(str(100*xPdays)+'-'+str(100*(xPdays+1)))

            data.append(int(person['previous']))

            data.append(person['poutcome'])

            data.append(person['y'])

            dataSet.append(data)
        writer.writerows(dataSet)
        csvfile.close()
            


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

def classContact(filename):
    """Group people who said 'yes' by their communication type"""
    nbPeople = 0
    moyen = { "cellular":0, "telephone":0, "unknown":0,}
                   
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)
            
            if person['y'] == 'yes':
                contact = person['contact']
                nbPeople += 1

                if contact in moyen:
                    moyen[contact] += 1
       
    for typ, val in moyen.items():
        print(typ, ':', val,'-',  "{0:.2f}".format(val/nbPeople))

def classMonth(filename):
    """Return the last contact month of year of people who said 'yes'"""
    nbPeople = 0
    mois = { "jan":0, "feb":0, "mar":0, "apr":0, "may":0, "jun":0,
              "jul":0, "aug":0, "sep":0, "oct":0, "nov":0, "dec":0, }
                   
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)
            
            if person['y'] == 'yes':
                month = person['month']
                nbPeople += 1

                if month in mois:
                    mois[month] += 1
       
    for mnth, val in mois.items():
        print(mnth, ':', val,'-',  "{0:.2f}".format(val/nbPeople))


def classDayofWeek(filename):
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
 

        
def classDuration(filename):
    """Return the last contact duration of people who said 'yes'"""
    nbPeople = totalPeople = 0
    MIN_DURATION =   0
    MAX_DURATION = 3060
    STEP = 60
    durationGroupYes = [0] * ((MAX_DURATION - MIN_DURATION) // STEP)
    durationGroupNo = [0] * ((MAX_DURATION - MIN_DURATION) // STEP)
    
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)
            totalPeople += 1
            
            if person['y'] == 'yes':
                duration = int(person['duration'])
                nbPeople += 1
                durationGroupYes[(duration - MIN_DURATION) // STEP] += 1
            else:
                duration = int(person['duration'])
                durationGroupNo[(duration - MIN_DURATION) // STEP] += 1

    print("Start End Yes No")    
    for i in range(len(durationGroupYes)):
        print(MIN_DURATION + STEP * i, '-', MIN_DURATION + STEP * (i+1), ':', durationGroupYes[i], durationGroupNo[i],)

    print(totalPeople, nbPeople)


def classCampaign(filename):
    """Group people who said 'yes' by their number of contact during this campaign"""
    nbPeople = 0
    # categories in the datasset :by number
    nb_contact = {}
                   
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)           
            if person['y'] == 'yes':
                contact = person['campaign']
                nbPeople += 1

                if contact in nb_contact:
                    nb_contact[contact] += 1
                else:
                    nb_contact[contact] = 1
                    
                
    for lvl, val in nb_contact.items():
        print(lvl, ':', val,'-',  "{0:.2f}".format(val/nbPeople))    


def classPdays(filename):
    """Group people who said 'yes' by their days after last contact"""
    verageAge = nbPeople = 0
    STEP    = 50
    dayGroup = {}
                   
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)           
            if person['y'] == 'yes':
                days = int(person['pdays'])
                nbPeople += 1


                if (days//STEP) in dayGroup:
                    dayGroup[days//STEP] +=1
                else:
                    dayGroup[days//STEP] =1
                                    
    for lvl, val in dayGroup.items():
        print(lvl, '*50-',lvl+1,'*50:', val,'-',  "{0:.2f}".format(val/nbPeople))



def classPrevious(filename):
    """Group people who said 'yes' by their number of contact"""
    nbPeople = 0

    nb_contact = {}
                   
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)           
            if person['y'] == 'yes':
                contact = person['previous']
                nbPeople += 1

                if contact in nb_contact:
                    nb_contact[contact] += 1
                else:
                    nb_contact[contact] = 1
                    
                
    for lvl, val in nb_contact.items():
        print(lvl, ':', val,'-',  "{0:.2f}".format(val/nbPeople))


def classPoutcome(filename):
    """Group people who said 'yes' by their outcome"""
    nbPeople = 0
    etat_outcome = { "failure":0, "success":0, "nonexistent":0, "unknown":0,"other":0,}
                   
    with open(filename) as f:
        next(f) # skip first line
        for line in f:
            person = splitLine(line)           
            if person['y'] == 'yes':
                etat = person['poutcome']
                nbPeople += 1

                if etat in etat_outcome:
                    etat_outcome[etat] += 1
                else:
                    print(etat)
                
    for lvl, val in etat_outcome.items():
        print(lvl, ':', val,'-',  "{0:.2f}".format(val/nbPeople))
        
def main():
    print('\n' + '*'*20 +'\n')
#    classAge(FILENAME)
    RWcsv(FILENAME) 
    print('\n' + '*'*20 +'\n')
#    classJob(FILENAME)
#    print('\n' + '*'*20 +'\n')
#    classMarital(FILENAME)
#    print('\n' + '*'*20 +'\n')
#    classEducation(FILENAME)
#    print('\n' + '*'*20 +'\n')
#    classDebts(FILENAME)
#    print('\n' + '*'*20 +'\n')
#    classCampaign(FILENAME)
#    print('\n' + '*'*20 +'\n')
#    classPDays(FILENAME)
#    print('\n' + '*'*20 +'\n')
#    classPrevious(FILENAME)
#    print('\n' + '*'*20 +'\n')
#    classPOutcome(FILENAME)
#    print('\n' + '*'*20 +'\n')
#    viewYear(FILENAME)
    
if __name__ == '__main__':
    main()
