% Input: number of features F
%        matrix X of features, with n rows (samples), d columns (features)
%            X(i,j) is the j-th feature of the i-th sample
%        vector y of scalar values, with n rows (samples), 1 column
%            y(i) is the scalar value of the i-th sample
% Output: vector of selected features S, with F rows, 1 column
%         vector thetaS, with F rows, 1 column
%           thetaS(1) corresponds to the weight of feature S(1)
%           thetaS(2) corresponds to the weight of feature S(2) and so on
%           and so forth
function [S thetaS] = forwardfitting(F, X, y)
    [n, d] = size(X);
    S = [];
    thetaS = [];
    for f = 1:F
        J = Inf;
        ind = -1;
        thetaS_res = 0;
        f_remain = setdiff(1:d, S);
        for i = 1:length(f_remain)
            j = f_remain(i);
            y_tmp = y;
            if length(thetaS) ~= 0
                y_tmp = y_tmp - (X(:, S) * thetaS);
            end
            thetaS_res_tmp = linreg(X(:, j), y_tmp);
            thetaS_tmp = [thetaS; thetaS_res_tmp];
            S_tmp = [S; j];
            tmp_J = 0.5 * sum((y - (X(:, S_tmp) * thetaS_tmp)) .^ 2);
            if tmp_J < J
                J = tmp_J;
                ind = j;
                thetaS_res = thetaS_res_tmp;
            end
        end
        S = [S; ind];
        thetaS = [thetaS; thetaS_res];
    end