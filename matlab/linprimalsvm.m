% Input: matrix X of features, with n rows (samples), d columns (features)
%            X(i,j) is the j-th feature of the i-th sample
%        vector y of labels, with n rows (samples), 1 column
%            y(i) is the label (+1 or -1) of the i-th sample
% Output: vector theta of d rows, 1 column
function theta = linprimalsvm(X,y)
Xsize = size(X);
n = Xsize(1);
d = Xsize(2);
H = eye(d);
f = zeros(d, 1);
A = -y .* X;
b = ones(n, 1) * -1;
theta = quadprog(H,f,A,b);