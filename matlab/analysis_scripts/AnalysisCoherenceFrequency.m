numbercomb = nchoosek(reg,2);

comb = flipud(combnk(1:reg,2));

for nc = 1:numbercomb
    reg1 = comb(nc,1);
    reg2 = comb(nc,2);

% coherence
    [cohe, phase,~,~,~,f,~,~,~] = coherencyc(hist_e(1,Tselection/dthist:length(hist_e(1,:,reg1)),reg1),hist_e(1,Tselection/dthist:length(hist_e(1,:,reg1)),reg2), params);
%     [cohi, ~,~,psdi1,psdi2,~,~,~,~] = coherencyc(hist_i(1,Tselection/dthist:length(hist_i(1,:,reg1)),reg1),hist_i(1,Tselection/dthist:length(hist_i(1,:,reg1)),reg2), params);
%     psd_e = [psde1,psde2];
%     psd_i = [psdi1,psdi2];
%     fpsd = f;

    coherences{l1, l2, nc}.coh_exc = cohe;
    coherences{l1, l2, nc}.f_exc = f';
    
    [cohit, phasi,~,~,~,f,~,~,~] = coherencyc(hist_i(1,Tselection/dthist:length(hist_i(1,:,reg1)),reg1),hist_i(1,Tselection/dthist:length(hist_i(1,:,reg1)),reg2), params);
    
    coherences{l1, l2, nc}.coh_inh = cohit;
    coherences{l1, l2, nc}.f_inh = f';
end