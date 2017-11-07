function accuracy = start(traincv_perc, F, n, d)
    %n = 1000;
    %d = 10;
    %traincv_perc = 0.7;
    
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
        [X y] = createsepdata(n, d);
    end
    
    [n d] = size(X);
    ntraincv = floor(n * traincv_perc);
    ntest = n - ntraincv;
    Xtraincv = X(1:ntraincv, :);
    ytraincv = y(1:ntraincv);
    Xtest = X(ntraincv+1:n, :);
    ytest = y(ntraincv+1:n);
    
    disp('Running Greedy Subset Selection')
    [S ~] = greedysubset(F, X, y);
    disp('Selecting features')
    S
    
    Xtraincv = Xtraincv(:, S);
    Xtest = Xtest(:, S);
    
    disp('Running Primal SVM')
    accuracy = testprimsvm(Xtraincv, ytraincv, Xtest, ytest);
    fprintf('Primal SVM Accuracy: %f\n', accuracy);
    %accuracy = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, 10, 1/2);
    
    disp('Running Dual SVM with K=5 fold crossvalidation')
    [C_opt gamma_opt accuracy_opt] = crossvalidation(5, Xtraincv, ytraincv);
    accuracy = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, C_opt, gamma_opt);
    fprintf('Dual SVM Accuracy: %f\n', accuracy);
    
 