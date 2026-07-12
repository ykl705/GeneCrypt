import os
import sys
import traceback
from kivy.utils import platform
from kivy.lang import Builder

# 日志文件放在应用私有目录
if platform == 'android':
    from android.storage import app_storage_path
    CRASH_LOG_PATH = os.path.join(app_storage_path(), 'crash.log')
else:
    CRASH_LOG_PATH = 'crash.log'

_CRASH_LOG = open(CRASH_LOG_PATH, 'w')

def _log_error(msg):
    if _CRASH_LOG:
        _CRASH_LOG.write(msg + '\n')
        _CRASH_LOG.flush()

_log_error('=== GeneCrypt Startup ===')

# Kivy 配置
try:
    from kivy.config import Config
    Config.set('graphics', 'width', '1400')
    Config.set('graphics', 'height', '900')
    Config.set('graphics', 'resizable', False)
    Config.set('kivy', 'exit_on_escape', '1')
except Exception as e:
    _log_error(f'Config error: {e}')

# 导入 Kivy 模块
try:
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
except Exception as e:
    _log_error(f'Kivy imports error: {e}\n{traceback.format_exc()}')
    raise

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入自定义模块
try:
    from gene_game import Game, Card, QUEST_DEFINITIONS
    _log_error('Imported gene_game OK')
except Exception as e:
    _log_error(f'gene_game import error: {e}\n{traceback.format_exc()}')
    raise

try:
    from screens.quest import QuestScreen
    from screens.bestiary import BestiaryScreen
    from screens.card_library import CardLibraryScreen
    from screens.gacha import GachaScreen
    from screens.breeding_lab import BreedingLabScreen
    from screens.gene_engineering import GeneEngineeringScreen
    from screens.tech_tree import TechTreeScreen
    from screens.battle import BattleScreen
    _log_error('Screen imports OK')
except Exception as e:
    _log_error(f'Screen import error: {e}\n{traceback.format_exc()}')
    raise

try:
    from services.save_manager import get_save_path
    from services.audio import preload_sounds
    _log_error('Service imports OK')
except Exception as e:
    _log_error(f'Service import error: {e}\n{traceback.format_exc()}')
    raise


class GeneCryptApp(App):
    def __init__(self):
        super().__init__()
        _log_error('App.__init__ start')
        try:
            save_path = get_save_path()
            _log_error(f'Save path: {save_path}')
            self.game = Game(load_save=True, save_dir=os.path.dirname(save_path))
            _log_error('Game created OK')
        except Exception as e:
            _log_error(f'Game init error: {e}\n{traceback.format_exc()}')
            raise

    def build(self):
        _log_error('App.build() start')
        
        # 🔥 关键修复：加载 KV 文件
        try:
            # 加载主 KV（如果存在）
            if os.path.exists('main.kv'):
                Builder.load_file('main.kv')
                _log_error('main.kv loaded')
            
            # 加载 screens 目录下的 KV 文件
            kv_files = [
                'screens/quest.kv',
                'screens/battle.kv',
                'screens/bestiary.kv',
                'screens/card_library.kv',
                'screens/gacha.kv',
                'screens/breeding_lab.kv',
                'screens/gene_engineering.kv',
                'screens/tech_tree.kv',
            ]
            for kv_file in kv_files:
                if os.path.exists(kv_file):
                    Builder.load_file(kv_file)
                    _log_error(f'Loaded: {kv_file}')
        except Exception as e:
            _log_error(f'KV loading error: {e}\n{traceback.format_exc()}')

        try:
            Window.clearcolor = (0.1, 0.1, 0.18, 1)
        except Exception as e:
            _log_error(f'Window.clearcolor error: {e}')

        try:
            preload_sounds()
        except Exception as e:
            _log_error(f'preload_sounds error: {e}')

        try:
            self.game._init_quests()
        except Exception as e:
            _log_error(f'Quest init error: {e}\n{traceback.format_exc()}')

        # 创建主界面
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

        _log_error('App.build() complete')
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
    _log_error('Starting app.run()')
    try:
        GeneCryptApp().run()
    except Exception as e:
        _log_error(f'App run error: {e}\n{traceback.format_exc()}')
        raise