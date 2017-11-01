function accuracy = testdualsvm(Xtraincv, ytraincv, X, y, C)
    alpha = kerdualsvm(Xtraincv,ytraincv, C);  
    accuracy = 0;
    [total ~] = size(X);
    for i=1:total
        pred = kerpred(alpha, Xtraincv, ytraincv, X(i,:)');
        accuracy = accuracy + (pred == y(i));
    end
    accuracy = accuracy / total;
    