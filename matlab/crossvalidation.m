function [C_opt gamma_opt accuracy_opt] = crossvalidation(k, X, y, logs)
C_range = [1e-3, 1e-2, 0, 1, 1e2, 1e3, 1e13];
gamma_range = [1e-3, 1e-2, 0, 1, 1e2, 1e3, 1e13];
%C_range = [1e-9, 1e-4, 1e-3, 1e-2, 0, 1, 3, 1e13];
%gamma_range = [1e-9, 1e-4, 1e-3, 1e-2, 0, 1, 3, 1e13];
results = [];
maxAccuracy = -1;
count = size(C_range, 2) * size(gamma_range, 2);
iter = 1;
for C=C_range
  for K_gamma=gamma_range
    if logs == true
        fprintf("%d/%d - Trying C: %.4e, gamma: %.4e", iter, count, C, K_gamma);
    end
    iter = iter + 1;
    accuracy = kfoldcv(k, X, y, C, K_gamma, @testdualsvm);
    result = [C, K_gamma, mean(accuracy)];
    if result(3) >= maxAccuracy
      C_opt = C;
      gamma_opt = K_gamma;
      accuracy_opt = result(3);
      maxAccuracy = result(3);
    end
    if logs == true
        fprintf(" accuracy: %.4f\n", result(3));
    end
    results = [results; result];
  end
end
end
    
