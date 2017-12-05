% Test Script for running with custom options and data
function [Xtrain, Xtest, ytrain, ytest, ypred, yconf, accuracy, feat_subset] = start(traincv_perc, classifier, feat_selector, k, F, logs, season_start, season_end, cumulative, per_season, features)       
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
            [Xtrain, Xtest, ytrain, ytest, prim_ypred, prim_yconf, dual_ypred, dual_yconf, feat_subset] = runSVM(X, y, traincv_perc, classifier, feat_selector, k, F, logs);
            if classifier == "primalsvm"
                accuracy = getaccuracy(prim_ypred, ytest);
                yconf = prim_yconf;
                ypred = prim_ypred;
            end

            if classifier == "dualsvm"
                accuracy = getaccuracy(dual_ypred, ytest);
                yconf = dual_yconf;
                ypred = dual_ypred;
            end
            
            if classifier == "logistic"
                [Xtrain, Xtest, ytrain, log_ytest, log_ypred, log_yconf, feat_subset] = logisticregression(X, y, traincv_perc, feat_selector, F, logs);
                log_acc = getaccuracy(log_ypred, log_ytest);
                accuracy = log_acc;
                ypred = log_ypred;
                ytest = log_ytest;
                yconf = log_yconf;
            end
            %if prim_acc == -1
            %    prim_acc_str = "Infeasible";
            %end
            %fprintf("Season %d: PrimalSVM = %s, DualSVM = %.4f, Logistic = %.4f\n", i, prim_acc_str, dual_acc, log_acc);
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
        log_acc = 0;                
        if classifier == "logistic"
            [Xtrain, Xtest, ytrain, log_ytest, log_ypred, log_yconf, feat_subset] = logisticregression(X, y, traincv_perc, feat_selector, F, logs);
            log_acc = getaccuracy(log_ypred, log_ytest);
            accuracy = log_acc;
            ypred = log_ypred;
            ytest = log_ytest;
            yconf = log_yconf;
        else 
            [Xtrain, Xtest, ytrain, ytest, ypred, yconf, feat_subset] = runSVM(X, y, traincv_perc, classifier, feat_selector, k, F, logs);
            accuracy = getaccuracy(ypred, ytest);
        end
        
        %prim_acc_str = num2str(prim_acc);
        %if prim_acc == -1
        %    prim_acc_str = "Infeasible";
        %end
        %fprintf("Result: PrimalSVM = %s, DualSVM = %.4f\n, Logistic = %.4f\n", prim_acc_str, dual_acc, log_acc);
    end
end 