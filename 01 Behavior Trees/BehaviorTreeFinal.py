"""

COMP 131 AI
HW 01 Behavior Tree for Roomba
Feb 9 2020
@author: Jiawei Wang

"""


"""
# This is a very straightforward program, please run it in command line or IDE, use keyboard for input 
# Let us assume that 1 second of cleaning consumes 1% of battery
# In order to implement the behavior tree, we need to do the following things:
# Define all node types; define all functions; initialize the tree and run the tree with input from blackboard
"""


"""
# First we need to define a new class for every type of node in the chart
"""


# Parent node type for all sub-types
class BaseNode:
    def __init__(self, children, blackboard):
        self.children = []
        self.children = children.copy()
        self.blackboard = blackboard
        self.name = None

    def update_running(self):
        self.blackboard.running = self
        string = self.name + "--> RUNNING" + "\n"
        self.blackboard.log += string

    def update_failed(self):
        self.blackboard.failed = self
        string = self.name + "--> FAILED" + "\n"
        self.blackboard.log += string

    def update_success(self):
        self.blackboard.success = self
        string = self.name + "--> SUCCESS" + "\n"
        self.blackboard.log += string

    def zap_battery(self, num=None):
        if not num:
            self.blackboard.battery_level -= 1
            string = "BATTERY LEVEL: " + str(self.blackboard.battery_level) + "\n"
            self.blackboard.log += string
        else:
            self.blackboard.battery_level -= num
            string = "BATTERY LEVEL: " + str(self.blackboard.battery_level) + "\n"
            self.blackboard.log += string


# Decorator node type
class Decorator(BaseNode):
    def __init__(self, task_node, blackboard):
        self.task = task_node
        self.name = None
        self.blackboard = blackboard

    def run(self):
        self.update_running()
        self.task.run()
        self.update_success()
        print(self.name+"--> SUCCESS")
        return True


class Timer(Decorator):
    def __init__(self, task_node, time, blackboard):
        self.task = task_node
        self.name = "Timer"
        self.time = time
        self.blackboard = blackboard

    def run(self):
        self.update_running()
        print("Execute", self.task.name, "for", self.time, "seconds")
        zap_amount = int(self.time)
        self.zap_battery(zap_amount)
        self.task.run()


class LogicalNegation(Decorator):
    def __init__(self, task_node, blackboard):
        self.task = task_node
        self.name = "Logical Negation"
        self.blackboard = blackboard

    def run(self):
        self.update_running()
        bool_val = self.task.run()
        if bool_val:
            self.update_failed()
            return False
        else:
            self.update_success()
            return True


class UntilFail(Decorator):
    def __init__(self, task_node, blackboard):
        self.task = task_node
        self.name = "Until Fail"
        self.blackboard = blackboard

    def run(self):
        self.update_running()
        while self.task.run():
            self.task.run()

        self.update_failed()
        return False


# Conditional node type
class Conditions(BaseNode):
    def __init__(self):
        self.name = None


class BatteryCheck(Conditions):
    def __init__(self, blackboard):
        self.blackboard = blackboard
        self.name = "Battery Check"

    def run(self):
        if self.blackboard.battery_level < 30:
            self.update_success()
            print("Battery level is low!")
            return True
        else:
            print("Battery level is above charging threshold.")
            self.update_failed()
            return False


class Spot(Conditions):
    def __init__(self, blackboard):
        self.name = "Spot"
        self.blackboard = blackboard

    def run(self):
        if self.blackboard.spot:
            self.update_success()
            print("Spot Clean Mode: --> On")
            return True
        else:
            self.update_failed()
            return False


class General(Conditions):
    def __init__(self, blackboard):
        self.name = "General"
        self.blackboard = blackboard

    def run(self):
        if self.blackboard.general:
            self.update_success()
            print("General Clean Mode: --> On")
            return True
        else:
            self.update_failed()
            return False


class DustySpot(Conditions):
    def __init__(self, blackboard):
        self.name = "Dusty Spot"
        self.blackboard = blackboard

    def run(self):
        if self.blackboard.spot:
            self.update_success()
            print("Dusty Spot Mode: --> On")
            return True
        else:
            self.update_failed()
            return False


