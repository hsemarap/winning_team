function accuracy = getaccuracy(ypred, ytest)
    accuracy = sum(ypred == ytest) / size(ytest, 1);
end