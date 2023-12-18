import json
import os


def load_levels_data(file_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "levels.json")
    with open(file_path, "r") as file:
        return json.load(file)


def generate_level_variables(levels_data):
    LEVELS = [data["name"] for data in levels_data]
    REVERSE_GRAVITY_LEVELS = [
        data["name"] for data in levels_data if data["reverse_gravity"]
    ]
    TIMED_SWITCH_LEVELS = [data["name"] for data in levels_data if data["timed_switch"]]
    RESET_SWITCH_LEVELS = [data["name"] for data in levels_data if data["reset_switch"]]
    HEAVY_LEVELS = [data["name"] for data in levels_data if data["heavy_level"]]
    RANDOM_GRAVITY_LEVELS = [data["name"] for data in levels_data if data["random_gravity"]]
    SWITCH_ON_JUMP = [data["name"] for data in levels_data if data["switch_on_jump"]]
    STICKY_LEVELS = [data["name"] for data in levels_data if data["sticky_levels"]]
    DIAL_LEVELS = [data["name"] for data in levels_data if data["dial_levels"]]
    
    return (
        LEVELS,
        REVERSE_GRAVITY_LEVELS,
        TIMED_SWITCH_LEVELS,
        RESET_SWITCH_LEVELS,
        HEAVY_LEVELS,
        RANDOM_GRAVITY_LEVELS,
        SWITCH_ON_JUMP,
        STICKY_LEVELS,
        DIAL_LEVELS,
    )
