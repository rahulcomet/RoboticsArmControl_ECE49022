import json
import socket
import math as m
from gpiozero import MCP3008
from time import sleep
from adafruit_servokit import ServoKit                                           

def reset(rst_list, kit):
    kit.servo[0].angle = rst_list[0]
    kit.servo[3].angle = rst_list[1]
    kit.servo[4].angle = rst_list[2]
    kit.servo[7].angle = rst_list[3]
    kit.servo[8].angle = rst_list[4]
    kit.servo[11].angle = rst_list[5]

def off(kit):
    kit.servo[0].angle = None
    kit.servo[3].angle = None
    kit.servo[4].angle = None
    kit.servo[7].angle = None
    kit.servo[8].angle = None
    kit.servo[11].angle = None

def test_func_OC(status, rst_angle0, kit): 
    for i in range (100, 190, 10):
        if status == 1 and read_sensor() == 0:
            kit.servo[0].angle = i
            #print(i)
            sleep(0.5)
        elif status == -1:
            kit.servo[0].angle = rst_angle0
            #print(rst_angle0)
            sleep(0.5)
            break
        else:
            break

def test_func_rotate(status, curr_angle, kit, conn):
    try:    
        # while True:
        if status == 1:              # N is placeholder for when nothing is received via ethernet()   
            curr_angle += 10
            kit.servo[3].angle = curr_angle
            #print(curr_angle)
            sleep(0.5)
            dict = read_json(conn)
            status = dict["Rotate"]
        elif status == -1:           # 1 and -1 are strings here since input() stores values as strings
            curr_angle -= 10
            kit.servo[3].angle = curr_angle
            #print(curr_angle)
            sleep(0.5)
            dict = read_json(conn)
            status = dict["Rotate"]
        # else:
            # break
        #print(curr_angle)
        return curr_angle
    except ValueError:
        print("\nAngle value out of range - rotate")
        return curr_angle

def test_func_ext1(status, curr_angle, kit, conn):
    try:
        # while True:
        if status == 1:    
            curr_angle += 5
            kit.servo[4].angle = curr_angle
            #print(curr_angle)
            sleep(0.5)
            dict = read_json(conn)
            status = dict["ZC"]
        elif status == -1: 
            curr_angle -= 5
            kit.servo[4].angle = curr_angle
            #print(curr_angle)
            sleep(0.5)
            dict = read_json(conn)
            status = dict["ZC"]
        # else:
            # break
        #print(curr_angle)
        return curr_angle
    except ValueError:
        print("\nAngle value out of range - ext1")
        return curr_angle

def test_func_ext2(status, curr_angle, ext1_angle, kit, conn):
    try:
        # while True:
        if status == 1:    
            curr_angle += 5
            ext1_angle += 5
            kit.servo[7].angle = curr_angle
            kit.servo[4].angle = ext1_angle
            #print(curr_angle)
            sleep(0.5)
            dict = read_json(conn)
            status = dict["Z"]
        elif status == -1: 
            curr_angle -= 5
            ext1_angle -= 5
            kit.servo[7].angle = curr_angle
            kit.servo[4].angle = ext1_angle
            #print(curr_angle)
            sleep(0.5)
            dict = read_json(conn)
            status = dict["Z"]
        # else:
            # break
        #print(curr_angle)
        return curr_angle
    except ValueError:
        print("\nAngle value out of range - ext2")
        return curr_angle

def test_func_ext3(status, curr_angle, ext2_angle, kit, conn):
    try:
        # while True:
        if status == 1:    
            #print("\n in x")
            curr_angle += 5
            ext2_angle += 5
            kit.servo[8].angle = curr_angle
            kit.servo[7].angle = ext2_angle
            #print(curr_angle)
            sleep(0.5)
            #dict = read_json(conn)
            #status = dict["X"]
        elif status == -1: 
            curr_angle -= 5
            ext2_angle -= 5
            kit.servo[8].angle = curr_angle
            kit.servo[7].angle = ext2_angle
            #print(curr_angle)
            sleep(0.5)
            #dict = read_json(conn)
            #status = dict["X"]
        # else:
            # print("\ngot 0 told to stop - x")
            # break
        #print(curr_angle)
        return curr_angle, ext2_angle
    except ValueError:
        print("\nAngle value out of range - ext3")
        return curr_angle, ext2_angle  
#Note: ext3 needs to update ext2 to keep ext1 on object and ext 2 needs to update ext1 to keep ext1 on object (1:1 for all angle updates)

