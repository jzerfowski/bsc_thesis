%% Run the startup file which initializes the path

% clear all;
% clc;
% close all;

MatlabStartup
tic;

%% Loading and saving - settings
% settings_function_handle = @settings_check_eIspecial_nonlinear;

settings_function_handle = @settings_check_eIspecial_linear

% settings_function_handle = str2func('settings_original'); %Alternative

[output_path, output_path_data, output_path_figures] = get_local_path();

loaddata = 1; % 0 = calc data; 1 = load from file
loadanalysis = 0; % 0 = redo analysis; 1 = load from file; -1 = TODO skip analysis
load_runnumber = 134; % if loaddata or loadanalysis are true, load the data of this run
% This loads the data for the latest run (with highest runnumber
% Be careful if there are several runs at the same time!
%load_runnumber = get_latest_runnumber(output_path_data, 'run');

savedata = 1;

%% Analyses - settings
analyzePPC = 1;
analyzeInfo = 1;

%% Plots - settings

plotDrive = 1; % measures vs input current for one area, vs freqdiff for two areas
plotPerCondition = 0; % see script for further specification

generate_figures = 0;
savefigures = 1; % Currently only for PlotDriveTwoAreas
saveformat = 'png'; % Currently only for PlotDriveTwoAreas


%% Load the settings from the given settings_function_name
simulation_settings = settings_function_handle;

%% Do necessary path and runnumber settings

if loaddata
    runnumber = load_runnumber;
else
    runnumber = get_latest_runnumber(output_path_data, 'run') + 1;
end

fprintf('runnumber: %i\n', runnumber);

%% Optional settings wich usually do not change

simulation_loop1start = 1;
simulation_loop2start = 1;

% TODO: Load analysis if not both 1
analysis_loop1start = 30;
analysis_loop2start = 10;

%% Load Parameters and allocate memory
GetParsNew; % Load common parameters
DetermineLoops % determine which parameters are looped over. l1steps, l2steps come from here
Preallocation % allocate memory for analysis

%% load some currents
LoadNoise

if sum(sett.Iipulse + sett.Iepulse) > 0
    analyzePulses = 1;
else
    analyzePulses = 0;
end

%% Run network

if loaddata == 0
    fprintf('Run #%i: Simulating %i steps\n', runnumber, l1steps*l2steps);
    
    if simulation_loop1start ~= 1 || simulation_loop2start ~= 1
       warning('Warning, starting simulation from step loop1=%i, loop2=%i', simulation_loop1start, simulation_loop2start);
    end
    

    
    for l1 = simulation_loop1start:l1steps
        tic;
        
        if analyzePulses == true && sum(sett.Ieper+sett.Iiper)==0
            l2 = 1;
            csett = changePars(sett, loopId, l1, l2); % change l1 parameter
            ReferenceRun;
        end
        
        for l2 = simulation_loop2start:l2steps
            tic;
            if analyzePulses == true && sum(sett.Ieper+sett.Iiper)
                csett = changePars(sett, loopId, l1, l2); % change l2 parameter
                ReferenceRun;
            end
            
            csett = changePars(sett, loopId, l1, l2); % change l2 parameter
                
            fprintf('Calculating data (run%i): l1 = %i of %i; l2 = %i of %i\n', runnumber, l1, l1steps, l2, l2steps);
            [spikes_i, spikes_e] = calcEInetworkRK4(sett, para, csett);
            if savedata == true
                savespikes(sett.savelocdata, spikes_i, spikes_e, l1, l2);
            end
            
            toc
        end
    end
    
    fprintf('Run #%i: Finished simulation of %i steps\n', runnumber, l1steps*l2steps);
end


%% Run analysis
if loadanalysis == 1 && ~plotPerCondition
    fprintf('Loading analyses...');
    LoadAnalysis
    fprintf(' Done\n');
elseif loadanalysis == 0 || plotPerCondition
    fprintf('Run #%i: Analyzing %i steps\n', runnumber, l1steps*l2steps);

    if analysis_loop1start ~= 1 || analysis_loop2start ~= 1
       warning('Warning, starting analysis from step loop1=%i, loop2=%i', analysis_loop1start, analysis_loop2start);
    end
    
    % the Analysis has to be done afterwards
    for l1 = analysis_loop1start:l1steps
        tic;

        if analyzePulses == true && sum(sett.Ieper+sett.Iiper)==0
            l2 = 1;
            csett = changePars(sett, loopId, l1, l2); % change l1 parameter
            ReferenceRun;
        end
        
        for l2 = analysis_loop2start:l2steps
            tic;
            if analyzePulses == true && sum(sett.Ieper+sett.Iiper)
                csett = changePars(sett, loopId, l1, l2); % change l2 parameter
                ReferenceRun;
            end
            
            csett = changePars(sett, loopId, l1, l2); % change l2 parameter
            
            fprintf('Loading data (run%i): l1 = %i of %i; l2 = %i of %i\n', runnumber, l1, l1steps, l2, l2steps);
            data = open([sett.savelocdata, 'l1', num2str(l1),'_l2', num2str(l2),'.mat']); %run 660
            spikes_i = data.spikes_i; spikes_e = data.spikes_e;
            
            
            fprintf('Analyzing spiketrains\n');
            AnalysisStandard1;
            if reg > 1
                AnalysisStandard2;
            end
            if analyzePulses == true && length(pulse_start) == 1
                AnalysisPulses;
            end
            if analyzeInfo == true
                AnalysisInfo;
                
                fprintf('Starting AnalysisInfo2\n');
                AnalysisInfo2;
            end

            % plots
            if generate_figures && plotPerCondition
                fprintf('Generating plot for condition');
                PlotPerCondition;
            end
            
            toc
        end
        fprintf('Completed step %i of %i steps of loop1\n', l1, l1steps);
        toc
    end
    
    %% Save
    SaveAnalysis
    
    fprintf('Run #%i: Finished analysis of %i steps\n', runnumber, l1steps*l2steps);

end


%% Plot
if generate_figures && loadanalysis ~= 2
    if plotDrive == true
        if reg == 1
            plotFreqe = freqe';
            plotFreqi = freqi';
            meanRe = re';
            meanRi = ri';
            plotPle = Phaselocke';
            plotPli = Phaselocki';
            plotCV   = CVe';
            PlotDriveOneArea
        else
            variableFreqAxis = 0;
            meanPli_12 = Phaselocki_12;
            meanPle_12 = Phaselocke_12;
            Phaseli = Phaselocki;
            Phasele = Phaselocke;
            PlotDriveTwoAreas
        end
    end

    %Pulses
    if analyzePulses == true
        PlotPulseOneArea
        if reg > 1
            PlotPulseTwoAreas
        end
    end

    % Information
    if analyzeInfo == true && reg == 2 && l1steps > 1
        PlotInfoTwoAreas
        PlotEffectiveDelay
    end
else
    fprintf('Not generating any figures because generate_figures = %i\n', generate_figures)
end

fprintf('Done...\n')
toc

fprintf('Finished ::run%i::\n', runnumber); % print runnumber for automated renaming of logfiles
