import os
import sys
import traceback

# ==========================================
# 早期诊断日志 —— /data/local/tmp/ 永远可写
# ==========================================
_DBG = lambda m: None
try:
    _dbg_path = '/data/local/tmp/genecrypt_debug.log'
    with open(_dbg_path, 'w') as _f:
        _f.write('=== genecrypt debug start ===\n')
    _DBG = lambda m: open(_dbg_path, 'a').write(str(m) + '\n')
    _DBG('1: early debug ready')
except Exception:
    pass

# ==========================================
# 全局未捕获异常处理器 —— 闪退时直接弹窗显示
# ==========================================
_CRASH_LOG_PATH = os.environ.get('ANDROID_PRIVATE', None)
if _CRASH_LOG_PATH:
    _CRASH_LOG_PATH = os.path.join(_CRASH_LOG_PATH, 'genecrypt_crash.log')
else:
    _CRASH_LOG_PATH = 'crash.log'
_DBG(f'2: crash path = {_CRASH_LOG_PATH}')

def _write_crash_log(msg):
    try:
        with open(_CRASH_LOG_PATH, 'a') as f:
            f.write(msg + '\n')
    except Exception:
        pass
    print(f'[GENECRYPT] {msg}', file=sys.stderr)

def _show_crash_dialog(msg):
    """4次尝试：SDL2 MessageBox → pyjnius → Kivy → /data/local/tmp/"""
    full_msg = f'{msg}\n\n日志: {_CRASH_LOG_PATH}'

    # 方法1: SDL2 MessageBox (ctypes, 不依赖任何Python库)
    try:
        import ctypes
        sdl2 = ctypes.cdll.LoadLibrary('libSDL2.so')
        sdl2.SDL_ShowSimpleMessageBox.argtypes = [ctypes.c_uint32, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p]
        sdl2.SDL_ShowSimpleMessageBox.restype = ctypes.c_int
        short = (full_msg[-5000:] + '\n[...上略]') if len(full_msg) > 5000 else full_msg
        sdl2.SDL_ShowSimpleMessageBox(0, b'GeneCrypt Error', short.encode('utf-8'), None)
        return
    except Exception as e:
        _write_crash_log(f'SDL2 dialog fail: {e}')

    # 方法2: PyJNIus
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        AlertDialog = autoclass('android.app.AlertDialog')
        activity = PythonActivity.mActivity
        if activity:
            Builder = AlertDialog.Builder(activity)
            Builder.setTitle('基因密码 - 启动错误')
            Builder.setMessage(full_msg)
            Builder.setPositiveButton('关闭', None)
            d = Builder.create()
            d.show()
            return
    except Exception as e:
        _write_crash_log(f'JNIus dialog fail: {e}')

    # 方法3: Kivy CrashApp
    try:
        from kivy.app import App
        from kivy.uix.screenmanager import Screen
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        class _CrashScreen(Screen):
            def __init__(self, error_msg, **kw):
                super().__init__(**kw)
                layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
                layout.add_widget(Label(text='[b]基因密码 - 启动错误[/b]', markup=True,
                                        size_hint_y=0.1, color=(1,0.3,0.3,1)))
                layout.add_widget(Label(text=f'日志: {_CRASH_LOG_PATH}',
                                        size_hint_y=0.1, color=(1,1,1,0.7)))
                txt = TextInput(text=error_msg, readonly=True, font_size=12)
                layout.add_widget(txt)
                btn = Button(text='关闭', size_hint_y=0.1)
                btn.bind(on_press=lambda x: App.get_running_app().stop())
                layout.add_widget(btn)
                self.add_widget(layout)
        class _CrashApp(App):
            def build(self):
                return _CrashScreen(error_msg=msg)
        _CrashApp().run()
        return
    except Exception as e:
        _write_crash_log(f'Kivy dialog fail: {e}')

    # 方法4: 最后手段 — /data/local/tmp/
    try:
        with open('/data/local/tmp/genecrypt_crash_last.txt', 'w') as f:
            f.write(full_msg)
    except Exception:
        pass

# 设置全局异常钩子
_original_excepthook = sys.excepthook
def _global_excepthook(exc_type, exc_value, exc_tb):
    msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    _write_crash_log(msg)
    try:
        sdcard = os.environ.get('EXTERNAL_STORAGE', '/sdcard')
        with open(os.path.join(sdcard, 'genecrypt_crash.log'), 'a') as f:
            f.write(msg + '\n')
    except Exception:
        pass
    _show_crash_dialog(msg)
sys.excepthook = _global_excepthook
_DBG('3: excepthook set')

_DBG('4: startup')
_write_crash_log('=== GeneCrypt Startup ===')

# ==========================================
# Kivy 配置（必须在其他 Kivy 导入之前）
# ==========================================
os.environ['KIVY_GL_BACKEND'] = 'gles'
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
        _show_crash_dialog(err_msg)
        raise
