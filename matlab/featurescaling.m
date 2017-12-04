function X_norm = featurescaling(X)
    mu = mean(X);
    sigma = std(X);
    ind = sigma~=0; % ignore zero variance features
    X_norm = X - mu;
    X_norm(:,ind) = X_norm(:,ind) ./ sigma(ind) ;
end