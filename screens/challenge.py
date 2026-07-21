from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from gene_config import CHALLENGE_FACTORS, CHALLENGE_GROUPS_BY_THEME


class ChallengeScreen(Screen):
    THEMES = [
        {'id': 'subject_rampage', 'name': '实验体暴乱', 'desc': '研究所实验体失控暴走，镇压暴乱',
         'difficulty': '★★★☆☆', 'unlock': 50},
        {'id': 'abandoned_lab', 'name': '废弃实验室', 'desc': '废弃研究所中的有毒废料和突变生物',
         'difficulty': '★★★★☆', 'unlock': 60},
        {'id': 'ancient_ruins', 'name': '远古遗迹', 'desc': '探索失落的远古文明遗迹，击败守护者',
         'difficulty': '★★★★★', 'unlock': 80},
        {'id': 'elemental_cycle', 'name': '元素轮回', 'desc': '打破元素循环，终结狂潮',
         'difficulty': '★★★★★★', 'unlock': 100},
        {'id': 'blind_box_war', 'name': '盲盒战争', 'desc': '每个盲盒隐藏未知威胁',
         'difficulty': '★★★★★★★', 'unlock': 120},
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._selected_theme = None
        self._selected_factors = set()
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        title = Label(text='主题挑战', size_hint_y=0.06, bold=True, color=(1, 0.85, 0, 1))
        main.add_widget(title)
        sv = ScrollView(size_hint_y=1)
        self._content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self._content.bind(minimum_height=self._content.setter('height'))
        sv.add_widget(self._content)
        main.add_widget(sv)
        self.add_widget(main)

    def on_enter(self):
        self._show_themes()

    def _show_themes(self):
        self._selected_theme = None
        self._content.clear_widgets()
        app = App.get_running_app()
        game = app.game
        for theme in self.THEMES:
            tid = theme['id']
            locked = game.max_stage < theme['unlock']
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(85),
                              spacing=dp(2), padding=dp(6))
            from kivy.graphics import Color as GfxColor, Rectangle
            with card.canvas.before:
                GfxColor(0.2, 0.3, 0.2, 1) if not locked else GfxColor(0.2, 0.2, 0.25, 1)
                card._bg = Rectangle(pos=card.pos, size=card.size)
            card.bind(pos=lambda c,v: setattr(c._bg,'pos',v),
                      size=lambda c,v: setattr(c._bg,'size',v))

            head = BoxLayout(orientation='horizontal', size_hint_y=0.35)
            name_color = (1, 0.85, 0, 1) if not locked else (0.5, 0.5, 0.5, 1)
            head.add_widget(Label(text=f'{theme["name"]}', color=name_color,
                                  bold=True, size_hint_x=0.55, halign='left'))
            head.add_widget(Label(text=theme['difficulty'], color=(0.7, 0.7, 0.7, 1),
                                  size_hint_x=0.45, halign='right'))
            card.add_widget(head)

            desc_lbl = Label(text=theme['desc'], size_hint_y=0.25, color=(0.7, 0.7, 0.7, 1), halign='left')
            card.add_widget(desc_lbl)

            bot = BoxLayout(orientation='horizontal', size_hint_y=0.4)
            if locked:
                bot.add_widget(Label(text=f'[通关第{theme["unlock"]}关解锁]', color=(0.6, 0.2, 0.2, 1)))
            else:
                hs = game.challenge_scores.get(tid)
                if hs:
                    tm = hs.get('time_str', '--:--')
                    bot.add_widget(Label(text=f'最高分: {hs["points"]}分  {tm}',
                                          color=(0.4, 1, 0.4, 1), size_hint_x=0.65))
                else:
                    bot.add_widget(Label(text='暂无记录', color=(0.5, 0.5, 0.5, 1), size_hint_x=0.65))
                btn = Button(text='选择因子', size_hint_x=0.35, background_color=(0.15, 0.5, 0.15, 1))
                btn.bind(on_press=lambda _, t=tid: self._show_factors(t))
                bot.add_widget(btn)
            card.add_widget(bot)
            self._content.add_widget(card)

    def _show_factors(self, theme_id):
        self._selected_theme = theme_id
        self._selected_factors.clear()
        self._content.clear_widgets()

        bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(38), spacing=dp(4))
        bar.add_widget(Button(text='返回', size_hint_x=0.2, on_press=lambda _: self._show_themes()))
        bar.add_widget(Button(text='一键全选', size_hint_x=0.25, on_press=lambda _: self._select_all(theme_id)))
        self._pts_lbl = Label(text='分: 0', size_hint_x=0.55, color=(1, 0.85, 0, 1))
        bar.add_widget(self._pts_lbl)
        self._content.add_widget(bar)

        theme_factors = [f for f in CHALLENGE_FACTORS if f.get('theme') == theme_id]
        grouped = {}
        for f in theme_factors:
            g = f.get('group', '其他')
            grouped.setdefault(g, []).append(f)

        for gname, factors in grouped.items():
            self._content.add_widget(Label(text=f'-- {gname} --', size_hint_y=None, height=dp(22),
                                            bold=True, color=(0, 0.85, 1, 1)))
            for f in factors:
                fid = f['id']
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(34), spacing=dp(3))
                sel = fid in self._selected_factors
                clr = (0.2, 0.7, 0.2, 1) if sel else (0.3, 0.3, 0.3, 1)
                btn = Button(text=f'{f["points"]}分 {f["name"]}', size_hint_x=0.3,
                             background_color=clr, font_size=dp(10))
                btn._fid = fid
                btn.bind(on_press=self._toggle_factor)
                row.add_widget(btn)
                row.add_widget(Label(text=f['desc'], size_hint_x=0.7, color=(0.7, 0.7, 0.7, 1),
                                     font_size=dp(10), halign='left'))
                self._content.add_widget(row)

        self._content.add_widget(Label(text='', size_hint_y=None, height=dp(8)))
        self._content.add_widget(Button(text='开始挑战', size_hint_y=None, height=dp(40),
                                         background_color=(0.2, 0.6, 0.2, 1),
                                         on_press=lambda _: self._start_challenge()))

    def _toggle_factor(self, btn):
        fid = getattr(btn, '_fid', None)
        if not fid:
            return
        factor = next((f for f in CHALLENGE_FACTORS if f['id'] == fid), None)
        if not factor:
            return
        if fid in self._selected_factors:
            self._selected_factors.discard(fid)
            btn.background_color = (0.3, 0.3, 0.3, 1)
        else:
            pre = factor.get('prereq')
            if pre and pre not in self._selected_factors and not pre.startswith('__'):
                return
            exc = factor.get('exclusive')
            if exc and exc not in ('team_3', 'team_4', 'bb_team_3', 'bb_team_4'):
                for sfid in list(self._selected_factors):
                    sf = next((f for f in CHALLENGE_FACTORS if f['id'] == sfid), None)
                    if sf and sf.get('exclusive') == exc:
                        self._selected_factors.discard(sfid)
            self._selected_factors.add(fid)
            btn.background_color = (0.2, 0.7, 0.2, 1)
        pts = sum(f['points'] for f in CHALLENGE_FACTORS if f['id'] in self._selected_factors)
        self._pts_lbl.text = f'分: {pts}'

    def _select_all(self, theme_id):
        self._selected_factors.clear()
        exclusives_seen = set()
        for f in CHALLENGE_FACTORS:
            if f.get('theme') != theme_id: continue
            pre = f.get('prereq')
            if pre and pre.startswith('__'): continue
            exc = f.get('exclusive')
            if exc and exc in exclusives_seen: continue
            if exc: exclusives_seen.add(exc)
            self._selected_factors.add(f['id'])
        pts = sum(f['points'] for f in CHALLENGE_FACTORS if f['id'] in self._selected_factors)
        self._pts_lbl.text = f'分: {pts}'
        self._show_factors(theme_id)

    def _start_challenge(self):
        if not self._selected_theme:
            return
        import time
        app = App.get_running_app()
        from battle_config import STAGES
        from gene_game import BattleSystem
        from screens.battle import BattleScreen

        battle_screen = app._screen_refs.get('战斗')
        if battle_screen is None or not isinstance(battle_screen, BattleScreen):
            return

        if not battle_screen._team:
            popup = Popup(title='错误', content=Label(text='请先在战斗页选好队伍！'),
                          size_hint=(0.5, 0.25))
            popup.open()
            return

        theme_info = next((t for t in self.THEMES if t['id'] == self._selected_theme), None)
        stage_num = theme_info['unlock'] if theme_info else 50
        stage = STAGES.get(stage_num, STAGES.get(1))
        grid = dict(battle_screen._team)
        enemy_data = [dict(e) for e in stage.get('enemies', [])]
        if not enemy_data:
            enemy_data = [{'name': '挑战敌人', 'health': 200, 'attack': 20, 'defense': 10, 'speed': 12,
                           'skills': [], 'passive_abilities': [], 'width': 1, 'height': 1, 'position': 0}]
        for e in enemy_data:
            e['health'] = int(e['health'] * 1.2)
            e['attack'] = int(e['attack'] * 1.2)

        bs = BattleSystem(grid, enemy_data, stage_num=stage_num, skill_enhance_level=0)
        bs.is_running = True
        battle_screen._battle_system = bs
        battle_screen._battle_running = True
        battle_screen._selected_stage = stage_num
        battle_screen._render_battle_grid()
        pts = sum(f['points'] for f in CHALLENGE_FACTORS if f['id'] in self._selected_factors)
        battle_screen.add_log(f'[挑战] 主题:{theme_info["name"] if theme_info else "?"} 积分:{pts}')
        self._challenge_start = time.time()
        self._challenge_pts = pts
        Clock.schedule_interval(battle_screen._battle_tick, 0.3)
        battle_screen._challenge_info = {
            'theme_id': self._selected_theme,
            'start_time': time.time(),
            'points': pts,
        }
        for tab in app.root.tab_list:
            if tab.text == '战斗':
                app.root.switch_to(tab)
                break
