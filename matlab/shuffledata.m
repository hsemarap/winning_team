function [X y] = shuffledata(X, y)
    [n d] = size(X);    
    s = RandStream('mcg16807','Seed',0);
    shuffle_order = randperm(s, n);
    X = X(shuffle_order, :);
    y = y(shuffle_order, :);
end