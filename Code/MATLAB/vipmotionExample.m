%% Motion Detection
% This example shows how to use sum of absolute differences (SAD) method for detecting motion
% in a video sequence. This example applies SAD independently to four quadrants of a video 
% sequence. If motion is detected in a quadrant, the example highlights the quadrant in red.

% Copyright 2004-2014 The MathWorks, Inc.

%% Example Model
% The following figure shows the Motion Detection example model:

close;
open_system('vipmotion');
blkName = find_system('vipmotion','blocktype','Scope');
close_system(blkName{1});

%% Motion Detection Results
% If you double-click the Switch block so that the signal is connected to the SAD
% side, the Video Viewer block displays the SAD values, which represent the
% absolute value of the difference between the current and previous image. When
% these SAD values exceed a threshold value, the example highlights the quadrant in
% red.
%
% Note that the difference image itself may be viewed, in place of the original
% intensity image, along with the red motion highlighting, which indicates 
% how the SAD metric works.

close_system('vipmotion');
sim('vipmotion',[0 10.5]);
set(allchild(0), 'Visible', 'off');

blkName = find_system('vipmotion','blocktype','Scope');
open_system(blkName{1});

%%

close_system(blkName{1});
captureVideoViewerFrame('vipmotion/See It/Video Viewer');

close_system('vipmotion');
