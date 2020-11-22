from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

opp = {
    's' : 'n',
    'n' : 's',
    'e' : 'w',
    'w' : 'e'
}

rev_list = []

#track visited rooms
visited = set()

#keep moving while there are still more rooms left than visited 
while len(room_graph) - 1 > len(visited) - 1:
    #initialize player_move at 0
    player_move = 0

    #loop over the rooms available
    for direction in player.current_room.get_exits():
        #check if that room in that direction is in visited, if not move to that direction
        if player.current_room.get_room_in_direction(direction) not in visited:
            player_move = direction

    #if you still have a direction to go in, append player_move to traversal_path
    if player_move is not 0:
        traversal_path.append(player_move)

        #append the reverse directions to move back
        rev_list.append(opp[player_move])

        #travel in the direction of the player_move
        player.travel(player_move)

        #track the visited rooms
        visited.add(player.current_room)
    else:
        #if upcoming move is 0, pop rev_list and set it to player_move to reverse directions
        player_move = rev_list.pop()

        #add it to traversal_path
        traversal_path.append(player_move)

        #travel in that direction
        player.travel(player_move)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
