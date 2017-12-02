function ynorm = normalizedata(y)
    ynorm = (y - min(y)) / (max(y) - min(y));