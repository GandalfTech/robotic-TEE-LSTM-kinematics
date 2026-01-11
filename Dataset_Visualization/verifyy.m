load('Robot_Data_Zero.mat');
x_1 = ir_positions(1,:)-ir_positions2(1,:);
y_1 = ir_positions(2,:)-ir_positions2(2,:);
z_1 = ir_positions(3,:)-ir_positions2(3,:);

o_1 = ir_quaternion_vector(1,:);
o_2 = ir_quaternion_vector(2,:);
o_3 = ir_quaternion_vector(3,:);
a   = ir_quaternion_scalar;
quat = transpose( [o_1 ; o_2 ;  o_3 ; a]);
m = 20010;
rotm = zeros(3,3,m);
rot_rotm = zeros(3,3,m);
W = zeros(m,3);
quat_2 = zeros(m,4);

for r = 1:(m)
    rotm(:,:,r) = quat2rotm(quat(r,:));
    rot_rotm(:,:,r) = rotx(0)*roty(0)*rotz(0)* rotm(:,:,r);
    W(r,:) = rotx(0)*roty(0)*rotz(0)*[ x_1(r); z_1(r); -y_1(r)];
    quat_2(r,:) = rotm2quat(rot_rotm(:,:,r));
    
end

X_2 = ((W(:,1)))*1000;
Y_2 = (W(:,2))*1000;
Z_2 = ((W(:,3)))*1000;

O_1 = quat_2(:,1);
O_2 = quat_2(:,2);
O_3 = quat_2(:,3);
A  =  quat_2(:,4);

% m_1 = transpose(deg2rad((double(motor_1_position_m)-2048)*360/4096));
% m_2 = transpose(deg2rad((double(motor_2_position_m)-2048)*360/4096));
% m_3 = transpose(deg2rad((double(motor_3_position_m)-2048)*360/4096));
% m_4 = transpose(deg2rad((double(motor_4_position_m))*360/526374));

posecell = [X_2 Y_2 Z_2 O_1 O_2 O_3 A];
% motorcell = [m_1 m_2 m_4 m_3 ];
% save('TEE_45_cellformat.mat','posecell','motorcell')
h1 = scatter3(X_2, Y_2,Z_2,'MarkerEdgeColor','b','MarkerFaceColor','w')



m = 20010;
W = zeros(3,m);
Y = zeros(size(x_1));
Z = zeros(size(x_1));
X = zeros(size(x_1));
rotm = quat2rotm(quat)
rotm = zeros(3,3,m);

 eulerXYZ = zeros(m,3);
for r = 1:(m)
    W(:,r) = rotx(0)*roty(0)*rotz(0)*[ x_1(r); z_1(r); -y_1(r)];
    eulerXYZ(r,:) = rotm2eul(rotm(:,:,r));
end

X_2 = ((W(1,:)))*1000;
Y_2 = (W(2,:))*1000;
Z_2 = ((W(3,:)))*1000;
h1 = scatter3(X_2, Y_2,Z_2,'MarkerEdgeColor','b','MarkerFaceColor','w')
%pose_45_m = [ X_2 ; Z_2 ; -Y_2-73.8];
%save('pose_45_m' , 'pose_45_m');
hold on


load('Robot_Data3_45.mat');
x_1 = ir_positions(1,:)-ir_positions2(1,:);
y_1 = ir_positions(2,:)-ir_positions2(2,:);
z_1 = ir_positions(3,:)-ir_positions2(3,:);
%scatter3(x_1, z_1,-y_1,25,'MarkerEdgeColor','r','MarkerFaceColor','w')
%plot3(x_1, z_1,-y_1)
hold on
m = 14674;
W = zeros(3,m);
Y = zeros(size(x_1));
Z = zeros(size(x_1));
X = zeros(size(x_1));
rotm = zeros(3,3,m);

 eulerXYZ = zeros(m,3);
for r = 1:(m)
%     W(:,r) = rotx(20)*roty(-8)*rotz(49)*[ x_1(r); z_1(r); -y_1(r)  ];
    W(:,r) = rotx(0)*roty(0)*rotz(0)*[ x_1(r); z_1(r); -y_1(r)  ];
    eulerXYZ(r,:) = rotm2eul(rotm(:,:,r));
end

X_2 = ((W(1,:)))*1000;
Y_2 = (W(2,:))*1000;
Z_2 = ((W(3,:)))*1000;
h2 = scatter3(X_2, Y_2,Z_2,'MarkerEdgeColor','k','MarkerFaceColor','w')
hold on

load('Robot_Data_90F.mat');
x_1 = ir_positions(1,:)-ir_positions2(1,:);
y_1 = ir_positions(2,:)-ir_positions2(2,:);
z_1 = ir_positions(3,:)-ir_positions2(3,:);
%scatter3(x_1, z_1,-y_1,25,'MarkerEdgeColor','r','MarkerFaceColor','w')
%plot3(x_1, z_1,-y_1)
hold on
m = 17342;
W = zeros(3,m);
Y = zeros(size(x_1));
Z = zeros(size(x_1));
X = zeros(size(x_1));
rotm = zeros(3,3,m);

 eulerXYZ = zeros(m,3);
for r = 1:(m)
    %W(:,r) = rotx(20)*roty(0)*rotz(49)*[ x_1(r); z_1(r); -y_1(r)  ];
    W(:,r) = rotx(0)*roty(0)*rotz(0)*[ x_1(r); z_1(r); -y_1(r)  ];

    eulerXYZ(r,:) = rotm2eul(rotm(:,:,r));
end

X_2 = ((W(1,:)))*1000;
Y_2 = (W(2,:))*1000;
Z_2 = ((W(3,:)))*1000;
h3 = scatter3(X_2, Y_2,Z_2, 'MarkerEdgeColor','k','MarkerFaceColor',	'm' )
h4 = scatter3(0, 0,0,750, 'o','MarkerEdgeColor','k','MarkerFaceColor',	'g', 'LineWidth',2 )
ax = gca
ax.LineWidth = 1.5


xlabel('x axis(mm)','fontweight','bold', 'FontSize', 16), ylabel('y axis(mm)','fontweight','bold', 'FontSize', 16), zlabel('z axis(mm)','fontweight','bold', 'FontSize', 16)
% xlim([-50 80]),ylim([-70 70]),zlim([40 100])
h = [h1;h2;h3;h4];
lgd =legend(h, '0  Degree Bending Gastroscope Tube (Blue)','45 Degrees Bending Gastroscope Tube (Black)','90 Degrees Bending Gastroscope Tube (Magenta)', 'Base Marker (Green)', 'Location','northeast') 
lgd.FontSize = 14;

grid on
view(3)