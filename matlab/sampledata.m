% Test Script for running with custom options and data
function accuracy = sampledata(traincv_perc, k, F, n, d)   
    logs = true;
    X = [1:2:n; [1:2:n] + rand(1, n/2)/4]';
    y = X(:, 1) > n/2;
    y = y * -2 + 1;        

    %adding outlier
    %X = [X; 8.0000    8.1773];    y=[y; 1.0000]
    X = [n/2-2  n/2-2; n/2-3  n/2-3; X];
    y = [-1; -1; y]
    %comment this to try out previous sample data
    %[X y] = createsepdata(n, d);
    [X y]
    [prim_acc, dual_acc] = runSVM(X, y, traincv_perc, k, F, logs);
    prim_acc_str = num2str(prim_acc);
    if prim_acc == -1
        prim_acc_str = "Infeasible";
    end
    fprintf("Final Result: Primal = %s, Dual = %f\n", prim_acc_str, dual_acc);
end 