from Elevator import STATE


class People:
    def __init__(self, direction, cur_floor, target_floor):
        self.direction = direction
        self.cur_floor = cur_floor
        self.target_floor = target_floor
        self.state()

    def state(self):
        print "I wanna go from {0} to {1}, direction is {2}. ".format(
            self.cur_floor, self.target_floor, STATE[self.direction])
