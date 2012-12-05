function [lambda,b] = dual_softmargin(K,y,beta)

[t n] = size(K);

I = eye(t);

H = (diag(y)*K*diag(y)) / beta;

f = -ones(t, 1);

A = [-I; y'; -y'; I];

b_qp = [zeros(t+2, 1); ones(t, 1)];

options = optimset('Algorithm','active-set','Display','off');

% This is done as by the forums
[t,~] = size(H);
H = H + 1e-15*eye(t);

%disp(H);
%disp(f);
%disp(A);
%disp(b);

[lambda] = quadprog(H, f, A, b_qp, [], [], 1, [], [], options);

row = find(lambda > 0 & lambda < 1);

% Find can return multiple values
row = row(1);

b = (K(row, :) * diag(y) * lambda * (1 / beta)) - (1 / y(row));

end
