function ypred = testprimsvm(Xtraincv, ytraincv, X, y, logs)
    [theta status] = linprimalsvm(Xtraincv,ytraincv);
    if status == -2
        if logs == true
            disp('Error: Linear Primal SVM: Infeasible Problem')
        end
        accuracy = -1;
        return
    end
    
    accuracy = 0;
    [total ~] = size(X);
    ypred = ones(total, 1);
    for i=1:total
        ypred(i) = linpred(theta, X(i,:)');
    end
    