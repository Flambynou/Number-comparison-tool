def get_value(path):
	True_value_change = -4
	return path[-1][0]+path[-1][1] + (len(path)-1)*True_value_change


class Pathfinder:
	def __init__(self, reference_number, input_number):
		self.reference = reference_number
		self.input = input_number
		self.matrix = []
		self.neighbors = {}
		self.dictionary = {}
		self.node_dict = self.create_node_dict()
		self.node_dict = self.find_node_paths_from_dict()
		self.best_node_path = self.get_best_path_from_dict()

	def create_node_dict(self):
		node_dict = {(-1,-1):([],True)}
		for i in range(len(self.input)):
			for j in range(len(self.reference)):
				if not bool(abs(int(self.reference[j])-int(self.input[i]))):
					node_dict[(i,j)] = ([(0,0)],False)
		return node_dict

	def find_node_paths_from_dict(self):
		node_dict = self.node_dict
		for node in node_dict:
			if not node_dict[node][1]:
				for neighbor in node_dict:
					if neighbor[0] > node[0] and neighbor[1] > node[1]:
						if get_value(node_dict[node][0]+[neighbor]) < get_value(node_dict[neighbor][0]):
							node_dict[neighbor] = (node_dict[node][0]+[neighbor],False)
				node_dict[node] = (node_dict[node][0],True)
		return node_dict

	def get_best_path_from_dict(self):
		best_node = ([],float("inf"))
		for node in self.node_dict:
			if node != (-1,-1):
				if get_value(self.node_dict[node][0]) < best_node[1]:
					best_node = (self.node_dict[node][0],get_value(self.node_dict[node][0]))
		return best_node[0]

	# Test of shortest path in a DAG



def create_sorted_list(input,reference):
	node_list = []
	for row in range(len(input)):
		for element in range(len(reference)):
			if reference[element] == input[row]:
				node_list.append((row,element))
	return node_list


def create_adjacency_index_list(node_list):
	adjacency_index_list = [[] for node in node_list]
	for node_index in range(len(node_list)):
		x,y = node_list[node_index]
		for neighbor_index in range(node_index+1,len(node_list)):
			if node_list[neighbor_index][0] > x and node_list[neighbor_index][1] > y:
				adjacency_index_list[node_index].append(neighbor_index)
	return node_list, adjacency_index_list


def DAG_path(node_list, adjacency_index_list):
	dist = [float("inf") for _ in range(len(node_list))]
	dist[0] = 0
	predecessor_index = [-1 for node in node_list]
	best_index = -1
	best_dist = float("inf")
	for node_index in range(len(node_list)):
		for neighbor_index in adjacency_index_list[node_index]:
			alt = dist[node_index] + find_edge_weight(node_list[node_index],node_list[neighbor_index])
			if  alt < dist[neighbor_index]:
				dist[neighbor_index] = alt
				predecessor_index[neighbor_index] = node_index
		if dist[node_index] < best_dist:
			best_dist = dist[node_index]
			best_index = node_index
	return dist, predecessor_index, best_index


def DAG_shortest_path(node_list, dist, predecessor_index, best_index):
	best_path = [node_list[best_index]]
	predecessor = predecessor_index[best_index]
	while predecessor >= 0:
		best_path.append(node_list[predecessor])
		predecessor = predecessor_index[predecessor]
	return best_path


EDGE_WEIGHT_BIAS = 3
def find_edge_weight(smallernode ,greaternode):
	return abs(greaternode[0] - smallernode[0]) + abs(greaternode[1] - smallernode[0]) - EDGE_WEIGHT_BIAS






def fill_path_holes(path, reference_number, input_number):
	new_path = []
	for i in range(len(path)): # Complete the path to have no holes
		dx=path[i][0]-path[i-1][0]
		dy=path[i][1]-path[i-1][1]
		while max(dx,dy) > 1:
			if dy > dx:
				for j in range(1,dy-dx+1):
					new_path.append((path[i-1][0],path[i-1][1]+j,False))
					dy -= 1
			elif dx > dy:
				for j in range(1,dx-dy+1):
					new_path.append((path[i-1][0]+j,path[i-1][1],False))
					dx -= 1
			else:
				new_path.append((path[i-1][0]+1,path[i-1][1]+1,False))
				dx -= 1
				dy -= 1
		new_path.append((path[i][0],path[i][1],True))
	return new_path

def decode_path(filled_path, reference_number, input_number):
	new_list = []
	right_list = []
	for i in range(len(filled_path)):
		if i == 0:
			if reference_number[0] == input_number[0]:
				new_list.append((input_number[0],"Right"))
			else:
				new_list.append((input_number[0],"Wrong"))
		else:
			dx= filled_path[i][0]-filled_path[i-1][0]
			dy= filled_path[i][1]-filled_path[i-1][1]
			if dy != 0 and dx != 0: # The digit is either right or wrong
				if filled_path[i][2]:
					new_list.append((input_number[filled_path[i][0]], "Right"))
				else:
					new_list.append((input_number[filled_path[i][0]],"Wrong"))
			elif dy == 0:
				new_list.append((input_number[filled_path[i][0]],"Added"))
			else:
				new_list.append((reference_number[filled_path[i][1]],"Missing"))
	return new_list

def get_right_list(decoded_path):
	right_list = []
	for i in range(len(decoded_path)):
		if decoded_path[i][1] == "Right":
			right_list.append(decoded_path[i][0])
	return right_list
# Test the functions

m = "14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912"
t = "14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912"


#print(decode_path(fill_path_holes(Pathfinder(m,t).best_node_path,m,t),m,t))

for _ in range(20):
	print()

# DAG test

thenodelist = create_sorted_list(m,t)
theadjacencylist = create_adjacency_index_list(thenodelist)
thedist, thepredecessorindex, thebestindex = DAG_path(*theadjacencylist)
thepath = DAG_shortest_path(thenodelist, thedist, thepredecessorindex, thebestindex)

print(f"Path : {thepath}")

# Test the class version

#print(f"Path : {Pathfinder(m,t).best_node_path}")

