import sys
import math
import json

from collections import deque

# Import a library of functions called 'pygame'
import pygame
size = 40;
step = math.floor(size/10);
key_size_x = 3
key_size_y = 3

# Define some colors
BLACK = (0, 0, 0)
GREY = (200,200,200)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
RED = (255, 0, 0)
BROWN = (160,82,45)
YELLOW = (225,225,25)

# Define EVENTS
LEFT = 1
RIGHT = 3


# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def offSet(a):
    return a + math.ceil((size+1)/2);

def drawRoad(screen,x,y,xP,yP):
    pygame.draw.line(screen, BLACK,
     [x, y], [xP, yP], 1)
    #pygame.draw.circle(screen, BLACK, (offSet(xP) , yP),
    #math.ceil(size/8), 0)
    return;

def clean(new_size, map):
# CLEAN the file
    queue = deque([])
    last = -1 #largest value Used after cleAN UP

    for k in range(new_size + 1):
        value_exists = False

        #Check if node index is being used
        for node in map["nodes"]:
            if node["index"] == str(k) or node["index"] == k:
                value_exists = True
                break

        #Append to the list of values not ues if it does not exist
        if not value_exists:
            queue.append(k)

        #Once you find one that exists after one that doesnt
        if value_exists and queue:
            #REPLACE it with the smallest number in queue
            queue.append(k) #Append what will be replaced
            replacement = queue.popleft()
            last = replacement
            for node in map["nodes"]:
                for edge in node["edges"]:
                    if edge == str(k) or edge == k:
                        node["edges"].remove(edge)
                        node["edges"].append(str(replacement))
                        break

                if node["index"] == str(k) or node["index"] == k:
                    node["index"] = str(replacement)

        elif value_exists:
            last = k

    map["len"] = str(last + 1)

    return last + 1

def addSteps(map):
    for node in map["nodes"]:
        node["x-steps"] = "0"
        node["y-steps"] = "0"

