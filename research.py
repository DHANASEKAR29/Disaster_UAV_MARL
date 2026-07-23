
import matplotlib.pyplot as plt

from environment import DisasterEnvironment
from drone import Drone
from coverage import CoverageMap
from communication import CommunicationSystem
from task_allocator import TaskAllocator
from qlearning import QLearning

EPISODES = 100
MAX_STEPS = 30

def run_simulation(mode="qlearning"):
    rewards=[]
    coverage_history=[]
    battery_history=[]
    mission_history=[]

    qlearning = QLearning() if mode=="qlearning" else None

    for episode in range(EPISODES):
        env = DisasterEnvironment()

        coverage = CoverageMap(env.grid_size)
        communication = CommunicationSystem()

        positions = env.drone_positions

        drones=[]
        for i,(x,y) in enumerate(positions):
            drones.append(Drone(i,x,y))

        allocator = TaskAllocator(drones)
        allocator.assign_zones()

        episode_reward=0

        for _ in range(MAX_STEPS):
            for drone in drones:
                if not drone.active:
                    continue

                drone.move(
                    env.grid,
                    communication,
                    qlearning=qlearning,
                    mode=mode
                )

                coverage.mark(drone.x, drone.y)

                episode_reward += drone.score

                if drone.status == "Need Replacement":
                    allocator.transfer_task(drone, communication)

        rewards.append(episode_reward)

        cov = coverage.get_coverage_percentage()
        coverage_history.append(cov)

        avg_battery = sum(d.battery for d in drones)/len(drones)
        battery_history.append(avg_battery)

        active = sum(1 for d in drones if d.active)

        mission = (cov + (active/len(drones))*100)/2
        mission_history.append(mission)

        print(f"[{mode.upper()}] Episode {episode+1}/{EPISODES} | "
              f"Reward={episode_reward:.1f} | "
              f"Coverage={cov:.1f}% | "
              f"Battery={avg_battery:.1f}% | "
              f"Mission={mission:.1f}%")

    return {
        "reward": rewards,
        "coverage": coverage_history,
        "battery": battery_history,
        "mission": mission_history
    }

def plot_comparison(random_results, qlearning_results):
    metrics=[
        ("reward","Reward","reward_comparison.png"),
        ("coverage","Coverage (%)","coverage_comparison.png"),
        ("battery","Battery (%)","battery_comparison.png"),
        ("mission","Mission Completion (%)","mission_comparison.png")
    ]

    for key,ylabel,filename in metrics:
        plt.figure(figsize=(10,5))
        plt.plot(random_results[key],label="Random Search")
        plt.plot(qlearning_results[key],label="Q-Learning")
        plt.title(ylabel+" Comparison")
        plt.xlabel("Episode")
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.legend()
        plt.savefig(filename)
        plt.close()

def print_summary(random_results,qlearning_results):
    print("="*70)
    print("RESEARCH PERFORMANCE COMPARISON")
    print("="*70)
    print(f"{'Metric':<25}{'Random':>12}{'Q-Learning':>15}{'Winner':>15}")
    print("-"*70)

    for name,key in [
        ("Coverage","coverage"),
        ("Reward","reward"),
        ("Battery","battery"),
        ("Mission Completion","mission")
    ]:
        r=sum(random_results[key])/len(random_results[key])
        q=sum(qlearning_results[key])/len(qlearning_results[key])
        winner="Q-Learning" if q>=r else "Random"
        print(f"{name:<25}{r:>12.2f}{q:>15.2f}{winner:>15}")

def main():
    print("Running Random Search...")
    random_results=run_simulation("random")

    print("\nRunning Q-Learning...")
    qlearning_results=run_simulation("qlearning")

    plot_comparison(random_results,qlearning_results)
    print_summary(random_results,qlearning_results)

    print("\nResearch experiment completed successfully.")

if __name__=="__main__":
    main()
