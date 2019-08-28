l1 = 4;
l2 = 10;

% clear coherences_e_mor;

data = open([sett.savelocdata, 'l1', num2str(l1),'_l2', num2str(l2),'.mat']);
spikes_i = data.spikes_i; spikes_e = data.spikes_e;

% [hist_i, histtime_i, smoothhist_i] = histograms(spikes_i, Ni, Ttot, dt, dthist, cutoff_freq_low, cutoff_freq_high, reg);
[hist_e, histtime_e, smoothhist_e] = histograms(spikes_e, Ne, Ttot, dt, dthist, cutoff_freq_low, cutoff_freq_high, reg);

% coherence
[cohe, phase,~,~,~,f,~,~,~] = coherencyc(hist_e(1,Tselection/dthist:length(hist_e(1,:,1)),1),hist_e(1,Tselection/dthist:length(hist_e(1,:,1)),2), params);
fcoh = f;
[~, fId] = min(abs(fcoh - avgmorfreq(l1,l2,1)));

signal_coherence = cohe(fId)

windowsize = 500/dthist;
stepsize = 10/dthist;

coherences_e = [];

for window_start_ = 1:stepsize:length(hist_e) - windowsize - Tselection/dthist
    window_start = Tselection/dthist + window_start_;
    window_end = window_start + windowsize;
    [cohe, phase,~,~,~,f,~,~,~] = coherencyc(hist_e(1,window_start:window_end,1),hist_e(1,window_start:window_end,2), params);
%     [cohe, phase,~,~,~,f,~,~,~] = coherencyc(hist_e(1,Tselection/dthist:length(hist_e(1,:,1)),1),hist_e(1,Tselection/dthist:length(hist_e(1,:,1)),2), params);
    fcoh = f;
    [~, fId_mor] = min(abs(fcoh - avgmorfreq(l1,l2,1)));
    [~, fId_freqe] = min(abs(fcoh - freqe(l1,l2,1)));

    coherences_e_mor(window_start_:window_start_+stepsize) = cohe(fId_mor);
%     coherences_e_freqe(window_start_:window_start_+stepsize) = cohe(fId_freqe);
end
hold on;
plot(1:length(coherences_e_mor), coherences_e_mor)
% plot(coherences_e_freqe);
yline(signal_coherence);