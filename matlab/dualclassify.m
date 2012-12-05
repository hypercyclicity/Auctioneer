function [yhat] = dualclassify(Ktest,lambda,b,y,beta,margintype)

if margintype == 1
    yhat = sign((Ktest * diag(y) * lambda) - b);
elseif margintype == 0
    yhat = sign((Ktest * diag(y) * lambda * (1 / beta)) - b);
else
    disp('margintype should be 1 for hard-margin classifier and 0 for soft-margin classifier');
end

end
