# main.py - Android 入口
import os
import sys
import traceback

# ========== 日志 ==========
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.log')

def log_error(msg):
    try:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
            f.flush()
    except:
        pass

log_error('=== GeneCrypt Startup ===')

# ========== Kivy 配置 ==========
try:
    from kivy.config import Config
    Config.set('graphics', 'width', '1400')
    Config.set('graphics', 'height', '900')
    Config.set('graphics', 'resizable', False)
except Exception as e:
    log_error(f'Config error: {e}')

# ========== Kivy 导入 ==========
try:
    from kivy.app import App
    from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
    from kivy.core.window import Window
    from kivy.clock import Clock
    from kivy.metrics import dp
    from kivy.lang import Builder
    from kivy.utils import platform
    from kivy.core.text import LabelBase, DEFAULT_FONT
except Exception as e:
    log_error(f'Kivy imports error: {e}\n{traceback.format_exc()}')
    raise

# ========== 中文字体注册 ==========
def _setup_cjk_font():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, 'assets', 'fonts', 'wqy-microhei.ttf'),
        os.path.join(base_dir, 'assets', 'fonts', 'DroidSansFallback.ttf'),
        '/system/fonts/DroidSansFallback.ttf',
    ]
    for fp in candidates:
        if os.path.exists(fp):
            try:
                LabelBase.register(DEFAULT_FONT, fn_regular=fp, fn_bold=fp, fn_italic=fp, fn_bolditalic=fp)
                log_error(f'CJK font registered: {fp}')
                return
            except Exception as e:
                log_error(f'Font register failed ({fp}): {e}')
    log_error('WARNING: No CJK font found - Chinese text may be garbled')

_setup_cjk_font()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ========== 关键修改：从 gene_game_core 导入（无 tkinter）==========
try:
    from gene_game_core import Game, Card, QUEST_DEFINITIONS
    log_error('Imported gene_game_core OK')
except Exception as e:
    log_error(f'gene_game_core import error: {e}\n{traceback.format_exc()}')
    raise

# ========== 导入屏幕 ==========
try:
    from screens.quest import QuestScreen
    from screens.bestiary import BestiaryScreen
    from screens.card_library import CardLibraryScreen
    from screens.gacha import GachaScreen
    from screens.breeding_lab import BreedingLabScreen
    from screens.gene_engineering import GeneEngineeringScreen
    from screens.tech_tree import TechTreeScreen
    from screens.battle import BattleScreen
    log_error('Screen imports OK')
except Exception as e:
    log_error(f'Screen import error: {e}\n{traceback.format_exc()}')
    raise

# ========== 保存路径 ==========
def get_save_dir():
    if platform == 'android':
        try:
            from android.storage import app_storage_path
            path = app_storage_path()
        except ImportError:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saves')
    else:
        path = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(path, exist_ok=True)
    return path

# ========== 主应用 ==========
class GeneCryptApp(App):
    game = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            save_dir = get_save_dir()
            self.game = Game(load_save=True, save_dir=save_dir)
            log_error(f'Game loaded: {len(self.game.cards)} cards')
        except Exception as e:
            log_error(f'Game init error: {e}\n{traceback.format_exc()}')
            self.game = Game(load_save=False, save_dir=get_save_dir())

    def build(self):
        try:
            Window.clearcolor = (0.1, 0.1, 0.18, 1)
        except Exception as e:
            log_error(f'Window error: {e}')
        
        # 加载 KV
        self._load_kv_files()
        
        # 创建 TabbedPanel
        tp = TabbedPanel(do_default_tab=False, tab_width=dp(120))
        tp.background_color = (0.1, 0.1, 0.2, 1)
        tp.background = ''
        
        screens = [
            ('卡牌库', CardLibraryScreen),
            ('繁殖实验室', BreedingLabScreen),
            ('基因工程', GeneEngineeringScreen),
            ('科技树', TechTreeScreen),
            ('基因抽卡', GachaScreen),
            ('战斗', BattleScreen),
            ('敌人图鉴', BestiaryScreen),
            ('任务', QuestScreen),
        ]
        
        self._screen_refs = {}
        for tab_name, screen_cls in screens:
            screen = screen_cls(name=tab_name.lower().replace(' ', '_'))
            screen.game = self.game  # 注入游戏实例
            self._screen_refs[tab_name] = screen
            
            header = TabbedPanelHeader(text=tab_name)
            header.content = screen
            tp.add_widget(header)
        
        def _on_tab_change(instance, value):
            for tab in tp.tab_list:
                content = tab.content
                if tab == tp.current_tab and hasattr(content, 'on_enter'):
                    content.on_enter()
        
        tp.bind(current_tab=_on_tab_change)
        
        # 定时保存
        Clock.schedule_interval(lambda dt: self._auto_save(), 30)
        Clock.schedule_interval(lambda dt: self._update_breeding(), 0.5)
        
        log_error('App.build() complete')
        return tp
    
    def _load_kv_files(self):
        kv_files = [
            'main.kv',
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
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), kv_file)
            if os.path.exists(path):
                try:
                    Builder.load_file(path)
                    log_error(f'Loaded KV: {kv_file}')
                except Exception as e:
                    log_error(f'KV error {kv_file}: {e}')
    
    def _auto_save(self):
        try:
            if self.game:
                self.game.save_game()
        except Exception as e:
            log_error(f'Auto-save: {e}')
    
    def _update_breeding(self):
        try:
            if self.game:
                self.game.update_breeding()
        except Exception:
            pass
    
    def refresh_breeding_combos(self):
        """供屏幕调用的刷新方法"""
        for name, screen in self._screen_refs.items():
            if hasattr(screen, 'on_enter'):
                screen.on_enter()
    
    def on_pause(self):
        try:
            if self.game:
                self.game.save_game()
        except Exception as e:
            log_error(f'Pause save: {e}')
        return True

if __name__ == '__main__':
    try:
        GeneCryptApp().run()
    except Exception as e:
        log_error(f'App run error: {e}\n{traceback.format_exc()}')
        raise