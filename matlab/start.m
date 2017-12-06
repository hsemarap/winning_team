% Test Script for running with custom options and data
function [Xtrain, Xtest, ytrain, ytest, ypred, yconf, accuracy, feat_subset, theta_alpha] = start(traincv_perc, classifier, feat_selector, k, F, logs, season_start, season_end, cumulative, per_season, features)       
    if (~exist('features','var'))
        logs = true;
        season_start = 3;
        season_end   = 3;
        cumulative = true;
        per_season = false;
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
            if classifier == "primalsvm"
                [Xtrain, Xtest, ytrain, ytest, ypred, yconf, feat_subset, theta_alpha] = runSVM(X, y, traincv_perc, classifier, feat_selector, k, F, logs);
            end

            if classifier == "dualsvm"
                [Xtrain, Xtest, ytrain, ytest, ypred, yconf, feat_subset, theta_alpha] = runSVM(X, y, traincv_perc, classifier, feat_selector, k, F, logs);
            end
            
            if classifier == "logistic"
                [Xtrain, Xtest, ytrain, ytest, ypred, yconf, feat_subset] = logisticregression(X, y, traincv_perc, feat_selector, F, logs);
            end
            
            if classifier == "ensemble"
                [Xtrain, Xtest, ytrain, ytest, ypred, yconf, feat_subset, theta_alpha] = ensemble(X, y, traincv_perc, feat_selector, k, F, logs);                
            end
            accuracy = getaccuracy(ypred, ytest);
        end
    end

    if ~per_season
        if logs
            fprintf("Running:\n");
        end
        X = Xfinal;
        y = yfinal;        
        y = double(y)';  
        prim_acc = 0;
        dual_acc = 0;
        log_acc = 0;                
        if classifier == "logistic"
            [Xtrain, Xtest, ytrain, ytest, ypred, yconf, feat_subset] = logisticregression(X, y, traincv_perc, feat_selector, F, logs);
        elseif classifier == "ensemble"
                [Xtrain, Xtest, ytrain, ytest, ypred, yconf, feat_subset, theta_alpha] = ensemble(X, y, traincv_perc, feat_selector, k, F, logs);
        else 
                [Xtrain, Xtest, ytrain, ytest, ypred, yconf, feat_subset, theta_alpha] = runSVM(X, y, traincv_perc, classifier, feat_selector, k, F, logs);
        end
        accuracy = getaccuracy(ypred, ytest);
    end
end 