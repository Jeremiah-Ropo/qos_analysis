import random

notifications = {
    'above_average': [
        "Your Internet is flying. Enjoy seamless streaming and gaming with your current speeds.",
        "Quality of Service (QoS) is very good. Your network is performing optimally.",
        "You are right now getting the best possible speeds.",
        "Network conditions are ideal. Perfect for online gaming, video calls, or heavy downloads.",
        "Your QoS is top-notch. Expect crystal-clear video streaming and fast file transfers."
    ],
    'average': [
        "Your Internet is stable and reliable. Suitable for general browsing and streaming.",
        "Stable Quality of Service (QoS): Your network is performing as expected.",
        "You are experiencing average speeds. Good for social media, email, and light browsing.",
        "Network conditions are normal. No concerns, but there is room for improvement.",
        "Your Quality of Service (QoS) is satisfactory."
    ],
    'below_average': [
        "Warning: Slow speeds and high latency detected. Check your network settings.",
        "Poor Quality of Service (QoS): Your network is experiencing issues.",
        "You are experiencing slow speeds. Not ideal for streaming or gaming.",
        "Network congestion detected. Try reducing data-intensive activities.",
        "Your QoS is below the industry benchmark. Consider switching networks."
    ]
}

def get_random_notification(qos_category):
    if qos_category == 'above_average':
        return random.choice(notifications['above_average'])
    elif qos_category == 'average':
        return random.choice(notifications['average'])
    else:
        return random.choice(notifications['below_average'])