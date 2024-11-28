from generate_message import generate_random_event
from load_yaml import loadRules
from compare_time import evaluate_event_timing
from check_events import check_system_in_config
from check_events import check_severity_config

def main():
    from generate_message import generate_random_event  # Assuming you saved the generator in generate_message.py

    # Initialize variables = defaulfs
    system_valid = False
    severity_valid = False

    print("Generate Random Event:")
    random_event = generate_random_event()
    print(random_event)

    # LOAD RULE SET
    rules = loadRules()

    # IS THE EVENT ON TIME?
    time_difference, log, time_valid = evaluate_event_timing(random_event, 3)

    print("TIME DIFFERENCE:", time_difference)
    print("RESULT:", log)

    # CHECK FOR SYSTEM
    if time_valid:
        system_valid, config_key, log = check_system_in_config(random_event, rules)
        print(config_key)

    # CHECK FOR SEVERITY
    if system_valid:
        severity_valid = check_severity_config(random_event, rules, config_key)

    # PRINT RESULT
    if time_valid and system_valid and severity_valid:
        print("Event is valid - FIRE FOR", config_key)

    else:
        print("Event is not valid - DO NOT FIRE")

    print("TIMING:", time_valid)
    print("SYSTEM:", system_valid)
    print("SEVERITY:", severity_valid)

if __name__ == "__main__":
    main()
