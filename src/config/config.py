import json

DEFAULT_CONFIG = {
    "screen": {
        "width": 1024,
        "height": 768
    },
    "camera": {
        "source": 0,
        "fps": 10,
        "resolution": (320, 240),
        "format": "YUYV"
    },
    "processing": {
        "interval": 60,
        "max_age": 10,
        "n_init": 4,
        "nms_max_overlap": 1.0,
        "detection_threshold": 0.4
    },
    "style": {
        "background_color": "white",
        "button": {
            "small": "background-color: #007BFF; color: white; border-radius: 5px; padding: 1px; font-size: 16px; width: 100px; height: 30px;",
            "medium": "background-color: #007BFF; color: white; border-radius: 5px; padding: 1px; font-size: 50px; width: 250px; height: 60px;",
            "large": "background-color: #007BFF; color: white; border-radius: 5px; padding: 1px; font-size: 80px; width: 500px; height: 120px;",
        },
        "label": {
            "small": "background-color: white; color: black; border-radius: 5px; padding: 1px; font-size: 16px; width: 100px; height: 20px;",
            "medium": "background-color: white; color: black; border-radius: 5px; padding: 1px; font-size: 32px; width: 200px; height: 40px;",
            "large": "background-color: white; color: black; border-radius: 5px; padding: 1px; font-size: 64px; width: 400px; height: 80px;",
        },
        "header": {
            "background_color": "white",
            "text_color": "black",
            "font": "Arial",
            "font-size": 18,
            "font-weight": "bold",
            "padding": "0px",
            "color": "white"
        },
        "footer": {
            "background_color": "white",
            "text_color": "black",
            "font": "Arial",
            "font-size": 12,
            "font-weight": "bold",
            "padding": "0px",
            "color": "white"
        },
        "body": {
            "background_color": "white",
            "text_color": "black",
            "font": "Arial",
            "font-size": 15,
            "font-weight": "bold",
            "padding": "0px",
            "color": "white"
        }
    }
}


def load_config():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = DEFAULT_CONFIG
    return config
