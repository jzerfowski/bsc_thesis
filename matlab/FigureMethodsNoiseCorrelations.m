clear correlations correlation_seeds;

%noisetype = 3 %1 White % 2 Brown % 3 Pink
correlation_threshold = 0.02;
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

first_seed = 45;
last_seed = 80;

for noisetype = 2:2

    correlations = zeros(1, last_seed-first_seed+1);
    correlation_seeds = zeros(1, last_seed-first_seed+1);
    low_correlation_seeds = [];
    low_correlations = [];
    fprintf('Testing noiseseeds: ');

    for i = 1:last_seed-first_seed+1
        noiseseed = i+first_seed-1;
        if mod(noiseseed, 100) == 0
            fprintf('%i, ', noiseseed);
        end

        if noisetype == 1
            [Ie_noise, Ii_noise] = noise_white(reg, tnumb, noiseseed, noisecor, Ienoise, Iinoise);
        elseif noisetype == 2 %Brown
            [Ie_noise, Ii_noise] = noise_brown(dt, reg, tnumb, noiseseed, noiseamp, noisecor, tau, Ienoise, Iinoise);
        elseif noisetype == 3 %Pink
            [Ie_noise, Ii_noise] = noise_pink(dt, reg, tnumb, noiseseed, noiseamp, noisecor, Ienoise, Iinoise);
        end

    %     correlations = crosscorrelation2(Ie_noise(1, :), Ie_noise(2, :), 200);
    %     plot(correlations)
        correlation = corr(Ie_noise(1, :)', Ie_noise(2, :)');
        correlations(i) = correlation;
        correlation_seeds(i) = noiseseed;
        if abs(correlation) <= correlation_threshold
           low_correlation_seeds = [low_correlation_seeds noiseseed];
           low_correlations = [low_correlations correlation];
        end

    end

    % for i = 1:length(correlations)
    %    fprintf('seed %i: correlation %f\n', correlation_seeds(i), correlations(i));
    % end
    

    fprintf('Low correlation noiseseeds for noisetype %i:\n', noisetype); 
    for i = length(low_correlation_seeds):-1:1
       fprintf('seed: %i, noiseseed: %i, correlation: %f\n', low_correlation_seeds(i)-19, low_correlation_seeds(i), low_correlations(i))
    end
    fprintf('\nThis corresponds to a ratio of %f\n', length(low_correlation_seeds)/length(correlations));

    
    if save_results
        if noisetype == 1 %White
            save('../py/mat/noise_correlations_white', 'correlations', 'correlation_seeds');
        elseif noisetype == 2 %Brown
            save('../py/mat/noise_correlations_brown', 'correlations', 'correlation_seeds');
        elseif noisetype == 3 %Pink
            save('../py/mat/noise_correlations_pink', 'correlations', 'correlation_seeds');
        end
    end
end
