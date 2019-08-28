sig_noise = nsig(:,Tselection/dthist:end-100);
for r = 1:reg
    sig_noise_norm(r,:) = (sig_noise(r,:) - min(sig_noise(r,:))) ./ max(sig_noise(r,:)- min(sig_noise(r,:)));
end


[freqosc, phaseosc, power, powermat] = freq_phase(hist_e, dthist, sett.corselection, reg, []);
% [freqosci, phaseosci, poweri, powermati] = freq_phase(hist_i, dthist, sett.corselection, reg, []);
avgmorfreq(l1,l2,:) = nanmean(freqosc(1,Tselection/dthist:end-100,:), 2);
% avgmorfreqi(l1,l2,:) = nanmean(freqosci(1,Tselection/dthist:end-100,:), 2);

sigfreq = freqosc(1,Tselection/dthist:end-99,:);
sigpower = power(1,Tselection/dthist:end-99,:);
% sigpeak = zeros(1,(Ttot-Tselection)/dthist - 99, reg);
% sigbase = zeros(1,(Ttot-Tselection)/dthist - 99, reg);
sigfper = zeros(1,(Ttot-Tselection)/dthist - 99, reg);

Fs = 1000/dthist;
% [b a] = butter(5, [30,90]./(Fs/2), 'stop'); % 10th order low pass filter, below 30 Hz
% [b a] = butter(5, 200./(Fs/2), 'high'); % 10th order low pass filter, below 30 Hz
% [b a] = butter(5, 20./(Fs/2), 'low'); % 10th order low pass filter, below 30 Hz
% fvtool(b,a)

[sigfreq_tshuf, sigpower_tshuf, sigfper_tshuf, ...
    sigfreq_pshuf, sigpower_pshuf, sigfper_pshuf] = deal(zeros(size(sigfreq)));

for r = 1:reg

    %     % peak signal
    %     s = 0.25*(1000/avgmorfreq(l1,l2,r))/dthist;
    %     c = s*1*sqrt(2*pi);
    %     gp = (c/(s*sqrt(2*pi)))*exp(-(-50:dthist:50).^2/(2*s^2));
    %
    %     deltaT = round(100/(avgmorfreq(l1,l2,r)*dthist));
    %     [peaks, times] = findpeaks(squeeze(hist_e(1,:,r)), 'sortstr', 'descend', 'npeaks', round(Ttot/floor(1000/avgmorfreq(l1,l2,r))), 'minpeakdistance', round(500/(dthist*avgmorfreq(l1,l2,r))));
    %     [times, Id] = sort(times);
    %     peaks = peaks(Id);
    %
    %     psig = zeros(1,length(hist_e(1,:,1)));
    %     psig(times) = peaks;
    %     psig2 = conv(psig, gp, 'same');
    %     sigpeak(1,:,r) = psig2(1,Tselection/dthist:end-100);

    % baseline firing rate
    %     [b a] = butter(5, [avgmorfreq(l1,l2,r)-20,avgmorfreq(l1,l2,r)+50]./(Fs/2), 'stop'); % 10th order low pass filter, below 30 Hz
    %     bsig = filtfilt(b, a, hist_e(:,:,r));
    %     bsig = hist_e(:,:,r);
    %     bsig = smooth(bsig,round((1000/avgmorfreq(l1,l2,r))/dthist));
    %     sigbase(1,:,r) = bsig(Tselection/dthist:end-100);

    % firing rate per period
    wnd = round((1000/avgmorfreq(l1,l2,r))/dthist)-1;
    avghist = zeros(1,size(hist_e,2)-wnd);
    for iw = 1:size(hist_e,2)-wnd
        avghist(1,iw) = sum(hist_e(1,iw:iw+wnd,r));
    end
    sigfper(1,:,r) = smooth(avghist(1,Tselection/dthist-wnd/2:end-100+wnd/2), round((1000/avgmorfreq(l1,l2,r))/dthist));

%         signal_stats(l1, l2, r).sigfreq = sigfreq(1,:,r);
%         signal_stats(l1, l2, r).sigpower = sigpower(1,:,r);
%         signal_stats(l1, l2, r).sigfper = sigfper(1,:,r);

    % normalize signals
    %     sigbase_norm(1,:,r) = (sigbase(1,:,r) - min(sigbase(1,:,r))) / max(sigbase(1,:,r)- min(sigbase(1,:,r)));
    sigfreq_norm(1,:,r) = (sigfreq(1,:,r) - min(sigfreq(1,:,r))) / max(sigfreq(1,:,r)- min(sigfreq(1,:,r)));
    sigpower_norm(1,:,r) = (sigpower(1,:,r) - min(sigpower(1,:,r))) / max(sigpower(1,:,r)- min(sigpower(1,:,r)));
    %     sigpeak_norm(1,:,r) = (sigpeak(1,:,r) - min(sigpeak(1,:,r))) / max(sigpeak(1,:,r)- min(sigpeak(1,:,r)));
    sigfper_norm(1,:,r) = (sigfper(1,:,r) - min(sigfper(1,:,r))) / max(sigfper(1,:,r)- min(sigfper(1,:,r)));
end
