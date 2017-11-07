% Input: matrix X of features, with n rows (samples), d columns (features)
%            X(i,j) is the j-th feature of the i-th sample
%        vector y of labels, with n rows (samples), 1 column
%            y(i) is the label (+1 or -1) of the i-th sample
%        positive scalar C
% Output: vector alpha of n rows, 1 column
function [alpha status] = kerdualsvm(X,y,C, K_gamma)
Xsize = size(X);
n = Xsize(1);
d = Xsize(2);
f = ones(n, 1) * -1;
u = zeros(n, 1);
v = ones(n, 1) * C;
H = ones(n, n);
for i=1:n
    for j=1:n
        H(i, j) = y(i) * y(j) * K(X(i, :), X(j, :), K_gamma);
    end
end
options = optimset('Display','off');
[alpha Fval status] = quadprog(H,f,[],[],[],[],u,v,[],options);