from Elevator import Elevator
from Queue import Queue
from People import People

class ElevatorControlSystem:
    def __init__(self, number_of_elevator, number_of_floor):
        self.elevators = [Elevator(i, number_of_floor) for i in range(number_of_elevator)]
        self.floors = number_of_floor

        # people start from certain floor that have a elevator come for them
        self.people_from_floors = [[Queue(), Queue()] for i in range(number_of_floor + 1)]

        # people cannot get elevators come to them
        self.waitlist = Queue()

    def step(self):
        # every elevator do something like get people in and out then move
        for elevator in self.elevators:
            elevator.action(self.people_from_floors)
            elevator.move()
        # check waitlist
        if not self.waitlist.empty():
            qsz = self.waitlist.qsize()
            for i in range(qsz):
                people = self.waitlist.get()
                self.pickup(people)

    def pickup(self, people):
        distances = []
        # choose the elevator that can pick people
        for elevator in self.elevators:
            query_result = elevator.can_pickup(people.cur_floor, people.direction)
            if query_result[0]:
                distances.append((query_result[1], elevator.uid))

        # if current no elevator available, add people to waitlist
        if len(distances) == 0:
            self.waitlist.put(people)
        else:
            # if there are more than one elevator can pick, choose the nearest one
            min_dist = min(distances)
            # tell elevator it has been chosen
            self.elevators[min_dist[1]].pickup_on_floor(people.cur_floor, people.direction)
            # arrange this people to the list
            self.people_from_floors[people.cur_floor][people.direction].put(people)
            # change elevator future state
            self.elevators[min_dist[1]].future_state = people.direction

    def status(self):
        for elevator in self.elevators:
            elevator.print_status()


if __name__ == '__main__':
    elevator_num = raw_input('How many elevators: ')
    floor_num = raw_input('How many floors: ')
    ecs = ElevatorControlSystem(int(elevator_num), int(floor_num))
    ecs.status()

    while True:
        behavior = raw_input('Enter behavior: ')
        if len(behavior) == 0:
            ecs.step()
        elif behavior[0] == 'p':
            parts = behavior.split(',')
            people = People(int(parts[1]), int(parts[2]), int(parts[3]))
            ecs.pickup(people)
        ecs.status()
