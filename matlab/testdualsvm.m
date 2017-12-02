function [ypred, y, yconf] = testdualsvm(Xtraincv, ytraincv, X, y, C, K_gamma, logs)
    [alpha status] = kerdualsvm(Xtraincv,ytraincv, C, K_gamma);  
    accuracy = 0;
    [total ~] = size(X);
    if status == -2
        if logs == true
            disp('Error: Kernel Dual SVM: Infeasible Problem')
        end
        accuracy = -1;
        return
    end
    if total == 0
        return
    end
    yconf = ones(total, 1);
    for i=1:total
        yconf(i) = kerpred(alpha, Xtraincv, ytraincv, X(i,:)', K_gamma);
    end
    ypred = (yconf > 0) * 2 - 1;  %get y > 0 => 1, y <= 0 => -1
