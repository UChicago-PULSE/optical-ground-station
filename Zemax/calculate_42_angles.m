function outTbl = compute_alpha_beta(csvPath, Latitude, Longitude)

%Inputs
%csvPath - path to the 42 data saved in a csv file
%Latitude and Longitude - coordinates for the area of interest (in this
%case UChicago [41.789722, -87.599724]

% Outputs
% outTbl- table with columns: timestamp, alpha_deg, beta_deg

    
    T = readtable(csvPath);

    Re = 6378137;  % meters
    lat = deg2rad(Latitude);
    lon = deg2rad(Longitude);
    g = [Re*cos(lat)*cos(lon); Re*cos(lat)*sin(lon); Re*sin(lat)];

    N = height(T);
    alpha_deg = zeros(N,1);
    beta_deg  = zeros(N,1);

    % rotation matrix
    quat2M = @(q0,q1,q2,q3) ( ...
        [ 1 - 2*norm([q0 q1 q2 q3])*(q2^2 + q3^2),   2*norm([q0 q1 q2 q3])*(q1*q2 - q3*q0),   2*norm([q0 q1 q2 q3])*(q1*q3 + q2*q0);
          2*norm([q0 q1 q2 q3])*(q1*q2 + q3*q0),   1 - 2*norm([q0 q1 q2 q3])*(q1^2 + q3^2),   2*norm([q0 q1 q2 q3])*(q2*q3 - q1*q0);
          2*norm([q0 q1 q2 q3])*(q1*q3 - q2*q0),     2*norm([q0 q1 q2 q3])*(q2*q3 + q1*q0), 1 - 2*norm([q0 q1 q2 q3])*(q1^2 + q2^2) ] );

    % First row of data will set the baseline for plane of incidence
    R0 = [T.pos_x_m(1); T.pos_y_m(1); T.pos_z_m(1)];
    q0 = [T.q0(1), T.q1(1), T.q2(1), T.q3(1)];
    M0 = quat2M(q0(1), q0(2), q0(3), q0(4));
    p0 = M0 * R0;
    r0 = R0 - g;
    n0 = cross(p0, r0);
    alpha_deg(1) = acosd( dot(p0, r0) / (norm(p0)*norm(r0)) );
    beta_deg(1)  = 0;

    % Calculate other rows
    for k = 2:N
        R = [T.pos_x_m(k); T.pos_y_m(k); T.pos_z_m(k)];
        q = [T.q0(k), T.q1(k), T.q2(k), T.q3(k)];
        M = quat2M(q(1), q(2), q(3), q(4));
        p = M * R;
        r = R - g;

        % α = angle between p and r
        alpha_deg(k) = acosd( dot(p, r) / (norm(p)*norm(r)) );

        % β = angle between plane normals n0 and n
        n = cross(p, r);
        beta_deg(k) = acosd( dot(n0, n) / (norm(n0)*norm(n)) );
    end

    outTbl = table(T.timestamp(1:N), alpha_deg(1:N), beta_deg(1:N), ...
        'VariableNames', {'timestamp','alpha_deg','beta_deg'});

   
    disp(outTbl);
end

