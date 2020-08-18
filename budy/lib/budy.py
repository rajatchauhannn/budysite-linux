import json
import time
import random
from itertools import chain
import sys


# TODO Work on the algorithm for generating a workout with dummy values, also update json for filler exercises
# TODO Add breaks inbetween intervals of exercises and finish the compile process, start working on the gui


class chooseWorkout:
    area = 'CHEST'
    timming = 300

    def __init__(self, data):
        self.data = data
        self.optionslst = []
        self.num = 1
        for i in data:
            print(str(self.num) + '. ' + i)
            self.optionslst.extend([self.num, i])
            self.num += 1

        self.area = int(input('Choose from the list above'))
        for i in range(len(self.optionslst)):
            if self.optionslst[i] == self.area:
                self.area = self.optionslst[i + 1]
                break
        chooseWorkout.timming = int(input('Enter the timmings in minutes (default = 30min):'))
        chooseWorkout.area = self.area

    def select(self):

        self.num = 1
        for i in self.data[f'{self.area}']:
            print(str(self.num) + '. ' + i)
            self.optionslst.extend([self.num, i])
            self.num += 1

        self.info = int(input('Choose from the list above'))
        for i in range(len(self.optionslst)):
            if self.optionslst[i] == self.info:
                self.info = self.optionslst[i + 1]
                break

        for i in [self.data[f'{self.area}'][f'{self.info}']]:
            for j in i:
                print(j, ' : ', i[j])


class algoWorkout:

    def __init__(self, area, timming, data):
        self.area = area
        self.timming = timming
        self.data = data
        self.veasylst = []
        self.easylst = []
        self.hardlst = []
        self.vhardlst = []


    def add_duration_rest(self, lst):
        tlst = []
        for exercise in lst:
            tlst.extend([exercise, self.data[self.area][exercise]["duration"], self.data[self.area][exercise]["rest"]])
        print(tlst)
        return tlst

    def calculate_no_exercise(self, list, sum):
        tlst = []
        if list != None:
            if self.timming_left > 0 and sum > 0:
                avgtime = self.timming / sum
                for i in list:
                    if self.data[self.area][i]["rest"] + self.data[self.area][i]["duration"] <= avgtime:
                        tlst.append(i)
                    else:
                        continue
                if tlst != []:
                    return random.choice(tlst).split()
            elif self.timming == 0:
                return "Way too less time given."
            elif sum == 0:
                self.timming_done = True
                return "No exercise available"
        else:
            return "Database has missing values"
        return tlst

    def sort_difficulty(self, lst):
        if lst:
            tlist = []
            for i in lst:
                if i.isalpha() == True:
                    tlist.append(i)
            # This loop will sort them in ascending order of difficulty

            prevj = tlist[0]
            for j in tlist:
                if j.isalpha() == True:
                    if self.data[self.area][j]["difficulty"] < self.data[self.area][prevj]["difficulty"]:
                        tlist.remove(j)
                        tlist.insert(0, j)
                    else:
                        continue
                    prevj = j

            return tlist

    def add_exercises(self, lst, sum):
        length_of_list = len(lst)
        missing_value = 'Database has missing values'
        no_exercise = 'No exercise available'
        lack_of_time = 'Way too less time given.'
        while self.calculate_no_exercise(self.veasylst,self.sum) == [] or self.calculate_no_exercise(
            self.easylst, self.sum) == []:
            self.ve = self.calculate_no_exercise(self.veasylst, self.sum)
            self.e = self.calculate_no_exercise(self.easylst, self.sum)
            self.sum -= 1
        else:
            self.ve = self.calculate_no_exercise(self.veasylst, self.sum)
            self.e = self.calculate_no_exercise(self.easylst, self.sum)

            if self.ve == missing_value:
                self.ve = None
            elif self.e == missing_value:
                self.e = None

            if self.ve == no_exercise or self.e == no_exercise:
                return 'No exercise available'
            elif self.ve == lack_of_time or self.e == lack_of_time:
                return 'Way too less time given.'

            else:
                self.sum = sum
                self.h = self.calculate_no_exercise(self.hardlst, self.sum)
                self.vh = self.calculate_no_exercise(self.vhardlst, self.sum)
                # print('ve:', self.ve, 'e:', self.e, 'h:', self.h, 'vh:', self.vh)

                if self.h == missing_value:
                    self.h = []
                if self.vh == missing_value:
                    self.vh = []

                if self.ve == None:
                    if self.h != []:
                        if self.vh != []:
                            lst.extend([self.e, self.h, self.vh])
                        elif self.vh == []:
                            lst.extend([self.e, self.h])
                    elif self.h == []:
                        if self.vh != []:
                            lst.extend([self.e, self.vh])
                        elif self.vh == []:
                            lst.extend([self.e])

                elif self.e == None:
                    if self.h != []:
                        if self.vh != []:
                            lst.extend([self.ve, self.h, self.vh])
                        elif self.vh == []:
                            lst.extend([self.ve, self.h])
                    elif self.h == []:
                        if self.vh != []:
                            lst.extend([self.ve, self.vh])
                        elif self.vh == []:

                            lst.extend([self.ve])
                else:
                    if self.h != []:
                        if self.vh != []:
                            lst.extend([random.choice([self.ve, self.e]), self.h, self.vh])
                        elif self.vh == []:
                            lst.extend([random.choice([self.ve, self.e]), self.h])
                    elif self.h == []:
                        if self.vh != []:
                            lst.extend([random.choice([self.ve, self.e]), self.vh])
                        elif self.vh == []:
                            lst.extend([random.choice([self.ve, self.e])])

        if len(lst) == length_of_list:
            self.timming_done = True
            return lst
        else:
            return lst

    def compile_workout(self):
        """

        This function will compile the selected exercise (self.area) and make a list of exercises with all difficulties
        and respective rest/duration period. It will also update and form based on the timmings provided.

        This will also have all the loops/algorithm inorder to sort the routine.

        FINAL FORMAT : [<exercise>, <duration>, <rest>, .....]

        """

        # Check for excluded exercises


        # This loop will put divide exercies in lists of level: veryeasy(1-2), easy(3-5), hard(6-8), veryhard(9-10)
        for i in self.data[self.area]:
            if self.data[self.area][i]["enable"] == True:
                if self.data[self.area][i]["difficulty"] <= 2:
                    self.veasylst.append(i)
                if 3 <= self.data[self.area][i]["difficulty"] <= 5:
                    self.easylst.append(i)
                if 6 <= self.data[self.area][i]["difficulty"] <= 8:
                    self.hardlst.append(i)
                if 9 <= self.data[self.area][i]["difficulty"] <= 10:
                    self.vhardlst.append(i)

        self.veasylst = self.sort_difficulty(self.veasylst)
        self.easylst = self.sort_difficulty(self.easylst)
        self.hardlst = self.sort_difficulty(self.hardlst)
        self.vhardlst = self.sort_difficulty(self.vhardlst)

        print('Total Exercises:', self.veasylst, self.easylst, self.hardlst, self.vhardlst)

        sum_of_ex = 0
        # This loop is to find total no. of exercises available
        for k in ([self.veasylst, self.easylst, self.hardlst, self.vhardlst]):
            if k is not None:
                for i in k:
                    sum_of_ex += 1

        self.sum = sum_of_ex
        print("No. of total exercises = ", self.sum)

        self.tlst = []
        self.timming_done = False
        self.timming_left = self.timming

        while not self.timming_done:
            self.duration = 0
            for i in self.tlst:
                self.duration += self.data[self.area][i[0]]["rest"] + self.data[self.area][i[0]]["duration"]
            self.timming_left = self.timming - self.duration
            if self.timming > self.duration:
                self.tlst = self.add_exercises(self.tlst, sum_of_ex)
                if self.tlst == 'No exercise available':
                    return self.tlst
            else:
                self.timming_done = True

        while self.timming_left < 0:
            self.tlst.pop()
            self.duration = 0
            for i in self.tlst:
                self.duration += self.data[self.area][i[0]]["rest"] + self.data[self.area][i[0]]["duration"]
            self.timming_left = self.timming - self.duration


        #Unlist elements of self.tlst
        self.tlst = list(chain.from_iterable(self.tlst))

        return self.tlst




