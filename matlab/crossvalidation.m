function [C_opt gamma_opt accuracy_opt] = crossvalidation(k, X, y)
C_range = [1e-3, 1e-2, 1, 1e2, 1e3];
gamma_range = [1e-3, 1e-2, 1, 1e2, 1e3];
results = [];
maxAccuracy = -1;
for C=C_range
  for K_gamma=gamma_range
    accuracy = kfoldcv(k, X, y, C, K_gamma, @testdualsvm);
    result = [C, K_gamma, mean(accuracy)];
    if result(3) >= maxAccuracy
      C_opt = C;
      gamma_opt = K_gamma;
      accuracy_opt = result(3);
      maxAccuracy = result(3);
    end
    results = [results; result];
  end
end
end
    
