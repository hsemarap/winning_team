% Input: number of folds k
%        matrix X of features, with n rows (samples), d columns (features)
%        vector y of scalar values, with n rows (samples), 1 column
% Output: vector z of k rows, 1 column
function z = kfoldcv(k,X,y, C, K_gamma, costFunc)
[n d] = size(X);
z = zeros(k, 1);
for i=1:k
    Tstart = floor(n * (i-1) / k) + 1;
    Tend   = floor(n * (i)   / k);
    T = Tstart:Tend;
    S = setdiff(1:n, T);
    Xtrain = X(S, :);
    ytrain = y(S);
    Xtest = X(T, :);
    ytest = y(T);
    [ypred, ~, ~, ~] = costFunc(Xtrain, ytrain, Xtest, ytest, C, K_gamma);
    z(i) = getaccuracy(ypred, ytest);
end
end
    
