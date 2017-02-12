STATE_IDLE = -1
STATE_MVUP = 0
STATE_MVDN = 1
STATE = [
    'STATE_MVUP',
    'STATE_MVDN',
    'STATE_IDLE',
]


class Elevator:
    def __init__(self, uid, number_of_floor):
        self.uid = uid
        self.floors = number_of_floor
        self.cur_floor = 1
        self.target_floor = 1
        self.target_floors = [1]

        self.state = STATE_IDLE
        self.future_state = STATE_IDLE

        # people to certain floor
        self.people_to_floors = {i:[] for i in range(number_of_floor + 1)}
        print("init elevator_{0}".format(self.uid))

    def print_status(self):
        string = "This is elevator_{0} to floor {1}, go to {2}, STATE:{3}, people:{4}"\
            .format(self.uid, self.cur_floor, self.target_floor, STATE[self.state], str(self.people_to_floors))
        print string

    def move(self):
        if self.target_floor > self.cur_floor:
            self.cur_floor += 1
            self.state = STATE_MVUP
        elif self.target_floor < self.cur_floor:
            self.cur_floor -= 1
            self.state = STATE_MVDN
        else:
            self.state = STATE_IDLE

    def pickup_on_floor(self, query_floor, direction):
        # add the floor to pick up people
        if self.state == STATE_IDLE:
            self.target_floor = query_floor
            self.target_floors.append(query_floor)
            if self.target_floor > self.cur_floor:
                self.state = STATE_MVUP
            elif self.target_floor < self.cur_floor:
                self.state = STATE_MVDN
            else:
                self.state = direction
        else:
            if self.state == STATE_MVDN:
                if query_floor not in self.target_floors:
                    self.target_floors.append(query_floor)
                    self.target_floor = min(self.target_floors)
            else:
                if query_floor not in self.target_floors:
                    self.target_floors.append(query_floor)
                    self.target_floor = max(self.target_floors)

    def can_pickup(self, query_floor, direction):
        # if query floor is on its way, or it's idle now, then it can go
        distance = abs(self.cur_floor - query_floor)
        if self.state == STATE_IDLE:
            return True, distance
        elif self.state == STATE_MVUP == direction:
            if self.cur_floor > query_floor:
                return False, -1
            else:
                return True, distance
        elif self.state == STATE_MVDN == direction:
            if self.cur_floor < query_floor:
                return False, -1
            else:
                return True, distance
        else:
            return False, -1

    def action(self, people_outside):
        # see if arrive at
        if self.cur_floor in self.target_floors:
            self.target_floors.remove(self.cur_floor)
            # people get out
            while len(self.people_to_floors[self.cur_floor]) != 0:
                self.people_to_floors[self.cur_floor].pop()
            # if empty
            if len(self.target_floors) == 0:
                self.state = self.future_state

            # people get in
            cur_floor_people_outside = people_outside[self.cur_floor][self.state]
            while not cur_floor_people_outside.empty():
                people = cur_floor_people_outside.get()
                self.people_to_floors[people.target_floor].append(people)
                self.pickup_on_floor(people.target_floor, people.direction)



