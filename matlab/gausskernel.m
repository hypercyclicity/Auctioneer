function [K] = gausskernel(X1,X2,sigma)
	[t1 n] = size(X1);
	[t2 n] = size(X2);
	D = repmat(diag(X1*X1'),1,t2) + repmat(diag(X2*X2')',t1,1) - 2*X1*X2';
	K = exp(-0.5*D/sigma^2);
