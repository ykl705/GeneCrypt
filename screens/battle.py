from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Line
from functools import partial


class BattleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._battle_system = None
        self._battle_running = False
        self._grid_widgets = {}
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        title = Label(text='战斗系统', size_hint_y=0.05, bold=True, color=(1, 1, 1, 1))
        main.add_widget(title)

        controls = BoxLayout(orientation='horizontal', size_hint_y=0.06, spacing=dp(5))
        controls.add_widget(Label(text='关卡:', color=(0.8, 0.8, 0.8, 1)))
        self._stage_btn = Button(text='选择关卡', on_press=lambda _: self._show_stage_select())
        controls.add_widget(self._stage_btn)
        self._team_btn = Button(text='选择队伍', on_press=lambda _: self._show_team_select())
        controls.add_widget(self._team_btn)
        self._start_btn = Button(text='开始战斗', on_press=lambda _: self._start_battle())
        self._start_btn.background_color = (0.2, 0.6, 0.2, 1)
        controls.add_widget(self._start_btn)
        self._auto_btn = Button(text='自动', on_press=lambda _: self._toggle_auto())
        controls.add_widget(self._auto_btn)
        self._exit_btn = Button(text='退出战斗', on_press=lambda _: self._exit_battle())
        controls.add_widget(self._exit_btn)
        main.add_widget(controls)

        self._battle_area = BoxLayout(orientation='vertical', size_hint_y=0.6, spacing=dp(5))
        self._battle_area.add_widget(Label(text='选择关卡和队伍后开始战斗', color=(0.5, 0.5, 0.5, 1)))
        main.add_widget(self._battle_area)

        log_box = BoxLayout(orientation='vertical', size_hint_y=0.3)
        log_box.add_widget(Label(text='战斗日志', size_hint_y=0.1, color=(0.8, 0.8, 0.8, 1)))
        sv = ScrollView()
        self._log = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(1))
        self._log.bind(minimum_height=self._log.setter('height'))
        sv.add_widget(self._log)
        log_box.add_widget(sv)
        main.add_widget(log_box)

        self._reward_box = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=dp(5))
        main.add_widget(self._reward_box)

        self.add_widget(main)
        self._selected_stage = 1
        self._team = {}
        self._pending_card = None

    def on_enter(self):
        pass

    def _show_stage_select(self):
        app = App.get_running_app()
        from battle_config import STAGES
        content = BoxLayout(orientation='vertical', spacing=dp(5))
        sv = ScrollView()
        inner = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        inner.bind(minimum_height=inner.setter('height'))
        for snum in sorted([s for s in STAGES if isinstance(s, int) and s in app.game.unlocked_stages]):
            stage = STAGES[snum]
            map_name = stage.get('map', '?')
            btn = Button(text=f'第{snum}关 ({map_name})', size_hint_y=None, height=dp(40),
                         on_press=lambda _, s=snum: self._select_stage(s))
            inner.add_widget(btn)
        sv.add_widget(inner)
        content.add_widget(sv)
        close_btn = Button(text='关闭', size_hint_y=0.15)
        content.add_widget(close_btn)
        popup = Popup(title='选择关卡', content=content, size_hint=(0.5, 0.6))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
        self._stage_popup = popup

    def _select_stage(self, snum):
        self._selected_stage = snum
        self._stage_btn.text = f'第{snum}关'
        if hasattr(self, '_stage_popup'):
            self._stage_popup.dismiss()

    def _show_team_select(self):
        app = App.get_running_app()
        content = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(10))

        hint_lbl = Label(text='选择出战卡牌: 点击下方卡牌选中，再点击上方格子放置',
                         size_hint_y=None, height=dp(30), color=(0.8, 0.8, 0.8, 1))
        content.add_widget(hint_lbl)

        self._pending_lbl = Label(text='', size_hint_y=None, height=dp(25),
                                   color=(0.4, 1, 0.4, 1))
        content.add_widget(self._pending_lbl)

        grid_label = Label(text='[ 出战阵型 - 点击格子放置/移除 ]', size_hint_y=None,
                            height=dp(25), color=(1, 1, 1, 1))
        content.add_widget(grid_label)

        self._grid_btns = {}
        grid = GridLayout(cols=3, spacing=dp(4), size_hint_y=None, height=dp(210))
        for pos in range(9):
            card_at_pos = self._team.get(pos)
            text = f'[{pos+1}] {card_at_pos.name}' if card_at_pos else f'[空{pos+1}]'
            color = (0.3, 0.8, 1, 1) if card_at_pos else (0.4, 0.4, 0.4, 1)
            btn = Button(text=text, size_hint=(1, None), height=dp(60),
                         background_color=color, halign='center')
            btn.bind(on_press=lambda _, p=pos: self._grid_cell_clicked(p))
            grid.add_widget(btn)
            self._grid_btns[pos] = btn
        content.add_widget(grid)

        card_label = Label(text='[ 可用卡牌 ]', size_hint_y=None, height=dp(25),
                            color=(1, 1, 1, 1))
        content.add_widget(card_label)

        sv = ScrollView(size_hint_y=0.4)
        inner = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        inner.bind(minimum_height=inner.setter('height'))
        for card in app.game.cards:
            if not card.is_alive:
                continue
            in_team = any(card.id == (c2.id if c2 else None) for c2 in self._team.values())
            prefix = '[已上阵] ' if in_team else ''
            btn = Button(
                text=f'{prefix}{card.name} ATK:{card.traits.get("attack",0)} HP:{card.traits.get("health",0)}',
                size_hint_y=None, height=dp(36))
            btn.bind(on_press=lambda _, c=card: self._pick_card(c))
            inner.add_widget(btn)
        sv.add_widget(inner)
        content.add_widget(sv)

        btn_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(44), spacing=dp(10))
        confirm = Button(text='确认编队')
        clear = Button(text='清空全部')
        btn_row.add_widget(confirm)
        btn_row.add_widget(clear)
        content.add_widget(btn_row)

        popup = Popup(title='选择队伍', content=content, size_hint=(0.8, 0.85))
        confirm.bind(on_press=lambda _: popup.dismiss())
        clear.bind(on_press=lambda _: self._clear_team_ui())
        popup.open()

    def _pick_card(self, card):
        self._pending_card = card
        self._pending_lbl.text = f'已选中: {card.name} (点击上方格子放置)'

    def _grid_cell_clicked(self, pos):
        if self._pending_card:
            self._team[pos] = self._pending_card
            self._pending_card = None
            self._pending_lbl.text = ''
            self._refresh_team_ui()
            self._team_btn.text = f'队伍: {len(self._team)}/3'
        elif pos in self._team:
            del self._team[pos]
            self._refresh_team_ui()
            self._team_btn.text = f'队伍: {len(self._team)}/3'

    def _refresh_team_ui(self):
        for pos, btn in self._grid_btns.items():
            card_at_pos = self._team.get(pos)
            btn.text = f'[{pos+1}] {card_at_pos.name}' if card_at_pos else f'[空{pos+1}]'
            btn.background_color = (0.3, 0.8, 1, 1) if card_at_pos else (0.4, 0.4, 0.4, 1)

    def _clear_team_ui(self):
        self._team = {}
        self._pending_card = None
        self._pending_lbl.text = ''
        self._refresh_team_ui()
        self._team_btn.text = '选择队伍'

    def _start_battle(self):
        try:
            self._start_battle_impl()
        except Exception as e:
            import traceback
            err_msg = f'战斗初始化失败:\n{str(e)[:200]}'
            popup = Popup(title='错误', content=Label(text=err_msg), size_hint=(0.7, 0.35))
            popup.open()

    def _start_battle_impl(self):
        if not self._team:
            popup = Popup(title='错误', content=Label(text='请选择队伍'), size_hint=(0.5, 0.3))
            popup.open()
            return
        from battle_config import STAGES
        if self._selected_stage not in STAGES:
            popup = Popup(title='错误', content=Label(text=f'关卡 {self._selected_stage} 不存在'),
                          size_hint=(0.5, 0.3))
            popup.open()
            return
        app = App.get_running_app()
        stage = STAGES[self._selected_stage]
        from gene_game import BattleSystem
        grid = {pos: card for pos, card in self._team.items()}
        enemy_data_raw = stage.get('enemies', stage.get('waves', []))
        enemy_data = []
        if enemy_data_raw and isinstance(enemy_data_raw, list):
            first = enemy_data_raw[0] if enemy_data_raw else None
            if isinstance(first, dict) and 'name' in first:
                enemy_data = [dict(e) for e in enemy_data_raw]
            else:
                for wave_entry in enemy_data_raw:
                    entries = wave_entry.get('enemies', [wave_entry]) if isinstance(wave_entry, dict) else wave_entry
                    if isinstance(entries, list):
                        for e in entries:
                            if isinstance(e, dict) and 'name' in e:
                                enemy_data.append(dict(e))
                            elif isinstance(e, str):
                                from battle_config import ENEMY_TEMPLATES
                                tmpl = ENEMY_TEMPLATES.get(e)
                                if tmpl:
                                    ed = {
                                        'name': tmpl['name'],
                                        'health': int(tmpl.get('base_health', 100)),
                                        'attack': int(tmpl.get('base_attack', 10)),
                                        'defense': int(tmpl.get('base_defense', 5)),
                                        'speed': int(tmpl.get('base_speed', 10)),
                                        'skills': [],
                                        'passive_abilities': tmpl.get('passive_abilities', []),
                                        'width': 1, 'height': 1,
                                    }
                                    enemy_data.append(ed)
        if not enemy_data:
            enemy_data = [{'name': '测试敌人', 'health': 50, 'attack': 10, 'defense': 5, 'speed': 8,
                           'skills': [], 'passives': [], 'width': 1, 'height': 1, 'position': 0}]
        stage_num = self._selected_stage
        skill_enhance = app.game.tech_tree.get('skill_enhance', {}).get('level', 0)
        self._battle_system = BattleSystem(grid, enemy_data, stage_num=stage_num,
                                           skill_enhance_level=skill_enhance)
        self._battle_system.is_running = True
        self._battle_running = True
        self._render_battle_grid()
        self.add_log('战斗开始!')
        Clock.schedule_interval(self._battle_tick, 0.3)

    def _render_battle_grid(self):
        self._battle_area.clear_widgets()
        self._grid_widgets = {}
        bs = self._battle_system
        grid_container = BoxLayout(orientation='horizontal', spacing=dp(20))
        player_side = BoxLayout(orientation='vertical', size_hint_x=0.5, spacing=dp(2))
        player_side.add_widget(Label(text='我方', color=(0.3, 0.8, 1, 1), size_hint_y=0.1))
        pg = GridLayout(cols=bs.grid_size, spacing=dp(2), size_hint_y=0.9)
        for unit in bs.player_team:
            cell = self._create_unit_cell(unit)
            pg.add_widget(cell)
            self._grid_widgets[unit.id] = cell
        player_side.add_widget(pg)
        grid_container.add_widget(player_side)

        enemy_side = BoxLayout(orientation='vertical', size_hint_x=0.5, spacing=dp(2))
        enemy_side.add_widget(Label(text='敌方', color=(1, 0.3, 0.3, 1), size_hint_y=0.1))
        eg = GridLayout(cols=bs.enemy_grid_size, spacing=dp(2), size_hint_y=0.9)
        for unit in bs.enemies:
            cell = self._create_unit_cell(unit)
            eg.add_widget(cell)
            self._grid_widgets[unit.id] = cell
        enemy_side.add_widget(eg)
        grid_container.add_widget(enemy_side)
        self._battle_area.add_widget(grid_container)

    def _create_unit_cell(self, unit):
        cell = BoxLayout(orientation='vertical', spacing=dp(1), padding=dp(2))
        cell.size_hint = (1, None)
        cell.height = dp(90)
        name_color = (0.3, 0.8, 1, 1) if unit.is_player else (1, 0.3, 0.3, 1)
        name_lbl = Label(text=unit.name, size_hint_y=0.2, color=name_color, font_size=dp(10))
        cell.add_widget(name_lbl)

        hp_bar = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=dp(2))
        hp_bar.add_widget(Label(text='HP', size_hint_x=0.2, font_size=dp(8), color=(1, 1, 1, 1)))
        hp_fill = Label(text=f'{unit.current_health}/{unit.max_health}', size_hint_x=0.8,
                        font_size=dp(8), color=(0.3, 1, 0.3, 1))
        hp_bar.add_widget(hp_fill)
        cell.add_widget(hp_bar)

        action_bar = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=dp(2))
        action_bar.add_widget(Label(text='ATB', size_hint_x=0.2, font_size=dp(8), color=(1, 1, 1, 1)))
        from battle_config import BATTLE_CONFIG
        max_bar = BATTLE_CONFIG['action_bar_max']
        ab = min(unit.action_bar / max_bar, 1.0)
        ab_lbl = Label(text=f'{ab*100:.0f}%', size_hint_x=0.8, font_size=dp(8), color=(0.8, 0.8, 0, 1))
        action_bar.add_widget(ab_lbl)
        cell.add_widget(action_bar)

        atk_lbl = Label(text=f'ATK:{unit.attack} SPD:{unit.speed}',
                        size_hint_y=0.2, font_size=dp(8), color=(0.8, 0.8, 0.8, 1))
        cell.add_widget(atk_lbl)
        return cell

    def _battle_tick(self, dt):
        if not self._battle_running:
            return False
        try:
            bs = self._battle_system
            if not bs.is_running:
                self._battle_running = False
                return False
            bs.update_action_bars_frame()
            bs.update_status_damage()
            unit = bs.get_next_unit()
            if unit:
                if unit.is_player and not bs.is_auto:
                    from battle_config import BATTLE_CONFIG as _BC
                    max_bar_val = _BC['action_bar_max']
                    unit.action_bar -= max_bar_val
                    if bs.marked_target:
                        target = bs.marked_target
                        bs.marked_target = None
                    else:
                        front = [e for e in bs.enemies if e.is_alive]
                        target = front[0] if front else None
                    if target:
                        result = bs.execute_turn(unit, [target])
                        if result:
                            self.add_log(f'{unit.name} → {target.name} 造成 {result.get("damage", 0)} 伤害')
                            if not target.is_alive:
                                self.add_log(f'{target.name} 被击败!')
                else:
                    result = bs.execute_turn(unit, None)
                    if result:
                        dmg = result.get('damage', 0)
                        tname = result.get('target', '?')
                        self.add_log(f'{unit.name} → {tname} 造成 {dmg} 伤害')
                self._check_battle_end()
                self._update_grid()
        except Exception as e:
            self.add_log(f'[ERROR] {e}')
        return True

    def _check_battle_end(self):
        bs = self._battle_system
        alive_players = [u for u in bs.player_team if u.is_alive]
        alive_enemies = [u for u in bs.enemies if u.is_alive]
        if not alive_enemies:
            bs.is_running = False
            self._battle_running = False
            self.add_log('🎉 战斗胜利!')
            self._handle_victory()
            return True
        if not alive_players:
            bs.is_running = False
            self._battle_running = False
            self.add_log('💀 战斗失败...')
            return True
        return False

    def _handle_victory(self):
        app = App.get_running_app()
        stage_num = self._selected_stage
        gacha_reward = 5 + stage_num // 2
        mat_reward = 2 * (5 + stage_num // 2)
        app.game.gacha_currency += gacha_reward
        app.game.battle_materials += mat_reward
        next_stage = stage_num + 1
        from battle_config import STAGES
        if next_stage in STAGES and next_stage not in app.game.unlocked_stages:
            app.game.unlocked_stages.append(next_stage)
            app.game.max_stage = max(app.game.max_stage, next_stage)
        app.game._check_all_quests()
        app.game.save_game()
        app.refresh_breeding_combos()
        self._reward_box.clear_widgets()
        reward_text = f'奖励: 🧬+{gacha_reward} 🧱+{mat_reward}'
        self._reward_box.add_widget(Label(text=reward_text, color=(1, 1, 0.6, 1)))

    def _update_grid(self):
        for uid, cell in self._grid_widgets.items():
            if uid in self._battle_system._all_units_cache:
                unit = next((u for u in self._battle_system._all_units_cache if u.id == uid), None)
                if unit:
                    children = cell.children
                    if len(children) >= 2:
                        hp_lbl = children[-2] if len(children) > 1 else None
                        if hp_lbl and hasattr(hp_lbl, 'children'):
                            hp_text = [c for c in hp_lbl.children if isinstance(c, Label)]
                            if hp_text:
                                hp_text[0].text = f'{unit.current_health}/{unit.max_health}'
                                hp_text[0].color = (0.3, 1, 0.3, 1) if unit.current_health > unit.max_health * 0.3 else (1, 0.3, 0.3, 1)
                    if not unit.is_alive:
                        cell.opacity = 0.3

    def _toggle_auto(self):
        if self._battle_system:
            self._battle_system.is_auto = not self._battle_system.is_auto
            self._auto_btn.text = '自动: ON' if self._battle_system.is_auto else '自动: OFF'

    def _exit_battle(self):
        self._battle_running = False
        if self._battle_system:
            self._battle_system.is_running = False
        self._battle_area.clear_widgets()
        self._battle_area.add_widget(Label(text='退出战斗', color=(0.5, 0.5, 0.5, 1)))
        self.add_log('已退出战斗')

    def add_log(self, msg):
        self._log.add_widget(Label(text=msg, size_hint_y=None, height=dp(20), font_size=dp(11),
                                    color=(0.8, 0.8, 0.8, 1)))
