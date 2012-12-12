import numpy as np
import matplotlib.pyplot as plt
import mlpy
import sys

def getYhat(xtrain,ytrain,solver):
    solver = mlpy.LibLinear(solver_type='l2r_lr', C=1, eps=0.01, weight={})

def printStats(y,yhat,algorithm,weight,beta,label, f):
    predictEnd = [0,0]
    predictNotEnd = [0,0] 
    for r1,r2 in zip(y,yhat):
        if r1 == 1:
            predictEnd[1] = predictEnd[1] + 1
            predictEnd[0] = predictEnd[0] + r2
        else:
            predictNotEnd[1] = predictNotEnd[1] + 1
            if r2 == 0:
                predictNotEnd[0] = predictNotEnd[0] + 1
    if (float(predictEnd[0])/float(predictEnd[1]))*(float(predictNotEnd[0])/float(predictNotEnd[1])) != 0:
    	f.write(str(weight)+" "+str(beta)+ " " +str(float(predictEnd[0])/float(predictEnd[1]))+" "+str(float(predictNotEnd[0])/float(predictNotEnd[1]))+ '\n')
   #     print label
   #     print algorithm + "  " + str(weight) + "  " + str(beta)
   #     print "Accuracy on winning bids = "+str(float(predictEnd[0])/float(predictEnd[1]))+ "  " + str(predictEnd[0])+"//"+str(predictEnd[1])
   #     print "Accuracy on non-winning bids = "+str(float(predictNotEnd[0])/float(predictNotEnd[1])) + str(predictNotEnd[0])+"//"+str(predictNotEnd[1])

def shuffle_in_unison_inplace(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

def main(xfile,yfile,algorithm=""):
    x = np.loadtxt(open(xfile,"rb"),delimiter=" ")
    y = np.loadtxt(open(yfile,"rb"),delimiter=",")

    
    x,y = shuffle_in_unison_inplace(x,y)

    tr_size = 6000
    te_size = 4000

    xtrain = x[0:tr_size]
    xtest = x[tr_size:(tr_size+te_size)]


    ytrain =  y[0:tr_size]
    ytest = y[tr_size:(tr_size+te_size)]
    
    algorithms = ['l1r_lr']
    for algorithm in algorithms:
    	print algorithm
	ftest = open(str(algorithm) +'_Test.csv','w')
	ftrain = open(str(algorithm) +'_Train.csv','w')
	ftest.write("Weight beta Accuracy_on_winning_bids Accuracy_on_nonwinning_bids\n")
	ftrain.write("Weight beta Accuracy_on_winning_bids Accuracy_on_nonwinning_bids\n")
        for i in range(1,10):
	    for b in range(1,20):
	    	
            	beta = .2 + .1*b
            	w={0:1, 1:(+i*.5)}
            	solver = mlpy.LibLinear(solver_type=algorithm, C=beta, eps=0.01, weight=w)
            	solver.learn(xtrain, ytrain)         

            	yhat = solver.pred(xtrain)
            	printStats(ytrain,yhat,algorithm,.0+i*.2,beta,"train errors",ftrain)
        
        	yhat = solver.pred(xtest)
            	printStats(ytest,yhat,algorithm,.0+i*.2,beta,"test errors", ftest)
	ftest.close()
	ftrain.close()
        

    ftest = open("Classification" +'_Test.csv','w')
    print "Class"
    ftrain = open("Classification"+'_Train.csv','w')
    ftest.write("Weight beta Accuracy_on_winning_bids Accuracy_on_nonwinning_bids\n")
    ftrain.write("Weight beta Accuracy_on_winning_bids Accuracy_on_nonwinning_bids\n")    
    solver = mlpy.ClassTree()
    solver.learn(xtrain, ytrain)         
    yhat = solver.pred(xtrain)
    printStats(ytrain,yhat,"Classification Tree","none","none","train errors", ftrain)
    yhat = solver.pred(xtest)
    printStats(ytest,yhat,"Classification Tree","none","none","test errors", ftest)
    ftest.close()
    ftrain.close()
  

if __name__ == "__main__":
    xfile = sys.argv[1]
    yfile = sys.argv[2]
    main(xfile,yfile)
