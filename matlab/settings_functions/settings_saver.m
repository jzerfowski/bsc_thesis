function [] = settings_saver(sett,para, savesettings)
% if savesettings == true, saves the settings. Should be called by each
% individual settings file

if savesettings == true
    mkdir([sett.path, 'Data/run',num2str(sett.runnumber)]);
    mkdir([sett.path, 'Figures/run',num2str(sett.runnumber)]);
    save([sett.savelocdata,'settings.mat'], 'sett','para');
    
    diary([sett.savelocdata, 'set.txt']);
    sett
    para
    diary off
    
    diary([sett.saveloc, 'set.txt']);
    sett
    para
    diary off
end
end
