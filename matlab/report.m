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
        %{["-alone-bowling-average-plus-strike-rate-plus-economy.mat"], 2, 10, true, false, [.7], ["ensemble"], ["greedy"], [22], "bowling_combo_C"},
        %%Reports batting features all config
        %{["-alone-average.mat", "-alone-rolling-stats.mat"], 2, 10, true, false, [.9,.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [44, 30, 20, 10, 6], "batting_avg_strike"},
        %%Reports batting combo features all config
        %{["-alone-batting-average-plus-strike-rate.mat"], 2, 10, true, false, [.9,.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [20, 10, 6], "batting_combo"},
        %%Reports bowling combo features all config
        %{["-alone-bowling-average-plus-strike-rate-plus-economy.mat"], 2, 10, true, false, [.9,.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [20, 10, 6], "bowling_combo"}
        
        %%Per season all features        
        %{all_features, 2, 2, true, false, [.7], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 3, 3, true, false, [.7], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 4, 4, true, false, [.7], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 5, 5, true, false, [.7], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 6, 6, true, false, [.7], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 7, 7, true, false, [.7], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 8, 8, true, false, [.7], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 9, 9, true, false, [.7], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 10, 10, true, false, [.7], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
                
        %%Per feature stats
        %{["-alone-rolling-stats.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [22, 14, 6], "batting_strike_rate"},
        %{["-alone-average.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [22, 14, 6], "batting_avg"},
        %{["-alone-bowling-economy.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [22, 14, 6], "bowling_econ"},
        %{["-alone-bowling-strike-rate.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [22, 14, 6], "bowling_strike_rate"},
        %{["-alone-team-win-rate.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [2], "team_win"},
        
        %{all_features, 2, 2, true, false, [.9,.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 3, 3, true, false, [.9,.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 4, 4, true, false, [.9,.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 5, 5, true, false, [.9,.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 6, 6, true, false, [.9,.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 7, 7, true, false, [.9,.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 8, 8, true, false, [.9,.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 9, 9, true, false, [.9,.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 10, 10, true, false, [.9,.8,.75,.7,.6], ["primalsvm", "dualsvm", "logistic"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        
        %{["-alone-average.mat", "-alone-rolling-stats.mat"], 2, 10, true, false, [.9,.8,.75,.7,.6], ["primalsvm"], ["greedy"], [22], "batting_avg_strike"},
        %{["-alone-average.mat", "-alone-rolling-stats.mat"], 2, 10, true, false, [0.7], ["primalsvm"], ["greedy"], [22], "batting_avg_strike"},
        %{["-alone-average.mat", "-alone-rolling-stats.mat"], 2, 10, true, false, [0.7], ["primalsvm"], ["forwardfitting"], [22], "batting_avg_strike"},
        %{["-alone-average.mat", "-alone-rolling-stats.mat"], 2, 10, true, false, [0.7], ["primalsvm"], ["myopic"], [22], "batting_avg_strike"},
        %{["-alone-batting-average-plus-strike-rate.mat"], 2, 10, true, false, [0.7], ["primalsvm", "dualsvm"], ["greedy"], [22, 10, 5], "batting_combo"}
        %{["-alone-bowling-average-plus-strike-rate-plus-economy.mat"], 2, 10, true, false, [0.7], ["primalsvm", "dualsvm"], ["greedy"], [22, 10, 5], "bowling_combo"}
        
        %%Reports for ensemble
        %%Reports batting features all config
        %{["-alone-average.mat", "-alone-rolling-stats.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["ensemble"], ["greedy"], [44, 30, 20, 10, 6], "batting_avg_strike"},
        %%Reports batting combo features all config
        %{["-alone-batting-average-plus-strike-rate.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["ensemble"], ["greedy"], [20, 10, 6], "batting_combo"},
        %%Reports bowling combo features all config
        %{["-alone-bowling-average-plus-strike-rate-plus-economy.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["ensemble"], ["greedy"], [20, 10, 6], "bowling_combo"}

        %%Per season all features        
        %{all_features, 2, 2, true, false, [.7], ["ensemble"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 3, 3, true, false, [.7], ["ensemble"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 4, 4, true, false, [.7], ["ensemble"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 5, 5, true, false, [.7], ["ensemble"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 6, 6, true, false, [.7], ["ensemble"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 7, 7, true, false, [.7], ["ensemble"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 8, 8, true, false, [.7], ["ensemble"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 9, 9, true, false, [.7], ["ensemble"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},
        %{all_features, 10, 10, true, false, [.7], ["ensemble"], ["greedy", "forwardfitting"], [90, 68, 46, 24, 12], "all_features"},

        %%Per feature stats
        {["-alone-rolling-stats.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [22, 14, 6], "batting_strike_rate"},
        {["-alone-average.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [22, 14, 6], "batting_avg"},
        {["-alone-bowling-economy.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [22, 14, 6], "bowling_econ"},
        {["-alone-bowling-strike-rate.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [22, 14, 6], "bowling_strike_rate"},
        {["-alone-team-win-rate.mat"], 2, 10, true, false, [.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [2], "team_win"},
        %{all_features, 2, 2, true, false, [.9,.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 3, 3, true, false, [.9,.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 4, 4, true, false, [.9,.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 5, 5, true, false, [.9,.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 6, 6, true, false, [.9,.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 7, 7, true, false, [.9,.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 8, 8, true, false, [.9,.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 9, 9, true, false, [.9,.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
        %{all_features, 10, 10, true, false, [.9,.8,.75,.7,.6], ["ensemble"], ["greedy", "forwardfitting"], [20, 10, 6], "all_features"},
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
        combination_idx = 0;
        combinations = size(train_percents, 2) * size(classifiers, 2) * size(feat_selectors, 2) * size(subset_sizes, 2); 
        %[features_list, season_start, season_end, cumulative, per_season, train_percents, classifiers, feat_selectors, subset_sizes] = config;
        plot_acc_num_samp = and(combinations > 1, combinations == size(train_percents, 2));
        inst_acc_num_samp_file = sprintf('../plots/%s_%s_%d_s%d_%d_acc_num_samp.jpg', classifiers(1), feat_selectors(1), subset_sizes(1), season_start, season_end);
        accuracies = [];
        numsamples = [];
        for train_percent=train_percents
            for classifier=classifiers
                for feat_selector=feat_selectors
                    for subset_size=subset_sizes
                        combination_idx = combination_idx + 1;
                        fprintf("Config %d/%d) combination %d/%d - %.2f percent data, %s, %s-%d, season:%d-%d\n", i, size(configurations, 1), combination_idx, combinations, train_percent, classifier, feat_selector, subset_size, season_start, season_end);
                        %[train_percent, classifier, feat_selector, k, subset_size, logs, season_start, season_end, cumulative, per_season, features]
                        inst_filename = sprintf("%s_%.2f_%s_%s_%d_s%d_%d", filename, train_percent, classifier, feat_selector, subset_size, season_start, season_end);
                        inst_prec_rec_file = sprintf('../plots/%s_prec_rec.jpg', inst_filename);                        
                        inst_stat_file = sprintf('../stats/%s_stat.txt', inst_filename);
                        [Xtrain, Xtest, ytrain, ytest, ~, yconf, accuracy, feat_subset, ~] = start(train_percent, classifier, feat_selector, k, subset_size, logs, season_start, season_end, cumulative, per_season, features);
                        numsamples = [numsamples; size(Xtrain, 1)];
                        accuracies = [accuracies; accuracy];
                        fileID = fopen(inst_stat_file,'w');
                        feat_subset_str = sprintf('%.0f,', feat_subset);
                        feat_subset_str = feat_subset_str(1:end-1);
                        fprintf(fileID,'%f\t%.2f\t%s\t%s\t%d\tfeat-{%s}\n', accuracy, train_percent, classifier, feat_selector, subset_size, feat_subset_str);
                        fclose(fileID);                        
                        start_r = 0; end_r = 1; count = 4;                            
                        plotprecisionrecall(yconf, ytest, start_r, end_r, count, inst_prec_rec_file);                        
                    end
                end
            end
        end
        if plot_acc_num_samp
            plotaccuracynumsamples(accuracies, numsamples, inst_acc_num_samp_file);
        end
    end   
end 