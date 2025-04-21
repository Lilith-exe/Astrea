import json
import os
import ui
import pygame


def save_game_data(high_score, settings):
    settings_copy = settings.copy()
    if isinstance(settings_copy["resolution"], tuple):
        settings_copy["resolution"] = list(settings_copy["resolution"])
    game_data = {
        "high_score": high_score,
        "settings": settings_copy
    }

    with open("game_data.json", "w") as file:
        json.dump(game_data, file)

def load_game_data():
    default_data = {
        "high_score": 0,
        "settings": {
            "sound_volume": 0.7,
            "difficulty": "normal",
            "player_name": "Player 1",
            "resolution": [1280, 720]
        }
    }

    try:
        with open("game_data.json", "r") as file:
            data = json.load(file)
            if "settings" in data and "resolution" in data["settings"]:
                data["settings"]["resolution"] = tuple(data["settings"]["resolution"])
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return default_data
    
def settings_menu(screen, current_settings, high_score=0):
    settings = current_settings.copy()
    ui_instance = ui.UI()

    options = [
        "Sound Volume: {}",
        "Difficulty: {}",
        "Player Name: {}",
        "Resolution: {}x{}",
        "Save",
        "cancel"
    ]

    selected_option = 0
    running = True
    name_selected = False

    flash_timer = 0
    flash_visible = True
    flash_speed = 500

    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(60)
        flash_timer += dt
        if flash_timer >= flash_speed:
            flash_timer = 0
            flash_visible = not flash_visible

        ui_instance.draw_settings_menu(screen, options, selected_option, settings, name_selected, flash_visible)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return current_settings
                if selected_option != 2 or not name_selected:
                    if event.key == pygame.K_w:
                        selected_option = (selected_option - 1) % len(options)
                    if event.key == pygame.K_s:
                        selected_option = (selected_option + 1) % len(options)
                if event.key == pygame.K_a and selected_option != 2:
                    if selected_option == 0:
                        settings["sound_volume"] = max(0, settings["sound_volume"] - 0.1)
                    elif selected_option == 1:
                        difficulties = ["easy", "normal", "hard"]
                        current_idx = difficulties.index(settings["difficulty"])
                        settings["difficulty"] = difficulties[(current_idx - 1) % len(difficulties)]
                    elif selected_option == 3:
                        resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080), (2560, 1440), (3840, 2160), (3840, 1600)]
                        current_idx = resolutions.index(tuple(settings["resolution"]))
                        settings["resolution"] = resolutions[(current_idx - 1) % len(resolutions)]

                if event.key == pygame.K_d and selected_option != 2:
                    if selected_option == 0:  # Sound volume
                        settings["sound_volume"] = min(1.0, settings["sound_volume"] + 0.1)
                    elif selected_option == 1:  # Difficulty
                        difficulties = ["easy", "normal", "hard"]
                        current_idx = difficulties.index(settings["difficulty"])
                        settings["difficulty"] = difficulties[(current_idx + 1) % len(difficulties)]
                    elif selected_option == 3:  # Resolution
                        resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080), (2560, 1440), (3840, 2160), (3840, 1600)]
                        current_idx = resolutions.index(tuple(settings["resolution"]))
                        settings["resolution"] = resolutions[(current_idx + 1) % len(resolutions)] 

                if selected_option == 2: 
                    if event.key == pygame.K_RETURN:
                        name_selected = not name_selected
                    elif name_selected:
                        if event.key == pygame.K_BACKSPACE:                    
                            settings["player_name"] = settings["player_name"][:-1]
                        elif event.unicode.isalnum():
                            settings["player_name"] += event.unicode

                if event.key == pygame.K_RETURN and selected_option != 2:
                    if selected_option == 4:
                        if settings["resolution"] != current_settings["resolution"]:
                            pygame.display.set_mode(settings["resolution"])
                        save_game_data(high_score, settings)
                        return settings
                    elif selected_option == 5:
                        return current_settings

        pygame.display.flip()
        clock.tick(30)
    return current_settings             
                    

        
        