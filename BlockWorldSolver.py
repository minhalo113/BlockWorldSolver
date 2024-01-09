import heapq
class State_Astar:
    def __init__(self):
        self.clear = []
        self.on = []
        self.on_table = []
        self.priority = 0
        self.g = 0
        self.path = []
    def __lt__(self, other):
        return self.priority < other.priority 
    
    def __eq__(self, other):
        return set(self.clear) == set(other.clear) and set(self.on) == set(other.on) and set(self.on_table) == set(other.on_table)
    
    def set_initial_state(self, clear, on, on_table, priority, path):
        self.clear = clear
        self.on = on
        self.on_table = on_table
        self.priority = priority
        self.path = path

    def print_stat(self):
        print(self.clear, self.on, self.on_table, self.priority, self.g)
    
    def set_clear(self, clear):
        self.clear = clear
    def get_clear(self):
        return self.clear.copy()
    
    def set_on(self, on):
        self.on = on
    def get_on(self):
        return self.on.copy()    
    
    def set_on_table(self, on_table):
        self.on_table = on_table
    def get_on_table(self):
        return self.on_table.copy()
    
    def set_priority(self, priority):
        self.priority = priority
    def get_priority(self):
        return self.priority
    
    def set_g(self, g):
        self.g = g
    def get_g(self):
        return self.g

    def set_path(self, path):
        self.path = path
    def get_path(self):
        return self.path.copy()

class BlockWorld:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def possible_actions(self, state):
        # Define possible actions based on the current state
        possible_actions = {1 : [], 2: [], 3: []}
        clear = state.get_clear()
        on_table = state.get_on_table()
        on = state.get_on()

        for x in on_table:
            if x in clear:
                for y in clear:
                    if y != x:
                        possible_actions[1].append(x+y)
        for x in clear:
            if x not in on_table:
                for y in clear:
                    if y != x:
                        possible_actions[2].append(x+y)
        for x in clear:
            for ele in on:
                if ele and ele[0] == x:
                    possible_actions[3].append(x+ele[1])

        return possible_actions

    def movefromTabletoBlock(self, x, y, state):
        clear = state.get_clear()
        on_table = state.get_on_table()
        on = state.get_on()
        if (x in clear) and (x in on_table) and (y in clear):
            on_table.remove(x)
            clear.remove(y)
            on.append(x + y)

        priority = state.get_priority()
        path = state.get_path()

        path.append("move " + x + " from table to block " + y) 

        new_state = State_Astar()
        new_state.set_g(state.get_g())
        new_state.set_initial_state(clear, on, on_table, priority, path)

        return new_state


    def movefromBlocktoBlock(self, x, y, state):
        clear = state.get_clear()
        on_table = state.get_on_table()
        on = state.get_on()
        new_on = []
        new_clear = []
        if (x in clear) and (y in clear) and (x not in on_table):
            for ele in on:
                if str(ele)[0] != x:
                    new_on.append(ele)
                else:
                    new_clear.append(ele[1])

            clear.extend(new_clear)
            clear.remove(y)
            on = new_on
            on.append(x+y)

        priority = state.get_priority()
        path = state.get_path()
        path.append("move block " + x + " to block " + y) 

        new_state = State_Astar()
        new_state.set_g(state.get_g())
        new_state.set_initial_state(clear, on, on_table, priority, path)

        return new_state
        
    def movefromblocktoTable(self, x,y ,state):
        clear = state.get_clear()
        on_table = state.get_on_table()
        on = state.get_on()
        if(x in clear) and ((x+y) in on):
            on_table.append(x)
            clear.append(y)
            on.remove(x+y)

        priority = state.get_priority()
        path = state.get_path()
        path.append("move " + x + " from block " + y + " to table") 

        new_state = State_Astar()
        new_state.set_g(state.get_g())
        new_state.set_initial_state(clear, on, on_table, priority, path)

        return new_state

    def heuristic(self, state):
        # Implement a heuristic function
        h_values = 0

        clear_goal = self.goal_state.get_clear()
        on_table_goal = self.goal_state.get_on_table()
        on_goal = self.goal_state.get_on()

        current_clear = state.get_clear()
        current_on_table = state.get_on_table()
        current_on = state.get_on()

        for ele in clear_goal:
            if ele not in current_clear:
                h_values = h_values + 1;

        for ele in on_table_goal:
            if ele not in current_on_table:
                h_values = h_values + 1;

        for ele in on_goal:
            if ele not in current_on:
                h_values = h_values + 1;
        return h_values

    def astar_search(self):
        # Implement the A* search algorithm
        open_list = []
        closed_list = []

        num = 0

        heapq.heappush(open_list, self.initial_state)
        while len(open_list)!= 0:
            current_state = heapq.heappop(open_list)

            possible_actions = self.possible_actions(current_state)

            """print(possible_actions)"""
            for i in range(1,4):
                for j in possible_actions[i]:
                    check = 0
                    if i == 1:
                        new_state = self.movefromTabletoBlock(j[0], j[1], current_state)
                    elif i == 2:
                        new_state = self.movefromBlocktoBlock(j[0], j[1], current_state)
                    elif i == 3:
                        new_state = self.movefromblocktoTable(j[0], j[1], current_state)

                    if new_state == goal_state:
                        return new_state.get_path()
                    else:
                        my_g = new_state.get_g() + 1
                        new_state.set_g(my_g)
                        my_priority = my_g + self.heuristic(new_state)
                        new_state.set_priority(my_priority)

                        if new_state in open_list:
                            matching_states = [state for state in open_list if state == new_state]
                            for ele in matching_states:
                                if ele < new_state:
                                    check = check + 1
                                    # print("stop1")
                                    break
                        
                        if new_state in closed_list:
                            matching_states = [state for state in closed_list if state == new_state]
                            for ele in matching_states:
                                if ele < new_state:
                                    check = check + 1
                                    # print("stop2")
                                    break
                        if check != 0:
                            continue
                        
                        heapq.heappush(open_list, new_state)

                    num = num + 1
                    if num == 100000:
                        return ["unable to find solution"]
                        
            closed_list.append(current_state)
            
        return ["unable to find solution"]


