import math


class TaskAllocator:

    def __init__(self, drones=None):

        if drones is None:
            drones = []

        self.drones = drones

    def set_drones(self, drones):

        self.drones = drones

    def assign_zones(self):

        zones = {
            "D1": "Zone-1",
            "D2": "Zone-2",
            "D3": "Zone-3",
            "D4": "Zone-4",
            "D5": "Support Zone"
        }

        print("\n========== AREA ALLOCATION ==========")

        for drone in self.drones:

            drone.zone = zones.get(drone.drone_id, "Unknown")

            print(f"{drone.drone_id} --> {drone.zone}")

    def find_replacement(self, failed_drone):

        nearest = None
        min_distance = float("inf")

        for drone in self.drones:

            # Skip same drone
            if drone.drone_id == failed_drone.drone_id:
                continue

            # Skip inactive drone
            if not drone.active:
                continue

            # Skip busy drone
            if drone.busy:
                continue

            # Skip low battery
            if drone.battery <= 20:
                continue

            distance = math.sqrt(
                (drone.x - failed_drone.x) ** 2 +
                (drone.y - failed_drone.y) ** 2
            )

            if distance < min_distance:
                min_distance = distance
                nearest = drone

        return nearest

    def transfer_task(self, failed_drone, communication):

        print("\n[TASK] Searching replacement drone...")

        replacement = self.find_replacement(failed_drone)

        if replacement is None:

            print("[TASK] No replacement drone available")
            return

        print(f"[TASK] {replacement.drone_id} selected")

        replacement.accept_mission(
            failed_drone,
            communication
        )

        replacement.busy = True

        failed_drone.deactivate()

        print(
            f"[TASK] Mission transferred from "
            f"{failed_drone.drone_id} "
            f"to "
            f"{replacement.drone_id}"
        )