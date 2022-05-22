import random
import copy
import pandas as pd
import os


def clear_console(): return os.system('cls')


COURSES = [
            ['AI 6H 0 0 2 0', 'AI 6G 0 1 2 1', 'AI 6F 0 2 2 2', 'AI 6J 1 0 3 0', 'AI 6D 1 1 3 1', 'AI 6B 1 2 3 2',
             'AI 6E 1 2 3 2', 'AI 6C 1 3 3 3', 'AI 6A 2 2 4 2'],
            ['PDC 6C 0 0 2 0', 'PDC 6E 0 0 2 0', 'PDC 6F 0 1 2 1', 'PDC 6D 0 3 2 3', 'PDC 6A 1 1 3 1',
             'PDC 6B 1 3 3 3', 'PDC 8A 1 5 3 5'],
            ['DIP 6A 0 0 2 0', 'DIP 6B 0 2 2 2', 'DIP 6B 0 3 2 3'],
            ['SE 6A 0 1 3 1', 'SE 6B 1 1 3 1', 'SE 6E 1 3 3 3', 'SE 6C 1 1 3 1', 'SE 6D 1 2 3 2',
             'SE 6F 1 0 4 0'],
            ['OB 6A 1 4 3 4', 'OB 6B 0 5 2 5']
]
COURSES_NAME = ['AI', 'PDC', 'DIP', 'SE', 'OB']
FITNESS_CONDITIONS = []
TIME = ['8:30-10:00', '10:00-11:30', '11:30-1:00', '1:00-2:30', '2:30-4:00', '4:00-5:30']
DAY = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']

POPULATION = []
BUFFER = []
POPULATION_SIZE = 500
BEST_FIT = 0.2
CROSSOVER = 0.4
MUTATION = 0.4


def take_user_input():
    print('Choose the off day')
    print('#0 for Monday')
    print('#1 for Tuesday')
    print('#2 for Wednesday')
    print('#3 for Thursday')
    print('#4 for Friday')
    day = int(input('Option # '))
    off_days = [day]
    FITNESS_CONDITIONS.append(off_days)

    print('Choose # of consecutive classes')
    print('#1 for 1')
    print('#2 for 2')
    print('#3 for 3')
    consecutive = int(input('Option # '))
    FITNESS_CONDITIONS.append(consecutive)
    print('Choose last class time for the day')
    print('#0 for 4:00-5:30')
    print('#1 for 2:30-4:00')
    last = 6 - int(input('Option # '))
    FITNESS_CONDITIONS.append(last)
    print('Choose first class time for the day')
    print('#0 for 8:30-10:00')
    print('#1 for 10:00-11:30')
    print('#2 for 11:30-1:00')
    first = int(input('Option # '))
    FITNESS_CONDITIONS.append(first)


class Sample:
    def __init__(self, timetable, fitness_val):
        self.timetable = timetable,
        self.fitness_val = fitness_val

    def print_timetable(self):
        print(TIME)
        for _itr in self.timetable:
            for course in _itr:
                print(course)

    def remove_course_return_index(self, course_name):
        _days = []
        _time = []
        _section = ""
        days_count = 0
        for _itr in self.timetable:
            for days in _itr:
                time_count = 0
                for time in days:
                    index = 0
                    for course in time:
                        if course.find(course_name) != -1:
                            _split = course.split()
                            _section = _split[1]
                            _days.append(days_count)
                            _time.append(time_count)
                            del time[index]

                        index += 1
                    time_count += 1
                days_count += 1

        return _days, _time, _section

    def __lt__(self, other):
        return self.fitness_val < other.fitness_val

    def __gt__(self, other):
        return self.fitness_val > other.fitness_val


def calculate_fitness(tt):
    value = 0
    days_off = FITNESS_CONDITIONS[0]
    for _i in days_off:
        for j in tt[_i]:
            if len(j) != 0:
                value += 500
    classes = FITNESS_CONDITIONS[1]

    for _i in tt:
        consecutive = 0
        for j in _i:
            if len(j) != 0:
                consecutive += 1
            else:
                consecutive = 0
            if consecutive > classes:
                value += 2
            if len(j) > 1:
                value += (500 * len(j))

    max_time = FITNESS_CONDITIONS[2]
    min_time = FITNESS_CONDITIONS[3]
    for _i in tt:
        for j in range(max_time, 6):
            if len(_i[j]) != 0:
                value += 10
    for _i in tt:
        for j in range(0, min_time):
            if len(_i[j]) != 0:
                value += 10

    return value


