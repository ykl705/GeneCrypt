import os
import sys

from kivy.config import Config
Config.set('graphics', 'width', '1400')
Config.set('graphics', 'height', '900')
Config.set('graphics', 'resizable', False)
Config.set('kivy', 'exit_on_escape', '1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gene_game import Game, Card
from screens.quest import QuestScreen
from screens.bestiary import BestiaryScreen
from screens.card_library import CardLibraryScreen
from screens.gacha import GachaScreen
from screens.breeding_lab import BreedingLabScreen
from screens.gene_engineering import GeneEngineeringScreen
from screens.tech_tree import TechTreeScreen
from screens.battle import BattleScreen
from services.save_manager import get_save_path
from services.audio import preload_sounds


class GeneCryptApp(App):
    QUEST_DEFINITIONS = None

    def __init__(self):
        super().__init__()
        save_path = get_save_path()
        self.game = Game(load_save=True, save_dir=os.path.dirname(save_path))

    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.18, 1)
        preload_sounds()
        from gene_game import QUEST_DEFINITIONS
        GeneCryptApp.QUEST_DEFINITIONS = QUEST_DEFINITIONS
        self.game._init_quests()

        tp = TabbedPanel(do_default_tab=False, tab_width=dp(100))
        tp.background_color = (0.1, 0.1, 0.2, 1)
        tp.background = ''

        tabs = [
            ('卡牌库', CardLibraryScreen(name='card_library')),
            ('繁殖实验室', BreedingLabScreen(name='breeding_lab')),
            ('基因工程', GeneEngineeringScreen(name='gene_engineering')),
            ('科技树', TechTreeScreen(name='tech_tree')),
            ('基因抽卡', GachaScreen(name='gacha')),
            ('战斗', BattleScreen(name='battle')),
            ('敌人图鉴', BestiaryScreen(name='bestiary')),
            ('任务', QuestScreen(name='quest')),
        ]

        for tab_name, screen in tabs:
            header = TabbedPanelHeader(text=tab_name)
            header.content = screen
            tp.add_widget(header)

        Clock.schedule_interval(lambda dt: self._auto_save(), 30)
        Clock.schedule_interval(lambda dt: self._update_breeding(), 0.5)
        return tp

    def _auto_save(self):
        try:
            self.game.save_game()
        except Exception:
            pass

    def _update_breeding(self):
        try:
            self.game.update_breeding()
        except Exception:
            pass

    def refresh_breeding_combos(self):
        for screen in self.root.children:
            if isinstance(screen, TabbedPanelHeader):
                if hasattr(screen.content, 'update_combos'):
                    screen.content.update_combos()
                if isinstance(screen.content, BreedingLabScreen):
                    screen.content.on_enter()


if __name__ == '__main__':
    GeneCryptApp().run()
