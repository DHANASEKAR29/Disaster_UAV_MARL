from environment import DisasterEnvironment
from drone import Drone
from coverage import CoverageMap
from communication import Communication
from task_allocator import TaskAllocator
from qlearning import QLearning
from simulation.simulator import Simulator


def main():

    # Environment
    env = DisasterEnvironment()
    env.place_objects()

    # Communication
    communication = Communication()

    # Q Learning
    qlearning = QLearning()

    # Coverage
    coverage = CoverageMap(10)

    # Create Drones
    drones = []

    positions = env.get_drone_positions()

    for i, pos in enumerate(positions):

        drone = Drone(
            f"D{i+1}",
            pos[0],
            pos[1]
        )

        drones.append(drone)

        coverage.mark(pos[0], pos[1])

    # Allocate Zones
    allocator = TaskAllocator(drones)
    allocator.assign_zones()

    # Create Simulator
    simulator = Simulator(env)

    # Main Loop
    while True:

        # Move drones
        for drone in drones:

            if not drone.active:
                continue

            drone.move(
                env.grid,
                communication,
                qlearning,
                mode="qlearning"
            )

            coverage.mark(
                drone.x,
                drone.y
            )

            if drone.status == "Need Replacement":

                allocator.transfer_task(
                    drone,
                    communication
                )

        # Update Screen
        simulator.update(
            drones,
            coverage.get_coverage_percentage()
        )

        # Stop if all drones dead
        if all(not drone.active for drone in drones):
            break

    print("Simulation Finished")


if __name__ == "__main__":
    main()