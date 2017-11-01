function J = squareError(y, X, theta)
H = y - sum(theta' .* X, 2);
J = 1 / size(H, 1) * sum(H .^ 2);
end