def test_func_sweep(status, curr_angle, kit, conn):
    v = 1
    try:
        # while True:
        if status == 1:              # N is placeholder for when nothing is received via ethernet()   
            curr_angle += 5
            kit.servo[11].angle = curr_angle
            #print(curr_angle)
            sleep(0.5)
            #dict = read_json(conn)
            #status = dict["Y"]
        elif status == -1:           # 1 and -1 are strings here since input() stores values as strings
            curr_angle -= 5
            kit.servo[11].angle = curr_angle
            #print(curr_angle)
            sleep(0.5)
            #dict = read_json(conn)
            #status = dict["Y"]
        # else:
            # break
        #print(curr_angle)
        return curr_angle
    except ValueError:
        print("\nAngle value out of range - sweep")
        return curr_angle

def json_input(rst_list, kit, conn):
    init_list = rst_list.copy()
    #print("reset list_input: " + str(rst_list))
    while True:
        #print("\nat input func")
        j_dict = read_json(conn)
        #print("\nafter read")
        if j_dict == {}:
            return
        if j_dict["OFF"] == 1:                #keyboard interrupt on server system can send OFF command and then stop all systems
            reset(rst_list, kit)
            break
        if j_dict["Reset"] == 1:
            reset(rst_list, kit)
            #init_list = rst_list
        
        MoveToBin(kit, rst_list, j_dict["Bin"], init_list[4], init_list[3], init_list[2])
        
        test_func_OC(j_dict["OC"], init_list[0], kit)
        init_list[1] = test_func_rotate(j_dict["Rotate"], init_list[1], kit, conn)
        init_list[2] = test_func_ext1(j_dict["ZC"], init_list[2], kit, conn)
        init_list[3] = test_func_ext2(j_dict["Z"], init_list[3], init_list[2], kit, conn)
        init_list[4], init_list[3] = test_func_ext3(j_dict["X"], init_list[4], init_list[3], kit, conn)
        init_list[5] = test_func_sweep(j_dict["Y"], init_list[5], kit, conn)

def read_sensor():
    sensor = MCP3008(0)
    MSB = sensor.raw_value
    if MSB <= 300:
        #print("\nnot enough force")
        #print(MSB)
        return 0
    else:
        #print("\nlimit reached")
        return 1

def read_json(conn):
    sleep(0.5)
    try:       
        #v = '1'
        #print("\nat recv")
        conn.settimeout(10.0)
        data = conn.recv(1024)
        #print(data)
        data1 = data.decode()
        data1 = data1.split('}')
        data1.pop()
        #print(data1)
        data2 = [json.loads(d + '}') for d in data1]
        #print(data2)
        # conn.send(v.encode())
        reset_indices = []
        for i, x in enumerate(data2):
            if x['Reset'] == 1:
                reset_indices.append(i)
        if len(reset_indices) > 0:
            return data2[reset_indices[0]]
        else:
            return data2[-1]
    except socket.timeout:
        print("\nSOCKET TIMEOUT")
        return {}
#Note: use socket.settimeout(time value (in s)) to prevent hanging socket

def z_calc(a1, a2, l1, l2, zb):
    z1 = abs(l1 * m.sin(a1))
    z2 = abs(l2 * m.sin(a2))

    if round(m.degrees(a2)) >= 0:
        z = z1 + z2 + zb
        #print("\n at z_calc (+ve)")
    else:
        #print("\n at z_calc (-ve)")
        z = z1 - z2 + zb 
    return z

