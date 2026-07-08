import os
from kivy.app import App

def get_save_path():
    app = App.get_running_app()
    user_dir = app.user_data_dir
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return os.path.join(user_dir, 'gene_game_save.json')
