# main.py - Android 入口
import os
import sys
import traceback
import json

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
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.textinput import TextInput
    from kivy.uix.popup import Popup
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
        os.path.join(base_dir, 'assets', 'fonts', 'NotoSansCJKsc-Regular.otf'),
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
    from screens.challenge import ChallengeScreen
    from screens.stats import StatsScreen
    from screens.dungeon import DungeonScreen
    from screens.pvp import PvPScreen
    from screens.debug_console import DebugConsole
    from screens.equipment import EquipmentScreen
    from screens.base_building import BaseBuildingScreen
    from screens.achievement import AchievementScreen
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
        
        self._load_kv_files()
        
        root = FloatLayout()
        self._main_panel = self._build_main_panel()
        self._login_panel = self._build_login_panel()
        self._main_panel.size_hint = (1, 1)
        self._login_panel.size_hint = (1, 1)
        root.add_widget(self._main_panel)
        root.add_widget(self._login_panel)
        self._main_panel.opacity = 0
        self._main_panel.disabled = True
        self._login_panel.opacity = 1
        self._login_panel.disabled = False
        
        Clock.schedule_once(lambda dt: self._check_update(), 2)
        
        log_error('App.build() complete')
        return root

    def _build_main_panel(self):
        tp = TabbedPanel(do_default_tab=False, tab_width=dp(100))
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
            ('主题挑战', ChallengeScreen),
            ('数据', StatsScreen),
            ('副本', DungeonScreen),
            ('PvP', PvPScreen),
            ('基建', BaseBuildingScreen),
            ('成就', AchievementScreen),
            ('控制台', DebugConsole),
        ]
        
        self._screen_refs = {}
        for tab_name, screen_cls in screens:
            screen = screen_cls(name=tab_name.lower().replace(' ', '_'))
            screen.game = self.game
            self._screen_refs[tab_name] = screen
            header = TabbedPanelHeader(text=tab_name)
            header.content = screen
            tp.add_widget(header)
        
        acct_header = TabbedPanelHeader(text='☁账户')
        acct_header.content = self._build_account_tab()
        self._acct_header = acct_header
        tp.add_widget(acct_header)
        
        def _on_tab_change(instance, value):
            for tab in tp.tab_list:
                content = tab.content
                if tab == tp.current_tab and hasattr(content, 'on_enter'):
                    content.on_enter()
            if tp.current_tab and tp.current_tab.text == '☁账户':
                self._refresh_account_tab()
        
        tp.bind(current_tab=_on_tab_change)
        
        Clock.schedule_interval(lambda dt: self._auto_save(), 30)
        Clock.schedule_interval(lambda dt: self._update_breeding(), 0.5)
        Clock.schedule_interval(lambda dt: self._cloud_tick(), 300)
        return tp

    def _build_account_tab(self):
        box = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(15))
        self._acct_info_lbl = Label(text='', halign='left', valign='top',
                                     size_hint_y=None, height=dp(120))
        box.add_widget(self._acct_info_lbl)
        nick_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(6))
        self._nick_input = TextInput(text='', multiline=False, size_hint_x=0.7,
                                     hint_text='新昵称')
        nick_row.add_widget(self._nick_input)
        nick_row.add_widget(Button(text='修改昵称', on_press=lambda _: self._do_change_nickname()))
        box.add_widget(nick_row)
        box.add_widget(Button(text='立即同步存档', size_hint_y=None, height=dp(40),
                              on_press=lambda _: self._manual_sync()))
        box.add_widget(Button(text='切换账号', size_hint_y=None, height=dp(40),
                              on_press=lambda _: self._switch_account()))
        box.add_widget(Label(text='', size_hint_y=1))
        return box

    def _refresh_account_tab(self):
        from services.cloud_save import CloudSave
        cs = CloudSave()
        if cs.is_logged_in():
            self._acct_info_lbl.text = (f'昵称: {cs.nickname}\n'
                                        f'登录名: {cs.username}\n'
                                        f'UUID: {cs.account_uuid or "未绑定"}\n\n'
                                        f'云端存档已启用，每5分钟自动同步')
        else:
            self._acct_info_lbl.text = '未登录'

    def _build_login_panel(self):
        box = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(30))
        box.add_widget(Label(text='基因密码 GeneCrypt', size_hint_y=None, height=dp(50),
                              font_size=dp(24), bold=True, color=(0, 0.85, 1, 1)))
        box.add_widget(Label(text='', size_hint_y=None, height=dp(20)))
        from services.account import get_last_username
        last_user = get_last_username()
        self._login_username = TextInput(text=last_user, multiline=False,
                                          size_hint_y=None, height=dp(44),
                                          hint_text='用户名')
        self._login_password = TextInput(text='', multiline=False, password=True,
                                          size_hint_y=None, height=dp(44),
                                          hint_text='密码')
        self._login_status = Label(text='', size_hint_y=None, height=dp(24), color=(1, 0.5, 0.5, 1))
        box.add_widget(Label(text='用户名:', size_hint_y=None, height=dp(20)))
        box.add_widget(self._login_username)
        box.add_widget(Label(text='密码:', size_hint_y=None, height=dp(20)))
        box.add_widget(self._login_password)
        box.add_widget(self._login_status)
        btn_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(46), spacing=dp(10))
        btn_row.add_widget(Button(text='登录', on_press=lambda _: self._do_login()))
        btn_row.add_widget(Button(text='注册新账号', on_press=lambda _: self._show_register()))
        box.add_widget(btn_row)
        box.add_widget(Label(text='登录后可跨设备同步存档', size_hint_y=None, height=dp(20),
                              color=(0.5, 0.5, 0.5, 1)))
        box.add_widget(Label(text='', size_hint_y=1))
        return box

    def _do_login(self):
        username = self._login_username.text.strip()
        password = self._login_password.text
        if not username or not password:
            self._login_status.text = '请输入用户名和密码'
            return
        from services.cloud_save import CloudSave
        cs = CloudSave()
        self._login_status.text = '登录中...'
        cs.login(username, password, callback=lambda r: self._on_login_result(r))

    def _show_register(self):
        from kivy.uix.popup import Popup
        from kivy.uix.scrollview import ScrollView
        content = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(10))
        content.add_widget(Label(text='注册新账号', size_hint_y=None, height=dp(24), bold=True))
        u_input = TextInput(text='', multiline=False, size_hint_y=None, height=dp(40), hint_text='用户名')
        p_input = TextInput(text='', multiline=False, password=True, size_hint_y=None, height=dp(40), hint_text='密码(至少4位)')
        p2_input = TextInput(text='', multiline=False, password=True, size_hint_y=None, height=dp(40), hint_text='确认密码')
        n_input = TextInput(text='', multiline=False, size_hint_y=None, height=dp(40), hint_text='昵称(可选)')
        status_lbl = Label(text='', size_hint_y=None, height=dp(22), color=(1, 0.5, 0.5, 1))
        content.add_widget(u_input)
        content.add_widget(p_input)
        content.add_widget(p2_input)
        content.add_widget(n_input)
        content.add_widget(status_lbl)
        popup = Popup(title='注册', content=content, size_hint=(0.85, 0.75))
        def _do_register(_):
            uname = u_input.text.strip()
            pw = p_input.text
            pw2 = p2_input.text
            nick = n_input.text.strip()
            if not uname or not pw:
                status_lbl.text = '请填写用户名和密码'; return
            if pw != pw2:
                status_lbl.text = '两次密码不一致'; return
            from services.cloud_save import CloudSave
            cs = CloudSave()
            cs.register(uname, pw, nick, callback=lambda r: self._on_register_result(r, popup, status_lbl))
            status_lbl.text = '注册中...'
        btn = Button(text='确认注册', size_hint_y=None, height=dp(40), on_press=_do_register)
        content.add_widget(btn)
        popup.open()

    def _on_register_result(self, result, popup, status_lbl):
        success, msg = result[0], result[1]
        if success:
            popup.dismiss()
            self._show_main_panel()
            self._refresh_account_tab()
        else:
            status_lbl.text = msg

    def _on_login_result(self, result):
        success = result[0]
        msg = result[1]
        if success:
            self._login_status.text = ''
            if len(result) > 2 and result[2]:
                save = result[2].get('save')
                if save:
                    try:
                        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gene_game_save.json')
                        with open(path, 'w', encoding='utf-8') as f:
                            json.dump(save, f, ensure_ascii=False)
                        self.game.load_game()
                    except:
                        pass
            self._show_main_panel()
            self._refresh_account_tab()
        else:
            self._login_status.text = msg

    def _show_main_panel(self):
        if self._login_panel.parent is not None:
            self._login_panel.parent.remove_widget(self._login_panel)
        self._main_panel.opacity = 1
        self._main_panel.disabled = False

    def _show_login_panel(self):
        if self._login_panel.parent is None and self._main_panel.parent is not None:
            self._main_panel.parent.add_widget(self._login_panel)
        self._main_panel.opacity = 0
        self._main_panel.disabled = True
        self._login_panel.opacity = 1
        self._login_panel.disabled = False
        from services.account import get_last_username
        self._login_username.text = get_last_username()
        self._login_password.text = ''

    def _do_change_nickname(self):
        nick = self._nick_input.text.strip()
        if not nick:
            return
        from services.cloud_save import CloudSave
        cs = CloudSave()
        cs.change_nickname(nick, callback=lambda r: self._on_nickname_result(r))

    def _on_nickname_result(self, result):
        from kivy.uix.popup import Popup
        Popup(title='提示', content=Label(text=result[1]), size_hint=(0.5, 0.25)).open()
        self._refresh_account_tab()

    def _manual_sync(self):
        from services.cloud_save import CloudSave
        cs = CloudSave()
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gene_game_save.json')
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                cs.upload(data, callback=lambda r: self._sync_result(r))
            except:
                pass

    def _sync_result(self, result):
        from kivy.uix.popup import Popup
        Popup(title='同步', content=Label(text=result[1]), size_hint=(0.5, 0.25)).open()

    def _switch_account(self):
        from services.cloud_save import CloudSave
        from services.account import set_last_username
        cs = CloudSave()
        cs.logout()
        self._show_login_panel()

    def _check_update(self):
        try:
            from services import updater
            updater.check_update(callback=self._on_update_check)
        except:
            pass

    def _on_update_check(self, result):
        latest, dl_url = result
        if not latest or not dl_url:
            return
        from services import updater
        if not updater.has_update(latest):
            return
        from kivy.uix.popup import Popup
        content = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(10))
        content.add_widget(Label(text=f'发现新版本 v{latest}\n当前版本 v{updater.APP_VERSION}',
                                 size_hint_y=None, height=dp(50)))
        self._update_progress = Label(text='', size_hint_y=None, height=dp(22), color=(0.4, 1, 0.4, 1))
        content.add_widget(self._update_progress)
        btn_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(8))
        popup = Popup(title='更新', content=content, size_hint=(0.75, 0.4))
        def _do_download(_):
            self._update_progress.text = '下载中...'
            updater.download_apk(dl_url,
                                 progress_cb=lambda p: setattr(self._update_progress, 'text', f'下载中 {p}%'),
                                 done_cb=lambda p: self._on_download_done(p, popup))
        btn_row.add_widget(Button(text='下载并更新', on_press=_do_download))
        btn_row.add_widget(Button(text='稍后再说', on_press=popup.dismiss))
        content.add_widget(btn_row)
        popup.open()

    def _on_download_done(self, apk_path, popup):
        if not apk_path:
            self._update_progress.text = '下载失败'
            return
        self._update_progress.text = '下载完成，打开安装器'
        from services import updater
        updater.open_installer(apk_path)
        popup.dismiss()

    def _cloud_tick(self):
        try:
            from services.cloud_save import CloudSave
            cs = CloudSave()
            if not cs.is_logged_in():
                return
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gene_game_save.json')
            if not os.path.exists(path):
                return
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            cs.upload(data)
        except:
            pass

    def show_cloud_login(self, *args):
        self._show_login_panel()
    
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
        for name, screen in self._screen_refs.items():
            if hasattr(screen, 'on_enter'):
                screen.on_enter()
        if self.game:
            newly = self.game._check_all_quests()
            for q in newly:
                from kivy.uix.popup import Popup
                from kivy.uix.boxlayout import BoxLayout
                from kivy.uix.label import Label
                from kivy.uix.button import Button
                content = BoxLayout(orientation='vertical', padding=dp(20))
                content.add_widget(Label(text=f'任务完成!\n{q["title"]}', halign='center'))
                btn = Button(text='确定', size_hint_y=None, height=dp(40))
                content.add_widget(btn)
                popup = Popup(title='任务完成', content=content, size_hint=(0.5, 0.3))
                btn.bind(on_press=popup.dismiss)
                popup.open()
    
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