# Composite node type
class Composite(BaseNode):
    def __init__(self, children, blackboard):
        self.children = []
        self.children = children.copy()
        self.blackboard = blackboard

    def run(self):
        pass


class Priority(Composite):
    def run(self):
        self.name = "Priority"
        self.update_running()
        self.children = sorted(self.children, key=lambda tup: tup[1])
        for i in self.children:
            i[0].run()
        self.update_success()


class Sequence(Composite):
    def run(self):
        self.name = "Sequence"
        self.update_running()
        for i in self.children:
            if not i.run():
                self.update_failed()
                return False
        self.update_success()
        return True


class Selection(Composite):
    def run(self):
        self.name = "Selection"
        self.update_running()
        fail_list = []
        for i in self.children:
            fail_list.append(i.run())
        for i in fail_list:
            if i:
                return True
        return False


# Task node type
class Task(BaseNode):
    def __init__(self, blackboard):
        self.name = None
        self.blackboard = blackboard

    def run(self):
        self.update_running()
        self.zap_battery()
        self.update_success()
        print("Executing", self.name)
        return True


class FindHome(Task):
    def run(self):
        self.name = "Find Home"
        self.update_running()
        home_path = self.blackboard.home_path
        self.zap_battery()
        self.update_success()
        print("Executing", self.name)
        return True


class GoHome(Task):
    def run(self):
        self.name = "Go Home"
        self.update_running()
        self.blackboard.home_path = "Go home --> SUCCESS"
        self.zap_battery()
        self.update_success()
        print("Executing", self.name)
        return True


class Dock(Task):
    def run(self):
        self.name = "Dock"
        self.update_running()
        charge_time = int(input("How long would you like to charge? (1% per second): "))
        if self.blackboard.battery_level + charge_time > 100:
            charge_time = 100 - self.blackboard.battery_level
            print("Max charge level is 100%. Roomba will charge", charge_time, "seconds.")
            self.blackboard.battery_level = 100
        else: self.blackboard.battery_level += charge_time
        self.blackboard.log += "BATTERY LEVEL:" + str(self.blackboard.battery_level) + "\n"
        self.update_success()
        print("Executing charging")
        print("All charged up and ready to clean!")
        return True


class SpotCleaning(Task):
    def __init__(self, blackboard):
        self.name = "Spot Cleaning"
        self.blackboard = blackboard

    def run(self):
        self.update_running()
        self.zap_battery()
        self.update_success()
        print("Executing", self.name)
        self.blackboard.spot = False
        return True


class DoneSpot(Task):
    def __init__(self, blackboard):
        self.name = "Spot Cleaning: --> SUCCESS"
        self.blackboard = blackboard


class GeneralCleaning(Task):
    def __init__(self, blackboard):
        self.name = "General Cleaning"
        self.blackboard = blackboard


class DoNothing(Task):
    def __init__(self, blackboard):
        self.name = "Do Nothing"
        self.blackboard = blackboard


class DoneGeneral(Task):
    def __init__(self, blackboard):
        self.name = "General Cleaning: --> SUCCESS"
        self.blackboard = blackboard

    def run(self):
        self.update_running()
        self.zap_battery()
        self.update_success()
        print("Executing", self.name)
        self.blackboard.general = False
        return True


"""
# Second we need to define the Behavior Tree
"""


class roomba:
    def __init__(self):
        self.head = None
        self.blackboard = blackboard()

    def setHead(self, head):
        self.head = head

    def runTree(self, num):
        string = "\nRoom Number: " + str(num + 1) + "\n"
        separate = "---------------------------" + "\n"
        self.blackboard.log += string
        self.blackboard.log += separate
        self.head.run()