def LowerClaw(a1, a2):
    l1 = 4.125
    l2 = 6.5
    l3 = 5.75

    z_ideal = 7
    z_base = 4

    theta1 = a1
    theta2 = a2 - theta1

    print("\na1:" + str(a1))
    print("\na2:" + str(a2))
    
    theta1 = m.radians(theta1)
    theta2 = m.radians(theta2)

    z = z_calc(theta1, theta2, l1, l2, z_base)
    #print (z)
    
    if z > z_ideal:
        delta = m.radians(-1)
    else:
        #print("z less than ideal")
        delta = m.radians(1)

    z_diff = abs(z - z_ideal)
    ztemp1 = z_calc(theta1 + delta, theta2, l1, l2, z_base)
    zt1_diff = abs(ztemp1 - z_ideal)
    ztemp2 = z_calc(theta1, theta2 + delta, l1, l2, z_base)
    zt2_diff = abs(ztemp2 - z_ideal)

    while abs(z - z_ideal) > 0.125 and (z_diff > zt1_diff or z_diff > zt2_diff):
        if z > z_ideal:
            delta = m.radians(-1)
        else:
            #print("z less than ideal")
            delta = m.radians(1)
        
        x1 = l2 * m.cos(theta2) - l1 * m.cos(theta1 + delta)
        x2 = l2 * m.cos(theta2 + delta) - l1 * m.cos(theta1)

        x_init = l2 * m.cos(theta2) - l1 * m.cos(theta1)

        x1_e = abs(x_init) - abs(x1)
        x2_e = abs(x_init) - abs(x2)

        if abs(x1_e) < abs(x2_e):
            theta1 = theta1 + delta
            #print("theta1 :" + str(round(m.degrees(theta1))))
        else:
            theta2 = theta2 + delta
            #print("theta2 :" + str(round(m.degrees(theta2))))

        #print("theta1 :" + str(round(m.degrees(theta1))))
        #print("theta2 :" + str(round(m.degrees(theta2))))

        z = z_calc(theta1, theta2, l1, l2, z_base)
        #print(z)

        z_diff = abs(z - z_ideal)
        ztemp1 = z_calc(theta1 + delta, theta2, l1, l2, z_base)
        zt1_diff = abs(ztemp1 - z_ideal)
        ztemp2 = z_calc(theta1, theta2 + delta, l1, l2, z_base)
        zt2_diff = abs(ztemp2 - z_ideal)
    #while loop ends

    a1f = theta1
    if theta2 >= 0:
        a2f = abs(theta2) + abs(theta1)
    else:
        a2f = abs(theta1) - abs(theta2)
    #print("a1f: " + str(round(abs(m.degrees(a1f)))))
    #print("a2f: " + str(round(abs(m.degrees(a2f) + 10))))
    return round(abs(m.degrees(a1f))), round(abs(m.degrees(a2f))), theta1, theta2

def MoveToBin(kit, rst_list, n, a1, a2, a3):
    #print("reset list_movetobin: " + str(rst_list))
    if n == 0:
        return
    elif n == 1:
        BinAngle = 105
    elif n == 2:
        BinAngle = 145
    else:
        BinAngle = 170
    #lowers claw to optimal height
    print("\n now lowering claw")
    sleep(2)
    A = LowerClaw(a1, a2 + 20)
    #ext3
    kit.servo[7].angle = A[1] - 15 
    #ext2
    kit.servo[8].angle = A[0] 
    #ext1
    kit.servo[4].angle = a3 - abs(a2 - A[1]) - 35
    sleep(2)
    kit.servo[4].angle = None
    sleep(2)

    #closes claw to grab object
    test_func_OC(1, 90, kit)
    sleep(2)

    kit.servo[7].angle = 55
    sleep(2)
    #print("\na3: " + str(a3))
    #print("a2f - a2:" + str(a2 - A[1]))
    #print("\nfinal angles returned (a1f, a2f, ...): " + str(A))
    #moves arm to reset position
    kit.servo[8].angle = 60
    sleep(2)
    #moves object above bin location specified by n
    kit.servo[11].angle = BinAngle
    sleep(2)
    #drop object
    test_func_OC(-1, 90, kit)
    sleep(2)
    #reset after dropping object in specified bin
    reset(rst_list, kit)
    '''while True:
        sleep(5)
        x = 0'''

def main():
    print("\nMain!!!!")
    kit = ServoKit(channels = 16)

    #kit.servo[11].actuation_range = 270
    kit.servo[0].set_pulse_width_range(500, 2500)
    kit.servo[3].set_pulse_width_range(500, 2500)
    kit.servo[4].set_pulse_width_range(500, 2500)
    kit.servo[7].set_pulse_width_range(500, 2500)
    kit.servo[8].set_pulse_width_range(500, 2500)
    kit.servo[11].set_pulse_width_range(500, 2100)
    
    rst_list = [90, 90, 55, 55, 60, 0]

    host = '192.168.137.3'
    port = 9999
    print("\nbefore reset")
    reset(rst_list, kit) 
    
    try:
        print("\n socket")
        sock = socket.socket()
        print("\n at sock")
        sock.bind((host, port))
        print("\n at bind")
        sock.listen()
        print("\n at listen")
        conn, addr = sock.accept()
                
        json_input(rst_list, kit, conn)
        off(kit)
        sock.close()

    except KeyboardInterrupt:
        off(kit)
        sock.close()
    except OSError:
        off(kit)
        sock.close()
    except IndexError:
        off(kit)
        sock.close()
    except json.decoder.JSONDecodeError:
        off(kit)
        sock.close()
    else:
        off(kit)
        sock.close()

if __name__ == '__main__':
    main()