function [maximumRunNumber] = get_latest_runnumber(dataDir,runPrefix)
%GETCURRENTRUNNUMBER returns the index of the latest run. To avoid overwriting
%data
%   Detailed explanation goes here
% dataDir: Directory, in which the Data for each run is. Used to figure out which
% was the last run
% runPrefix: e.g. "run" to extract the integer of the run from the
% directory name

% Get a list of all files and folders in this folder.
files = dir(dataDir);
% Get a logical vector that tells which is a directory.
dirFlags = [files.isdir];
% Extract only those that are directories.
subFolders = files(dirFlags);

for k = 1 : length(subFolders)
%   fprintf('Sub folder #%d = %s\n', k, subFolders(k).name);
  dirName = subFolders(k).name;
  if startsWith(dirName, runPrefix)
    existingRuns(k) = str2num(char(extractAfter(dirName,runPrefix)));
  end
end

maximumRunNumber = max(existingRuns);