# Example usage:
# Example1
"""clear = ["a","b","c"]
on_table = ["a", "b", "c"]
on = []
path = []
initial_state = State_Astar()
initial_state.set_initial_state(clear, on, on_table, 0, path)

clear = ["a"]
on_table = ["c"]
on = ["ab", "bc"]
goal_state = State_Astar()
goal_state.set_initial_state(clear, on, on_table, 0,path)

block_world = BlockWorld(initial_state, goal_state)
solution = block_world.astar_search()
print("Solution:", solution)"""

# Example2
"""clear = ["a", "c", "e"]
on_table = ["b", "d", "e"]
on = ["ab", "cd"]
path = []
initial_state = State_Astar()
initial_state.set_initial_state(clear, on, on_table, 0, path)

clear = ["a"]
on_table = ["e"]
on = ["ab", "bc", "cd", "de"]
goal_state = State_Astar()
goal_state.set_initial_state(clear, on, on_table, 0,path)

block_world = BlockWorld(initial_state, goal_state)
solution = block_world.astar_search()
print("Solution:", solution)"""

# Example3
"""clear = ["a", "d", "g"]
on_table = ["c", "f", "i"]
on = ["ab","bc","de", "ef", "gh", "hi"]
path = []
initial_state = State_Astar()
initial_state.set_initial_state(clear, on, on_table, 0, path)

clear = ["a"]
on_table = ["i"]
on = ["ab", "bc", "cd", "de", "ef", "fg" , "gh", "hi"]
goal_state = State_Astar()
goal_state.set_initial_state(clear, on, on_table, 0,path)

block_world = BlockWorld(initial_state, goal_state)
solution = block_world.astar_search()
print("Solution:", solution) """

# Example4
"""clear = ["a", "d", "e", "f", "g"]
on_table = ["c", "d", "e", "f", "g"]
on = ["ab","bc"]
path = []
initial_state = State_Astar()
initial_state.set_initial_state(clear, on, on_table, 0, path)

clear = ["a"]
on_table = ["g"]
on = ["ab", "bc", "cd", "de", "ef", "fg"]
goal_state = State_Astar()
goal_state.set_initial_state(clear, on, on_table, 0,path)

block_world = BlockWorld(initial_state, goal_state)
solution = block_world.astar_search()
print("Solution:", solution)"""