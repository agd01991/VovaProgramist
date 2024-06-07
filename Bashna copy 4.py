from collections import deque
import heapq

def generate_disks(peg_number, n):
    """
    Генерирует список дисков для заданного номера шпинделя.
    Диаметр диска определяется формулой: M * 10 + N,
    где M – номер шпинделя, а N – номер диска на шпинделе (сверху вниз).
    """
    return [(peg_number * 10 + (n - j)) for j in range(n)]

def hanoi_8_pegs(n):
    """
    Решает задачу Ханойских башен с 8 шпинделями и ограничениями на перемещения.
    """
    # Проверка входных данных
    if n <= 0:
        raise ValueError("Количество дисков должно быть положительным числом.")
    
    # Создаем начальное состояние для 8 шпинделей
    initial_state = [generate_disks(1, 7), [], generate_disks(3, 2), [], generate_disks(5, 8), generate_disks(6, 2), generate_disks(7, 1), []]

    
    # Очередь для хранения состояний и посещенных состояний
    priority_queue = []
    heapq.heappush(priority_queue, (0, initial_state, []))
    visited = set()
    
    def state_to_tuple(state):
        """
        Преобразует состояние в кортеж для возможности использования в set.
        """
        return tuple(tuple(peg) for peg in state)
    
    def is_goal(state):
        """
        Проверяет, является ли текущее состояние целевым.
        """
        return all(len(state[i]) == 0 for i in range(7)) and len(state[7]) == n
    
    def possible_moves(state):
        """
        Возвращает список возможных ходов из текущего состояния.
        """
        moves = []
        for i in range(8):
            if state[i]:
                disk = state[i][-1]
                if i == 0:
                    if i + 1 < 8 and (not state[i + 1] or state[i + 1][-1] > disk):
                        moves.append((i, i + 1))
                    if i + 2 < 8 and (not state[i + 2] or state[i + 2][-1] > disk):
                        moves.append((i, i + 2))
                elif i == 7:
                    if i - 1 >= 0 and (not state[i - 1] or state[i - 1][-1] > disk):
                        moves.append((i, i - 1))
                    if i - 2 >= 0 and (not state[i - 2] or state[i - 2][-1] > disk):
                        moves.append((i, i - 2))
                else:
                    if i - 1 >= 0 and (not state[i - 1] or state[i - 1][-1] > disk):
                        moves.append((i, i - 1))
                    if i + 1 < 8 and (not state[i + 1] or state[i + 1][-1] > disk):
                        moves.append((i, i + 1))
        return moves

    def move_disk(state, from_peg, to_peg):
        """
        Перемещает диск с одного шпинделя на другой, возвращая новое состояние.
        """
        new_state = [peg[:] for peg in state]
        disk = new_state[from_peg].pop()
        new_state[to_peg].append(disk)
        return new_state

    def print_state(state):
        """
        Выводит текущее состояние шпинделей.
        """
        for i, peg in enumerate(state):
            print(f"Peg {i + 1}: {peg}")
        print("-" * 20)

    while priority_queue:
        priority, current_state, path = heapq.heappop(priority_queue)
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
            new_tuple = state_to_tuple(new_state)
            if new_tuple not in visited:
                new_priority = -new_state[7][-1] if new_state[7] else 0  # Чем больше диск, тем выше приоритет
                heapq.heappush(priority_queue, (new_priority, new_state, path + [(from_peg, to_peg)]))

    return None

# Пример использования
n = 3  # Количество дисков
solution = hanoi_8_pegs(n)
if solution:
    print("Решение найдено:")
    for move in solution:
        print(f"Переместить диск с {move[0] + 1} на {move[1] + 1}")
else:
    print("Решение не найдено.")
