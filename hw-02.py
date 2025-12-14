import random

list_cell = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']  # список всех полей

# список всех линий
list_line = [['a1', 'b2', 'c3']]
list_line.append(['a3', 'b2', 'c1'])
for n in '123':
    list_line.append(['a' + n, 'b' + n, 'c' + n])
for x in 'abc':
    list_line.append([x + '1', x + '2', x + '3'])

# печать поля
def view_board(fg_x):
    sign = 1 if fg_x else -1
    x = '\033[31mx\033[0m'  # красный крестик
    o = '\033[34mo\033[0m'  # синий нолик
    dict_xo = {k: x if v * sign > 0 else (o if v * sign < 0 else '-') for k, v in dict_position.items()}
    print('')
    print('  A B C')
    for n in '123':
        print(n + ' ' + dict_xo['a' + n] + ' ' + dict_xo['b' + n] + ' ' + dict_xo['c' + n])
    print('')

# проверка позиции: 1 - победа, 0 - ничья, -1 - поражение
def check_position(dict_cell):
    for line in list_line:
        res = sum(map(lambda x: dict_cell[x], line))
        if res == 3:
            return 1
        if res == -3:
            return -1
    return 0

# проверка хода
# n - чей ход (1 компьютер, -1 игрок), cell - поле, dict_pos - позиция
# результат: 1 - победа, 0 - ничья, -1 - поражение
def check_move(n, cell, dict_pos):
    dict_pos_new = dict_pos.copy()
    dict_pos_new[cell] = n
    res = check_position(dict_pos_new)
    if res != 0:
        return res
    list_possible = list(filter(lambda x: dict_pos_new[x] == 0, list_cell))
    if len(list_possible) == 0:
        return 0
    for x in list_possible:
        dict_pos_x = dict_pos_new.copy()
        dict_pos_x[x] = -n
        res = check_position(dict_pos_x)
        if res != 0:
            return res
    res = None
    for x in list_possible:
        dict_pos_x = dict_pos_new.copy()
        dict_pos_x[x] = -n
        res_x = check_move(-n, x, dict_pos_x)
        if res is None:
            res = res_x
        elif res != res_x:
            if n == 1:
                res = min(res, res_x)
            else:
                res = max(res, res_x)
    return res

# подбор лучшего хода
def best_move():
    dict_pos = dict_position.copy()
    list_possible = list(filter(lambda x: dict_pos[x] == 0, list_cell))
    random.shuffle(list_possible)
    cell = None
    for x in list_possible:
        res = check_move(1, x, dict_pos)
        if res == 1:
            return x
        elif res == 0 and cell is None:
            cell = x
    return cell


fg_x = random.choice([True, False])  # случайным образом определяем, у кого крестики
while True:
    dict_position = dict.fromkeys(list_cell, 0)

    for i in range(len(list_cell)):

        view_board(fg_x)

        if i % 2 == 0 and not fg_x or i % 2 != 0 and fg_x:
            while True:
                cell = input("Ваш ход: ").lower()
                if dict_position.get(cell) is None:
                    cell = cell[::-1]
                if dict_position.get(cell) is None:
                    print('Неверный ход. Введите имя поля, например: A1, 3b, 2c ...')
                elif dict_position.get(cell) != 0:
                    print('Неверный ход, поле занято.')
                else:
                    dict_position[cell] = -1
                    break
        else:
            cell = best_move()
            print('Ход: ', cell.upper())
            dict_position[cell] = 1

        res = check_position(dict_position)
        if res != 0:
            break

    view_board(fg_x)
    if res == 1:
        print('Поражение')
    else:
        print('Ничья')

    print('')
    fg_ok = input("Ещё раз? <Y/n>: ").lower()
    if fg_ok == 'n':
        break

    fg_x = not fg_x  # меняемся сторонами
