# q_play.py
import argparse
import time
from rl_utils import QTable, encode_state
from env import LaneDodgeEnv

def play(episodes: int, table_path: str, seed: int | None):
    qtab = QTable()
    qtab.load_json(table_path)

    env = LaneDodgeEnv(render_mode="human", seed=seed)
    for ep in range(1, episodes + 1):
        obs, _ = env.reset()
        done = False
        steps = 0
        total_reward = 0.0
        total_passed = 0

        while not done:
            s = encode_state(obs)
            a = qtab.best_action(s)
            obs, r, done, info = env.step(a)
            total_reward += r
            steps += 1
            total_passed += info.get("passed", 0)
            if info.get("closed"):
                done = True

        print(f"[Play {ep}] steps={steps}, reward={total_reward:.2f}, passed={total_passed}")
        time.sleep(0.4)

    env.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes", type=int, default=3)
    ap.add_argument("--table", type=str, default="q_table.json")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    play(args.episodes, args.table, args.seed)
