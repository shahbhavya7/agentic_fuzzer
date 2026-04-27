from core.graph import app

def main():
    # Python script that sleeps for 2 seconds to simulate a timeout
    python_script = """import time
time.sleep(2)
print("Done sleeping!")
"""

    initial_state = {
        "target_code": python_script,
        "language": "python",
        "time_limit": 1.0,
        "loop_count": 0,
        "test_history": []
    }

    print("Running LangGraph workflow...")
    final_state = app.invoke(initial_state)
    
    print("\n--- Final Output State ---")
    print(final_state)

if __name__ == "__main__":
    main()
