import yaml

def get_rules(rules_yaml):
    with open(rules_yaml, 'r') as file:
        configuration = yaml.safe_load(file)
    configuration = configuration["matrixConfig"]

    rules = {}
    for key, value in configuration.items():
        rules[key] = {
            'kind': value.get('kind'),
            'severity': value.get('severity'),
            'systems': value.get('systems')
        }
        # Conditionally add 'text' if it is not None
        if value.get('text') is not None:
            rules[key]['text'] = value.get('text')
            rules[key]['font'] = value.get('font')
        # Conditionally add 'image' if it is not None
        if value.get('image') is not None:
            rules[key]['image'] = value.get('image')
        # Conditionally add 'duration' if it is not None
        if value.get('duration') is not None:
            rules[key]['duration'] = value.get('duration')

    print("Rules: ", rules)
    return rules
