function [output_path, output_path_data, output_path_figures] = get_local_path()
%LOCAL_SETTINGS Summary of this function goes here
%   Detailed explanation goes here

output_path = './GridOutput/';
output_path_data = fullfile(output_path, 'Data/');
output_path_figures = fullfile(output_path, 'Figures/');

end

