function accuracy = start(traincv_perc, k, F, n, d)   
    if (~exist('n','var') || isempty(n)) || (~exist('d','var') || isempty(d))
        Xfinal = []; yfinal = [];
        load("../extracted-stats/season2-wrt-season1.mat");
        Xfinal = X; yfinal = y;
        load("../extracted-stats/season2-alone-rolling-stats.mat");
        Xfinal = [Xfinal; X]; yfinal = [yfinal y];
        load("../extracted-stats/season3-alone-rolling-stats.mat");
        Xfinal = [Xfinal; X]; yfinal = [yfinal y];
        load("../extracted-stats/season4-alone-rolling-stats.mat");
        Xfinal = [Xfinal; X]; yfinal = [yfinal y];
        load("../extracted-stats/season5-alone-rolling-stats.mat");
        Xfinal = [Xfinal; X]; yfinal = [yfinal y];
        load("../extracted-stats/season6-alone-rolling-stats.mat");
        Xfinal = [Xfinal; X]; yfinal = [yfinal y];
        load("../extracted-stats/season7-alone-rolling-stats.mat");
        Xfinal = [Xfinal; X]; yfinal = [yfinal y];
        load("../extracted-stats/season8-alone-rolling-stats.mat");
        Xfinal = [Xfinal; X]; yfinal = [yfinal y];
        load("../extracted-stats/season9-alone-rolling-stats.mat");
        Xfinal = [Xfinal; X]; yfinal = [yfinal y];
        load("../extracted-stats/season10-alone-rolling-stats.mat");
        Xfinal = [Xfinal; X]; yfinal = [yfinal y];
        X = Xfinal;
        y = yfinal;
        
        y = double(y)';              
    else
        %X = [1:n; 1:n]';
        %y = X(:, 1) > n/2;
        %y = y * -2 + 1;        
        
        [X y] = createsepdata(n, d);
        %[X y]
    end
       
    [n d] = size(X);
    %ordering = randperm(n);
    %X = X(ordering, :);
    %y = y(ordering, :);
    ntraincv = floor(n * traincv_perc);
    ntest = n - ntraincv;

    Xtraincv = X(1:ntraincv, :);
    ytraincv = y(1:ntraincv);
    Xtest = X(ntraincv+1:n, :);
    ytest = y(ntraincv+1:n);
    
    if F < d
        disp('Running Greedy Subset Selection')    
        [S ~] = greedysubset(F, X, y);
        disp('Selecting features')
        S
    else
        S =  1:d;
    end
    
    Xtraincv = Xtraincv(:, S);
    Xtest = Xtest(:, S);
    
    disp('Running Primal SVM')
    accuracy = testprimsvm(Xtraincv, ytraincv, Xtest, ytest);
    fprintf('Primal SVM Accuracy: %f\n', accuracy);
    %accuracy = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, 10, 1/2);
    
    fprintf('Running Dual SVM with K=%d fold crossvalidation\n', k);
    [C_opt gamma_opt accuracy_opt] = crossvalidation(k, Xtraincv, ytraincv)
    %C_opt = 1000; gamma_opt = 1e-3;
    accuracy = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, C_opt, gamma_opt);
    fprintf('Dual SVM Accuracy: %f\n', accuracy);
    
 