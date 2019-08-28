% analysis_info2_max_lag = 200; % corresponds to (lag in ms)/dthist
% 
% rhos_lags = (-analysis_info2_max_lag:analysis_info2_max_lag)*dthist;

xticks_pos = 1:10:length(rhos_lags);
xtickslabels = rhos_lags(1:10:end);

correlation_threshold = 0.3;

%%%% For debugging purposes:
% Plot the crosscorrelation curves for each run
% For firing rate:
figure; hold on;
for i = 1:size(rhos_freq_noise1_reg1, 1)
    % If we do not have feedback, the correlation for each feedforward
    % condition is the same.
    plot(squeeze(rhos_fper_noise1_reg1(i,1,:)));
end
title('Firing rate lags')

xline(length(rhos_lags)/2+0.5);
xlabel('Lag in ms');
xticks(xticks_pos);
xticklabels(xtickslabels);
xlim([1, length(rhos_lags)]);

yline(0);
ylim([0, 1]);
ylabel('Correlation');

if savefigures
    saveas(gcf, [sett.saveloc,'firingrate_noise1_reg1_lag_vs_correlations', '.', saveformat],saveformat)
end

% For frequency
figure; hold on;
for i = 1:size(rhos_freq_noise1_reg1, 1)
    % If we do not have feedback, the correlation for each feedforward
    % condition is the same.
    plot(squeeze(rhos_freq_noise1_reg1(i,1,:)));
end
title('Frequency lags')

xline(length(rhos_lags)/2+0.5);
xlabel('Lag in ms');
xticks(xticks_pos);
xticklabels(xtickslabels);
xlim([1, length(rhos_lags)]);

yline(0);
ylim([0, 1]);
ylabel('Correlation');

if savefigures
    saveas(gcf, [sett.saveloc,'frequency_noise1_reg1_lag_vs_correlations', '.', saveformat],saveformat)
end

%% Firing rate plots
% region 1 <-> region 2
[max_rhos, max_idx] = max(rhos_fper_reg1_reg2, [], 3);

figure;
scatter(max_idx(:), max_rhos(:));
title('Firing rate - Lag vs. max. Correlation (reg_1 <-> reg_2)');

xline(length(rhos_lags)/2+0.5);
xlabel('Lag in ms');
xticks(xticks_pos);
xticklabels(xtickslabels);
xlim([1, length(rhos_lags)]);

yline(0);
ylim([-1, 1]);
ylabel('Correlation');

if savefigures
    saveas(gcf, [sett.saveloc,'firingrate_lag_vs_correlation', '.', saveformat],saveformat)
end

% noise 1 -> region 1 and noise 1 -> region 2
[max_rhos11, max_idx11] = max(rhos_fper_noise1_reg1, [], 3);
[max_rhos12, max_idx12] = max(rhos_fper_noise1_reg2, [], 3);


figure;
hold on;
scatter(max_idx11(:), max_rhos11(:), 'red');
scatter(max_idx12(:), max_rhos12(:), 'blue');

legend('noise1 -> reg_1','noise1 -> reg_2')

title('Firing rate - Lag vs. max. Correlation (noise1 -> reg_1 & reg_2)');

xline(length(rhos_lags)/2+0.5);
xlabel('Lag in ms');
xticks(xticks_pos);
xticklabels(xtickslabels);
xlim([1, length(rhos_lags)]);

yline(0);
ylim([-1, 1]);
ylabel('Correlation');


if savefigures
    saveas(gcf, [sett.saveloc,'firingrate_noise1_region12_lag_vs_correlation', '.', saveformat],saveformat)
end


%% Power plots
% region 1 <-> region 2
[max_rhos, max_idx] = max(rhos_power_reg1_reg2, [], 3);

figure;
scatter(max_idx(:), max_rhos(:));
title('Power - Lag vs. max. Correlation (reg_1 <-> reg_2)');

xline(length(rhos_lags)/2+0.5);
xlabel('Lag in ms');
xticks(xticks_pos);
xticklabels(xtickslabels);
xlim([1, length(rhos_lags)]);

yline(0);
ylim([-1, 1]);
ylabel('Correlation');

if savefigures
    saveas(gcf, [sett.saveloc,'power_lag_vs_correlation', '.', saveformat],saveformat)
end

%% Frequency plots
% region 1 <-> region 2
[max_rhos, max_idx] = max(rhos_freq_reg1_reg2, [], 3);

figure;
scatter(max_idx(:), max_rhos(:));
title('Frequency - Lag vs. max. Correlation (reg_1 <-> reg_2)');

xline(length(rhos_lags)/2+0.5);
xlabel('Lag in ms');
xticks(xticks_pos);
xticklabels(xtickslabels);
xlim([1, length(rhos_lags)]);

yline(0);
ylim([-1, 1]);
ylabel('Correlation');

if savefigures
    saveas(gcf, [sett.saveloc,'frequency_lag_vs_correlation', '.', saveformat],saveformat)
end

% noise 1 -> region 1 and noise 1 -> region 2
[max_rhos11, max_idx11] = max(rhos_freq_noise1_reg1, [], 3);
[max_rhos12, max_idx12] = max(rhos_freq_noise1_reg2, [], 3);


figure;
hold on;
scatter(max_idx11(:), max_rhos11(:), 'red');
scatter(max_idx12(:), max_rhos12(:), 'blue');

legend('noise1 -> reg_1','noise1 -> reg_2');


title('Frequency - Lag vs. max. Correlation (noise1 -> reg_1 & reg_2)');

xline(length(rhos_lags)/2+0.5);
xlabel('Lag in ms');
xticks(xticks_pos);
xticklabels(xtickslabels);
xlim([1, length(rhos_lags)]);

yline(0);
ylim([-1, 1]);
ylabel('Correlation');
hold off;

if savefigures
    saveas(gcf, [sett.saveloc,'frequency_noise1_region12_lag_vs_correlation', '.', saveformat],saveformat)
end
