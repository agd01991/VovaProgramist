from collections import deque

def generate_moves(state, num_poles):
    moves = []
    for i in range(num_poles):
        if not state[i]:
            continue
        disk = state[i][-1]
        if i > 0 and (not state[i-1] or state[i-1][-1] > disk):
            new_state = [pole[:] for pole in state]
            new_state[i].pop()
            new_state[i-1].append(disk)
            moves.append(new_state)
        if i < num_poles - 1 and (not state[i+1] or state[i+1][-1] > disk):
            new_state = [pole[:] for pole in state]
            new_state[i].pop()
            new_state[i+1].append(disk)
            moves.append(new_state)
        if i == 0 and i + 2 < num_poles and (not state[i+2] or state[i+2][-1] > disk):
            new_state = [pole[:] for pole in state]
            new_state[i].pop()
            new_state[i+2].append(disk)
            moves.append(new_state)
        if i == num_poles - 1 and i - 2 >= 0 and (not state[i-2] or state[i-2][-1] > disk):
            new_state = [pole[:] for pole in state]
            new_state[i].pop()
            new_state[i-2].append(disk)
            moves.append(new_state)
    return moves

def hanoi_graph_solution(num_disks, num_poles):
    start_state = [list(range(num_disks, 0, -1))] + [[] for _ in range(num_poles - 1)]
    goal_state = [[] for _ in range(num_poles - 1)] + [list(range(num_disks, 0, -1))]
    
    queue = deque([(start_state, [])])
    visited = set()
    
    while queue:
        current_state, path = queue.popleft()
        if tuple(tuple(pole) for pole in current_state) in visited:
            continue
        visited.add(tuple(tuple(pole) for pole in current_state))
        
        if current_state == goal_state:
            return path
        
        for next_state in generate_moves(current_state, num_poles):
            queue.append((next_state, path + [next_state]))

    return None

def print_solution(solution):
    if solution:
        for step in solution:
            print(step)
    else:
        print("Нет решения")

# Пример вызова функции для 3 дисков и 4 штырей
solution = hanoi_graph_solution(7, 8)
print_solution(solution)
