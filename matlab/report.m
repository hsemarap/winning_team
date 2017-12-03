function report()   
    clc;
    traincv_perc = 0.7;
    k = 5;
    start_season = 2; end_season = 10;
    logs = false;
    all_features =  [
                        "-alone-rolling-stats.mat", ...
                        "-alone-average.mat", ...
                        "-alone-bowling-economy.mat", ...
                        "-alone-bowling-strike-rate.mat", ...
                        "-alone-team-win-rate.mat"
                    ];    
    
    datasets =      [
                        "single_features_all_seasons",
                        "multiple_features_all_seasons",
                        "single_features_per_season",
                        "multiple_features_per_season",
                        "multiple_features_final_vs_league_all_seasons",
                        "multiple_features_final_vs_league_per_season"
                    ];  

    classifiers =   [
                        "primalsvm",
                        "dualsvm",
                        "logistic",
                        "ensemble"
                    ];
    
    feat_selectors = [
                        "all_features",
                        "greedy",
                        "forward_fitting",
                        "L1_norm"
                     ];
    configurations = [
        {["-alone-average.mat", "-alone-rolling-stats.mat"], 2, 10, true, false, [0.7, 0.5], ["logistic"], ["greedy"], [22, 10, 5], "batting_avg_strike"}
    ];
    for i=1:size(configurations, 1)
        config = configurations(i, :);
        features = config{1};
        season_start = config{2};
        season_end = config{3};
        cumulative = config{4};
        per_season = config{5};
        train_percents = config{6};
        classifiers = config{7};
        feat_selectors = config{8};
        subset_sizes = config{9};
        filename = config{10};
        %[features_list, season_start, season_end, cumulative, per_season, train_percents, classifiers, feat_selectors, subset_sizes] = config;
        for train_percent=train_percents
            for classifier=classifiers
                for feat_selector=feat_selectors
                    for subset_size=subset_sizes
                        %[train_percent, classifier, feat_selector, k, subset_size, logs, season_start, season_end, cumulative, per_season, features]
                        inst_filename = sprintf("%s_%.2f_%s_%s_%d", filename, train_percent, classifier, feat_selector, subset_size);
                        inst_prec_rec_file = sprintf('../plots/%s_prec_rec.jpg', inst_filename);                        
                        inst_stat_file = sprintf('../stats/%s_stat.txt', inst_filename);
                        [ytest, ~, yconf, accuracy] = start(train_percent, classifier, feat_selector, k, subset_size, logs, season_start, season_end, cumulative, per_season, features);
                        fileID = fopen(inst_stat_file,'w');
                        fprintf(fileID,'%f\t%.2f\t%s\t%s\t%d\n', accuracy, train_percent, classifier, feat_selector, subset_size);
                        fclose(fileID);                        
                        start_r = 0; end_r = 1; count = 4;                            
                        plotprecisionrecall(yconf, ytest, start_r, end_r, count, inst_prec_rec_file);
                    end
                end
            end
        end
    end   
end 