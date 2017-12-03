function [precision, recall] = plotprecisionrecall(yconf, ytest, start_r, end_r, count, filename)
    ytest = ((ytest==0) * -1) + ytest; % change 0s to -1
    yconf = normalizedata(yconf);
    numrange = start_r:(end_r-start_r)/count:end_r;
    numrange = numrange(2:count+1);
    precision = zeros(count, 1);
    recall = zeros(count, 1);   
    for i=1:count
        curr_ypred = yconf > numrange(i);
        curr_ypred = ((curr_ypred==0) * -1) + curr_ypred; % change 0s to -1
        %curr_ypred
        tp = sum((curr_ypred == 1) .* (ytest == curr_ypred));
        fp = sum((curr_ypred == 1) .* (ytest ~= curr_ypred));
        fn = sum((curr_ypred ~= 1) .* (ytest ~= curr_ypred));        
        %[tp fp fn]
        precision(i) = tp / (tp + fp);
        recall(i) = tp / (tp + fn);
    end
    %[recall, sort_order]= sort(recall);
    %precision = precision(sort_order);
    %[recall, precision];
    figure1 = figure('Visible','off');
    plot(recall, precision);    
    title('Precision vs Recall');
    xlabel('Recall');
    ylabel('Precision');
    if (exist('filename','var'))
        saveas(figure1, filename);
    end