def main():

    #Check Arguments
    space_type = "B"
    touched = None

    draw_mode = False
    edit_mode = False

    if len(sys.argv)==2:
        file = open(sys.argv[1])
        map = json.loads(file.read())
        file.close()


        if map["edit"] == "true":
            draw_mode = True
            edit_mode = True

        print ("NAME : " + map["name"]);

    else:
        draw_mode = True
        map = { "name" : "prototype",
                "edit" : "true",
                "start" : "",
                "width" : "12",
                "height" : "10",
                "len" : "0",
                "nodes" : []
                }
        #map["nodes"].append({"index":"0", "x":"17", "y":"14","type":"B", "edges":[] "\n"})

    # Initialize the game engine
    SIZE = int(map["len"])
    start = False if map["start"] == "" else True
        #map width and height
    width = int(map["width"]);
    height = int(map["height"]);
        #display width and height
    if not draw_mode:
        WIDTH = size*(width + 2)
        HEIGHT = size*(height + 2)
    else:
        WIDTH = size*(width + 2 + (key_size_x + 1))
        HEIGHT = size*(height + 2) if height > key_size_y else size*(key_size_y + 2)

    dimensions = (WIDTH, HEIGHT);
    screen = pygame.display.set_mode(dimensions);
    pygame.display.set_caption(map["name"] + "'s Board Graph");

    pygame.font.init() # you have to call this at the start,
    myfont = pygame.font.SysFont('Comic Sans MS', math.ceil(2*size/3))

    pygame.init()



    # -------- Main Program Loop -----------
        #bottom and right most part of the main map
    bottom = size*(height + 2)
    right = size*(width + 2)
    done = False;
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN and touched != None:
                xSteps = int(map["nodes"][touched]["x-steps"])
                ySteps = int(map["nodes"][touched]["y-steps"])

                if event.key == pygame.K_LEFT:
                    xSteps = xSteps - 1 if xSteps != -5 else -5
                elif event.key == pygame.K_RIGHT:
                    xSteps = xSteps + 1 if xSteps != 5 else 5
                elif event.key == pygame.K_UP:
                    ySteps = ySteps - 1 if ySteps != -5 else -5
                elif event.key == pygame.K_DOWN:
                    ySteps = ySteps + 1 if ySteps!= 5 else 5

                map["nodes"][touched]["x-steps"] = str(xSteps)
                map["nodes"][touched]["y-steps"] = str(ySteps)

            # DRAW
            # ---NEW SPACES
            elif event.type == pygame.MOUSEBUTTONDOWN and draw_mode:
                x,y = event.pos
                x = math.floor(x/size) - 1
                y = math.floor(y/size) - 1
                exists = False

                #CHANGE DRAW ICON
                if y == 0:
                    if x == width + 1:
                        space_type = "B"
                    if x == width  + 2:
                        space_type = "G"
                    if x == width  + 3:
                        space_type = "R"


                if x < width and y < height:
                    l = 0 #index of current node being looked at
                    for node in map["nodes"]:
                        if node["x"]==x and node["y"]==y:
                            exists = True

                            #--- DRAW NEW EDGES
                            if touched == None:
                                touched = l

                            else:
                                edge_exists = False

                                for edge in map["nodes"][touched]["edges"]:
                                    if edge == str(l):
                                        edge_exists = True
                                        break

                                if not edge_exists and l != touched:
                                    map["nodes"][touched]["edges"].append(str(l))

                                if edge_exists:
                                    map["nodes"][touched]["edges"].remove(str(l))

                                touched = None

                            break

                        l += 1

                    if not exists:
                        touched = None

                    if not exists and event.button == LEFT:
                        map["nodes"].append({"index": str(SIZE), "x":x, "y":y,
                        "x-steps": "0","y-steps": "0", "type":space_type, "edges":[]})
                        SIZE += 1
                        print ("Added node at (%d, %d)" % (x,y))

                    if exists and event.button == RIGHT:

                        #DELETE EDGES OF NODE
                        node_index = map["nodes"][l]["index"]
                        for node in map["nodes"]:
                            for edge in node["edges"]:
                                if edge == node_index:
                                    node["edges"].remove(edge)
                                    break;

                        #delete node
                        map["nodes"].pop(l)
                        touched = None

                        print ("Deleted node at (%d, %d)" % (x,y))

        # --- Game logic should go here
        SIZE = clean(SIZE, map)

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(WHITE)

        # --- Drawing code should go here
            # VERTICAL LINES = 1 more than boxes
        for x in range(width + 1):
            pos = (x+1)*size
            pygame.draw.line(screen, GREY , [pos, size], [pos,bottom - size], 1)
            #X-Coordinates
            if x != width:
                txt = myfont.render(str(x), False, BLACK);
                screen.blit(txt,(pos + math.ceil(size/4),math.ceil(size/2)))

            # HORIZONTAL LINES = 1 more than boxes
        for y in range(height + 1):
            pos = (y+1)*size
            pygame.draw.line(screen, GREY , [size, pos], [right - size,pos], 1)
            #Y-Coordinates
            if y != height:
                txt = myfont.render(str(y), False, BLACK);
                screen.blit(txt,(math.ceil(size/3), pos + math.ceil(size/4)))

            #DRAW EDGES FIRST - FIND NODES in Graph
        for node in map["nodes"]:
            x = int(node["x"]) + 1;
            y = int(node["y"]) + 1;
            xOff = int(node["x-steps"])*step
            yOff = int(node["y-steps"])*step

            #START edge
            if node["index"] == "0" and start == True :
                drawRoad(screen,offSet(x*size) + xOff,offSet(y*size) + yOff,
                    offSet(size*(width)),offSet(size*(height)));

            #EDGES in NODE
            for edge in node["edges"]:
                if int(edge) >= len(map["nodes"]):
                    print (edge)
                    print (node["index"])

                nodeP = map["nodes"][int(edge)];
                xP = int(nodeP["x"]) + 1;
                yP = int(nodeP["y"]) + 1;
                xPOff = int(nodeP["x-steps"])*step
                yPOff = int(nodeP["y-steps"])*step


                drawRoad(screen,offSet(x*size)+xOff,offSet(y*size)+yOff,
                    offSet(xP*size)+xPOff,offSet(yP*size)+yPOff);

            #DRAW NODES NOW
            l = 0
        for node in map["nodes"]:
            x = int(node["x"]) + 1;
            y = int(node["y"]) + 1;
            xOff = int(node["x-steps"])*step
            yOff = int(node["y-steps"])*step
            COLOR = RED;

            if(node["type"] == "B"):
                COLOR = BLUE;
            elif(node["type"] == "G"):
                COLOR = GREEN;

            pygame.draw.circle(screen, COLOR, (offSet(size*x)+xOff, offSet(size*y)+yOff),
            math.ceil(size/3), 0);

            if touched == l:
                pygame.draw.circle(screen, YELLOW, (offSet(size*x)+xOff, offSet(size*y)+yOff),
                math.ceil(size/3) + math.ceil(size/15), math.ceil(size/15));

            l += 1

            #DRAW OBJECTS
            #---START
        if map["start"] == "BL" :
            pygame.draw.rect(screen,BROWN,
            (offSet(size*(width - 1)), offSet(size*(height - 1)),size*2,size*2))


            #---DRAW KEY
        if draw_mode:
            screen.blit(myfont.render("KEY", False, BLACK),
            (size*math.floor(key_size_x/2) + right, math.ceil(size/2)))

            key_bottom = (key_size_y + 1)*size
            for x in range(key_size_x + 1):
                pos = (x)*size + right
                pygame.draw.line(screen, GREY , [pos, size], [pos,key_bottom], 1)

            key_right = (key_size_x)*size + right
            for y in range(key_size_y + 1):
                pos = (y+1)*size
                pygame.draw.line(screen, GREY , [right, pos], [key_right,pos], 1)

            #KEY SPACES
            #---BLUE SPACE
            pygame.draw.circle(screen, BLUE, (offSet(right), offSet(size)),
            math.ceil(size/3), 0);
            if space_type == "B":
                pygame.draw.circle(screen, YELLOW, (offSet(right), offSet(size)),
                math.ceil(size/3) + math.ceil(size/15), math.ceil(size/15));

            #---GREEN SPACE
            pygame.draw.circle(screen, GREEN, (offSet(right + size), offSet(size)),
            math.ceil(size/3), 0);
            if space_type == "G":
                pygame.draw.circle(screen, YELLOW, (offSet(right + size), offSet(size)),
                math.ceil(size/3) + math.ceil(size/15), math.ceil(size/15));

            #---RED SPACE
            pygame.draw.circle(screen, RED, (offSet(right + 2*size), offSet(size)),
            math.ceil(size/3), 0);
            if space_type == "R":
                pygame.draw.circle(screen, YELLOW, (offSet(right + 2*size), offSet(size)),
                math.ceil(size/3) + math.ceil(size/15), math.ceil(size/15));

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()

    # Create New JSON if draw_mode on
    clean(SIZE, map)
    #addSteps(map)

    JSON = 'prototype.json' if not edit_mode else sys.argv[1]

    if draw_mode:
        with open(JSON, 'w') as fp:
            json.dump(map, fp, indent=2)


    #FINISHED INFO
    print("\n FINISHED! \n");


if __name__ == "__main__":
    main()
