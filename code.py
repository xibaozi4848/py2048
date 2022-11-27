import random as rd
import numpy as np


def game_start():
    print('''
    control keys:
    W or w means moving up,
    S or s means moving down,
    A or a means moving left,
    D or d means moving right

    ''')
    mat = []
    np.array(mat)
    for i in range(4):
        mat.append([0, 0, 0, 0])
    mat = generator('start', mat)
    return np.array(mat)


def generator(status, mat):
    # during the game, everytime generate a '2'
    if status == 'resume':
        scope = []
        for i in range(4):
            for j in range(4):
                if mat[i][j] == 0:
                    scope.append([i, j])
        index = rd.choice(scope)
        mat[index[0]][index[1]] = 2
        return mat
    if status == 'start':
        scope = []
        for i in range(4):
            for j in range(4):
                if mat[i][j] == 0:
                    scope.append([i, j])
        index = rd.choice(scope)
        mat[index[0]][index[1]] = 2
        scope = []
        for i in range(4):
            for j in range(4):
                if mat[i][j] == 0:
                    scope.append([i, j])
        index_2 = rd.choice(scope)
        mat[index_2[0]][index_2[1]] = 2
        return mat
    if status == 'stop':
        # for test purposes
        return 'no movement'


# movement functions are defined below:
# in the movement functions series, I would define a reverse and a transpose function
# to convert the movements of moving up, right, and down to moving left.
# Therefore, the compress, merge, and left functions are only need to consider moving left.
def compress(mat):
    change = False
    for i in range(4):
        des = 0
        for j in range(4):
            if mat[i][j] != 0:
                mat[i][des] = mat[i][j]
                if j != des:
                    mat[i][j] = 0
                    change = True
                des += 1
    return mat, change


def merge(new_mat):
    change = False
    for i in range(4):
        for j in range(3):
            if new_mat[i][j] != 0 and new_mat[i][j] == new_mat[i][j + 1]:
                change = True
                new_mat[i][j] *= 2
                new_mat[i][j + 1] = 0
    return new_mat, change


def reverse(mat):
    for i in range(4):
        mat[i][0], mat[i][-1] = mat[i][-1], mat[i][0]
        mat[i][1], mat[i][-2] = mat[i][-2], mat[i][1]
    return mat


def transpose(mat):
    for i in range(4):
        for j in range(i, 4):
            mat[i][j], mat[j][i] = mat[j][i], mat[i][j]
    return mat


def left(mat):
    first_mat, change_1 = compress(mat)
    second_mat, change_2 = merge(first_mat)
    third_mat, change_3 = compress(second_mat)
    print('change 1: {}, change 2: {}, change 3: {}'.format(change_1, change_2,
                                                            change_3))  # for debuging and test purposes
    change = (change_1 == True or change_2 == True or change_3 == True)
    return third_mat, change


def right(mat):
    new_mat = reverse(mat)
    new_mat, change = left(new_mat)
    return reverse(new_mat), change


def up(mat):
    new_mat = transpose(mat)
    new_mat, change = left(new_mat)
    return np.array(transpose(new_mat)), change


def down(mat):
    new_mat = transpose(mat)
    new_mat, change = right(mat)
    return np.array(transpose(new_mat)), change


# status checking functions are defined below:
def get_status(mat):
    for i in range(4):
        for j in range(4):
            if mat[i][j] == 2048:
                return 'win'
            elif mat[i][j] == 0:
                return 'resume'
    for i in range(3):
        for j in range(3):
            if mat[i][j] == mat[i][j + 1] or mat[i][j] == mat[i + 1][j]:
                return 'resume'
    return False


# Development stage 2:
'''
Here is the main procedure of the game

'''


def exit_round(exit):
    exit = exit.lower()
    if exit == 'y':
        return False
    # exception handling:
    elif exit == 'n':
        return True
    else:
        exit = input("Please enter Y/N")
        exit_round(exit)


def game_2048():
    mat = game_start()
    go_on = True
    while go_on == True:
        print(mat)
        x = input('what\'s your move?')
        y = x.lower()
        if y == 'a':
            mat, change = left(mat)
            if get_status(mat) == 'resume':
                if change == True:
                    mat = generator('resume', mat)
                else:
                    mat = generator('stop', mat)
            elif get_status(mat) == 'win':
                print('You win!')
                go_on = False
            else:
                print('You lose!')
                go_on = False
        elif y == 'd':
            mat, change = right(mat)
            if get_status(mat) == 'resume':
                if change == True:
                    mat = generator('resume', mat)
                else:
                    mat = generator('stop', mat)
            elif get_status(mat) == 'win':
                print('You win!')
                go_on = False
            else:
                print('You lose!')
                go_on = False
        elif y == 'w':
            mat, change = up(mat)
            if get_status(mat) == 'resume':
                if change == True:
                    mat = generator('resume', mat)
                else:
                    mat = generator('stop', mat)
            elif get_status(mat) == 'win':
                print('You win!')
                go_on = False
            else:
                print('You lose!')
                go_on = False
        elif y == 's':
            mat, change = down(mat)
            if get_status(mat) == 'resume':
                if change == True:
                    mat = generator('resume', mat)
                else:
                    mat = generator('stop', mat)
            elif get_status(mat) == 'win':
                print('You win!')
                go_on = False
            else:
                print('You lose!')
                go_on = False
        elif y == 'e':
            exit = input('Do you want to end this round?(Y/N)')
            go_on = exit_round(exit)

        # exception handling:
        elif y not in ['a', 's', 'w', 'd', 'e']:
            print('use "w", "s", "a", "d" to move or "e" to exit')
            go_on = True
    print('Restart or exit the program?')
    return restart()


def restart():
    num = input('1-restart/2-exit program')

    def helper(num):
        if num == '1':
            return game_2048()
        elif num == '2':
            return print('Have a great day!')
        # exceptions handling
        else:
            num = input('please reply with 1 or 2')
            return helper(num)

    return helper(num)
