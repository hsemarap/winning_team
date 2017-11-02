function accuracy = start(n, d, traincv_perc)
    %n = 1000;
    %d = 10;
    %traincv_perc = 0.7;
    
    [X y] = createsepdata(n, d);
    %load data;
    [n d] = size(X);
    ntraincv = n * traincv_perc;
    ntest = n - ntraincv;
    Xtraincv = X(1:ntraincv, :);
    ytraincv = y(1:ntraincv);
    Xtest = X(ntraincv+1:n, :);
    ytest = y(ntraincv+1:n);
      
    %accuracy = testprimsvm(Xtraincv, ytraincv, Xtest, ytest);
    %accuracy = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, 10, 1/2);
    [C_opt gamma_opt accuracy_opt] = crossvalidation(5, Xtraincv, ytraincv);
    accuracy = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, C_opt, gamma_opt);
    
