function plotaccuracynumsamples(accuracies, numsamples, filename)
    figure1 = figure('Visible','off');
    %figure1 = figure;
    plot(numsamples, accuracies);    
    title('Accuracy vs No. of samples');
    xlabel('No. of samples');
    ylabel('Accuracy');
    if (exist('filename','var'))
        saveas(figure1, filename);
    end