function [Xtraincv ytraincv Xtest ytest] = splitdata(X, y, traincv_perc)
    [n d] = size(X);
    if traincv_perc == -1
        ntraincv = n - 4;
    else
        ntraincv = floor(n * traincv_perc);
    end
    Xtraincv = X(1:ntraincv, :);
    ytraincv = y(1:ntraincv);
    Xtest = X(ntraincv+1:n, :);
    ytest = y(ntraincv+1:n);
end