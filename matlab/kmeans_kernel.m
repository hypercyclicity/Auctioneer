function [Y,B,A,obj] = kmeans_kernel(K,k,beta)

[t n] = size(K);

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
        obj = ((1/t) / 2) * trace( (eye(t) -Y * B) * K * (eye(t) - Y * B)');
    end
    
    % Change in objective (last - this)
    if ((last_objective - obj) < threshold)
        % We have reached where we want to be
        break
    end
    
    % Optimal B given Y
    B = (Y' * Y) \ (Y');
    
    % Optimal Y given B
    D = ((1/2) * diag(K) * ones(k, 1)') ...
        + ((1/2) * ones(t, 1) * diag(B * K * B')') - (K * B');
    
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

A = (K + (beta * eye(size(K)))) \ (B' * (Y' * Y));

end

