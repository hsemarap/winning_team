% Input: matrix X of features, with n rows (samples), d columns (features)
%            X(i,j) is the j-th feature of the i-th sample
%        vector y of labels, with n rows (samples), 1 column
%            y(i) is the label (+1 or -1) of the i-th sample
% Output: vector theta of d rows, 1 column
function [accuracy] = logisticregression(X, y, traincv_perc)
    [n d] = size(X);
    [n d] = size(X);    

    X = [ones(n, 1) X]; %add offset feature as 1
    y = (y + 1)/2; %convert -1,+1 to 0,+1
    [X y] = shuffledata(X, y);
    [Xtrain ytrain Xtest ytest] = splitdata(X, y, traincv_perc);
    
    theta = zeros(d + 1, 1);
    
    options = optimoptions('fminunc', 'GradObj', 'on', 'Display','off', 'MaxIter', 1000);

    lambda = 3000;
    [theta, cost] = fminunc(@(t)(logisticcost(t, Xtrain, ytrain, lambda)), theta, options);
    
    predy = logisticprediction(theta, Xtest);
    
    accuracy = sum(predy == ytest) / size(ytest, 1);
end

function predy = logisticprediction(theta, X)
    predy = round(sigmoid(X * theta));
end

function [J, grad] = logisticcost(theta, X, y, lambda)
    [n d] = size(X);
    grad = zeros(d, 1);

    H = sigmoid(X * theta);
    theta_reg = [0; theta(2:d)];
    J = -1/n * sum((y .* log(H)) + ((1-y) .* log(1-H))) + (lambda/(2*n)) * (theta_reg' * theta_reg);
        
    grad = 1/n * (X' * (H-y) + lambda * theta_reg);
end

function s = sigmoid(z)
    s = 1 ./ (1 + exp(-z));
end

