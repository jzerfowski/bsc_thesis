function [corrs] = crosscorrelation2(signal1, signal2, max_lag)
    max_lag = max_lag + 1;
    corrsleft(max_lag) = 0;
    corrsright(max_lag) = 0;
    
    for i = 1:max_lag
        corrsleft(i) = nancorr(signal1(1:end-i+1)', signal2(i:end)');
        corrsright(i) = nancorr(signal1(i:end)', signal2(1:end-i+1)');
    end
    corrs = [flip(corrsleft(:))', corrsright(2:end)];
end