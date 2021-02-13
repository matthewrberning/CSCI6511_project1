#imports
import re
import heapq

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position #the VertexID

        self.g = 0 #distance from current vertex to start
        self.h = 0 #distance from current vertex to goal -based upon heuristic
        self.f = 0 #effective cost of current vertex 

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path 


def get_adj_verts(current_vert, vertex_adj_dict):
    
    #create a simple list of the verticies to search through
    simp_list_adj_verts = []
    for vert in vertex_adj_dict[current_vert]:
        simp_list_adj_verts.append(vert[0])
        
    return vertex_adj_dict[current_vert], simp_list_adj_verts


def a_star(vertex_adj_dict, vertID_squareLoc_dict, dest, source):
    
    #create source node
    source_node = Node(None, int(source))
    source_node.g = source_node.h = source_node.f = 0
    
    #create dest node
    dest_node = Node(None, int(dest))
    dest_node.g = dest_node.h = dest_node.f = 0
    
    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and add the source to heap
    heapq.heapify(open_list) 
    heapq.heappush(open_list, source_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = 100000

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1
        print("\nWhile Loop Iters: ", outer_iterations, "\n")

        if outer_iterations > max_iterations:
            print("TOO MANY ITERATIONS?!!??")
            return return_path(current_vert)
        
        current_vert = heapq.heappop(open_list)
        closed_list.append(current_vert)
        
        #check if we made it to the destination
        if current_vert == dest_node:
            return return_path(current_vert)
        print("current_vert: ",current_vert)
        
        
        #collect children of the current vertex from data structures        
        current_verts_children, current_verts_children_simp_list = get_adj_verts(str(current_vert.position), vertex_adj_dict)
    
        children = []
        for child in current_verts_children:
#             print(child)
            
            #the parent and the vertexID start the node
            new_child = Node(current_vert, int(child[0]))
            
            #calculate g by using the exact distance from data_struct
            new_child.g = current_vert.g + int(child[1])
            
            #calculate h by finding the euclidian distance, knowing which square in the 10x10
            #the current node and the dest nodes are
            new_child.h = (int(vertID_squareLoc_dict[child[0]])**2) + (int(vertID_squareLoc_dict[dest])**2)
        
            children.append(new_child)
            
        
        #cacluate the g, h, and f values for each child and place on heap
        for child in children:
#             print(child)
            
            #check if the child has already been explored
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue
            
            #calculate f by summing g: distance traveled and h: expected distance yet to travel
            child.f = child.g + child.h
            
            print(child)
            #add those nodes to the heap -> then keep going in while loop
            heapq.heappush(open_list, child)
                
        
    #error out
    print("didn't work :(")
    return None


def main():

	#strip and ingest text file
	file = open('p1_graph.txt', 'r')
	Lines = file.readlines()

	for line in Lines:
	    if "Vertices" in line:
	        vert_start = Lines.index(line)
	        
	    if "Edges" in line:
	        edge_start = Lines.index(line)
	        vert_end = Lines.index(line) -1
	    if "Source" in line:
	        edge_end = Lines.index(line) -1
	        source = Lines[(Lines.index(line) +1)].strip().split(',')[1]
	        dest = Lines[(Lines.index(line) +2)].strip().split(',')[1]
	        
	verts = Lines[vert_start:vert_end]
	edges = Lines[edge_start:edge_end]


	#parse out the information for the locations of each vertex 
	#within the larger 10x10 square
	vertID_squareLoc_dict = {}

	for elem in verts:
	    if not re.search('[a-zA-Z]', elem):
	        #remove newline charecter
	        elem = elem.strip()
	        elem_split = elem.split(',')
	        
	        #assign each vertexID as the key, and it's location value in the 10x10
	        vertID_squareLoc_dict[elem_split[0]] = elem_split[1]

	#create an adjacency dictionary of dictionaries for each vertex
	vertex_adj_dict = {}

	#temporary list to strip out elements to be added to dict
	temp_list = []
	for elem in edges:
	    if not re.search('[a-zA-Z]', elem):
	        #remove newline charecter
	        elem = elem.strip()
	        elem_split = elem.split(',')
	        temp_list.append(elem_split)

	#for each entry in the list, find all the ones for a sin
	#vertex and add them to a single key, and each value is a list
	#of tuples, with the vertex and the distance to it
	for item in temp_list:
	    current_vertex = item[0]
	    vertex_adj_dict[current_vertex] = []
	    for i in temp_list:
	        if i[0] == current_vertex:
	            vertex_adj_dict[current_vertex].append((i[1],i[2]))

	a_star(vertex_adj_dict, vertID_squareLoc_dict, dest, source)

if __name__ == '__main__':
    main()