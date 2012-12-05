function [lambda,b] = dual_hardmargin(K,y,beta)

[t,~] = size(K);

I = eye(t);

H = diag(y)*K*diag(y);

f = -ones(t, 1);

A = [-I; y'; -y'];

b_qp = zeros(t+2, 1);

options = optimset('Algorithm','active-set','Display','off');

% This is done as by the forums
[t,~] = size(H);
H = H + 1e-15*eye(t);

%disp(H);
%disp(f);
%disp(A);
%disp(b);

[lambda] = quadprog(H, f, A, b_qp, [], [], 1, [], [], options);

[~,row] = max(lambda);

b = (K(row, :) * diag(y) * lambda) - (1 / y(row));

end
