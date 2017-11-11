function accuracy = testprimsvm(Xtraincv, ytraincv, X, y, logs)
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
    for i=1:total
        pred = linpred(theta, X(i,:)');
        accuracy = accuracy + (pred == y(i));
    end
    accuracy = accuracy / total;
    