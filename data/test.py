import numpy as np
import matplotlib.pyplot as plt
import mlpy
import sys

def getYhat(xtrain,ytrain,solver):
    solver = mlpy.LibLinear(solver_type='l2r_lr', C=1, eps=0.01, weight={})

def printStats(y,yhat,algorithm,weight,beta,label):
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
        print label
        print algorithm + "  " + str(weight) + "  " + str(beta)
        print "Accuracy on winning bids = "+str(float(predictEnd[0])/float(predictEnd[1]))+ "  " + str(predictEnd[0])+"//"+str(predictEnd[1])
        print "Accuracy on non-winning bids = "+str(float(predictNotEnd[0])/float(predictNotEnd[1])) + str(predictNotEnd[0])+"//"+str(predictNotEnd[1])

def shuffle_in_unison_inplace(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]


def main(xfile,yfile):
    x = np.loadtxt(open(xfile,"rb"),delimiter=" ")
    y = np.loadtxt(open(yfile,"rb"),delimiter=",")

    
    x , y = shuffle_in_unison_inplace(x,y)

    tr_size = 1000
    te_size = 1000

    xtrain = x[0:tr_size]
    xtest = x[tr_size:(tr_size+te_size)]

    y = np.loadtxt(open(yfile,"rb"),delimiter=",")

    ytrain =  y[0:tr_size]
    ytest = y[tr_size:(tr_size+te_size)]
    
    algorithms = ['l2r_lr','l2r_l2loss_svc_dual','l2r_l2loss_svc','l2r_l1loss_svc_dual','mcsvm_cs','l1r_l2loss_svc','l1r_lr','l2r_lr_dual']
    for algorithm in algorithms:
        for i in range(1,1000):
            beta =1
            w={0:0.1, 1:(1+i*.01)}
            solver = mlpy.LibLinear(solver_type=algorithm, C=beta, eps=0.01, weight=w)
            
            solver.learn(xtrain, ytrain)         

            yhat = solver.pred(xtrain)
            printStats(ytrain,yhat,algorithm,w,beta,"train errors")
        
            yhat = solver.pred(xtest)
            printStats(ytest,yhat,algorithm,w,beta,"test errors")

if __name__ == "__main__":
    xfile = sys.argv[1]
    yfile = sys.argv[2]
    main(xfile,yfile)
