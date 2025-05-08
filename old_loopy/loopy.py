"""
WVU Interactive Robotics Laboratory

Loopy 
 
Author: Nathan Adkins
"""
from interfacing import *
from time import sleep

P_GAIN = 5
I_GAIN = 5
D_GAIN = 0

def main():
    try:                    
        print("\n---PID Gain Setting---")
        write_to_all(ADDR_POSITION_D_GAIN,LEN_POSITION_PID_GAIN, P_GAIN)
        write_to_all(ADDR_POSITION_I_GAIN,LEN_POSITION_PID_GAIN, I_GAIN)
        write_to_all(ADDR_POSITION_P_GAIN,LEN_POSITION_PID_GAIN, D_GAIN)
        print("---PID Gain Setting---\n")

        print("---Enabling Torque and LED---")
        write_to_all(ADDR_TORQUE_CONTROL,LEN_TORQUE_ENABLE, TORQUE_ENABLE)
        write_to_all(ADDR_LED_CONTROL,LEN_LED_CONTROL, LED_ON)
        print("---Enabling Torque and LED---\n")

        while True:

            curr_pos = read_from_all(ADDR_GOAL_POSITION,LEN_PRESENT_POSITION)
            print(curr_pos)
            crazy_loopy("Circle","C",1,10)

    except KeyboardInterrupt:
        write_to_all(ADDR_TORQUE_CONTROL, LEN_TORQUE_ENABLE, TORQUE_DISABLE) 
        write_to_all(ADDR_LED_CONTROL,LEN_LED_CONTROL, LED_OFF) 


def crazy_loopy(shape1,shape2,time_delay,iterations):

    shape1_list = create_shape_list(shape1)
    shape2_list = create_shape_list(shape2)

    for n in range(iterations): 
        write_to_individual(ADDR_GOAL_POSITION,LEN_GOAL_POSITION, shape1_list)
        sleep(time_delay)
        write_to_individual(ADDR_GOAL_POSITION,LEN_GOAL_POSITION, shape2_list)
        sleep(time_delay)

if __name__ == "__main__":
    main()

 