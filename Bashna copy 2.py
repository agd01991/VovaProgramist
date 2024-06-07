from collections import deque

def hanoi_4_pegs(n):
    # Создаем начальное состояние
    initial_state = [list(range(n, 0, -1)), [], [], []]
    
    # Очередь для хранения состояний
    queue = deque([(initial_state, [])])
    visited = set()
    
    def state_to_tuple(state):
        return tuple(tuple(peg) for peg in state)
    
    def is_goal(state):
        return len(state[0]) == 0 and len(state[1]) == 0 and len(state[2]) == 0 and len(state[3]) == n
    
    def possible_moves(state):
        moves = []
        for i in range(4):
            if state[i]:
                disk = state[i][-1]
                # Правила перемещения дисков с учетом ограничений
                if i == 0:
                    if i + 1 < 4 and (not state[i + 1] or state[i + 1][-1] > disk):
                        moves.append((i, i + 1))
                    if i + 2 < 4 and (not state[i + 2] or state[i + 2][-1] > disk):
                        moves.append((i, i + 2))
                elif i == 3:
                    if i - 1 >= 0 and (not state[i - 1] or state[i - 1][-1] > disk):
                        moves.append((i, i - 1))
                    if i - 2 >= 0 and (not state[i - 2] or state[i - 2][-1] > disk):
                        moves.append((i, i - 2))
                else:
                    if i - 1 >= 0 and (not state[i - 1] or state[i - 1][-1] > disk):
                        moves.append((i, i - 1))
                    if i + 1 < 4 and (not state[i + 1] or state[i + 1][-1] > disk):
                        moves.append((i, i + 1))
        return moves

    def move_disk(state, from_peg, to_peg):
        new_state = [peg[:] for peg in state]
        disk = new_state[from_peg].pop()
        new_state[to_peg].append(disk)
        return new_state

    def print_state(state):
        for i, peg in enumerate(state):
            print(f"Peg {i + 1}: {peg}")
        print("-" * 20)

    while queue:
        current_state, path = queue.popleft()
        current_tuple = state_to_tuple(current_state)

        if current_tuple in visited:
            continue
        visited.add(current_tuple)

        print("Current state:")
        print_state(current_state)

        if is_goal(current_state):
            return path

        for from_peg, to_peg in possible_moves(current_state):
            new_state = move_disk(current_state, from_peg, to_peg)
            queue.append((new_state, path + [(from_peg, to_peg)]))

    return None

# Пример использования
n = 3  # Количество дисков
solution = hanoi_4_pegs(n)
if solution:
    print("Решение найдено:")
    for move in solution:
        print(f"Переместить диск с {move[0] + 1} на {move[1] + 1}")
else:
    print("Решение не найдено.")
