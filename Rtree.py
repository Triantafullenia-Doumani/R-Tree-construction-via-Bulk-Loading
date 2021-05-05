#TRIANTAFYLLIW DOUMANI 4052
import sys

_DIVISORS = [180.0 / 2 ** n for n in range(32)]
MAX_CAPACITY = 20
MIN_CAPACITY = 8

def main(argv):

    global coords
    global offsets
    global output


    coords = open(sys.argv[1], "r")
    offsets = open(sys.argv[2], "r")
    output = open("Rtree.txt" , "w")

    read_offsets()
    balance()
    write_to_output_file()

    coords.close()
    offsets.close()
    output.close()

def read_offsets():

    offsets_line = offsets.readline().replace('\n',',').split(",")

    MBR_list = []
    unsorted_objects = []
    while(len(offsets_line) > 1 ):

        object = []
        id = int(offsets_line[0])
        start = int(offsets_line[1])
        end = int(offsets_line[2])

        read_this_amound_of_lines = (end - start)
        MBR = read_coords_and_return_MBR(read_this_amound_of_lines)
        z = calculate_z(MBR)

        object.append(id)
        object.append(MBR)
        object.append(z)

        unsorted_objects.append(object)

        offsets_line = offsets.readline().replace('\n',',').split(",")

    Rtree(unsorted_objects)

def read_coords_and_return_MBR(read_this_amound_of_lines):

        coords_line = coords.readline().replace('\n',',').split(",")
        x_hight = coords_line[0]
        x_low = coords_line[0]
        y_hight = coords_line[1]
        y_low = coords_line[1]

        if(read_this_amound_of_lines > 1):
            while(read_this_amound_of_lines >  0 ):

                coords_line = coords.readline().replace('\n',',').split(",")
                x = coords_line[0]
                y = coords_line[1]

                if float(x) > float(x_hight):
                    x_hight = x
                if float(x) < float(x_low):
                    x_low = x
                if float(y) > float(y_hight):
                    y_hight = y
                if float(y) < float(y_low):
                    y_low = y

                read_this_amound_of_lines -= 1

            MBR = [ float(x_low) ,float(x_hight) , float(y_low) ,  float(y_hight)]
            return MBR

def Rtree(unsorted_objects):

    global Rtree_list

    node_id = 0
    level = 0
    objects = generate_sorted_objects(unsorted_objects)
    Rtree_list = []
    next = 0
    object_node = []
    while(1):
        object_node = []
        object_nodes = [0 , node_id , []]
        node_id += 1
        for i in range(MAX_CAPACITY):
            object_nodes[2].append(objects[next])
            next += 1
        Rtree_list.append(object_nodes)
        if(next == len(objects)):
            break
    print(str(len(Rtree_list)) +" nodes at level "+ str(level))
    generate_nodes(Rtree_list, node_id , level+1)

def generate_sorted_objects(MBR_list):
    MBR_list.sort(key=lambda x: x[2])
    for i in range(0,len(MBR_list)):
        MBR_list[i].pop(2)
    return MBR_list

def generate_nodes(nodes_list , node_id , level):

    global Rtree_list
    global next_level_nodes

    next_level_nodes =  []
    next = 0
    nodes = []
    while(1):
        node = []
        nodes = [1 , node_id , []]
        node_id+=1

        for i in range(MAX_CAPACITY):
            MBR = list(find_new_MBR(nodes_list[next]))
            next_id_MBR = [nodes_list[next][1] , MBR]
            nodes[2].append(next_id_MBR)
            next += 1
            if(next == (len(nodes_list) )):
                break

        next_level_nodes.append(nodes)

        if(next == (len(nodes_list) )):
            break
    print(str(len(next_level_nodes)) +" nodes at level "+ str(level))

    for x in next_level_nodes:
        Rtree_list.append(x)

    if(len(next_level_nodes) > 1):
        generate_nodes(next_level_nodes, node_id , level+1)


def find_new_MBR(node):

    x_low = float(node[2][1][1][0])
    x_hight  = float(node[2][1][1][1])
    y_hight = float(node[2][1][1][2])
    y_low = float(node[2][1][1][3])

    for i in range(len(node[2])):

        x = float(node[2][i][1][0])
        if x < x_low:
            x_low = x

        x = float(node[2][i][1][1])
        if x > x_hight:
            x_hight = x

        y = float(node[2][i][1][2])
        if y < y_low:
            y_low = y

        y = float(node[2][i][1][3])
        if y > y_hight:
            y_hight = y

    new_MBR = [x_low , x_hight , y_low , y_hight]
    return new_MBR


def calculate_z(MBR):

    x = (float(MBR[0]) + float(MBR[1])) / 2
    y = (float(MBR[2]) + float(MBR[3])) / 2

    return floaterleave_latlng(y,x)

def floaterleave_latlng(lat, lng):
    if not isinstance(lat, float) or not isinstance(lng, float):
        prfloat('Usage: floaterleave_latlng(float, float)')
        raise ValueError("Supplied arguments must be of type float!")

    if (lng > 180):
        x = (lng % 180) + 180.0
    elif (lng < -180):
        x = (-((-lng) % 180)) + 180.0
    else:
        x = lng + 180.0
    if (lat > 90):
        y = (lat % 90) + 90.0
    elif (lat < -90):
        y = (-((-lat) % 90)) + 90.0
    else:
        y = lat + 90.0

    morton_code = ""
    for dx in _DIVISORS:
        digit = 0
        if (y >= dx):
            digit |= 2
            y -= dx
        if (x >= dx):
            digit |= 1
            x -= dx
        morton_code += str(digit)

    return morton_code

def balance():
    global Rtree_list

    lenght = len(Rtree_list) - 1
    #for root balance
    if(len(Rtree_list[lenght][2]) < 2):
        MBR_of_prev_node = Rtree_list[lenght - 1][2].pop()
        Rtree_list[lenght][2].insert(0,MBR_of_prev_node)

    #for nodes balance
    for x in range(lenght - 1, -1  ,-1):
        while(len(Rtree_list[x][2]) < 8):
            MBR_of_prev_node = Rtree_list[x - 1][2].pop()
            Rtree_list[x][2].insert(0,MBR_of_prev_node)

def write_to_output_file():

    for x in range(0,len(Rtree_list)):
        output.write(str(Rtree_list[x])+ "\n")

if __name__ == "__main__":
    main(sys.argv)
