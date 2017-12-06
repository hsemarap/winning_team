function plot_and_save(visible, X, y, Xname, yname, title_str, filename)
    if visible
        figure1 = figure;
    else
        figure1 = figure('Visible','off');
    end
    plot(X, y, '-*');    
    title(title_str); %'Precision vs Recall');
    xlabel(Xname); %('Recall');
    ylabel(yname); %('Precision');
    if (exist('filename','var'))
        saveas(figure1, filename);
    end