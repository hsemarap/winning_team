function [Xtraincv, Xtest, ytraincv, ytest, ypred, yconf, S, theta_alpha] = ensemble(X, y, traincv_perc, feat_selector, k, F, logs)
    y = ((y==0) * -1) + y;
    [n d] = size(X);    
    if(traincv_perc ~= -1)        
        [X y] = shuffledata(X, y);
        %Else No need to shuffle for league vs final, as ntest=4 (just finals)
    end
    [Xtraincv ytraincv Xtest ytest] = splitdata(X, y, traincv_perc);
    
    X_ensemble = ones(n, d);
    y_ensemble = y;
    
    for i=1:d
        X_f = X(:, i);
        [~, ~, ~, ~, ~, ~, ~, theta] = runSVM(Xtraincv, ytraincv, 1, "primalsvm", feat_selector, k, 1, logs);
        yconf = ones(n, 1);

        for j=1:n
            yconf(j) = linpred(theta, X_f(j, :)');
        end
        X_ensemble(:, i) = (yconf > 0) * 2 - 1;
    end
    [Xtraincv, Xtest, ytraincv, ytest, ypred, yconf, S, theta_alpha] = runSVM(X_ensemble, y, traincv_perc, "primalsvm", feat_selector, k, 1, logs);
    accuracy = getaccuracy(ypred, ytest);