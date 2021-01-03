'''
wumpus.py

Weather has been implemented into the wumpus world, using ID3, SVM and ANN
classification algorithms to determine when the arrow can or cannot be shot.

@author: Rajesh Sakhamuru
@version: 11/30/2019
'''
# Hunt the Wumpus
# From a vintage BASIC game program
# by CREATIVE COMPUTING MORRISTOWN, NEW JERSEY
# Rewritten in Python by Gordon Reeder
# Python 3.4
# ** To do **
# - Make connections within cave random. So that no two caves are the same.

import random
import sys
from weather.weather_ID3_SVM_ANN import WeatherClassify


def show_instructions():
    print ("""
        WELCOME TO 'HUNT THE WUMPUS'
        THE WUMPUS LIVES IN A CAVE OF 20 ROOMS. EACH ROOM
        HAS 3 TUNNELS LEADING TO OTHER ROOMS. (LOOK AT A
        DODECAHEDRON TO SEE HOW THIS WORKS-IF YOU DON'T KNOW
        WHAT A DODECHADRON IS, ASK SOMEONE, or Google it.)
        
    HAZARDS:
        BOTTOMLESS PITS: TWO ROOMS HAVE BOTTOMLESS PITS IN THEM
        IF YOU GO THERE, YOU FALL INTO THE PIT (& LOSE!)
        SUPER BATS: TWO OTHER ROOMS HAVE SUPER BATS. IF YOU
        GO THERE, A BAT GRABS YOU AND TAKES YOU TO SOME OTHER
        ROOM AT RANDOM. (WHICH MIGHT BE TROUBLESOME)
    WUMPUS:
        THE WUMPUS IS NOT BOTHERED BY THE HAZARDS (HE HAS SUCKER
        FEET AND IS TOO BIG FOR A BAT TO LIFT). USUALLY
        HE IS ASLEEP. TWO THINGS THAT WAKE HIM UP: YOUR ENTERING
        HIS ROOM OR YOUR SHOOTING AN ARROW.
        IF THE WUMPUS WAKES, HE MOVES (P=.75) ONE ROOM
        OR STAYS STILL (P=.25). AFTER THAT, IF HE IS WHERE YOU
        ARE, HE TRAMPLES YOU (& YOU LOSE!).
    YOU:
        EACH TURN YOU MAY MOVE OR SHOOT AN ARROW
        MOVING: YOU CAN GO ONE ROOM (THRU ONE TUNNEL)
        ARROWS: YOU HAVE 5 ARROWS. YOU LOSE WHEN YOU RUN
        OUT. YOU AIM BY TELLING
        THE COMPUTER THE ROOM YOU WANT THE ARROW TO GO TO.
        IF THE ARROW HITS THE WUMPUS, YOU WIN.
    WARNINGS:
        WHEN YOU ARE ONE ROOM AWAY FROM WUMPUS OR A HAZARD,
        THE COMPUTER SAYS:
        WUMPUS:   'I SMELL A WUMPUS'
        BAT   :   'BATS NEAR BY'
        PIT   :   'I FEEL A DRAFT'
        """)


class Room:
    """Defines a room. 
    A room has a name (or number),
    a list of other rooms that it connects to.
    and a description. 
    How these rooms are built into something larger 
    (cave, dungeon, skyscraper) is up to you.
    """

    def __init__(self, **kwargs):
        self.number = 0
        self.name = ''
        self.connects_to = []  # These are NOT objects
        self.description = ""

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return str(self.number)

    def remove_connect(self, arg_connect):
        if arg_connect in self.connects_to:
            self.connects_to.remove(arg_connect)

    def add_connect(self, arg_connect):
        if arg_connect not in self.connects_to:
            self.connects_to.append(arg_connect)

    def is_valid_connect(self, arg_connect):
        return arg_connect in self.connects_to

    def get_number_of_connects(self):
        return len(self.connects_to)

    def get_connects(self):
        return self.connects_to

    def describe(self):
        if len(self.description) > 0:
            print(self.description)
        else:
            print("You are in room {}.\nPassages lead to {}".format(self.number, self.connects_to))


class Thing:
    """Defines the things that are in the cave.
    That is the Wumpus, Player, pits and bats.
    """

    def __init__(self, **kwargs):
        self.location = 0  # this is a room object

        for key, value in kwargs.items():
            setattr(self, key, value)

    def move(self, a_new_location):
        if a_new_location.number in self.location.connects_to or a_new_location == self.location:
            self.location = a_new_location
            return True
        else:
            return False

    def validate_move(self, a_new_location):
        return a_new_location.number in self.location.connects_to or a_new_location == self.location

    def get_location(self):
        return self.location.number

    def wakeup(self, a_cave):
        if random.randint(0, 3):  # P=.75 that we will move.
            self.location = a_cave[random.choice(self.location.connects_to) - 1]

    def is_hit(self, a_room):
        return self.location == a_room


def create_things(a_cave):

    Things = []
    Samples = random.sample(a_cave, 6)
    for room in Samples:
        Things.append(Thing(location=room))

    return Things


