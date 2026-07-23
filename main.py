from environment import DisasterEnvironment
from drone import Drone
from coverage import CoverageMap
from communication import Communication
from task_allocator import TaskAllocator
from qlearning import QLearning
from simulation.simulator import Simulator


def main():

    env = DisasterEnvironment()
    env.place_objects()

    communication = Communication()
    qlearning = QLearning()

    coverage = CoverageMap(15)

    # Fixed Drone Positions
    drones = [
        Drone("D1", 13, 1),
        Drone("D2", 13, 13),
        Drone("D3", 1, 1),
        Drone("D4", 1, 13),
        Drone("D5", 7, 7),
    ]

    for drone in drones:
        coverage.mark(drone.x, drone.y)

    allocator = TaskAllocator(drones)
    allocator.assign_zones()

    simulator = Simulator(env)

    print("\n========== UAV SWARM STARTED ==========")

    for drone in drones:
        print(
            f"{drone.drone_id} -> Position ({drone.x},{drone.y})  Zone: {drone.zone}"
        )

    print("=======================================\n")

    step = 0

    while True:

        step += 1

        # --------------------------------
        # Dynamic Disaster
        # --------------------------------

        if step % 30 == 0:
            print("\n🔥 Fire Spread...")
            env.spread_fire()

        if step % 50 == 0:
            print("\n🌊 Flood Spread...")
            env.spread_flood()

        # --------------------------------
        # Drone Movement
        # --------------------------------

        for drone in drones:

            if not drone.active:
                continue

            old_x = drone.x
            old_y = drone.y

            drone.move(
                env.grid,
                communication,
                qlearning,
                mode="qlearning"
            )

            coverage.mark(drone.x, drone.y)

            if old_x != drone.x or old_y != drone.y:

                print(
                    f"{drone.drone_id}: ({old_x},{old_y}) -> ({drone.x},{drone.y})"
                )

            else:

                print(
                    f"{drone.drone_id}: NO MOVE ({drone.x},{drone.y})"
                )

            # Mission Transfer
            if drone.status == "Need Replacement":

                allocator.transfer_task(
                    drone,
                    communication
                )

        # --------------------------------
        # Dashboard + Simulation
        # --------------------------------

        simulator.update(
            drones,
            coverage.get_coverage_percentage()
        )


if __name__ == "__main__":
    main()