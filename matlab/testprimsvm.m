function accuracy = testprimsvm(Xtraincv, ytraincv, X, y)
    theta = linprimalsvm(Xtraincv,ytraincv);  
    accuracy = 0;
    [total ~] = size(X);
    for i=1:total
        pred = linpred(theta, X(i,:)');
        accuracy = accuracy + (pred == y(i));
    end
    accuracy = accuracy / total;
    