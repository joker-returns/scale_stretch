function Demo(Ratio1, Ratio2)
% ==== (SNS matlab code)======
% The Code (Version 1) is created by ZHANG Yabin,
% Nanyang Technological University, 2015-12-30
% which is based on the method described in the following paper 
% [1] Wang, Yu-Shuen, et al. "Optimized scale-and-stretch for image resizing." 
% ACM Transactions on Graphics (TOG) 27.5 (2008): 118. 
% The binary code is provided on the project page:
% http://graphics.csie.ncku.edu.tw/Image_Resizing/
% The Matlab codes are for non-comercial use only.
% Note that the importance maps are slightly different from the original
% ones, and the retargeted images are influenced.

%clear all; clc
p = pwd;
%path = strcat(pwd, '/../images/importance_maps/imp.jpg')
im =  imread('../images/graph/in.jpg');
im_SNS = imread('/home/han/Desktop/temp/SNS_matlab-master/tajmahal_0.50_sns.png');

% im =  imread('Brasserie_L_Aficion.png');
% im_SNS = imread('Brasserie_L_Aficion_0.50_sns.png');

% parameters
%Ratio1 = 1;
%Ratio2 = 0.7;
mesh_size = 20; % using mesh_size x mesh_size quad
[h, w, ~] = size(im);
quad_num_h = floor(h/mesh_size);
quad_num_w = floor(w/mesh_size);

% the regular mesh on original image
Vertex_set_org = ImgRegualrMeshGrid(im, mesh_size);

% the importance map generation
%importance_map =  SNS_importanceMap(im, true); % generate the importance map

importance_map = SNS_importanceMap(im, true);
importance_quad = SNS_importanceMap_quad(importance_map, Vertex_set_org);
importance_quad = importance_quad/sum(importance_quad(:)); % the importance weight for the quad


% the naive initialization of the mesh
% retargeting on the width
Vertex_warped_initial = Vertex_set_org;
Vertex_warped_initial(:,:,2) = Vertex_warped_initial(:,:,2)*Ratio2;

Vertex_warped_initial(:,:,1) = Vertex_warped_initial(:,:,1)*Ratio1;

% the mesh grid optimization
[Vertex_updated] = ...
    SNS_optimization(Vertex_set_org ,Vertex_warped_initial, importance_quad);

% warp the new image
im_warped = MeshBasedImageWarp(im, [Ratio1 Ratio2], Vertex_set_org, Vertex_updated);
imwrite(im_warped,'../images/graph/out.jpg')
%figure; subplot(1,2,1); imshow(im_warped); title(['My warped'], 'FontSize' , 15); 
%subplot(1,2,2); imshow(im_SNS); title(['Original SNS warped'], 'FontSize' , 15); 

% show the mesh grid on the original image and retargeted image
% MeshGridImgPlot(im, Vertex_set_org, [0.5 0.0 0.5]);
% title(['Regular mesh grid on original image'], 'FontSize' , 15);
% MeshGridImgPlot(im_warped, Vertex_updated, [0.5 0.0 0.5]);
% title(['Warped image '], 'FontSize' , 15); 