def create_cave():
    # First create a list of all the rooms.
    for number in range(20):
        Cave.append(Room(number=number + 1))

    # Then stich them together.
    for idx, room in enumerate(Cave):

        # connect to room to the right
        if idx == 9:
            room.add_connect(Cave[0].number)
        elif idx == 19:
            room.add_connect(Cave[10].number)
        else:
            room.add_connect(Cave[idx + 1].number)

        # connect to the room to the left
        if idx == 0:
            room.add_connect(Cave[9].number)
        elif idx == 10:
            room.add_connect(Cave[19].number)
        else:
            room.add_connect(Cave[idx - 1].number)

        # connect to the room in the other ring
        if idx < 10:
            room.add_connect(Cave[idx + 10].number)  # I connect to it.
            Cave[idx + 10].add_connect(room.number)  # It connects to me.


def weather():
    """
    Randomly generate weather for all 20 rooms
    """

    weatherList = []

    for n in range(20):

        outlook = random.choice([115, 111, 114])
        temperature = random.choice(range(64, 86))
        humidity = random.choice(range(65, 96))
        windy = random.choice([102, 116])

        weatherList.append([outlook, temperature, humidity, windy])
        n += 0

    return weatherList


def weatherString(weather):
    """
    Print the weather from an array describing the weather from weatherList
    """
    outlook = ""
    temperature = weather[1]
    humidity = weather[2]
    windy = ""

    if weather[0] == 115:
        outlook = "sunny"
    elif weather[0] == 111:
        outlook = "overcast"
    else:
        outlook = "rainy"

    if weather[3] == 102:
        windy = "not windy"
    else:
        windy = "windy"

    weatherString = "It is " + outlook + ", " + str(temperature) + " degrees, " \
    +str(humidity) + "% humidity, and it is " + windy + "."

    return weatherString

# ============ BEGIN HERE ===========


Cave = []
create_cave()

# Make player, wumpus, bats, pits and put into cave.

Wumpus, Player, Pit1, Pit2, Bats1, Bats2 = create_things(Cave)

Arrows = 5

# Using given weather data, ID3, SVM and ANN classifiers for whether the
# arrow can be fired or not in the current conditions is generated.
# All 3 models vote to determine whether the arrow can be fired or not.
classifier = WeatherClassify()

# Array of randomly generated weather for all 20 rooms in the cave
weather = weather()

# # Can fire arrow or not for all 20 rooms will print if uncommented
# for n in range(20):
#     print(n + 1, ": ", weather[n] , ": " , classifier.predict(weather[n]))

# Now play the game

print("""\n   Welcome to the cave, Great White Hunter.
    You are hunting the Wumpus.
    On any turn you can move or shoot.
    Commands are entered in the form of ACTION LOCATION
    IE: 'SHOOT 12' or 'MOVE 8'
    type 'HELP' for instructions.
    'QUIT' to end the game.
    """)

while True:
    Player.location.describe()

    print(weatherString(weather[Player.location.number - 1]))
    canKillWumpus = classifier.predict(weather[Player.location.number - 1])

    print("Arrows remaining:", Arrows)

    # Check each <Player.location.connects_to> for hazards.
    for room in Player.location.connects_to:
        if Wumpus.location.number == room:
            print("I smell a Wumpus!")
            if canKillWumpus == 0:
                print("Bad Weather! Cannot SHOOT Wumpus from here!")
            else:
                print("Great Weather! Can SHOOT Wumpus from here!")
        if Pit1.location.number == room or Pit2.location.number == room:
            print("I feel a draft!")
        if Bats1.location.number == room or Bats2.location.number == room:
            print("Bats nearby!")

    raw_command = input("\n> ")
    command_list = raw_command.split(' ')
    command = command_list[0].upper()
    if len(command_list) > 1:
        try:
            move = Cave[int(command_list[1]) - 1]
        except:
            print("\n **What??")
            continue
    else:
        move = Player.location

    if command == 'HELP' or command == 'H':
        show_instructions()
        continue

    elif command == 'QUIT' or command == 'Q':
        print("\nOK, Bye.")
        sys.exit()

    elif command == 'MOVE' or command == 'M':
        if Player.move(move):
            if Player.location == Wumpus.location:
                print("... OOPS! BUMPED A WUMPUS!")
                Wumpus.wakeup(Cave)
        else:
            print("\n **You can't get there from here")
            continue

    elif command == 'SHOOT' or command == 'S':
        if Player.validate_move(move) and canKillWumpus == 1:
            print("\n-Twang-")
            if Wumpus.location == move:
                print("\n Good Shooting!! You hit the Wumpus. \n Wumpi will have their revenge.\n")
                sys.exit()
        elif canKillWumpus == 0:
            print("\n** BAD WEATHER! Cannot fire arrow!")
            continue
        else:
            print("\n** Stop trying to shoot through walls.")

        Wumpus.wakeup(Cave)
        Arrows -= 1
        if Arrows == 0:
            print("\n You are out of arrows\n Better luck next time\n")
            sys.exit()

    else:
        print("\n **What?")
        continue

    # By now the player has moved. See what happened.
    # Handle problems with pits, bats and wumpus.

    if Player.location == Bats1.location or Player.location == Bats2.location:
        print("ZAP--SUPER BAT SNATCH! ELSEWHEREVILLE FOR YOU!")
        Player.location = random.choice(Cave)

    if Player.location == Wumpus.location:
        print("TROMP TROMP - WUMPUS GOT YOU!\n")
        sys.exit()

    elif Player.location == Pit1.location or Player.location == Pit2.location:
        print("YYYIIIIEEEE . . . FELL INTO A PIT!\n China here we come!\n")
        sys.exit()

    else:  # Keep playing
        pass

