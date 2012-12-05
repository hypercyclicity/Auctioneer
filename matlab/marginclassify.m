function [yhat] = marginclassify(Xtest,w,b)

yhat = sign((Xtest*w) - b);

end
