#!FOR REFERENCE ONLY
import cnfgen

class Formula:

    def __init__(self, size, points):
        self.size = size
        self.colors = len(points)
        self.points = points
        self.e1 = [] #contains all endpoints that mark the beggining of a path
        self.e2 = [] #contains all endpoints that mark the end of a path (lists of lists according to color)
        self.ne = [] #contains all non encnfdpoints (lists of lists according to grid position)
    
    def get_endpoints(self):
        endpoints = []
        for e in self.points:
            endpoints.append(e[0])
            endpoints.append(e[1])
        
        return endpoints

    def generate_variables(self):
        col = 0

        #generate endpoints
        for pair in self.points:
            col +=1
            self.e1.append('E1|{color}|{path_pos}|{position}'.format(color = col, path_pos = 1, position = pair[0]))

            curr_e2 = []
            for i in range(2, self.size * self.size + 1):
                curr_e2.append('E2|{color}|{path_pos}|{position}'.format(color = col, path_pos = i, position = pair[1]))

            self.e2.append(curr_e2)

        #generate non endpoints
        for i in range(1, self.size * self.size + 1):
            endpoints = self.get_endpoints()
            if i not in endpoints:
                curr_ne = []
                for c in range(1, self.colors + 1):
                    curr_c = []
                    for p in range(2, self.size * self.size):
                        curr_c.append('x|{color}|{path_pos}|{position}'.format(color = c, path_pos = p, position = i))
                    
                    curr_ne.append(curr_c)

                self.ne.append(curr_ne)

    def solve(self):

        #add variables
        f = cnfgen.CNF()

        for i in self.e1:
            f.add_variable(i)

        for i in self.e2:
            for j in i:
                f.add_variable[j]
        
        for i in self.ne:
            for j in i:
                for k in j:
                    f.add_variable[k]
        
        #formula 1
        index = 0
        for e1 in self.e1:
            for e2 in self.e2[index]:
                f.add_clause([(True, e1), (True, e2)])
            
            index += 1

        def generate_variables(self):
        col = 0

        #generate endpoints
        for pair in self.points:
            col +=1
            self.e1.append('E1|{color}|{path_pos}|{position}'.format(color = col, path_pos = 1, position = pair[0]))

            curr_e2 = []
            for i in range(2, self.size * self.size + 1):
                curr_e2.append('E2|{color}|{path_pos}|{position}'.format(color = col, path_pos = i, position = pair[1]))

            self.e2.append(curr_e2)

        #generate non endpoints
        for i in range(1, self.size * self.size + 1):
            endpoints = self.get_endpoints()
            if i not in endpoints:
                curr_ne = []
                for c in range(1, self.colors + 1):
                    curr_c = []
                    for p in range(2, self.size * self.size):
                        curr_c.append('x|{color}|{path_pos}|{position}'.format(color = c, path_pos = p, position = i))
                    
                    curr_ne.append(curr_c)

                self.ne.append(curr_ne)

    def solve(self):

        #add variables
        f = cnfgen.CNF()

        for i in self.e1:
            f.add_variable(i)

        for i in self.e2:
            for j in i:
                f.add_variable[j]
        
        for i in self.ne:
            for j in i:
                for k in j:
                    f.add_variable[k]
        
        #formula 1
        index = 0
        for e1 in self.e1:
            for e2 in self.e2[index]:
                f.add_clause([(True, e1), (True, e2)])
            
            index += 1

        #formula 2

        def generate_variables(self):
        col = 0

        #generate endpoints
        for pair in self.points:
            col +=1
            self.e1.append('E1|{color}|{path_pos}|{position}'.format(color = col, path_pos = 1, position = pair[0]))

            curr_e2 = []
            for i in range(2, self.size * self.size + 1):
                curr_e2.append('E2|{color}|{path_pos}|{position}'.format(color = col, path_pos = i, position = pair[1]))

            self.e2.append(curr_e2)

        #generate non endpoints
        for i in range(1, self.size * self.size + 1):
            endpoints = self.get_endpoints()
            if i not in endpoints:
                curr_ne = []
                for c in range(1, self.colors + 1):
                    curr_c = []
                    for p in range(2, self.size * self.size):
                        curr_c.append('x|{color}|{path_pos}|{position}'.format(color = c, path_pos = p, position = i))
                    
                    curr_ne.append(curr_c)

                self.ne.append(curr_ne)

    def solve(self):

        #add variables
        f = cnfgen.CNF()

        for i in self.e1:
            f.add_variable(i)

        for i in self.e2:
            for j in i:
                f.add_variable[j]
        
        for i in self.ne:
            for j in i:
                for k in j:
                    f.add_variable[k]
        
        #formula 1
        index = 0
        for e1 in self.e1:
            for e2 in self.e2[index]:
                f.add_clause([(True, e1), (True, e2)])
            
            index += 1

        #formula 2

        def generate_variables(self):
        col = 0

        #generate endpoints
        for pair in self.points:
            col +=1
            self.e1.append('E1|{color}|{path_pos}|{position}'.format(color = col, path_pos = 1, position = pair[0]))

            curr_e2 = []
            for i in range(2, self.size * self.size + 1):
                curr_e2.append('E2|{color}|{path_pos}|{position}'.format(color = col, path_pos = i, position = pair[1]))

            self.e2.append(curr_e2)

        #generate non endpoints
        for i in range(1, self.size * self.size + 1):
            endpoints = self.get_endpoints()
            if i not in endpoints:
                curr_ne = []
                for c in range(1, self.colors + 1):
                    curr_c = []
                    for p in range(2, self.size * self.size):
                        curr_c.append('x|{color}|{path_pos}|{position}'.format(color = c, path_pos = p, position = i))
                    
                    curr_ne.append(curr_c)

                self.ne.append(curr_ne)

    def solve(self):

        #add variables
        f = cnfgen.CNF()

        for i in self.e1:
            f.add_variable(i)

        for i in self.e2:
            for j in i:
                f.add_variable[j]
        
        for i in self.ne:
            for j in i:
                for k in j:
                    f.add_variable[k]
        
        #formula 1
        index = 0
        for e1 in self.e1:
            for e2 in self.e2[index]:
                f.add_clause([(True, e1), (True, e2)])
            
            index += 1

        #formula 2
        

                
        
form = Formula(3, [(1,4), (2,5)])
form.generate_variables()
print(form.e1)
print(form.e2)
print(form.ne)
print(form.colors)
#form.solve()

F = cnfgen.CNF()
F.add_clause([(True,"X"),(False,"Y")])
F.add_clause([(False,"X")])
F.is_satisfiable()
F.add_clause([(True,"Y")])
F.is_satisfiable()
