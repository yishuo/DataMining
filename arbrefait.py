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


def createDataSet(filename):
#    dataSet=[[1,1,1,'yes'],
#             [1,1,0,'yes'],
#             [1,1,2,'yes'],
#             [0,1,3,'yes'],
#             [1,0,0,'no'],
#             [0,1,1,'no'],
#             [0,0,2,'no'],
#             [0,0,3,'no']]
#    dataSet = "bank.csv"
    dataSet=[]
#    csvfile = open('csv_test.csv', 'w')
#    writer = csv.writer(csvfile)
    with open(filename) as f:
        next(f)
        for line in f:
            data = []
            person = splitLine(line)
            age = int(person['age'])
            xAge = int(age/5)
            if((xAge<=4)):
                data.append('0-20')
            elif((xAge>4)&(xAge<=14)):
                data.append('20-70')
            else:
                data.append('>70')
                
#            data.append(str(5*xAge)+'-'+str(5*(xAge+1)))

            if((person['job']=='student')&(person['job']=='unemployed')&(person['job']=='unknown')):
                data.append('no income')
            else:
                data.append('income')

#            data.append(person['job'])

            data.append(person['marital'])

            if(person['education']=='tertiary'):
                data.append('tertiary')
            else:
                data.append('<=secondary')

#            data.append(person['education'])


            default = 0 if person["default"] == 'no' else 1
            housing = 0 if person["housing"] == 'no' else 1
            loan    = 0 if person["loan"] == 'no' else 1
            Debts = '-'+str(default)+str(housing)+str(loan)+'-'
            if(Debts=='-000-'):
                data.append('no loan')
            else:
                data.append('loan')

            data.append(person['contact'])

            if((person['month']=='jul')&(person['month']=='aug')
               &(person['month']=='dec')&(person['month']=='jan')):
                data.append('vacation(1,7,8,12)')
            else:
                data.append('work(others)')

#            data.append(person['month'])

            duration = int(person['duration'])
            xDuration = int(duration/60)
            if((xDuration>0)&(xDuration<=8)):
                data.append('0-8(min)')
#            elif((xDuration>4)&(xDuration<=8)):
#                data.append('4-8(min)')                
            else:
                data.append('>8(min)')
                
#            data.append(str(500*xDuration)+'-'+str(500*(xDuration+1)))

            if((int(person['campaign'])>0)&(int(person['campaign'])<=5)):
                data.append('0-5')
            elif((int(person['campaign'])>5)&(int(person['campaign'])<=10)):
                data.append('5-10')
            else:
                data.append('>10')
#            data.append(int(person['campaign']))

            #-1的情况是什么.
#            pdays = int(person['pdays'])
#            xPdays = int(pdays/100)
#            data.append(str(100*xPdays)+'-'+str(100*(xPdays+1)))
            if(int(person['pdays'])<0):
                data.append('<0')
            elif((int(person['pdays'])>=0)&(int(person['pdays'])<=7)):
                data.append('0-7')
            else:
                data.append('>7')

            if(int(person['previous'])==0):
                data.append('=0')
            else:
                data.append('>0')

#            data.append(int(person['previous']))

            if(person['poutcome']=='success'):
                data.append('success')
            else:
                data.append('other')
                
#            data.append(person['poutcome'])

            data.append(person['y'])

            dataSet.append(data)
    labels = ['age', 'job', 'marital', 'education', 'Debts',
              'contact','month', 'duration',
              'campaign', 'pdays', 'previous', 'poutcome']
    return dataSet, labels

'''
def createDataSet():
#    dataSet=[[30, 'unemployed', 'married', 'primary', 1, -1, 0, 'unknown', 'yes'], [33, 'services', 'married', 'secondary', 1, 339, 4, 'failure', 'no'], [35, 'management', 'single', 'tertiary', 1, 330, 1, 'failure', 'yes'], [30, 'management', 'married', 'tertiary', 4, -1, 0, 'unknown', 'no'], [59, 'blue-collar', 'married', 'secondary', 1, -1, 0, 'unknown', 'no'], [35, 'management', 'single', 'tertiary', 2, 176, 3, 'failure', 'no'], [36, 'self-employed', 'married', 'tertiary', 1, 330, 2, 'other', 'no'], [39, 'technician', 'married', 'secondary', 2, -1, 0, 'unknown', 'no'], [41, 'entrepreneur', 'married', 'tertiary', 2, -1, 0, 'unknown', 'no']]

    labels = ['age', 'job', 'marital', 'education',
              'campaign', 'pdays', 'previous', 'poutcome']
    return dataSet, labels
'''
#计算香农熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for feaVec in dataSet:
        currentLabel = feaVec[-1]
        if currentLabel not in labelCounts:
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
     
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1#因为数据集的最后一项是标签
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy -newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature
             
