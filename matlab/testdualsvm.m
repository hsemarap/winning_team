function accuracy = testdualsvm(Xtraincv, ytraincv, X, y, C, K_gamma)
    [alpha status] = kerdualsvm(Xtraincv,ytraincv, C, K_gamma);  
    if status == -2
        disp('Error: Kernel Dual SVM: Infeasible Problem')
        accuracy = 0;
        return
    end        
    accuracy = 0;
    [total ~] = size(X);
    for i=1:total
        pred = kerpred(alpha, Xtraincv, ytraincv, X(i,:)', K_gamma);
        accuracy = accuracy + (pred == y(i));
    end
    accuracy = accuracy / total;
    