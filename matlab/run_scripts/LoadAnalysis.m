% load analysis

load([sett.savelocdata,'analysis', '.mat']);

if reg > 1;  load([sett.savelocdata,'analysis2', '.mat']); end
if loopId(5) > 0;  load([sett.savelocdata,'analysis_pulses', '.mat']); end
if analyzeInfo; load([sett.savelocdata,'analysis_info', '.mat']); end
if analyzeInfo; load([sett.savelocdata,'analysis_info2', '.mat']); end



%% Old workaround for runnumbers and versions of the simulation:
% 
% 
% if runnumber < 650%  %? 652
%     %TODO: Why this condition?
%     load([sett.savelocdata,'analysis', '.mat']);
%     if reg > 1;
%         load([sett.savelocdata,'analysis2', '.mat']);
% %         load([sett.savelocdata,'analysis3', '.mat']);
% %         load([sett.savelocdata,'analysis4', '.mat']);
% %         load([sett.savelocdata,'analysis5', '.mat']);
%     end
%     
% else
%     warning('Runnumber > 650, therefore we load the analysis automagically');
%     load([sett.savelocdata,'analysis', '.mat']);
%     if reg > 1;  load([sett.savelocdata,'analysis2', '.mat']); end
%     if loopId(5) > 0;  load([sett.savelocdata,'analysis_pulses', '.mat']); end
%     if analyzeInfo; load([sett.savelocdata,'analysis_info', '.mat']); end
%     if analyzeDirection; load([sett.savelocdata,'analysis_direction', '.mat']); end
% end