# Tree initiation function
def behaviorTree(roomba):
    # Battery level check
    battery = BatteryCheck(roomba.blackboard)
    find_home = FindHome(roomba.blackboard)
    go_home = GoHome(roomba.blackboard)
    dock = Dock(roomba.blackboard)
    battery_check = [battery, find_home, go_home, dock]
    left_subtree = Sequence(battery_check, roomba.blackboard)

    # Spot cleaning
    spot = Spot(roomba.blackboard)
    clean_spot_task = SpotCleaning(roomba.blackboard)
    clean_spot = Timer(clean_spot_task, 20, roomba.blackboard)
    done_spot = DoneSpot(roomba.blackboard)
    spot_cleaning = [spot, clean_spot, done_spot]
    mid_left_subtree = Sequence(spot_cleaning, roomba.blackboard)

    # General cleaning (from bottom to top)
    # Bottom level
    d_spot = DustySpot(roomba.blackboard)
    clean = SpotCleaning(roomba.blackboard)
    timer = Timer(clean, 35, roomba.blackboard)
    bottom_level = [d_spot, timer]
    bottom_seq = Sequence(bottom_level, roomba.blackboard)

    # 4th level
    clean2 = GeneralCleaning(roomba.blackboard)
    forth_level = [bottom_seq, clean2]
    forth_sel = Selection(forth_level, roomba.blackboard)

    # 3rd level
    third_battery = BatteryCheck(roomba.blackboard)
    logical_negation = LogicalNegation(third_battery, roomba.blackboard)
    third_level = [logical_negation, forth_sel]
    third_seq = Sequence(third_level, roomba.blackboard)
    until_fail_seq = UntilFail(third_seq, roomba.blackboard)

    # 2nd level
    done_general = DoneGeneral(roomba.blackboard)
    second_level = [until_fail_seq, done_general]
    second_seq = Sequence(second_level, roomba.blackboard)
    gen_check = General(roomba.blackboard)

    # Top level
    top_level = [gen_check, second_seq]

    # Combine Spot cleaning and General cleaning
    mid_right_subtree = Sequence(top_level, roomba.blackboard)
    mid_tree_list = [mid_left_subtree, mid_right_subtree]
    mid_subtree = Selection(mid_tree_list, roomba.blackboard)

    # Do nothing
    do_nothing = DoNothing(roomba.blackboard)
    right_subtree = do_nothing

    # Behavior Tree root initialization
    priority_left = (left_subtree, 1)
    priority_mid = (mid_subtree, 2)
    priority_right = (right_subtree, 3)

    children = [priority_left, priority_mid, priority_right]
    priority_root = Priority(children, roomba.blackboard)
    roomba.setHead(priority_root)


# Input recognition
def trueOrFalse(answer):
    if answer.lower() == "y" or answer.lower() == "yes":
        return True
    return False


"""
# Last we need to initialize and run the tree with input from blackboard
"""


# A blackboard has 2 functions: 1. to store the initialization input; 2. to store the executing info
# Blackboard initiation
class blackboard:
    def __init__(self):
        self.battery_level = int(input("Enter initial battery level: "))
        self.spot = trueOrFalse(input("Do you want to run a spot clean? (Y/N): "))
        self.general = trueOrFalse(input("Do you want to run a general clean? (Y/N): "))
        self.dusty_spot = trueOrFalse(input("Is there a dusty spot? (Y/N): "))
        self.home_path = "This is a home path"
        self.running = None
        self.failed = None
        self.success = None
        self.log = str()


# Run the tree with input
def runRoomba():
    print('---------------------------------------------------------------')
    print('Roomba started. With every second, the battery decreases by 1%.')
    print('---------------------------------------------------------------')
    my_little_roomba = roomba()
    behaviorTree(my_little_roomba)
    loop = int(input("How many rooms would you like Roomba to clean? "))
    print('-----------------------------------------------')
    for i in range(0, loop):
        print("Room Number:", str(i+1))
        my_little_roomba.runTree(i)
        if i < loop - 1:
            print('-------------------------------------------------------')
            update = input("Would you like to change your blackboard settings?(Y/N)")
            if trueOrFalse(update):
                my_little_roomba.blackboard.spot = trueOrFalse(input("Enter spot (Y/N): "))
                my_little_roomba.blackboard.general = trueOrFalse(input("Enter general (Y/N): "))
                my_little_roomba.blackboard.dusty_spot = trueOrFalse(input("Enter dusty spot (Y/N): "))
    print('------------------------------------------------')
    print_log = trueOrFalse(input("Would you like to print the activity log? (Y/N) "))
    if print_log:
        print("\n", my_little_roomba.blackboard.log)
    print('----------------')
    print("MISSION COMPLETE")
    print('----------------')


runRoomba()

