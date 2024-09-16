import matplotlib.pyplot as plt
import numpy as np

# не будет вылезать иконка Python
import matplotlib
matplotlib.use("Agg")

# ages = [23, 45, 32, 13, 76]


# Построение графика статистики по возрасту зарегистрированных пользователей
def make_graph_age(ages):
    age_groups = {(0, 20): 0,
                  (21, 30): 0,
                  (31, 40): 0,
                  (41, 50): 0,
                  (51, 60): 0,
                  (61, 70): 0,
                  (71, 100): 0}
    for a in ages:
        for key in age_groups:
            if key[0] <= a <= key[1]:
                age_groups[key] += 1
    groups = [f'{str(i[0])}-{str(i[1])}' for i in list(age_groups.keys())]
    values_1 = list(age_groups.values())
    plt.bar(groups, values_1, color='orange')  # Посроение столбчатой диаграммы
    plt.yticks(np.arange(min(values_1), max(values_1)+1, 1.0))  # изменяем шаг делений на оси y до целых значений
    plt.xlabel('Возрастная группа')  # Подпись для оси х
    plt.ylabel('Кол-во человек')  # Подпись для оси y
    plt.title('Статистика пользователей по возрасту')  # Название
    plt.savefig('sub_processes/age.png')  # Сохранение графика
    plt.close(fig='all')


# Построение графика статистики по регионам зарегистрированных пользователей
def make_graph_region(regions):
    regions_dict = {'Азиатский регион': 0,
                    'Европа': 0,
                    'Латинская Америка': 0,
                    'Россия': 0,
                    'США': 0}
    for key in regions_dict.keys():
        value = regions.count(key)
        regions_dict[key] = value
    # keys = list(regions_dict.keys())
    values_2 = list(regions_dict.values())
    lower_names = ['Азиатский\nрегион', 'Европа', 'Латинская\nАмерика', 'Россия', 'США']
    plt.bar(lower_names, values_2, color='green')  # Посроение столбчатой диаграммы
    plt.yticks(np.arange(min(values_2), max(values_2)+1, 1.0))  # изменяем шаг делений на оси y до целых значений
    # plt.xlabel('Регион')  # Подпись для оси х
    plt.ylabel('Кол-во человек')  # Подпись для оси y
    plt.title('Статистика пользователей по региону')  # Название
    plt.savefig('sub_processes/region.png')  # Сохранение графика
    plt.close(fig='all')
