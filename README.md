# Lane Runner RL Game 

# Lane Runner RL — Pygame + Q-Learning

**2D lane-runner car game in Python (Pygame) with a Gym-style env and a Q-learning bot.**  
Dodge trashcans, rocks, an old lady with a cane, and a broken-down car across 3 lanes. Images auto-download on first run; training stays local and offline.

https://github.com/<your-username>/lane-runner-rl

---

## ✨ Features
- **Simple, fast** top-down car dodger (Pygame)
- **Gym-like environment** (`reset()`, `step()`) for RL
- **Heuristic bot** (baseline autopilot)
- **Tabular Q-learning** agent with discretized state
- Assets auto-download to `assets/` (public domain / CC0 sources)
- Clean modular code; easy to extend to DQN later

---

## 📂 Project Structure
├─ main.py # run a human-playable game
├─ game.py # game loop + drawing + collisions
├─ sprites.py # Car / Obstacle / lane helpers
├─ assets.py # downloads + loads sprites (with fallbacks)
├─ config.py # game constants and UI/fonts
├─ env.py # Gym-like wrapper around the game
├─ run_bot.py # heuristic autopilot (no learning)
├─ rl_utils.py # Q-table + discretization helpers
├─ q_train.py # tabular Q-learning trainer
├─ q_play.py # plays using a saved Q-table
├─ requirements.txt
├─ .gitignore
└─ assets/ # (auto-created) downloaded images cache



---

## 🖥️ Requirements
- Python 3.10–3.12
- Windows/macOS/Linux
- `pygame`, `requests` (installed via `requirements.txt`)

---

## 🚀 Quickstart (Command Prompt / **CMD**)
From your project folder:

```cmd
firstvenv.venv\Scripts\activate.bat
pip install -r requirements.txt
python main.py
```

## 🤖 Run the heuristic bot (no learning)
```cmd
python run_bot.py
```

## 🧠 Train the Q-learning agent
```cmd
python q_train.py --episodes 800
:: Peek at progress every 100 episodes (renders one quick run):
python q_train.py --episodes 800 --render_every 100

:: Play with the learned table:
python q_play.py --episodes 5 --table q_table.json
```
Resume training (optional): add this to q_train.py to continue from an existing table:
```python
import os
# after qtab = QTable()
if os.path.exists(save_path):
    qtab.load_json(save_path)
    print(f"Resumed from {save_path} (entries={len(qtab.Q)})")

```
## 📝 .gitignore
```
__pycache__/
*.pyc
firstvenv.venv/
venv/
.venv/
assets/
q_table.json
.DS_Store
Thumbs.db
```

