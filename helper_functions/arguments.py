from jinja2 import Template
from cachetools import Cache

def get_arguments(rules, event):
    event_args = []
    event_args.clear()
    print("/////////////////////////////////////")
    print(event)
    print("/////////////////////////////////////")
    cache = Cache(maxsize=10)
    for rule_name, rule in rules.items():
        if event_args:
            break
        kind = rule.get('kind')
        severitys = rule.get('severity')
        systems = rule.get('systems')
        event_system = event.get('system')
        event_severity = event.get('severity')
        event_timestamp = event.get('timestamp')

        print(f"Checking rule: {rule_name}")
        print(f"Event system: {event_system}, Event severity: {event_severity}")
        print(f"Rule systems: {systems}, Rule severity: {severitys}")

        args = {}  # Create a new args dictionary for each rule

        # Check if the event matches the rule's systems and severity
        if event_system in systems and event_severity in severitys:
            # If the rule has a text key, process it
            if kind in ["static", "text", "ticker"]:
                print_text = rule.get('text')
                print_text = Template(print_text).render(**event)
                if event_system == "scale":
                    bool_calories = calories(cache, print_text)
                    if bool_calories:
                        args["calories"] = cache["amount_calories"]
                    else:
                        args["more_sweets"] = cache["more_sweets"]
                args["text"] = print_text
                args['font'] = rule.get('font')
            # Add other arguments from the rule
            elif kind in ["gif", "image"]:
                args['image'] = rule.get('image')
            event_args.append({"mode": kind, "severity": severitys, "systems": systems, "timestamp": event_timestamp, "args": args})
    print(f"Generated event arguments: {event_args}")
    return event_args

def get_speed(speed):
    sleep_dict = {"5": 0.01, "4": 0.03, "3": 0.05, "2":0.1, "1":0.2}
    return sleep_dict[str(speed)]

def get_color(color):
    color = color.replace("(","").replace(")","").replace(" ","")
    color = color.split(",")
    return color 

def calories(cache, print_text):
    global CHECK_WEIGHT
    kcal_1g = 4
    if CHECK_WEIGHT is not "empty":
        weight_sum = int(CHECK_WEIGHT) - int(print_text)
        if weight_sum > 0:
            weight_calories = int(weight_sum) * kcal_1g
            cache["amount_calories"] = weight_calories
            bool_calories = True
        else:
            more_sweets = abs(weight_sum)
            cache["more_sweets"] = more_sweets
            bool_calories = False
    CHECK_WEIGHT = print_text
    return bool_calories
    