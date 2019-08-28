function [sett, para] = settings_fixed_feedback_smallsteps(savesettings, runnumber)

fprintf('Loading settings from %s', mfilename);

[sett, para] = settings_comments(false, runnumber);

sett.fromfile = mfilename;

%%% Change the relevant settings here

%% driving currents
% loop over driving currents
sett.loopIi = [5,0]; % 0 is no loop, 1 = loop 5 = specialloop (see later);
sett.loopIe = [5,0];

% Defines the 'special' loops over driving currents
sett.iIspecial{1} = linspace(0.4, 2.0, 40);
sett.eIspecial{1} = 0.4652*sett.iIspecial{1}.^4 - 1.9860*sett.iIspecial{1}.^3 + 3.2879*sett.iIspecial{1}.^2 - 1.0623*sett.iIspecial{1} + 0.7546;


%% connections 
%values are total gsyns; divide by Njj to obtain unitary gsyn. Values are
%given after % for connectiontype == 3
sett.g_syn_ii = 0.0120 * sett.Msynii*sett.Ni; %1.1; %mS/cm2
sett.g_syn_ie = 0.0050 * sett.Msynie*sett.Ni; %0.24; 
sett.g_syn_ee = 0.0012 * sett.Msynee*sett.Ne;  %0.01; 
sett.g_syn_ei = 0.0010 * sett.Msynei*sett.Ne; %0.34; 

sett.g_syn_ee_r = [[0.00, 0.00];
                   [0.00, 0.00]];
sett.g_syn_ei_r = [[0.00, 0.10];
                   [0.00, 0.00]];
sett.g_syn_ii_r = [[0.00, 0.00];
                   [0.00, 0.00]];
sett.g_syn_ie_r = [[0.00, 0.00];
                   [0.00, 0.00]];

sett.g_syn_loop = [[0, 0]; % 1 is loop for E projections; -1 for I projections; 2 is for both
                   [1, 0]];

sett.g_syn_r_max = 0.30;
sett.g_syn_r_step = 0.01;

sett.g_syn_ifactor = 1;



% Important: Always save the settings
settings_saver(sett, para, true);

end
