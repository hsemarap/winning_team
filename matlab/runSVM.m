 function [ytest, ypred, yconf] = runSVM(X, y, traincv_perc, classifier, feat_selector, k, F, logs)
    y = ((y==0) * -1) + y;
    [n d] = size(X);    
    [X y] = shuffledata(X, y);
    [Xtraincv ytraincv Xtest ytest] = splitdata(X, y, traincv_perc);
    
    if F < d
        if feat_selector == "greedy"
            if logs
                disp('Running Greedy Subset Selection')    
            end
            [S ~] = greedysubset(F, X, y);            
        else if feat_selector == "forwardfitting"
            if logs
                disp('Running Forward fitting')    
            end
            [S ~] = forwardfitting(F, X, y);
        else if feat_selector == "myopic"
            if logs
                disp('Running Myopic Forwad fitting')    
            end
            [S ~] = myopicfitting(F, X, y);
        else
            S = 1:d;
        end
        if logs
            disp('Selecting features')
            sort(S)
        end
    else
        S =  1:d;
    end
    
    Xtraincv = Xtraincv(:, S);
    Xtest = Xtest(:, S);
    
    if classifier == "primalsvm"
        if logs == true
            disp('Running Primal SVM')
        end
        [ypred, ~, yconf] = testprimsvm(Xtraincv, ytraincv, Xtest, ytest, logs);
    end
    
    if classifier == "dualsvm"
        if logs == true
            fprintf('Running Dual SVM with K=%d fold crossvalidation\n', k);
        end

        [C_opt gamma_opt accuracy_opt] = crossvalidation(k, Xtraincv, ytraincv, logs);
        %C_opt = 1000; gamma_opt = .01; accuracy_opt = 0;
        [ypred, ~, yconf] = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, C_opt, gamma_opt, logs);
    end
    
 end    
