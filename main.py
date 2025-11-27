import subprocess
import time

steps = [
    ("Filter 1 - Symbols", ["python3", "filters/filter1_symbols.py"]),
    ("Filter 2 - Check Dates", ["python3", "filters/filter2_check_dates.py"]),
    ("Filter 3 - Fill Data", ["python3", "filters/filter3_fill_data.py"]),
    ("Feature Generation", ["python3", "features/feature_generator.py"]),
    ("Train XGBoost Model", ["python3", "models/train_xgboost.py"])
]

for name, cmd in steps:
    print(f"\n[INFO] Running {name}...")
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    end = time.time()
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    print(f"[INFO] {name} finished in {end-start:.2f} seconds")
