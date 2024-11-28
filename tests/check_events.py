def check_system_in_config(test_message, matrix_config):
    """
    Check if the system in the test message matches the list of systems in the configuration.

    Args:
        test_message (dict): The message to check, containing a 'system' key.
        matrix_config (dict): The loaded matrix configuration.

    Returns:
        bool: True if the system matches one of the allowed systems, otherwise False.
        str: Explanation of the result.
    """
    system_to_check = test_message.get("system")

    # Iterate over the matrixConfig to find the systems field in each matrix entry
    for key, value in matrix_config.items():
        # GET SYSTEMS FOR THE CURRENT MATRIX ENTRY
        for entry, values in value.items():
            systems = values.get("systems", [])
            print(entry, systems)
            entryConfig = entry

        # Debugging: Print the systems list for this entry
        print(f"Systems list for kind", entry)

        # Special case handling for 'all'
        if "all" in systems or system_to_check in systems:
            return True, entryConfig, f"System '{system_to_check}' is valid for matrix config '{key}'"

    return False, f"System '{system_to_check}' is not valid in any matrix config."


def check_severity_config(test_message, matrix_config, config_key):

    for key, value in matrix_config.items():

        for entry, values in value.items():

            if entry == config_key:
                severities = values.get("severity", [])
                print(severities)


    # CHECK IF SEVERITY FROM TEST MESSAGE IS IN SEVERITY LIST FOR CONFIG KEY + BOOLEAN RETURN
    print("SEVERITY FROM TEST MESSAGE:", test_message.get("severity"))

    if test_message.get("severity") in severities:
        print("SEVERITY IS VALID")
        return True
    else:
        print("SEVERITY IS INVALID")
        return False
