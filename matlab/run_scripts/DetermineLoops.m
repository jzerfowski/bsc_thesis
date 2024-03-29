% Determine Loops: find the parameters that require looping, according to
% settings.m.

% there are currently 8 possible settings that can be looped over, ...
% 2 of those can be combined in 1 run.
loopId = zeros(8,1); 

% loop over i current(s)
if sum(sett.loopIi == 1) >= 1;      loopId(1) = sum(sett.loopIi == 1);      end 
% loop over e current(s)
if sum(sett.loopIe == 1) >= 1;      loopId(2) = sum(sett.loopIe == 1);      end 
% loop over special current path(s) (Driving current)
if sum(sett.loopIe == 5) >= 1;      loopId(3) = sum(sett.loopIe == 5);      end 
% loop over noise amplitude
if sett.Inoise_loop == 1;           loopId(4) = 1;                          end 
% loop over pulse time or amplitude
if sett.Iapploop == 1 || sett.Iapploop == 2
                                    loopId(5) = 1; 
elseif sett.Iapploop == 3                    
                                    loopId(5) = 2;
end
% loop over period (and amplitude) of periodic current
if sett.Iperloop ==1 || sett.Iperloop == 2        
                                    loopId(6) = 1;
elseif sett.Iperloop == 3
                                    loopId(6) = 2;  
end 
% loop over inter-region connections
if sum(abs(sett.g_syn_loop(:)))>0;  loopId(7) = 1;                          end
% loop over delayed onset of area 2
if sett.lateonset == 1;             loopId(8) = 1;                          end 


%% check the numbers

switch sum(loopId) 
    case 0 
            fprintf('Variable loops: 0 loop variables were identified \n')
            l1steps = 1;
            l2steps = 1;
    case 1
            l1steps = determineSteps(sett, find(loopId == 1), 1);
            l2steps = 1;
            fprintf('Variable loops: 1 loop variable was identified: l1_steps = %d \n', l1steps); 
    case 2
            if ~isempty(find(loopId == 2, 1))
                steps = determineSteps(sett, find(loopId == 2, 1), 2);
                l1steps = steps(1);
                l2steps = steps(2);
            else
                l1steps = determineSteps(sett, find(loopId == 1, 1, 'first'), 1);
                l2steps = determineSteps(sett, find(loopId == 1, 1, 'last'), 1);
            end
            fprintf('Variable loops: 2 loop variables were identified: l1_steps = %d; l2_steps = %d\n', l1steps, l2steps);
    otherwise
        error('Error: Too many loop variables were specified.')
end    