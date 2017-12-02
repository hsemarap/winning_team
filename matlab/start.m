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
            [prim_acc, dual_acc] = run(X, y, traincv_perc, k, F, logs);
            if prim_acc == -1
                prim_acc_str = "Infeasible";
            end
            fprintf("Season %d: Primal = %s, Dual = %f\n", i, prim_acc_str, dual_acc);
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

        [prim_acc, dual_acc] = run(X, y, traincv_perc, k, F, logs);
        prim_acc_str = num2str(prim_acc);
        if prim_acc == -1
            prim_acc_str = "Infeasible";
        end
        fprintf("Final result: Primal = %s, Dual = %f\n", prim_acc_str, dual_acc);
    end
end 