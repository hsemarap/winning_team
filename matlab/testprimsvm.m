function [ypred, y, yconf, theta] = testprimsvm(Xtraincv, ytraincv, X, y, logs)
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
    yconf = ones(total, 1);
    for i=1:total
        yconf(i) = linpred(theta, X(i,:)');
    end
    ypred = (yconf > 0) * 2 - 1;  %get y > 0 => 1, y <= 0 => -1