class displayWorkout:
    def __init__(self, data):
        self.tlst = list_of_workouts
        self.area = chooseWorkout.area
        self.data = data

    def show(self):
        print(self.tlst)
        time.sleep(3)
        for r in self.tlst:
            time_left = self.data[f'{self.area}'][f'{r}']['duration']
            while time_left > 0:
                time.sleep(1)
                sys.stdout.write(f'\r{r} %d' %time_left)
                sys.stdout.flush()
                time_left -= 1
            else:
                rest_left = self.data[f'{self.area}'][f'{r}']['rest']
                while rest_left > 0:
                    time.sleep(1)
                    sys.stdout.write('\rREST %d' %rest_left)
                    rest_left -= 1


# __main__

if __name__ == '__main__':
    with open('./budyjs.json') as budyjs:
        data = json.load(budyjs)
    #Takes area and timming and searches for exercies in the json
    totalworkouts = chooseWorkout(data)

    #Puts both area value amd timming value to process
    compileworkouts = algoWorkout(chooseWorkout.area, chooseWorkout.timming, data)

    list_of_workouts = compileworkouts.compile_workout()
    display_workouts = displayWorkout(data)
    display_workouts.show()

def phase1(area, time):
    with open('budy/lib/budyjs.json') as budyjs:
        data = json.load(budyjs)
    compileworkouts = algoWorkout(area, time, data)
    list_of_workouts = compileworkouts.compile_workout()
    list_of_workouts = compileworkouts.add_duration_rest(list_of_workouts)
    print(list_of_workouts)

    return list_of_workouts