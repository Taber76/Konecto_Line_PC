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
            "small": "background-color: #007BFF; color: white; border-radius: 5px; padding: 1px",
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
