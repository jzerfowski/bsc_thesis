function [sett, para] = settings_single_region(savesettings, runnumber)

fprintf('Loading settings from %s', mfilename)

[sett, para] = settings_comments(false, runnumber)

sett.Nregions = 1;


%% driving currents
% loop over driving currents
sett.loopIi = [1]; % 0 is no loop, 1 = loop 5 = specialloop (see later);
sett.loopIe = [1];

sett.Istep = 0.1;

sett.iIu = [0.0]; %uA/cm^2, average amplitude of applied current; if reg > 1 and length(iIu) == 1, this value is used for all regions, if reg ~= length(iIu) an error occurs
sett.iIu_max = [3];

sett.eIu = [0]; %uA/cm^2
sett.eIu_max = [4];

%% applied currents
% noisy input per region
sett.Iinoise = [0];%0 = no noise; 1 = noise;
sett.Ienoise = [0];

% pulses
sett.Iipulse = [0]; % 0 = no applied current; 1 = pulse;
sett.Iepulse = [0];

% sinusoid
sett.Iiper = [0]; % 0 = no applied current; 1 = oscillatory input to region;
sett.Ieper = [0];

% ramp
sett.Iiramp = [0];
sett.Ieramp = [0];

% stepwise changing currents
sett.Iistep = [0];
sett.Iestep = [0];

%% connections 
sett.g_syn_loop = [0];

% Important: Always save the settings
sett.fromfile = mfilename;
settings_saver(sett, para, true)

end