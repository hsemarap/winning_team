function [Xtraincv ytraincv Xtest ytest] = splitdata(X, y, traincv_perc)
    [n d] = size(X);
    ntraincv = floor(n * traincv_perc);
    ntest = n - ntraincv;

    Xtraincv = X(1:ntraincv, :);
    ytraincv = y(1:ntraincv);
    Xtest = X(ntraincv+1:n, :);
    ytest = y(ntraincv+1:n);
end