#因为我们递归构建决策树是根据属性的消耗进行计算的，所以可能会存在最后属性用完了，但是分类
#还是没有算完，这时候就会采用多数表决的方式计算节点分类
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    return max(classCount)         
    
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) ==len(classList):#类别相同则停止划分
        return classList[0]
    if len(dataSet[0]) == 1:#所有特征已经用完
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]#为了不改变原始列表的内容复制了一下
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, 
                                        bestFeat, value),subLabels)
    return myTree








#定义文本框和箭头格式  
decisionNode = dict(boxstyle="sawtooth", fc="0.8") #定义判断节点形态  
leafNode = dict(boxstyle="round4", fc="0.5") #定义叶节点形态  
arrow_args = dict(arrowstyle="<-") #定义箭头  
  
#绘制带箭头的注解  
#nodeTxt：节点的文字标注, centerPt：节点中心位置,  
#parentPt：箭头起点位置（上一节点位置）, nodeType：节点属性  
def plotNode(nodeTxt, centerPt, parentPt, nodeType):  
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',  
             xytext=centerPt, textcoords='axes fraction',  
             va="center", ha="center", bbox=nodeType, arrowprops=arrow_args )

#计算叶节点数  
def getNumLeafs(myTree):  
    numLeafs = 0  
    firstStr = list(myTree.keys())[0]   
    secondDict = myTree[firstStr]   
    for key in secondDict.keys():  
        if type(secondDict[key]).__name__=='dict':#是否是字典  
            numLeafs += getNumLeafs(secondDict[key]) #递归调用getNumLeafs  
        else:   numLeafs +=1 #如果是叶节点，则叶节点+1  
    return numLeafs  
  
#计算数的层数  
def getTreeDepth(myTree):  
    maxDepth = 0  
    firstStr = list(myTree.keys())[0]  
    secondDict = myTree[firstStr]  
    for key in secondDict.keys():  
        if type(secondDict[key]).__name__=='dict':#是否是字典  
            thisDepth = 1 + getTreeDepth(secondDict[key]) #如果是字典，则层数加1，再递归调用getTreeDepth  
        else:   thisDepth = 1  
        #得到最大层数  
        if thisDepth > maxDepth:  
            maxDepth = thisDepth

        maxDepth = 3
    return maxDepth

#在父子节点间填充文本信息  
#cntrPt:子节点位置, parentPt：父节点位置, txtString：标注内容  
def plotMidText(cntrPt, parentPt, txtString):  
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]  
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]  
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)

    #绘制树形图  
#myTree：树的字典, parentPt:父节点, nodeTxt：节点的文字标注  
def plotTree(myTree, parentPt, nodeTxt):  
    numLeafs = getNumLeafs(myTree)  #树叶节点数  
    depth = getTreeDepth(myTree)    #树的层数  
    firstStr = list(myTree.keys())[0]     #节点标签  
    #计算当前节点的位置  
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)  
    plotMidText(cntrPt, parentPt, nodeTxt) #在父子节点间填充文本信息  
    plotNode(firstStr, cntrPt, parentPt, decisionNode) #绘制带箭头的注解  
    secondDict = myTree[firstStr]  
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD  
    for key in secondDict.keys():  
        if type(secondDict[key]).__name__=='dict':#判断是不是字典，  
            plotTree(secondDict[key],cntrPt,str(key))        #递归绘制树形图  
        else:   #如果是叶节点  
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW  
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)  
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))  
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD  
  
#创建绘图区  
def createPlot(inTree):  
    fig = plt.figure(1, facecolor='white')  
    fig.clf()  
    axprops = dict(xticks=[], yticks=[])  
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)      
    plotTree.totalW = float(getNumLeafs(inTree)) #树的宽度  
    plotTree.totalD = float(getTreeDepth(inTree)) #树的深度  
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;  
    plotTree(inTree, (0.5,1.0), '')  
    plt.show()








    
def main():
#    data,label = createDataSet(FILENAME)
    data,label = createDataSet(FILENAME)
    t1 = time.clock()
    myTree = createTree(data,label)
    t2 = time.clock()
#    print(myTree)
    createPlot(myTree)
    print('execute for ',t2-t1)
if __name__=='__main__':
    main()
