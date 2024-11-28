import yaml

def loadRules():
    # Path to the YAML file
    yaml_file_path = "rules.yaml"

    # Load YAML content from the file
    with open(yaml_file_path, "r") as file:
        data = yaml.safe_load(file)

    # Return the resulting Python dictionary
    return data
