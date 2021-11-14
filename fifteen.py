#! /usr/bin/python3

## Импортируем библиотеки os (для очистки терминала), 
## random (для случайного перемешивания блоков на поле)
## click (для захвата нажатий кнопок)
import os
import random
import click

## генерирует массив с с числами от 0 до 15,
## затем случайно перемешивает данный массив
def generate():
    block = list(range(16))
    random.shuffle(block)
    return block

## получает на вход текущий массив и определяет в нем 
## индекс блока "0", возвращает индекс блока
def zero_block(block):
    index_select = block.index(0)
    return index_select

## выводит текущий массив block на экран
def visualisation(block, ind_select):
    ## создаем пустую строку
    visual_str = ''
    ## для каждой из четырех строк устанавливаем смещение индекса
    for i in range(0,4):
        if i == 0:
            ## если это первая строка добавляем элементы в строку без смещения
            iter = 0
        elif i == 1:
            ## если вторая добавляем элементы в строку с 4 элемента
            iter = i + 3
        elif i == 2:
            ## если третья с 7 элемента
            iter = i + 6
        elif i == 3:
            ## если 4 строка, то с 10
            iter = i + 9
            ## обрабатываем столбцы 
        for elem_in_row in range(0,4):
            ## если индекс элемента указывает на "0" блок и содержимое блока меньше 10
            ## отрисовываем индикатор выделения с пробелом
            if iter + elem_in_row == ind_select and block[iter + elem_in_row] < 10:
                visual_str = visual_str + '[|' + str(block[iter + elem_in_row]) + ' |]'
            ## если больше 10, отрисовываем индикатор выделения без пробела
            elif iter + elem_in_row == ind_select:
                visual_str = visual_str + '[|' + str(block[iter + elem_in_row]) + '|]'
            ## если содержимое блока меньше 10 отрисовываем границы блока с пробелом
            elif block[iter + elem_in_row] < 10:
                visual_str = visual_str + '[ ' + str(block[iter + elem_in_row]) + '  ]'
            ## иначе отрисовываем без пробела
            else:
                visual_str = visual_str + '[ ' + str(block[iter + elem_in_row]) + ' ]'
            ## если это 4 элемент в строке добавляем перевод строки
            if elem_in_row == 3:
                visual_str = visual_str + '\n' 
    print(visual_str)
    return visual_str

## определяем не выходит ли индикатор за границы массива, если выходит
## ничего не происходит
def posible_move_select(result_select):
    if result_select in range(0,16):
        return True
    else:
        return False

## меняет местами блок "0" и блок на котором стоит выделение
## через промежуточные переменные
def move_block(block, ind_select):
    sub_sel_block = block[ind_select]
    sub_zero_block = block[block.index(0)] 
    block[block.index(0)] = sub_sel_block
    block[ind_select] = sub_zero_block
 
## проверяет что блоки которые должны поменятся местами
## стоят в соседних клетках -1 +1, либо находятся в соседних клетках по вертикале +4 -4
def check_move_block(block, ind_select):
    if ind_select - block.index(0) == -1:
        move_block(block, ind_select)
    elif ind_select - block.index(0) == 1:
        move_block(block, ind_select)
    elif ind_select - block.index(0) == -4:
        move_block(block, ind_select)  
    elif ind_select - block.index(0) == 4:
        move_block(block, ind_select)
    else:
        pass
    return block

## проверяет выигрышную комбинацию и выводит сообщение о победе
## либо продолжает игру
def check_win(block):
    if block == [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]:
        print('You WIN!!!')
    else:
        pass    

## Начало основного цикла игры
## Генерируем случайное поле
block = generate()

## Определяем положение блока "0"
ind_select = zero_block(block)

## Основной цикл
while True:
    try:
        ## Очищает терминал после каждого действия
        os.system('cls' if os.name == 'nt' else 'clear')
        ## отрисовывает поле
        visualisation(block, ind_select)
        ## выводит сообщение "Ваш ход"
        click.echo('Ваш ход', nl=False)
        ## проверяет не сложилась ли выиграшная комбинация
        check_win(block)
        ## записывает нажатую клавишу на клавиатуре в переменную c
        c = click.getchar()
        #click.echo()
        ## если нажатая клавиша Esc то завершает игру
        if c == '\x1b': # Esc
            click.echo('Abort!')
            break
        ## если стрелка, то определяет возможно ли перемещение в такую позицию
        ## если да то перемещает индикатор выделения в эту позицию
        elif c == '\x1b[D': # Left
            result_select = ind_select - 1
            if posible_move_select(result_select) == True: 
                ind_select = result_select
        elif c == '\x1b[C': # Right
            result_select = ind_select + 1
            if posible_move_select(result_select) == True: 
                ind_select = result_select
        elif c == '\x1b[A': # Up
            result_select = ind_select - 4
            if posible_move_select(result_select) == True: 
                ind_select = result_select
        elif c == '\x1b[B': # Down
            result_select = ind_select + 4
            if posible_move_select(result_select) == True: 
                ind_select = result_select
        ## если нажатая клавиша Space, то делаем проверку на возможность перемещения
        ## если проверка пройдена, то меняем местами блоки 
        elif c == '\x20':   # Space
            block = check_move_block(block, ind_select)
        else:
            click.echo('Управление стрелками, переместить блок [SPACE] \n Завершить игру [ESC]')
    ## если ловим исключение Ctrl+C, то завершаем программу
    except KeyboardInterrupt:
        break
         
