import datetime
import random

def generate_random_event():
    """
    Generate a random event message with predefined and randomized data.

    Returns:
        dict: A random event message.
    """
    # Predefined options for randomization
    titles = ["Server Alert", "Disk Space Low", "Network Latency Detected", "Service Restarted"]
    messages = [
        "High CPU usage detected",
        "Disk space below 10%",
        "Latency exceeds 200ms",
        "Service successfully restarted"
    ]
    severities = ["info", "warning", "error", "success"]
    authors = ["Monitoring System", "System Admin", "Automated Alert", "DevOps Team"]
    systems = ["github", "gitlab", "Network Monitoring", "scale"]
    tags_options = [
        "server, monitoring, cpu",
        "disk, alert, storage",
        "network, latency, connectivity",
        "system, restart, status"
    ]
    assignee_addresses = [
        "admin@example.com",
        "support@example.com",
        "team@example.com",
        "alerts@example.com"
    ]
    assignee_names = ["System Admin", "Support Team", "On-Call Engineer", "Alert Manager"]
    artifact_notes = [
        "CPU logs available",
        "Disk usage reports generated",
        "Network trace logs stored",
        "System restart logs"
    ]
    urls = [
        "https://example.com/alerts/123",
        "https://example.com/alerts/456",
        "https://example.com/alerts/789",
        "https://example.com/alerts/101112"
    ]

    # Generate a random timestamp 1-15 seconds in the past
    current_time = datetime.datetime.now()
    random_time_offset = random.randint(1, 8)  # Random seconds
    random_timestamp = (current_time - datetime.timedelta(seconds=random_time_offset)).isoformat()
    random_system = random.choice(systems)
    if "scale" in random_system:
        messages = [{"Message": "WEIGHT: 1000"}]
    # Construct the random event message
    return {
        "Title": random.choice(titles),
        "Message": random.choice(messages),
        "Severity": random.choice(severities),
        "Author": random.choice(authors),
        "Timestamp": random_timestamp,
        "System": random_system,
        "Tags": random.choice(tags_options),
        "Assignee_address": random.choice(assignee_addresses),
        "Assignee_name": random.choice(assignee_names),
        "Artifacts": random.choice(artifact_notes),
        "Url": random.choice(urls)
    }
