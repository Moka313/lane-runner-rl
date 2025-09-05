# run_bot.py
import time
from env import LaneDodgeEnv, LEFT, STAY, RIGHT

def greedy_safe_policy(obs, cooldown_frames: int, last_action: int):
    """
    Simple heuristic:
    - If current lane is 'dangerously close' to an obstacle, switch to the lane
      with the largest clear distance (tie-break toward center).
    - Otherwise stay.
    - Cooldown prevents jittery lane swapping.
    """
    lane, dL, dM, dR = int(obs[0]), obs[1], obs[2], obs[3]
    dists = [dL, dM, dR]
    center_bias = [1, 0, 1]  # prefer middle lane on ties
    best_lane = max(range(3), key=lambda i: (dists[i], -center_bias[i]))

    DANGER = 0.18
    action = STAY

    if cooldown_frames == 0 and dists[lane] < DANGER and best_lane != lane:
        action = LEFT if best_lane < lane else RIGHT
    else:
        action = STAY

    # Slight preference to return to center if it's clearly better and safe
    if cooldown_frames == 0 and action == STAY and lane != 1 and dists[1] > dists[lane] + 0.15:
        action = LEFT if 1 < lane else RIGHT

    return action

def main():
    env = LaneDodgeEnv(render_mode="human", seed=0)
    episodes = 30  # play N episodes then exit
    for ep in range(1, episodes + 1):
        obs, _ = env.reset()
        done = False
        steps = 0
        total_reward = 0.0
        cooldown = 0
        last_action = STAY

        while not done:
            action = greedy_safe_policy(obs, cooldown, last_action)
            obs, reward, done, info = env.step(action)
            total_reward += reward
            steps += 1
            last_action = action
            cooldown = max(0, cooldown - 1) if action == STAY else 6  # ~0.1s at 60 FPS

            if info.get("closed"):
                done = True

        print(f"[Episode {ep}] steps={steps}, total_reward={total_reward:.2f}, final_score={info.get('score')}")
        time.sleep(0.5)  # tiny pause between runs

    env.close()

if __name__ == "__main__":
    main()
