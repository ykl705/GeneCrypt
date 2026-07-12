import os
import sys
import traceback

# ==========================================
# 全局未捕获异常处理器 —— 闪退时直接弹窗显示
# ==========================================
_CRASH_LOG_PATH = None

def _write_crash_log(msg):
    global _CRASH_LOG_PATH
    if _CRASH_LOG_PATH is None:
        app = App.get_running_app() if 'App' in dir() else None
        if app is not None:
            _CRASH_LOG_PATH = os.path.join(app.user_data_dir, 'genecrypt_crash.log')
        else:
            _CRASH_LOG_PATH = 'crash.log'
    try:
        with open(_CRASH_LOG_PATH, 'a') as f:
            f.write(msg + '\n')
    except Exception:
        pass

# 设置全局异常钩子
_original_excepthook = sys.excepthook
def _global_excepthook(exc_type, exc_value, exc_tb):
    msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    _write_crash_log(msg)
    # Also try to print for logcat
    print(f'[GENECRYPT_CRASH] {msg}', file=sys.stderr)
sys.excepthook = _global_excepthook

_write_crash_log('=== GeneCrypt Startup ===')

# ==========================================
# Kivy 配置（必须在其他 Kivy 导入之前）
# ==========================================
try:
    from kivy.config import Config
    Config.set('graphics', 'width', '1400')
    Config.set('graphics', 'height', '900')
    Config.set('graphics', 'resizable', False)
    Config.set('kivy', 'exit_on_escape', '1')
except Exception as e:
    _write_crash_log(f'Config error: {e}')

# ==========================================
# 导入 Kivy 模块
# ==========================================
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
    from kivy.lang import Builder
except Exception as e:
    _write_crash_log(f'Kivy imports error: {e}\n{traceback.format_exc()}')
    raise

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ==========================================
# 导入自定义模块
# ==========================================
try:
    from gene_game import Game, Card, QUEST_DEFINITIONS
    _write_crash_log('gene_game imports OK')
except Exception as e:
    _write_crash_log(f'gene_game import error: {e}\n{traceback.format_exc()}')
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
except Exception as e:
    _write_crash_log(f'Screen import error: {e}\n{traceback.format_exc()}')
    raise

try:
    from services.save_manager import get_save_path
    from services.audio import preload_sounds
except Exception as e:
    _write_crash_log(f'Service import error: {e}\n{traceback.format_exc()}')
    raise


class ErrorPopup(Screen):
    """显示崩溃信息的全屏页面"""
    def __init__(self, error_msg, **kw):
        super().__init__(**kw)
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        title = Label(text='[b]基因密码 - 启动错误[/b]', markup=True,
                      size_hint_y=0.1, color=(1,0.3,0.3,1))
        info = Label(text=f'错误已保存到:\n{_CRASH_LOG_PATH}',
                     size_hint_y=0.1, color=(1,1,1,0.7))
        txt = TextInput(text=error_msg, readonly=True,
                        background_color=(0.15,0.15,0.25,1),
                        foreground_color=(1,0.3,0.3,1), font_size=12)
        btn = Button(text='关闭', size_hint_y=0.1,
                     background_color=(0.3,0.3,0.5,1))
        btn.bind(on_press=lambda x: App.get_running_app().stop())
        layout.add_widget(title)
        layout.add_widget(info)
        layout.add_widget(txt)
        layout.add_widget(btn)
        self.add_widget(layout)


class GeneCryptApp(App):
    def __init__(self):
        super().__init__()
        _write_crash_log('App.__init__ start')
        try:
            save_path = get_save_path()
            _write_crash_log(f'Save path: {save_path}')
            self.game = Game(load_save=True, save_dir=os.path.dirname(save_path))
            _write_crash_log('Game created OK')
        except Exception as e:
            _write_crash_log(f'Game init error: {e}\n{traceback.format_exc()}')
            raise

    def build(self):
        _write_crash_log('App.build() start')
        try:
            Window.clearcolor = (0.1, 0.1, 0.18, 1)
        except Exception as e:
            _write_crash_log(f'Window.clearcolor error: {e}')

        try:
            preload_sounds()
        except Exception as e:
            _write_crash_log(f'preload_sounds error: {e}')

        try:
            self.game._init_quests()
        except Exception as e:
            _write_crash_log(f'Quest init error: {e}\n{traceback.format_exc()}')

        tp = TabbedPanel(do_default_tab=False, tab_width=dp(100))
        tp.background_color = (0.1, 0.1, 0.2, 1)
        tp.background = ''

        self._screens = []
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
            self._screens.append(screen)
            header = TabbedPanelHeader(text=tab_name)
            header.content = screen
            tp.add_widget(header)

        Clock.schedule_interval(lambda dt: self._auto_save(), 30)
        Clock.schedule_interval(lambda dt: self._update_breeding(), 0.5)

        _write_crash_log('App.build() complete')
        return tp

    def refresh_breeding_combos(self):
        """Refresh breeding dropdowns across all screens after card changes."""
        for screen in getattr(self, '_screens', []):
            if hasattr(screen, 'update_combos'):
                try:
                    screen.update_combos()
                except Exception:
                    pass

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


if __name__ == '__main__':
    _write_crash_log('Starting app.run()')
    try:
        GeneCryptApp().run()
    except Exception as e:
        err_msg = traceback.format_exc()
        _write_crash_log(f'App run error: {err_msg}')
        # Try to show error on screen via Kivy
        try:
            class CrashApp(App):
                def build(self):
                    return ErrorPopup(err_msg)
            CrashApp().run()
        except Exception:
            pass
        raise
