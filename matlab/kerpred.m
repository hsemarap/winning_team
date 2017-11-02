% Input: vector alpha of n rows, 1 column
%        matrix X of features, with n rows (samples), d columns (features)
%            X(i,j) is the j-th feature of the i-th sample
%        vector y of labels, with n rows (samples), 1 column
%            y(i) is the label (+1 or -1) of the i-th sample
%        vector x of d rows, 1 column
% Output: label (+1 or -1)
function label = kerpred(alpha,X,y,x, K_gamma)
Xsize = size(X);
n = Xsize(1);
d = Xsize(2);
s = 0;
for i=1:n,
   s = s + alpha(i) * y(i) * K(X(i, :)', x, K_gamma);
end
%shorter version
%s = sum(alpha .* y .* K(X', repelem(x, 1, n))');
if s > 0
    label = 1;
else
    label = -1;
end