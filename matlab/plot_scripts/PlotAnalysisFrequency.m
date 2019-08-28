l2_index = 10

dimx = size(coherences, 1);
dimy = 779

coherences_current_frequency = zeros(dimy, dimx);


for l1 = 1:size(coherences, 1)
    coherences_frequency = coherences(l1, l2_index);
    coherences_current_frequency(:, l1) = coherences_frequency{1}.coh_exc;
end

frequencies = coherences_frequency{1}.f_exc;

heatmap(coherences_current_frequency, 'GridVisible', 'off');
% yticks(1:10:length(frequencies))
yticklabels(frequencies(1:10:end))
