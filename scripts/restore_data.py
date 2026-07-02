import subprocess
import os
import sys

def run_script(script_name):
    script_path = os.path.join("scripts", script_name)
    if not os.path.exists(script_path):
        print(f"Error: Script not found at {script_path}")
        return False
        
    print(f"\n=======================================================")
    print(f"  RUNNING: {script_name}...")
    print("=======================================================")
    
    try:
        # Run script with current python interpreter
        result = subprocess.run([sys.executable, script_path], check=True)
        if result.returncode == 0:
            print(f"SUCCESS: {script_name} completed successfully.")
            return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {script_name} failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"ERROR executing {script_name}: {e}")
        return False

def main():
    print("Starting Automated Data Restoration Pipeline...")
    
    # Check that we are in the correct working directory
    if not os.path.exists("scripts") or not os.path.exists("data"):
        print("Error: Please run this script from the root directory of the project.")
        print(f"Current directory is: {os.getcwd()}")
        sys.exit(1)
        
    # List of scripts to run in sequence
    restoration_steps = [
        "filter_lexicons.py",          # Step 1: Download & filter dictionaries (Jieba, HanLP, THUOCL)
        "download_hanviet_csv.py",     # Step 2: Download Hán Việt character mapping
        "prepare_synthetic_data.py",   # Step 3: Create Chinese-Vietnamese translation mock dataset
        "prepare_constrained_data.py"  # Step 4: Tokenize, map Hán Việt tags, and output training dataset
    ]
    
    success = True
    for step in restoration_steps:
        if not run_script(step):
            success = False
            print(f"\nPipeline halted: {step} failed.")
            break
            
    if success:
        print("\n=======================================================")
        print("🎉 ALL DATA RESTORED SUCCESSFULLY!")
        print("=======================================================")
        print("You can verify the setup by running the benchmark:")
        print("python scripts/optimize_and_benchmark.py")
    else:
        print("\n=======================================================")
        print("❌ DATA RESTORATION FAILED.")
        print("=======================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
