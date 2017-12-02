function report()   
    clc;
    traincv_perc = 0.7;
    k = 5;
    start_season = 2; end_season = 10;
    logs = false;
    all_features = ["-alone-rolling-stats.mat", ...
                    "-alone-average.mat", ...
                    "-alone-bowling-economy.mat", ...
                    "-alone-bowling-strike-rate.mat", ...
                    "-alone-team-win-rate.mat"];
    report_list = [3];
    
    rep_no = 1;    
    if ismember(rep_no, report_list)
        disp("====================================");
        fprintf("%d) With different percentage of data for training\n", rep_no);
        disp("====================================");
        F = 22 * size(all_features, 1);
        features = all_features;
        train_percents = [.95 .9 .85 .75 .7];  
        for train_percent=train_percents
            fprintf("Train percent %.2f:\n", train_percent);
            start(train_percent, k, F, logs, start_season, end_season, true, false, features);
            disp("------------------------------------");        
        end
    end

    rep_no = 2;
    if ismember(rep_no, report_list)
        disp("====================================");
        fprintf("%d) All features - Greedy different subset sizes\n", rep_no);
        disp("====================================");
        for F=[6 10 30 50]
            fprintf("All Features Subset Size %d:\n", F);
            features = all_features;
            start(traincv_perc, k, F, logs, start_season, end_season, true, false, features);
            disp("------------------------------------");
        end
    end    

    rep_no = 3;    
    if ismember(rep_no, report_list)
        disp("====================================");
        fprintf("%d) One feature at a time - Greedy different feature subset sizes\n", rep_no);
        disp("====================================");
        for feature=all_features
            for F=[5 10 15 22]
                fprintf("Feature %s Subset Size %d:\n", feature, F);
                features = [feature];
                start(traincv_perc, k, F, logs, start_season, end_season, true, false, features);
                disp("------------------------------------");
            end
        end    
    end    

    rep_no = 4;    
    if ismember(rep_no, report_list)
        disp("====================================");
        fprintf("%d) One feature at a time - no feature selection\n", rep_no);
        disp("====================================");
        for feature=all_features
            fprintf("Feature %s:\n", feature);
            F = 22;
            features = [feature];
            start(traincv_perc, k, F, logs, start_season, end_season, true, false, features);
            disp("------------------------------------");
        end
    end    

    rep_no = 5;    
    if ismember(rep_no, report_list)
        disp("====================================");
        fprintf("%d) All features - all seasons\n", rep_no);
        disp("====================================");
        F = 22 * size(all_features, 1);
        features = all_features;
        start(traincv_perc, k, F, logs, start_season, end_season, true, false, features);
        disp("------------------------------------");
    end    

    rep_no = 6;    
    if ismember(rep_no, report_list)
        disp("====================================");
        fprintf("%d) All features - 3 seasons at once\n", rep_no);
        disp("====================================");
        F = 22 * size(all_features, 1);
        features = all_features;
        s_start = start_season; s_end = min(s_start + 3, end_season);
        while s_start <= end_season
            fprintf("Season %d to %d:\n", s_start, s_end);
            start(traincv_perc, k, F, logs, s_start, s_end, true, false, features);
            s_start = s_end + 1; s_end = min(s_start + 3, end_season);
            disp("------------------------------------");        
        end
    end

    rep_no = 7;
    if ismember(rep_no, report_list)
        disp("====================================");
        fprintf("%d) All features - 1 season at a time\n", rep_no);
        disp("====================================");
        F = 22 * size(all_features, 1);
        features = all_features;
        for season_no=start_season:end_season
            fprintf("Season %d:\n", season_no);
            start(traincv_perc, k, F, logs, season_no, season_no, true, false, features);
            disp("------------------------------------");        
        end
    end
    
    % disp("------------------------------------");
    % disp("Strikerate, Avg");
    % F = 22 * 2;
    % features = ["-alone-rolling-stats.mat", "-alone-average.mat"];
    % start(traincv_perc, k, F, logs, start_season, end_season, true, false, features);
    % disp("------------------------------------");
    
end 