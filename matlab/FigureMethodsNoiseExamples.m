% FigureMethodsNoiseExamples

correlation_threshold = 0.05;
save_results = 0;

Ttot = 3200;
dt = 0.05;
reg = 2;
tnumb = Ttot /dt +1;
noiseamp = 1;
noisecor = 0;
tau = 200; % Only for brown noise
Ienoise = [1, 1];
Iinoise = [0, 0];

noiseseed = 46

White = noise_white(reg, tnumb, noiseseed, noisecor, Ienoise, Iinoise)/5;
Brown = noise_brown(dt, reg, tnumb, noiseseed, noiseamp, noisecor, tau, Ienoise, Iinoise);
Pink = noise_pink(dt, reg, tnumb, noiseseed, noiseamp, noisecor, Ienoise, Iinoise);

corr(Brown(1, :)', Brown(2, :)')

plot(Brown(2, :)); 
figure; plot(crosscorrelation2(Brown(1, :), Brown(2, :), 100))

if save_results
    save('../py/mat/noise_examples', 'White', 'Brown', 'Pink');
end