function accuracy = start(traincv_perc, k, F, n, d)   
    logs = true;
    season_start = 2;
    season_end   = 10;
    cumulative = true;
    per_season = false;
    feature_types = ["-alone-rolling-stats.mat", "-alone-average.mat", "-alone-bowling-economy.mat"];
    %feature_types = ["-alone-average.mat"];
    %feature_types = ["-alone-rolling-stats.mat"];
    %feature_types = ["-alone-bowling-economy.mat"];
if (~exist('n','var') || isempty(n)) || (~exist('d','var') || isempty(d))
        if cumulative
            fprintf("Season Cumulative statistics\n")
        else
            fprintf("Per season statistics\n")
        end
        Xfinal = []; yfinal = [];
        %load("../extracted-stats/season2-alone-rolling-stats.mat");
        %Xfinal = X; yfinal = y;
        for i=season_start:season_end                      
            if ~cumulative                
                Xfinal = []; yfinal = [];
            end
            
            Xcur = [];
            
            for feature_type=feature_types
                load(strcat("../extracted-stats/season", num2str(i), feature_type));
                Xcur = [Xcur X];
            end
            
            Xfinal = [Xfinal; Xcur]; yfinal = [yfinal y];
            
            if per_season
                fprintf("Running Season %d\n", i);
                X = Xfinal;
                y = double(yfinal)';
                [prim_acc, dual_acc] = run(X, y, traincv_perc, k, F, logs);
                if prim_acc == -1
                    prim_acc_str = "Infeasible";
                end
                fprintf("Season %d: Primal = %s, Dual = %f\n", i, prim_acc_str, dual_acc);
            end
        end
        
        if ~per_season
            fprintf("Running:\n");
            X = Xfinal;
            y = yfinal;        
            y = double(y)';  
            [prim_acc, dual_acc] = run(X, y, traincv_perc, k, F, logs);
            if prim_acc == -1
                prim_acc_str = "Infeasible";
            end
            fprintf("Final result: Primal = %s, Dual = %f\n", prim_acc_str, dual_acc);
        end
    else
        X = [1:2:n; [1:2:n] + rand(1, n/2)/4]';
        y = X(:, 1) > n/2;
        y = y * -2 + 1;        
        
        %comment this to try out previous sample data
        [X y] = createsepdata(n, d);
        [X y]
        [prim_acc, dual_acc] = run(X, y, traincv_perc, k, F, logs);
        prim_acc_str = num2str(prim_acc);
        if prim_acc == -1
            prim_acc_str = "Infeasible";
        end
        fprintf("Final Result: Primal = %s, Dual = %f\n", prim_acc_str, dual_acc);
    end
end

 function [prim_acc, dual_acc] = run(X, y, traincv_perc, k, F, logs)
    [n d] = size(X);
    %ordering = randperm(n);
    %X = X(ordering, :);
    %y = y(ordering, :);
    ntraincv = floor(n * traincv_perc);
    ntest = n - ntraincv;

    Xtraincv = X(1:ntraincv, :);
    ytraincv = y(1:ntraincv);
    Xtest = X(ntraincv+1:n, :);
    ytest = y(ntraincv+1:n);
    
    if F < d
        if logs
            disp('Running Greedy Subset Selection')    
        end
        [S ~] = greedysubset(F, X, y);
        if logs
            disp('Selecting features')
            S
        end
    else
        S =  1:d;
    end
    
    Xtraincv = Xtraincv(:, S);
    Xtest = Xtest(:, S);
    
    if logs == true
        disp('Running Primal SVM')
    end
    accuracy = testprimsvm(Xtraincv, ytraincv, Xtest, ytest, logs);
    prim_acc = accuracy;
    if logs == true && accuracy ~= -1
        fprintf('Primal SVM Accuracy: %f\n', accuracy);
    end
    %accuracy = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, 10, 1/2);
    
    if logs == true
        fprintf('Running Dual SVM with K=%d fold crossvalidation\n', k);
    end
    [C_opt gamma_opt accuracy_opt] = crossvalidation(k, Xtraincv, ytraincv, logs);
    
    %C_opt = 1000; gamma_opt = .01;
    accuracy = testdualsvm(Xtraincv, ytraincv, Xtest, ytest, C_opt, gamma_opt, logs);
    dual_acc = accuracy;
    if logs == true
        [C_opt gamma_opt accuracy_opt]
        fprintf('Dual SVM Accuracy: %f\n', accuracy);
    end
 end    
 