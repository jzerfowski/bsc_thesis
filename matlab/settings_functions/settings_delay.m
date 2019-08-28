function [sett, para] = settings_dummy(savesettings, runnumber)

fprintf('Loading settings from %s', mfilename);

[sett, para] = settings_comments(false, runnumber);

%%% Change the relevant settings here

%% time steps, population size and initial conditions
sett.dt = 0.05; %ms, time step
sett.Ttot = 2000; % ms, duration of simulation

%% connections 
sett.g_syn_r_max = 0.30;
sett.g_syn_r_step = 0.02;

sett.delay = 1; %ms
sett.delay_reg_e = 10; %ms
sett.delay_reg_i = 10; %ms requirement: delay_reg_i >= delay_reg_e


% Important: Always save the settings
sett.fromfile = mfilename;
settings_saver(sett, para, true);

end