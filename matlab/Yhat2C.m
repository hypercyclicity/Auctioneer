function [C] = Yhat2C(Yhat)
% rounds a continuous matrix Yhat
% into a hard classification matrix C

[t,k] = size(Yhat);
[ymax,y] = max(Yhat,[],2);
C = zeros(t,k);
C((y-1)*t + (1:t)') = ones(t,1);
