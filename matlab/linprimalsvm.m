% Input: matrix X of features, with n rows (samples), d columns (features)
%            X(i,j) is the j-th feature of the i-th sample
%        vector y of labels, with n rows (samples), 1 column
%            y(i) is the label (+1 or -1) of the i-th sample
% Output: vector theta of d rows, 1 column
function [theta status] = linprimalsvm(X,y)
[n, d] = size(X);
H = eye(d);
f = zeros(d, 1);
A = zeros(n, d);
b = ones(n, 1) * -1;
for i = 1:n
    for j = 1:d
        A(i, j) = -y(i) * X(i, j);
    end
end
options = optimset('Display','on');
%theta = quadprog(H, f, A, b); status=0;
[theta Fval status] = quadprog(H,f,A,b, [], [], [], [], [], options);
