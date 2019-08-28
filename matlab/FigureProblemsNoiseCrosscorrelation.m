% FigureMethodsNoiseExamples

correlation_threshold = 0.05;
% save_results = 0;

Ttot = 3200;
dt = 0.05;
reg = 2;
tnumb = Ttot /dt +1;
noiseamp = 1;
noisecor = 0;
tau = 200; % Only for brown noise
Ienoise = [1, 1];
Iinoise = [0, 0];
noiseseeds = [24, 36, 45, 46, 73, 80];
num_seeds = length(noiseseeds);
lag_max = 200;

crosscorrs = zeros(seeds_stop, 2*lag_max+1);


for i = 1:num_seeds
    noiseseed = noiseseeds(i)
    brown_noise = noise_brown(dt, reg, tnumb, noiseseed, noiseamp, noisecor, tau, Ienoise, Iinoise);
    crosscorrs(i, :) = crosscorrelation2(brown_noise(1, :), brown_noise(2, :), lag_max);
    
%     plot((crosscorr - min(crosscorr))/(max(crosscorr)-min(crosscorr))
end


figure; hold on;
for i = 1:num_seeds
   crosscorr = crosscorrs(i, :);
   noiseseed = noiseseeds(i);
   plot((crosscorr), 'DisplayName',['noiseseed: ', num2str(noiseseed)])
end
legend;
% 
% if save_results
%     save('../py/mat/noise_examples', 'White', 'Brown', 'Pink');
% end