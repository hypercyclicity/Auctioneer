function [Y,U,W,obj] = kmeans(X,k,beta)

[t n] = size(X);

max = 1000;
threshold = 1e-9;
last_objective = 9999;
obj = 9;

% Randomly initialize Y
Y = eye(t, k);
permutation = randsample(1:t,t);
Y = Y(permutation,:);

for i=1:max
    if i ~= 1
        obj = ((1/t) / 2) * (norm(X - Y * U, 'fro')^2);
    end
    
    % Change in objective (last - this)
    if ((last_objective - obj) < threshold)
        % We have reached where we want to be
        break
    end
    
    % Optimal U given Y
    U = (Y' * Y) \ (Y' * X);
    
    % Optimal Y given U
    D = ((1/2) * diag(X * X') * ones(k, 1)') + ((1/2) * ones(t, 1) * diag(U * U')') - (X * U');
    
    % Zero Y because we're going to completely change it
    Y = zeros(t, k);
    for i_row = 1:t
               % Index of the minimum value in the row
               % Make that row in Y have 1 at that index and zero elsewhere
               [value index] = min(D(i_row,:));
               Y(i_row, index) = 1;
    end
    
    last_objective = obj;
end

W = ((X' * X) + beta * eye(n)) \ (X' * Y);

end

