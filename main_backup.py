import sys
import os

# Add the 'logic' directory to sys.path to ensure imports within logic modules work correctly
# when run from the root directory.
current_dir = os.path.dirname(os.path.abspath(__file__))
logic_dir = os.path.join(current_dir, 'logic')
sys.path.append(logic_dir)

from logic.edt_generator import generer_edt

if __name__ == "__main__":
    print("🚀 Starting Timetable Generation...")
    try:
        edt = generer_edt()
        print(f"✨ Timetable generated successfully with {len(edt)} sessions.")
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        sys.exit(1)
