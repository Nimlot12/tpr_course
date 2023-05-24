from scipy.optimize import linprog
import csv
from rich.console import Console
from rich.progress import track
from time import sleep
console = Console()

# добавление ограничений
left_ogr = []
right_ogr = []


def add_ogr(lefr_ogr, right_ogr):
    console.print('Введите значения ограничений на каждый продукт на левую '
                  'часть матрицы, добавленный вами, если на продукт нет ограничения, '
                  'то введите "0"', style="bold red")
    mas_promez = []
    for i in range(len(mas1)):
        mas_promez.append(int(input()))
    left_ogr.append(mas_promez)
    console.print('Введите значения ограничений на каждый продукт '
                  'на правую часть матрицы, добавленный вами, если на продукт '
                  'нет ограничения, то введите "0"', style="bold red")
    right_ogr.append(int(input()))


# добавление новых продуктов в наш scv file
def add_csv():
    console.print('введите номер, название продукта, количество калорий, '
                  'белков, жиров, углеводов и стоимость продукта', style="bold red")
    number = input()
    name = input()
    kk = input()
    bel = input()
    lip = input()
    ugl = input()
    cost = input()
    with open('dataset_course2.csv', 'a', newline='') as r_file1:
        spamwriter = csv.writer(r_file1, delimiter=';')
        spamwriter.writerow([number, name, kk, bel, lip, ugl, cost])
        r_file1.close()


mas1 = []

console.print('введите количество продуктов, которые хотите добавить', style="bold red")
console.print('если ваш список пуст, то введите не менее 5 продуктов', style="bold red")
count = int(input())
for i in range(count):
    add_csv()

console.print('введите количество ограничений на продукты питания, если ограничений нет, введите "0"', style="bold red")
count2 = int(input())
for i in range(count2):
    add_ogr()

if (len(mas1)) == 0:
    console.print('ваш список продуктов пуст, вычисления провести невозможно', style="bold red")

# чтение нашего сsv файла с продуктами и данными
with open("dataset_course2.csv", encoding='cp1251') as r_file:
    reader_object = csv.reader(r_file, delimiter=';')
    for row in reader_object:
        mas1.append(list(row))
    r_file.close()
a = len(mas1)
for i in range(len(mas1)):
    for j in range(5):
        mas1[i][j+2] = float(mas1[i][j+2])
for i in range(len(mas1)):
    for j in range(5):
        mas1[i][0] = int(mas1[i][0])
# print(mas1)
z = []
mas2 = []


# заполнение целевой функции
for i in range(len(mas1)):
    z.append(mas1[i][6])

# заполнение левых значений по матрице
for i in range(len(mas1)):
    mas3 = []
    for j in range(4):
        mas3.append(int(mas1[i][j+2]))
    mas2.append(mas3)
left_st = [[0 for j in range(len(mas2))] for i in range(len(mas2[0]))]
for i in range(len(mas2)):
    for j in range(len(mas2[0])):
        left_st[j][i] = mas2[i][j]

# правые значения по матрице
right_st = [2000,
            75,
            70,
            250]


# ограничения на положительные элементы по х
bnd = []
for i in range(len(z)):
    bnd.append((0, float("inf"))) # Границы x
# print(bnd)


# нахождение решения через симплекс метод
def process_data():
    sleep(0.05)


for step in track(range(100), description='[green]Progress'):
    process_data()
if len(left_ogr) != 0:
    opt = linprog(c=z, A_ub=left_ogr, b_ub=right_ogr,
                  A_eq=left_st, b_eq=right_st, bounds=bnd,
                  method="revised simplex")
else:
    opt = linprog(c=z,
                  A_eq=left_st, b_eq=right_st, bounds=bnd,
                  method="revised simplex")
listik = opt.x
mas_i = []
mas_count = []


# нахождение продуктов которые нам подходят
for i in range(len(listik)):
    if listik[i] != 0:
        mas_i.append(i+1)
        mas_count.append(listik[i])
# print(mas_i)
console.print('Значение целевой функции, или наименьшей стоимости продуктов равно ', opt.fun, style="bold red")
mas_name = []
for i in range(len(mas1)):
    for j in range(len(mas_i)):
        if mas1[i][0] == mas_i[j]:
            mas_name.append(mas1[i][1])
#console.print(opt, style="bold green")
console.print("продукты, которые можно употребить: ", *mas_name, style="bold green")
console.print("количество этих продуктов: ", *mas_count, style="bold green")

# очистка csv файла c данными
console.print('введите "1", если хотите очистить список продуктов, или "0" в ином случае', style="bold red")
check = int(input())
if check == 1:
    for step in track(range(100), description='[green]Progress'):
        process_data()
    f = open("dataset_course2.csv", "w")
    f.truncate()
    f.close()
    console.print('список продуктов успешно очищен', style="bold red")
elif check == 0:
    for step in track(range(100), description='[green]Progress'):
        process_data()
    console.print('список продуктов не очищен', style="bold red")

while(True):
    l = input()