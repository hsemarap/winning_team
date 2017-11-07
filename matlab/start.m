function accuracy = start(traincv_perc, F, n, d)
    %n = 1000;
    %d = 10;
    %traincv_perc = 0.7;
    
    if (~exist('n','var') || isempty(n)) || (~exist('d','var') || isempty(d))
        load("../extracted-stats/season2-wrt-season1.mat");
        y = double(y)';
    else
        [X y] = createsepdata(n, d);
    end
    
    [n d] = size(X);
    ntraincv = floor(n * traincv_perc);
    ntest = n - ntraincv;
    Xtraincv = X(1:ntraincv, :);
    ytraincv = y(1:ntraincv);
    Xtest = X(ntraincv+1:n, :);
    ytest = y(ntraincv+1:n);
    
    [S ~] = greedysubset(F, X, y);
    
    Xtraincv = Xtraincv(:, S);
    Xtest = Xtest(:, S);
    
    %accuracy = testprimsvm(Xtraincv, ytraincv, Xtest, ytest);
    %accuracy = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, 10, 1/2);
    [C_opt gamma_opt accuracy_opt] = crossvalidation(5, Xtraincv, ytraincv);
    accuracy = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, C_opt, gamma_opt);
    
 