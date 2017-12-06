 function [Xtraincv, Xtest, ytraincv, ytest, ypred, yconf, S, theta_alpha] = runSVM(X, y, traincv_perc, classifier, feat_selector, k, F, logs)
    y = ((y==0) * -1) + y;
    [n d] = size(X);
    if(traincv_perc ~= -1)
        [X y] = shuffledata(X, y);
        %Else No need to shuffle for league vs final, as ntest=4 (just finals)
    end
    [Xtraincv ytraincv Xtest ytest] = splitdata(X, y, traincv_perc);
    
    S = featureselection(feat_selector, F, X, y, logs);
    
    Xtraincv = Xtraincv(:, S);
    Xtest = Xtest(:, S);
    
    if classifier == "primalsvm"
        if logs == true
            disp('Running Primal SVM')
        end
        [ypred, ~, yconf, theta_alpha] = testprimsvm(Xtraincv, ytraincv, Xtest, ytest, logs);
    end
    
    if classifier == "dualsvm"
        if logs == true
            fprintf('Running Dual SVM with K=%d fold crossvalidation\n', k);
        end

        [C_opt gamma_opt accuracy_opt] = crossvalidation(k, Xtraincv, ytraincv, logs);
        %C_opt = 1000; gamma_opt = .01; accuracy_opt = 0;
        [ypred, ~, yconf, theta_alpha] = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, C_opt, gamma_opt, logs);
    end
    
 end    
