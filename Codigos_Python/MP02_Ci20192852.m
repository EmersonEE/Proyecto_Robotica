function C = MP201902852(T)
    px = T(1,4);
    py = T(2,4);
    pz = T(3,4);

    d1 = pz;

    theta2 = atan2(py, px);

    theta3_1 = 0;
    theta3_2 = pi;

    R = T(1:3,1:3);

    theta5 = atan2(sqrt(R(3,1)^2 + R(3,2)^2), R(3,3));

    if sin(theta5) ~= 0
        theta4 = atan2(R(2,3), R(1,3));
        theta6 = atan2(R(3,2), -R(3,1));
    else
        theta4 = 0;
        theta6 = atan2(-R(1,2), R(1,1));
    end

    C = [
        d1, theta2, theta3_1, theta4, theta5, theta6;
        d1, theta2, theta3_2, theta4, theta5, theta6
    ];

end
