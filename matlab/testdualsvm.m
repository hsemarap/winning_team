function accuracy = testdualsvm(Xtraincv, ytraincv, X, y, C, K_gamma, logs)
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
    for i=1:total
        pred = kerpred(alpha, Xtraincv, ytraincv, X(i,:)', K_gamma);
        accuracy = accuracy + (pred == y(i));
    end
    accuracy = accuracy / total;
    