import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"

DEFAULTS = {
    "hotkey": "ctrl+alt+space",
    "window": {"x": 200, "y": 200, "w": 320, "h": 420},
    "theme": {
        "bg_color": [30, 30, 30],
        "bg_alpha": 200
    },
    "shortcuts": []
}

def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            cfg = DEFAULTS.copy()
            cfg.update({k: v for k, v in data.items() if k in DEFAULTS})
            # Глубокое слияние для theme
            if "theme" in data:
                cfg["theme"].update(data["theme"])
            return cfg
        except Exception:
            pass
    return DEFAULTS.copy()

def save_config(cfg: dict) -> None:
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Не удалось сохранить config:", e)