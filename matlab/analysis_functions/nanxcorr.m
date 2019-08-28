function [correlations, lags] = nanxcorr(sig1, sig2)

sel = ~isnan(sig1) & ~isnan(sig2);

if length(sig1) ~= length(sig2)
    error('Signals do not have the same lengths');
end

lags = zeros(length(sig2), 1);
correlations = zeros(length(sig2), 1);

[correlations(sel), lags(sel)] = xcorr(sig1(sel)-mean(sig1(sel)), sig2(sel)-mean(sig2(sel)),floor ceil(sum(sel)/2));

end