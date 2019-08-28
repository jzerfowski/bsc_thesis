function [sett, para] = settings_dummy(savesettings, runnumber)

fprintf('Loading settings from %s', mfilename);

[sett, para] = settings_comments(false, runnumber);

%%% Change the relevant settings here




% Important: Always save the settings
sett.fromfile = mfilename;
settings_saver(sett, para, true);

end