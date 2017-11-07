function accuracy = testprimsvm(Xtraincv, ytraincv, X, y)
    [theta status] = linprimalsvm(Xtraincv,ytraincv);
    if status == -2
        disp('Error: Linear Primal SVM: Infeasible Problem')
        accuracy = 0;
        return
    end
    
    accuracy = 0;
    [total ~] = size(X);
    for i=1:total
        pred = linpred(theta, X(i,:)');
        accuracy = accuracy + (pred == y(i));
    end
    accuracy = accuracy / total;
    