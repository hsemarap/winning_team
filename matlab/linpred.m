% Input: vector theta of d rows, 1 column
%        vector x of d rows, 1 column
% Output: yconf - confidence
function yconf = linpred(theta,x)
x = [x; 1]; % add offset feature
yconf = dot(theta, x);