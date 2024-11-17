"""
WVU Interactive Robotics Laboratory

Loopy 

Author: Nathan Adkins
"""
from dynamixel_sdk import * 
from settings import *
import os 

port0 = PortHandler(DEVICE0); port0.openPort(); port0.setBaudRate(BAUDRATE)
port1 = PortHandler(DEVICE1); port1.openPort(); port1.setBaudRate(BAUDRATE)

pack0 = Protocol2PacketHandler()
pack1 = Protocol2PacketHandler()

group0_read = GroupSyncRead(port0, pack0, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
group1_read = GroupSyncRead(port1, pack1, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

group0_write = GroupSyncWrite(port0, pack0, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
group1_write = GroupSyncWrite(port1, pack1, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)

def write_to_all(address: int, length: int , value: int ):
    """
    Writes to all of the  

    Parameters:
        None
    Returns:
        positions - a list of dynamixel positions 
    """

    group0_write.start_address = address
    group1_write.start_address = address

    group0_write.data_length = length
    group1_write.data_length = length

    port0.openPort()
    port1.openPort()


    new_value = int.to_bytes(value, length, 'little')

    for n in range(AGENTS):
        if n < 18:
            group0_write.addParam(n, new_value)
        else:
            group1_write.addParam(n, new_value)

    group0_write.txPacket()
    group1_write.txPacket()    

    group0_write.clearParam()
    group1_write.clearParam()

    port0.closePort()
    port1.closePort()
    print("Finished writing to all")


def write_to_individual(address: int, length: int, values: list):

    # if address == ADDR_GOAL_POSITION:
    #     if not angle_checksum_acceptable(values):
    #         write_to_all(ADDR_TORQUE_CONTROL, LEN_TORQUE_ENABLE, TORQUE_DISABLE) 
    #         write_to_all(ADDR_LED_CONTROL,LEN_LED_CONTROL, LED_OFF) 
    #         sys.exit("Not writing to dynamixels, proposed goal positions invalid")

    group0_write.start_address = address
    group1_write.start_address = address

    group0_write.data_length = length
    group1_write.data_length = length

    port0.openPort()
    port1.openPort()

    new_values: list[bytes] = [] 

    for value in values:
        new_values.append(int.to_bytes(value, length, 'little'))

    for n in range(AGENTS):
        if n < 18:
            group0_write.addParam(n, new_values[n])
        else:
            group1_write.addParam(n, new_values[n])

    group0_write.txPacket()
    group1_write.txPacket()    

    group0_write.clearParam()
    group1_write.clearParam()

    port0.closePort()
    port1.closePort()
    print("Finished writing to individual")


def read_from_all(address, length):
    """
    Collects the current positions of the dynamixels 

    Parameters:
        None
    Returns:
        positions - a list of dynamixel positions 
    """

    group0_write.start_address = address
    group1_write.start_address = address

    group0_write.data_length = length
    group1_write.data_length = length

    port0.openPort()
    port1.openPort()

    for n in range(AGENTS):
        if n < 18:
            group0_read.removeParam(n)
            group0_read.addParam(n)
        else:
            group1_read.removeParam(n)
            group1_read.addParam(n)

    group0_read.txRxPacket()
    group1_read.txRxPacket()

    positions = []
    for n in range(AGENTS):
        if n < 18:
            positions.append( group0_read.getData(n, address, length) )
        else:
            positions.append( group1_read.getData(n, address, length) )
        
    group0_read.clearParam()
    group1_read.clearParam()

    port0.closePort()
    port1.closePort()

    return positions

def angle_checksum_acceptable(values: list):
    """
    Sets the dynamixels to a proposed shape

    Parameters:
        proposed_shape - a list of positions that the dynamixels will go to 
    Returns:
        None
    """
    # total positions : 0 - 4095 (2^12)
    total_pos = sum(values)

    largest_pos: int = 4095
    pos_per_angle: float = largest_pos / 360
    total_legal_angles: int = ( AGENTS - 2 ) * 180 # degrees 
    total_legal_pos: int = total_legal_angles * pos_per_angle # pos units # for 36 agents - 69615
   

    if ( total_pos >= total_legal_pos + CHECKSUM_TOLERANCE ) or ( total_pos <= total_legal_pos - CHECKSUM_TOLERANCE ):
        return False
    else:
        return True
        
def set_positions(proposed_shape: list):
    """
    Sets the dynamixels to a proposed shape

    Parameters:
        proposed_shape - a list of positions that the dynamixels will go to 
    Returns:
        None
    """

    proposed_shape_param = [] 
    for pos in proposed_shape:
        proposed_shape_param.append( [DXL_LOBYTE(DXL_LOWORD(pos)), DXL_HIBYTE(DXL_LOWORD(pos)), DXL_LOBYTE(DXL_HIWORD(pos)), DXL_HIBYTE(DXL_HIWORD(pos))] )

    for n in range(AGENTS):
        if n < 18:
            group0_write.removeParam(n)
            group0_write.addParam(n, (proposed_shape_param[n]))
        else:
            group1_write.removeParam(n)
            group1_write.addParam(n, (proposed_shape_param[n]))

    group0_write.txPacket()
    group1_write.txPacket()
    print("Setting positions to" + str(proposed_shape))
    group0_write.clearParam()
    group1_write.clearParam()


def create_shape_list_param(shape_name):
    """
    Loads a shape from a csv file and returns a list of position parameters for that shape 

    Parameters:
        saved_shape - shape saved in a csv file that will be loaded
    Returns:
        None
    """
    returned_shape = [] 
    # print("Loading shape: Loopy_" + str(shape_name) + ".csv" )
    loaded_shape = open( SHAPE_LIST_PATH + str(shape_name) + ".csv", "r")
   
    for id in range(AGENTS):
        current_line = loaded_shape.readline().split(",")
        position = int(current_line[1])
        param_position = [DXL_LOBYTE(DXL_LOWORD(position)), DXL_HIBYTE(DXL_LOWORD(position)), DXL_LOBYTE(DXL_HIWORD(position)), DXL_HIBYTE(DXL_HIWORD(position))]
        returned_shape.append( param_position )

    loaded_shape.close()
    # print("Loaded shape: Loopy_" + str(shape_name) + ".csv" )
    return returned_shape


def create_shape_list(shape_name):
    """
    Loads a shape from a csv file and returns a list of position parameters for that shape 

    Parameters:
        saved_shape - shape saved in a csv file that will be loaded
    Returns:
        None
    """
    returned_shape = [] 
    # print("Loading shape: Loopy_" + str(shape_name) + ".csv" )
    loaded_shape = open( SHAPE_LIST_PATH + str(shape_name) + ".csv", "r")
   
    for id in range(AGENTS):
        current_line = loaded_shape.readline().split(",")
        position = int(current_line[1])
        returned_shape.append(position)

    loaded_shape.close()
    # print("Loaded shape: Loopy_" + str(shape_name) + ".csv" )
    return returned_shape


def save_current_shape(shape_name):
    """
    Stores the current shape of Loopy in a csv file   

    Parameters:
        shape_name - the name of the shape you are trying to store 
    Returns:
        None
    """
    print("Creating shape: Loopy_" + str(shape_name) + ".csv" )
    new_file = open( SHAPE_LIST_PATH + str(shape_name) + ".csv", "w")
    shape = read_from_all(ADDR_PRESENT_POSITION,LEN_PRESENT_POSITION)

    for n in range(AGENTS):
        new_file.write( "agent" + str(n) + "," + str(shape[n]) + "\n")

    new_file.close()
    print("Created shape: Loopy_" + str(shape_name) + ".csv")


def mass_shape_saving():
    """
    Allows for a user to create new shapes saved in the "Loopy_Shapes" folder

    Parameters:
        None
    Returns:
        None
    """
    while True:
        write_to_all(ADDR_TORQUE_CONTROL,LEN_TORQUE_ENABLE,TORQUE_DISABLE)
        letter = input("What character would you like to save? \n")
        save_current_shape( letter )


def shape_list_creation():
    shape_list = []
    for shape_file in os.listdir("loopy_shapes"):

        loaded_shape = open(shape_file)
        print(shape_file)
        loaded_shape = shape_file
        new_shape = []

        for agent in range(AGENTS):
            current_line = loaded_shape.readline().split(",")
            position = int(current_line[1])
            new_shape.append(position)

        shape_list.append(new_shape)

    return shape_list
