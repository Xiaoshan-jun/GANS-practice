%=========================================================================
%Simulation of the smooth turn mobility model in a rectangular area with the reflection boundary model
%Author: Yi Zhou and Yan Wan
%Date: 03/19/2013
%=========================================================================
clc
clear all
%Width and length of the simulation area (km^2)
Length=300;
Width=400;
axis([0,Length,0,Width]);

delta_T=6; % Simulation unit time step (second)
ScaleFactor=0.001; %1 meter=0.001km
NoofTimeInterval=20000;%Total number of simulation time steps
V=100; % Speed (meter/second)
x=1.5e5; % Initialization of the X coordinate of the node location (meter)
y=2e5; % Initialization of the Y coordinate of the node location (meter)
X=x*ScaleFactor;
Y=y*ScaleFactor;
phi=0; % Heading angle (radian)
j=0; % Time counter to record the elapsed duration of maintaining the current turning radius
R=16103; % Initialization of the turning radius (meter)

% Initialization of the turn center
center_X=x+R*sin(phi);
center_Y=y-R*cos(phi);
Center_X= center_X*ScaleFactor;
Center_Y= center_Y*ScaleFactor;
line(Center_X,Center_Y,'Marker','o','MarkerSize',3,'MarkerEdgeColor','g');

W=V/R; % Initialization of angular velocity (radian/s)
theta=W*delta_T;% Initialization of the turn angle (radian)
varian=3.105e-5; % Variance of the Gaussian variable, determining the preference between straight trajectories and turns
ExponentialMean=100;% Mean duration between the changes of turning centers (second)
changetime=random('exponential',ExponentialMean)/delta_T; %Initialization of the waiting time before the change of turn center
for i=1:NoofTimeInterval
    j=j+1;
    %When the waiting time is reached, a new waiting time and a new turn
    %radius are generated. Turn angle and turn radius are calculated
    %accordingly.
    if j>changetime
        changetime=random('exponential',ExponentialMean)/delta_T;
        j=0;
        R_d_1=random('Normal', 0, varian);
        R=1/R_d_1;
        W=V/R;
        theta=W*delta_T;
        center_X=x+R*sin(phi);
        center_Y=y-R*cos(phi);
        Center_X= center_X*ScaleFactor;
        Center_Y= center_Y*ScaleFactor;
        %Reflect the turn center when the trajectory is out of boundary
        if (X>Length)||(X<0)||(Y<0)||(Y>Width)
            Center_X=2*Length*abs((Center_X/2/Length-floor(Center_X/2/Length+0.5)));
            Center_Y=2*Width*abs((Center_Y/2/Width-floor(Center_Y/2/Width+0.5)));
            
        end
        line(Center_X,Center_Y,'Marker','o','MarkerSize',3,'MarkerEdgeColor','g');
    end
    %Update the X location, Y location and the heading angle
    x=center_X+R*sin(theta-phi);
    y=center_Y+R*cos(theta-phi);
    phi=phi-theta;
    % Convert the unit of location from meter to km
    X= x*ScaleFactor;
    Y= y*ScaleFactor;
    %Reflection Boundary model
    a=2*Length*abs((X/2/Length-floor(X/2/Length+0.5)));
    b=2*Width*abs((Y/2/Width-floor(Y/2/Width+0.5)));
    %Plot trajectory every 5*6second=30 seconds
    if rem(i,5)==0;
        line(a,b,'Marker','o','MarkerSize',3,'MarkerEdgeColor','r');
        hold on;
        M=getframe;
    end
end

