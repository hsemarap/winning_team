% Test Script for running with custom options and data
function accuracy = start(traincv_perc, k, F, logs, season_start, season_end, cumulative, per_season, features)   
    
    if (~exist('features','var'))
        logs = true;
        season_start = 3;
        season_end   = 3;
        cumulative = true;
        per_season = false;
        %features = ["-alone-rolling-stats.mat", "-alone-average.mat", "-alone-bowling-economy.mat"];
        %features = ["-alone-average.mat"];
        %features = ["-alone-rolling-stats.mat"];
        %features = ["-alone-bowling-economy.mat"];
        features = ["-alone-rolling-stats.mat", "-alone-average.mat"];
    end
    
    if logs
        if cumulative
            fprintf("Season Cumulative statistics\n")
        else
            fprintf("Per season statistics\n")
        end
    end
    
    Xfinal = []; yfinal = [];
    for i=season_start:season_end                      
        if ~cumulative                
            Xfinal = []; yfinal = [];
        end

        Xcur = [];

        for feature_type=features
            load(strcat("../extracted-stats/season", num2str(i), feature_type));
            Xcur = [Xcur X];
        end

        Xfinal = [Xfinal; Xcur]; yfinal = [yfinal y];

        if per_season
            if logs
                fprintf("Running Season %d\n", i);
            end
            X = Xfinal;
            y = double(yfinal)';
            [ytest, prim_ypred, prim_yconf, dual_ypred, dual_yconf] = runSVM(X, y, traincv_perc, k, F, logs);
            prim_acc = getaccuracy(prim_ypred, ytest);
            dual_acc = getaccuracy(dual_ypred, ytest);
            
            [log_ypred, log_ytest, log_yconf] = logisticregression(X, y, traincv_perc);
            logistic_acc = getaccuracy(log_ypred, log_ytest);
            if prim_acc == -1
                prim_acc_str = "Infeasible";
            end
            fprintf("Season %d: PrimalSVM = %s, DualSVM = %.4f, Logistic = %.4f\n", i, prim_acc_str, dual_acc, logistic_acc);
        end
    end

    if ~per_season
        if logs
            fprintf("Running:\n");
        end
        X = Xfinal;
        y = yfinal;        
        y = double(y)';  

%             s = 1; e = size(X, 1); 
%             fs = 1; fe = 22;
%             X = X(s:e, fs:fe);
%             y = y(s:e);
%                         
%             y = y * 2 - 1;
%             X
%             y

        prim_acc = 0;
        dual_acc = 0;
        logistic_acc = 0;
        [ytest, prim_ypred, prim_yconf, dual_ypred, dual_yconf] = runSVM(X, y, traincv_perc, k, F, logs);
        prim_acc = getaccuracy(prim_ypred, ytest);
        dual_acc = getaccuracy(dual_ypred, ytest);
        
        [log_ypred, log_ytest, log_yconf] = logisticregression(X, y, traincv_perc);
        logistic_acc = getaccuracy(log_ypred, log_ytest);
        prim_acc_str = num2str(prim_acc);
        if prim_acc == -1
            prim_acc_str = "Infeasible";
        end
        fprintf("Result: PrimalSVM = %s, DualSVM = %.4f\n, Logistic = %.4f\n", prim_acc_str, dual_acc, logistic_acc);
        
%        plotprecisionrecall(prim_yconf, 
    end
end 