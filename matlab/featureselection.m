function S = featureselection(feat_selector, F, X, y, logs)
    [n, d] = size(X);
    if F < d
        if feat_selector == "greedy"
            if logs
                disp('Running Greedy Subset Selection')    
            end
            [S ~] = greedysubset(F, X, y);            
        elseif feat_selector == "forwardfitting"
            if logs
                disp('Running Forward fitting')    
            end
            [S ~] = forwardfitting(F, X, y);
        elseif feat_selector == "myopic"
            if logs
                disp('Running Myopic Forwad fitting')    
            end
            [S ~] = myopicfitting(F, X, y);
        else
            S = 1:d;
        end
        S = sort(S);
        if logs
            disp('Selecting features')
            S
        end
    else
        S =  1:d;
    end