def generate_timetable():
    tt = []
    for _i in range(5):
        tt.append([])
        for j in range(6):
            tt[_i].append([])

    for _i in range(5):
        index = random.randint(0, len(COURSES[_i])-1)
        _split = COURSES[_i][index].split()
        course = _split[0] + " " + _split[1]
        tt[int(_split[2])][int(_split[3])].append(course)
        tt[int(_split[4])][int(_split[5])].append(course)
    return tt


def generate_population():
    for _i in range(POPULATION_SIZE):
        tt = generate_timetable()
        value = calculate_fitness(tt)
        sample_tt = Sample(tt, value)
        POPULATION.append(sample_tt)


def filter_best_fit():
    BUFFER.clear()
    for _i in range(int(BEST_FIT*POPULATION_SIZE)):
        BUFFER.append(POPULATION[_i])


def apply_crossover():
    for _i in range(int(CROSSOVER*POPULATION_SIZE)):
        # pick two parent samples at random
        parent_one = random.randint(0, POPULATION_SIZE // 2)
        parent_two = random.randint(parent_one + 1, POPULATION_SIZE - 1)
        # pick course to swap
        course = COURSES_NAME[random.randint(0, (len(COURSES_NAME)-1))]

        child_1 = copy.deepcopy(POPULATION[parent_one])
        child_2 = copy.deepcopy(POPULATION[parent_two])

        child_1.remove_course_return_index(course)
        day_2, time_2, section_2 = child_2.remove_course_return_index(course)
        course_2 = course + " " + section_2
        child_1.timetable[0][day_2[0]][time_2[0]].append(course_2)
        child_1.timetable[0][day_2[1]][time_2[1]].append(course_2)
        BUFFER.append(child_1)


def apply_mutation():
    for _i in range(int(MUTATION * POPULATION_SIZE)):
        course = COURSES_NAME[random.randint(0, (len(COURSES_NAME)-1))]
        # pick the sample on which you need to apply mutation on
        _parent = random.randint(0, POPULATION_SIZE - 1)
        mutant = copy.deepcopy(POPULATION[_parent])
        mutant.remove_course_return_index(course)
        _index = 0
        for _itr in COURSES:
            if _itr[0].find(course) != -1:
                break
            _index += 1
        index = random.randint(0, (len(COURSES[_index])-1))
        _split = COURSES[_index][index].split()
        course = _split[0] + " " + _split[1]
        mutant.timetable[0][int(_split[2])][int(_split[3])].append(course)
        mutant.timetable[0][int(_split[4])][int(_split[5])].append(course)
        BUFFER.append(mutant)


def buffer_to_population():
    # helper function to copy data from buffer to population
    POPULATION.clear()
    for _i in range(POPULATION_SIZE):
        BUFFER[_i].fitness_val = calculate_fitness(BUFFER[_i].timetable[0])
        POPULATION.append(BUFFER[_i])
    BUFFER.clear()


take_user_input()

generate_population()
POPULATION.sort()
itr = 0


clear_console()
print('CALCULATING...')
while POPULATION[0].fitness_val != 0 and itr < 100:
    # print(POPULATION[0].fitness_val, " Iteration : ", itr)
    filter_best_fit()
    apply_crossover()
    apply_mutation()
    buffer_to_population()
    POPULATION.sort()
    itr += 1


clear_console()

if POPULATION[0].fitness_val == 0:
    print("Target Reached")
else:
    print("Iteration Limit Reached (Best Samples)")


df_0 = pd.DataFrame(POPULATION[0].timetable[0], columns=TIME, index=DAY)
print(df_0)
print('--------------------------------------------------------------------------')
df_1 = pd.DataFrame(POPULATION[1].timetable[0], columns=TIME, index=DAY)
print(df_1)
print('--------------------------------------------------------------------------')
df_2 = pd.DataFrame(POPULATION[2].timetable[0], columns=TIME, index=DAY)
print(df_2)

e = "e"
while e != "":
    e = input('Press enter key to exit')
