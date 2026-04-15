function T = MP02_CD201902852(C)
    d1 = C(1);
    theta2 = C(2);
    theta3 = C(3);
    theta4 = C(4);
    theta5 = C(5);
    theta6 = C(6);

    function A = dh(theta, d, a, alpha)
        A = [cos(theta), -sin(theta)*cos(alpha),  sin(theta)*sin(alpha), a*cos(theta);
             sin(theta),  cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta);
             0,           sin(alpha),             cos(alpha),            d;
             0,           0,                      0,                     1];
    end

    A1 = dh(0, d1, 0, 0);
    A2 = dh(theta2, 1, 2, 0);       
    A3 = dh(theta3, 0, 0, 0);
    A4 = dh(theta4, 0, 0, -pi/2);
    A5 = dh(theta5, 0, 0, pi/2);
    A6 = dh(theta6, 1, 0, 0);

    T = A1 * A2 * A3 * A4 * A5 * A6;

end
