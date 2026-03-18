
% CAEA Assignment 1
%
% Matthew Smith 22173112
% Rourke Poirer
% Steve Millar
% Jackson Long
%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Setup Routine
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Read External Data File
array = readmatrix('data_structure.xlsx');
data = array;

% Assign variables from file (HARDCODED data positions)
n_element =     data(1,1);
n_nodes =       data(1,2);
E =             data(1,8);
A =             data(1,9);
ncon =          [data(:,3),data(:,4),data(:,5)];
X =             data(:,6);
Y =             data(:,7);
NDU =           data(1,11);
dzero =         data(:,12);
F =             data(:,10);
v =             data(1,13);
t =             data(1,14);

% Initialise Matrices
KE = zeros(6);
K = zeros(2*n_nodes);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Main Processing
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%% ASSEMBLY %%%%%
% For Each Element in data_structure
for i = 1:n_element
    
    % Call Pre_processing function
    [KE] = pre_processing(i, ncon, X, Y, E, A, t, v);
    
    % Assemble Overall Stiffness Matrix (HARDCODED Assingmnet)
    n1 = ncon(i,1);
    n2 = ncon(i,2);
    n3 = ncon(i,3);

    % Assign 6DOF
    ROC(1) = (2*n1)-1;
    ROC(2) = (2*n1);
    ROC(3) = (2*n2)-1;
    ROC(4) = (2*n2);
    ROC(5) = (2*n3)-1;
    ROC(6) = (2*n3);
    
    % 2D Iteration to construct overall Stiffness Matrix, K
    for IX = 1:6
        MI = ROC(IX);

        for JX = 1:6
            MJ = ROC(JX);
            K(MI, MJ) = K(MI, MJ) + KE(IX, JX);
        end
    end
end

%%%%% PROCESSING %%%%%

KM = K; % Copy stiffness matrix to new variable

% Call post_processing function
[U, Sx, Sy, Sxy] = post_processing(n_element, KM, NDU, dzero, F, ncon, X, Y, E, A, v);

%%%%% OUTPUT %%%%%

% Write outputs to Excel files
writematrix(U,   'displacement.xlsx')
writematrix(Sx,  'stress_x.xlsx'    )
writematrix(Sy,  'stress_y.xlsx'    )
writematrix(Sxy, 'stress_xy.xlsx'   )

% Call Display function
% display_structure(n_element, ncon, X, Y, U);

%%%%% FUNCTION DEFINITIONS %%%%%

function [KE] = pre_processing(i, ncon, X, Y, E, A, t, v)

    % Calcluate [B] (Strain-Displacement) & [D] (Strain-Stress) Matrices
    [B, D, A] = calulate_B_D_matrix(i, ncon, X, Y, E, v);

    % Calculate KE (Elemental Stiffness Matrix):
    % t = element thickness
    % A = Area of Element
    % B = Strain-Displacement Matrix
    % D = Strain-Stress Matrix
    KE = t*A*(B.')*D*B;

end

function [U, Sx, Sy, Sxy] = post_processing(n_element, KM, NDU, dzero, F, ncon, X, Y, E, A, v)
    
    for k = 1:NDU
        n = dzero(k);
        KM(n,:) = 0;
    end

    for k = 1:NDU
        n = dzero(k);
        KM(:,n) = 0;
    end

    for k = 1:NDU
        n = dzero(k);
        KM(n,n) = KM(n,n) + 1;
    end

    U = inv(KM) * F;

    % Return empty for now TODO: Implement Sx, Sy, Sxy (Sigma)
    Sx = zeros(n_element,1);
    Sy = zeros(n_element,1);
    Sxy = zeros(n_element,1);

end

% Calcluate [B] (Strain-Displacement), [D] (Strain-Stress) Matrices, 
% & [A] Area of Triangular Element
% i = iterator
% ncon = nodal connectivity matrix
% X = x-coord
% Y = y-coord
% E = Young's Modulus (Of the material)
% A = Area of Element
% v = Poisson's Ratio (lateral deformation coupling)
function[B, D, A] = calulate_B_D_matrix(i, ncon, X, Y, E, v)

    n1 = ncon(i,1);
    n2 = ncon(i,2);
    n3 = ncon(i,3);
    
    x1 = X(n1);
    x2 = X(n2);
    x3 = X(n3);

    y1 = Y(n1);
    y2 = Y(n2);
    y3 = Y(n3);

    b1 = (y2-y3);
    b2 = (y3-y1);
    b3 = (y1-y2);

    c1 = (x3-x2);
    c2 = (x1-x3);
    c3 = (x2-x1);
    
    % Calculate Area of Triangular Element
    A = 0.5 * det([1 x1 y1; 1 x2 y2; 1 x3 y3]);

    % Construct B Matrix
    B = (1/(2*A))*[

        b1 0 b2 0 b3 0
        0 c1 0 c2 0 c3
        c1 b1 c2 b2 c3 b3

        ];
    
    % Construct D Matrix
    D = (E/(1-v^2))*[

        1 v 0
        v 1 0
        0 0 (1-v)/2

        ];
end
