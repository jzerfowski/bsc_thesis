function [sett, para] = settings_noise_2regions(savesettings, runnumber)

fprintf('Loading settings from %s', mfilename);

[sett, para] = settings_comments(false, runnumber);

%%% Change the relevant settings here

%% time steps, population size and initial conditions
sett.dt = 0.05; %ms, time step
sett.Ttot = 3200; % ms, duration of simulation


%% driving currents
% loop over driving currents
sett.loopIi = [5,0]; % 0 is no loop, 1 = loop 5 = specialloop (see later);
sett.loopIe = [5,0];
sett.Istep = 0.1;

sett.iIu = [0.95,0.95]; %uA/cm^2, average amplitude of applied current; if reg > 1 and length(iIu) == 1, this value is used for all regions, if reg ~= length(iIu) an error occurs
sett.iIu_max = [4,5];

sett.eIu = [1.5,1.5]; %uA/cm^2
sett.eIu_max = [2,1.7173];

% Defines the 'special' loops over driving currents
sett.iIspecial{1} = linspace(0.4, 2.0, 40);

% Todo: Why that complicated?
sett.eIspecial{1} = 0.4652*sett.iIspecial{1}.^4 - 1.9860*sett.iIspecial{1}.^3 + 3.2879*sett.iIspecial{1}.^2 - 1.0623*sett.iIspecial{1} + 0.7546;

%% applied currents

% fraction of cells affected:
sett.Idyn_frac = 1; % not for pulses! 

% noisy input per region
sett.Iinoise = [0,0];%0 = no noise; 1 = noise;
sett.Ienoise = [1,1];
sett.Inoise_loop = 0; % change noise amp % Loop over noise amplitudes

sett.noisetype = 2; % 1 = white noise; 2 = brownian noise; 3 = Pink;
sett.tau = 200; %in ms, for brownian noise
sett.subregion_noise = 0; %0: just into region; 1 = into region and subregion; 2 = just into subregion
sett.noiseamp = 0.5;
sett.noiseamp_max = 1.5;
sett.noiseamp_step = 1;%
sett.noisecor = 0; % creates a correlation between area 1 and area reg
sett.noiseseed = sett.seed+ 19; 

%% connections 
%values are total gsyns; divide by Njj to obtain unitary gsyn. Values are
%given after % for connectiontype == 3
sett.g_syn_ii = 0.0120 * sett.Msynii*sett.Ni; %1.1; %mS/cm2
sett.g_syn_ie = 0.0050 * sett.Msynie*sett.Ni; %0.24; 
sett.g_syn_ee = 0.0012 * sett.Msynee*sett.Ne;  %0.01; 
sett.g_syn_ei = 0.0010 * sett.Msynei*sett.Ne; %0.34; 

% columns: from, rows: to; access: sett.g_syn_xx_r(from, to)
sett.g_syn_ee_r = [[0.00, 0.00];
                   [0.00, 0.00]];
sett.g_syn_ei_r = [[0.00, 0.00];
                   [0.00, 0.00]];
sett.g_syn_ii_r = [[0.00, 0.00];
                   [0.00, 0.00]];
sett.g_syn_ie_r = [[0.00, 0.00];
                   [0.00, 0.00]];

sett.g_syn_loop = [[0, 0]; % 1 is loop for E projections; -1 for I projections; 2 is for both
                   [1, 0]];

sett.g_syn_r_max = 0.30;
sett.g_syn_r_step = 0.02;

sett.g_syn_ifactor = 1; % Ratio: E->I conductance = g_syn_ifactor * E->E conductance


% Important: Always save the settings
sett.fromfile = mfilename;
settings_saver(sett, para, true);

end