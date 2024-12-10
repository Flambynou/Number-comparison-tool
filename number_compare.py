def get_value(path):
	True_value_change = -4
	return path[-1][0]+path[-1][1] + (len(path)-1)*True_value_change


class Pathfinder:
	def __init__(self, reference_number, input_number):
		self.reference = reference_number
		self.input = input_number
		#self.matrix = self.create_matrix()
		self.matrix = []
		#self.neighbors = self.precompute_all_neighbors()
		self.neighbors = {}
		#self.dictionary = {(0,0):([(0,0)],False, False)}
		self.dictionary = {}
		#self.node_paths = self.find_node_paths()
		self.node_dict = self.create_node_dict()
		self.node_dict = self.find_node_paths_from_dict()
		#self.best_node_path = self.get_best_node_path()
		self.best_node_path = self.get_best_path_from_dict()
	def create_matrix(self):
		# Create a matrix of size len(b) x len(a) where each element shows if the digit is the same of not
		matrix =[]
		for i in range(len(self.input)):  # loop over every digit in b
			line = []
			for j in range(len(self.reference)): # loop over evey digit in a
				value = not bool(abs(int(self.reference[j])-int(self.input[i])))
				line.append(value) #appends wether the digit is the same or not as a bool
			matrix.append(line)
		return matrix
	def precompute_all_neighbors(self):
		neighbors = {}
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix[0])):
				if self.matrix[i][j] or (i==0 and j==0):
					neighbor_list = []
					for k in range(i+1,len(self.matrix)):
						for l in range(j+1,len(self.matrix[0])):
							if self.matrix[k][l]:
								neighbor_list.append((k,l))
					neighbors[(i,j)] = neighbor_list
		neighbors[(-1,-1)] = [(i,j) for i in range(len(self.matrix)) for j in range(len(self.matrix[0])) if self.matrix[i][j]]
		return neighbors
	def find_node_paths(self):
		while True:
			tmp_dict = self.dictionary.copy()
			for node in tmp_dict:
				if not self.dictionary[node][1]:
					for neighbor in self.neighbors.get(node,[]):
						if neighbor not in self.dictionary or get_value(self.dictionary[node][0]+[neighbor]) < get_value(self.dictionary[neighbor][0]):
							self.dictionary[neighbor] = (self.dictionary[node][0]+[neighbor],False, bool(self.neighbors.get(neighbor,[])))
					self.dictionary[node] = (self.dictionary[node][0],True, bool(self.neighbors.get(node,[])))
			if not False in [self.dictionary[node][1] for node in self.dictionary]:
				break
	def get_best_node_path(self):
		best_node = ([],float("inf"))
		for node in self.dictionary:
			if self.dictionary[node][1] and self.neighbors.get(node, []) == []:
				if get_value(self.dictionary[node][0]) < best_node[1]:
					best_node = (self.dictionary[node][0],get_value(self.dictionary[node][0]))
		return best_node[0]

	def __str__(self):
		# The str method returns a string with the matrix, the node dictionary and the best node path
		string = "Matrix : \n"
		for column in range(len(self.matrix[0])):
			for row in self.matrix:
				if row[column]:
					string += "█"
				else:
					string += "░"
			string+="\n"
		string += "Node dictionary : \n"
		for node in self.dictionary:
			string += f"Node {node} : " + str(self.dictionary[node][0]) + " Value: " + str(get_value(self.dictionary[node][0])) + " " + str(self.dictionary[node][1]) + "\n"
		string += "Best node path : " + str(self.best_node_path)
		return string

	#Test of optimized version by not creating a matrix, instead creating a dictionary with each true node and no neighbor list but simply iterate over the dictionary

	def create_node_dict(self):
		node_dict = {(0,0):([(0,0)],True)}
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
			if self.node_dict[node][1]:
				if get_value(self.node_dict[node][0]) < best_node[1]:
					best_node = (self.node_dict[node][0],get_value(self.node_dict[node][0]))
		return best_node[0]






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

m = "1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989"
t = "14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460"


print(decode_path(fill_path_holes(Pathfinder(m,t).best_node_path,m,t),m,t))

