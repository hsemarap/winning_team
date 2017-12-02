 function [prim_acc, dual_acc] = runSVM(X, y, traincv_perc, k, F, logs)
    y = ((y==0) * -1) + y;
    [n d] = size(X);    
    [X y] = shuffledata(X, y);
    [Xtraincv ytraincv Xtest ytest] = splitdata(X, y, traincv_perc);
    
    if F < d
        if logs
            disp('Running Greedy Subset Selection')    
        end
        [S ~] = greedysubset(F, X, y);
        if logs
            disp('Selecting features')
            sort(S)
        end
    else
        S =  1:d;
    end
    
    Xtraincv = Xtraincv(:, S);
    Xtest = Xtest(:, S);
    
    if logs == true
        disp('Running Primal SVM')
    end
    accuracy = testprimsvm(Xtraincv, ytraincv, Xtest, ytest, logs);
    prim_acc = accuracy;
    if logs == true && accuracy ~= -1
        fprintf('Primal SVM Accuracy: %f\n', accuracy);
    end
    %accuracy = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, 10, 1/2);
    
    if logs == true
        fprintf('Running Dual SVM with K=%d fold crossvalidation\n', k);
    end
    
    [C_opt gamma_opt accuracy_opt] = crossvalidation(k, Xtraincv, ytraincv, logs);
    
    %C_opt = 1000; gamma_opt = .01; accuracy_opt = 0;
    accuracy = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, C_opt, gamma_opt, logs);
    dual_acc = accuracy;
    if logs == true
        %[C_opt gamma_opt accuracy_opt]
        fprintf('Dual SVM Accuracy: %f\n', accuracy);
    end
 end    
