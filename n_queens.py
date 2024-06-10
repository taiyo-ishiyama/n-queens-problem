import queue
import random
import time

class State:
  def __init__(self, queens):
    self.queens = queens # store positions for all queens

def bfs(n):
  frontier = queue.Queue()
  frontier.put(State([])) # store neighbors
  solutions = [] # store solutions
  while not frontier.empty():
    current_state = frontier.get()
    current_row = len(current_state.queens)
    for i in range(n): # iterate each column
      queens = current_state.queens.copy()
      queens.append((current_row, i)) # place queen
      next_state = State(queens)
      if is_valid(next_state) and len(next_state.queens) >= n: # if valid and all rows are filled
        solutions.append(next_state.queens)
      elif is_valid(next_state) and len(next_state.queens) < n: # if valid
        frontier.put(next_state)
  return solutions

def hill_climbing(n):
  current = State(create_intial(n)) # initilize board
  initial_state = current.queens.copy()
  solution_found = False
  id = 0
  count = 0
  while not solution_found and count < 10000:
    if get_heuristic(n, current) == 0: # if heuristic is 0
      solution_found = True
      continue
    neighbors = queue.PriorityQueue() # store all neighbors
    for i in range(n): # generate all neighbors
      for j in range(n):
        if current.queens[i] == j:
          continue
        copy_queens = current.queens.copy()
        copy_queens[i] = (i, j)
        neighbor = State(copy_queens)
        neighbors.put((get_heuristic(n, neighbor), id, neighbor))
        id = id + 1
    next = neighbors.get()
    if get_heuristic(n, next[2]) >= get_heuristic(n, current):
      current = State(create_intial(n)) # initilize board
      initial_state = current.queens.copy()
      count += 1
      continue
    current = next[2]
  if solution_found:
    return current.queens, initial_state
  else:
    return None, initial_state



def is_valid(state):
  num_queens = len(state.queens)
  for i in range(1, num_queens): # check conflicts
    for j in range(0, i):
      queen1_x, queen1_y = state.queens[i]
      queen2_x, queen2_y = state.queens[j]
      if queen1_x == queen2_x or queen1_y == queen2_y or abs(queen1_x - queen2_x) == abs(queen1_y - queen2_y): # check vertical, horizontal, diagonal
        return False
  return True

def create_intial(n):
  queens = []
  for i in range(n):
    queens.append((i, random.randint(0, n-1))) # ramdomly place queens
  return queens

def get_heuristic(n, state):
  h = 0
  for i in range(1, n):
    for j in range(0, i):
      queen1_x, queen1_y = state.queens[i]
      queen2_x, queen2_y = state.queens[j]
      if queen1_x == queen2_x or queen1_y == queen2_y or abs(queen1_x - queen2_x) == abs(queen1_y - queen2_y): # count conflicts vertically, horizontally, diagonally
        h = h + 1
  return h

start_bfs = time.time()
for n in range (1, 12):
  if n < 1 or n > 20:
    print("Invalid input")
    exit()
  start = time.time() # measure time taken
  solutions = bfs(n)
  end = time.time()
  if n <= 6:
    print("Number of solutions for n = ", n, ": ", len(solutions), sep='')
    print("The time taken for n = ", n, ": ", end - start, " seconds", sep='')
    for solution in solutions:
      for i in range(n):
        for j in range(n):
          if (i, j) in solution:
            print("Q", end=" ")
          else:
            print("*", end=" ")
        print("")
      print("")
  else:
    print("Number of solutions for n = ", n, ": ", len(solutions), sep='')
    print("The time taken for n = ", n, ": ", end - start, " seconds", sep='')
end_bfs = time.time()
print("The time taken for bfs (N = 1 to N = 11):", end_bfs - start_bfs, "seconds")

start_hc = time.time() # measure time taken
for n in range(1, 21):
  start = time.time() # measure time taken
  solution, initial_state = hill_climbing(n)
  end = time.time()
  print("The time taken for n = ", n, ": ", end - start, "seconds", sep='')
  if solution:
    print("Initial state for n = ", n, ": ", sep='')
    for i in range(n):
      for j in range(n):
        if (i, j) in initial_state:
          print("Q", end=" ")
        else:
          print("*", end=" ")
      print("")
    print("")
    print("Final solution for n = ", n, ": ", sep='')
    for i in range(n):
      for j in range(n):
        if (i, j) in solution:
          print("Q", end=" ")
        else:
          print("*", end=" ")
      print("")
  else:
    print("No solution found for n =", n)
end_hc = time.time()
print("The time taken for hill climbing (N = 1 to N = 20):", end_hc - start_hc, "seconds")