analysis_info2_max_lag = 200; % corresponds to (lag in ms)/dthist

signal_noise1 = squeeze(sig_noise_norm(1,:));
signal_noise2 = squeeze(sig_noise_norm(2,:));

rhos_lags = (-analysis_info2_max_lag:analysis_info2_max_lag)*dthist;

rhos_fper_noise1_reg1(l1, l2, :) = crosscorrelation2(signal_noise1, squeeze(sigfper_norm(1,:,1)), analysis_info2_max_lag);
rhos_fper_noise1_reg2(l1, l2, :) = crosscorrelation2(signal_noise1, squeeze(sigfper_norm(1,:,2)), analysis_info2_max_lag);
rhos_fper_noise2_reg1(l1, l2, :) = crosscorrelation2(signal_noise2, squeeze(sigfper_norm(1,:,1)), analysis_info2_max_lag);
rhos_fper_noise2_reg2(l1, l2, :) = crosscorrelation2(signal_noise2, squeeze(sigfper_norm(1,:,2)), analysis_info2_max_lag);
rhos_fper_reg1_reg2(l1, l2, :) = crosscorrelation2(squeeze(sigfper_norm(1,:,1)), squeeze(sigfper_norm(1,:,2)), analysis_info2_max_lag);

rhos_freq_noise1_reg1(l1, l2, :) = crosscorrelation2(signal_noise1, squeeze(sigfreq_norm(1,:,1)), analysis_info2_max_lag);
rhos_freq_noise1_reg2(l1, l2, :) = crosscorrelation2(signal_noise1, squeeze(sigfreq_norm(1,:,2)), analysis_info2_max_lag);
rhos_freq_noise2_reg1(l1, l2, :) = crosscorrelation2(signal_noise2, squeeze(sigfreq_norm(1,:,1)), analysis_info2_max_lag);
rhos_freq_noise2_reg2(l1, l2, :) = crosscorrelation2(signal_noise2, squeeze(sigfreq_norm(1,:,2)), analysis_info2_max_lag);
rhos_freq_reg1_reg2(l1, l2, :) = crosscorrelation2(squeeze(sigfreq_norm(1,:,1)), squeeze(sigfreq_norm(1,:,2)), analysis_info2_max_lag);

rhos_power_noise1_reg1(l1, l2, :) = crosscorrelation2(signal_noise1, squeeze(sigpower_norm(1,:,1)), analysis_info2_max_lag);
rhos_power_noise1_reg2(l1, l2, :) = crosscorrelation2(signal_noise1, squeeze(sigpower_norm(1,:,2)), analysis_info2_max_lag);
rhos_power_noise2_reg1(l1, l2, :) = crosscorrelation2(signal_noise2, squeeze(sigpower_norm(1,:,1)), analysis_info2_max_lag);
rhos_power_noise2_reg2(l1, l2, :) = crosscorrelation2(signal_noise2, squeeze(sigpower_norm(1,:,2)), analysis_info2_max_lag);
rhos_power_reg1_reg2(l1, l2, :) = crosscorrelation2(squeeze(sigpower_norm(1,:,1)), squeeze(sigpower_norm(1,:,2)), analysis_info2_max_lag);