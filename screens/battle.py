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
from battle_config import BATTLE_CONFIG


class BattleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._battle_system = None
        self._battle_running = False
        self._unit_cells = {}
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
        content = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(10))
        content.add_widget(Label(text='点击下方卡牌选中，再点击上方格子放置',
                                 size_hint_y=None, height=dp(28), color=(0.8, 0.8, 0.8, 1)))
        self._pending_lbl = Label(text='', size_hint_y=None, height=dp(22), color=(0.4, 1, 0.4, 1))
        content.add_widget(self._pending_lbl)
        content.add_widget(Label(text='出战阵型 - 点击格子放置/移除',
                                 size_hint_y=None, height=dp(22), color=(1, 1, 1, 1)))

        self._grid_btns = {}
        grid = GridLayout(cols=3, spacing=dp(4), size_hint_y=None, height=dp(210))
        for pos in range(9):
            card_at = self._team.get(pos)
            txt = f'[{pos+1}] {card_at.name[:4]}' if card_at else f'[空{pos+1}]'
            clr = (0.3, 0.8, 1, 1) if card_at else (0.4, 0.4, 0.4, 1)
            btn = Button(text=txt, size_hint=(1, None), height=dp(60),
                         background_color=clr, halign='center')
            btn._pos = pos
            btn.bind(on_press=self._on_grid_cell)
            grid.add_widget(btn)
            self._grid_btns[pos] = btn
        content.add_widget(grid)

        content.add_widget(Label(text='可用卡牌', size_hint_y=None, height=dp(22), color=(1, 1, 1, 1)))
        sv = ScrollView(size_hint_y=0.4)
        inner = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        inner.bind(minimum_height=inner.setter('height'))
        for card in app.game.cards:
            if not card.is_alive:
                continue
            in_t = card.id in [c.id for c in self._team.values() if c]
            prefix = '[已上阵] ' if in_t else ''
            atk = card.traits.get('attack', 0)
            hp = card.traits.get('health', 0)
            btn = Button(text=f'{prefix}{card.name} ATK:{atk} HP:{hp}',
                         size_hint_y=None, height=dp(36))
            btn._card = card
            btn.bind(on_press=self._on_card_pick)
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
        clear.bind(on_press=lambda _: self._do_clear_team())
        popup.open()

    def _on_card_pick(self, btn):
        card = getattr(btn, '_card', None)
        if card:
            self._pending_card = card
            self._pending_lbl.text = f'已选中: {card.name}'

    def _on_grid_cell(self, btn):
        pos = getattr(btn, '_pos', -1)
        if pos < 0:
            return
        if self._pending_card:
            self._team[pos] = self._pending_card
            self._pending_card = None
            self._pending_lbl.text = ''
            self._refresh_grid_btns()
            self._team_btn.text = f'队伍: {len(self._team)}/3'
        elif pos in self._team:
            del self._team[pos]
            self._refresh_grid_btns()
            self._team_btn.text = f'队伍: {len(self._team)}/3'

    def _refresh_grid_btns(self):
        for pos, btn in self._grid_btns.items():
            card_at = self._team.get(pos)
            btn.text = f'[{pos+1}] {card_at.name[:4]}' if card_at else f'[空{pos+1}]'
            btn.background_color = (0.3, 0.8, 1, 1) if card_at else (0.4, 0.4, 0.4, 1)

    def _do_clear_team(self):
        self._team = {}
        self._pending_card = None
        if hasattr(self, '_pending_lbl') and self._pending_lbl:
            self._pending_lbl.text = ''
        self._refresh_grid_btns()
        self._team_btn.text = '选择队伍'

    def _start_battle(self):
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
        grid = dict(self._team)
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
                                    enemy_data.append({
                                        'name': tmpl['name'],
                                        'health': tmpl.get('base_health', 100),
                                        'attack': tmpl.get('base_attack', 10),
                                        'defense': tmpl.get('base_defense', 5),
                                        'speed': tmpl.get('base_speed', 10),
                                        'skills': [],
                                        'passive_abilities': tmpl.get('passive_abilities', []),
                                        'width': 1, 'height': 1,
                                    })
        if not enemy_data:
            enemy_data = [{'name': '测试敌人', 'health': 50, 'attack': 10, 'defense': 5, 'speed': 8,
                           'skills': [], 'passive_abilities': [], 'width': 1, 'height': 1, 'position': 0}]
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
        self._unit_cells = {}
        bs = self._battle_system

        grid_container = BoxLayout(orientation='horizontal', spacing=dp(15))
        gs = 3

        player_side = BoxLayout(orientation='vertical', size_hint_x=0.5, spacing=dp(2))
        player_side.add_widget(Label(text='我方', color=(0.3, 0.8, 1, 1), size_hint_y=None, height=dp(22)))
        pg = GridLayout(cols=gs, spacing=dp(2), size_hint_y=0.95)
        pmap = {u.position: u for u in bs.player_team}
        for i in range(gs * gs):
            unit = pmap.get(i)
            cell = self._make_cell(unit, is_player=True)
            pg.add_widget(cell)
            if unit:
                self._unit_cells[unit.id] = cell
        player_side.add_widget(pg)
        grid_container.add_widget(player_side)

        enemy_side = BoxLayout(orientation='vertical', size_hint_x=0.5, spacing=dp(2))
        enemy_side.add_widget(Label(text='敌方', color=(1, 0.3, 0.3, 1), size_hint_y=None, height=dp(22)))
        eg = GridLayout(cols=gs, spacing=dp(2), size_hint_y=0.95)
        emap = {}
        for u in bs.enemies:
            ops = u.occupied_positions if u.occupied_positions else [u.position]
            for op in ops:
                emap[op] = u
        for i in range(gs * gs):
            unit = emap.get(i)
            cell = self._make_cell(unit, is_player=False)
            eg.add_widget(cell)
            if unit and i == unit.position:
                self._unit_cells[unit.id] = cell
        enemy_side.add_widget(eg)
        grid_container.add_widget(enemy_side)

        self._battle_area.add_widget(grid_container)

    def _make_cell(self, unit, is_player):
        cell = BoxLayout(orientation='vertical', spacing=dp(1), padding=dp(2))
        cell.size_hint = (1, None)
        cell.height = dp(76)

        if unit is None:
            cell.add_widget(Label(text='', color=(0.15, 0.15, 0.2, 1)))
            return cell

        name_color = (0.3, 0.8, 1, 1) if is_player else (1, 0.4, 0.4, 1)
        name_lbl = Label(text=unit.name[:6], size_hint_y=0.26, color=name_color,
                         font_size=dp(9), bold=True)
        cell.add_widget(name_lbl)

        hp_pct = unit.current_health / max(unit.max_health, 1)
        hp_color = (0.3, 1, 0.3, 1) if hp_pct > 0.3 else (1, 0.3, 0.3, 1)
        cell._hp_lbl = Label(text=f'HP:{unit.current_health}/{unit.max_health}',
                             size_hint_y=0.24, font_size=dp(8), color=hp_color)
        cell.add_widget(cell._hp_lbl)

        cell._atk_lbl = Label(text=f'ATK:{unit.attack} SPD:{unit.speed}',
                              size_hint_y=0.24, font_size=dp(8), color=(0.8, 0.8, 0.8, 1))
        cell.add_widget(cell._atk_lbl)

        max_bar = BATTLE_CONFIG['action_bar_max']
        ab = min(unit.action_bar / max_bar, 1.0) if max_bar > 0 else 0
        cell._atb_lbl = Label(text=f'ATB:{ab*100:.0f}%', size_hint_y=0.26, font_size=dp(8),
                              color=(0.9, 0.9, 0, 1))
        cell.add_widget(cell._atb_lbl)

        return cell

    def _battle_tick(self, dt):
        if not self._battle_running:
            return False
        try:
            bs = self._battle_system
            if bs is None or not bs.is_running:
                self._battle_running = False
                return False
            bs.update_action_bars_frame()
            bs.update_status_damage()
            bs.process_enemy_passives()
            bs.cleanup_summons()
            if bs.check_winner():
                self._battle_running = False
                self._update_all_cells()
                if bs.winner == 'player':
                    self.add_log('战斗胜利!')
                    self._handle_victory()
                else:
                    self.add_log('战斗失败...')
                return False

            unit = bs.get_next_unit()
            if unit:
                max_bar_val = BATTLE_CONFIG['action_bar_max']
                unit.action_bar -= max_bar_val

                if unit.is_player and not bs.is_auto:
                    if bs.marked_target:
                        target = bs.marked_target
                        bs.marked_target = None
                    else:
                        front = [e for e in bs.enemies if e.is_alive]
                        target = front[0] if front else None
                    if target:
                        result = bs.execute_turn(unit, [target])
                        self._flash_attack(unit, target)
                        if result:
                            dmg = result.get('damage', 0)
                            self.add_log(f'{unit.name} -> {target.name} {dmg}伤害')
                            if not target.is_alive:
                                self.add_log(f'{target.name} 被击败!')
                else:
                    result = bs.execute_turn(unit, None)
                    if result:
                        dmg = result.get('damage', 0)
                        tname = result.get('target', '?')
                        self.add_log(f'{unit.name} -> {tname} {dmg}伤害')

            self._update_all_cells()
        except Exception as e:
            self.add_log(f'[ERR] {e}')
        return True

    def _flash_attack(self, attacker, target):
        atk_cell = self._unit_cells.get(attacker.id)
        tgt_cell = self._unit_cells.get(target.id)
        if atk_cell:
            atk_cell.opacity = 0.4
            Clock.schedule_once(lambda dt: setattr(atk_cell, 'opacity', 1.0), 0.12)
        if tgt_cell:
            tgt_cell.opacity = 0.4
            Clock.schedule_once(lambda dt: setattr(tgt_cell, 'opacity', 1.0), 0.16)

    def _update_all_cells(self):
        bs = self._battle_system
        if bs is None:
            return
        max_bar = BATTLE_CONFIG['action_bar_max']
        for uid, cell in list(self._unit_cells.items()):
            unit = None
            for u in bs._all_units_cache:
                if u.id == uid:
                    unit = u
                    break
            if unit is None:
                continue
            hp_pct = unit.current_health / max(unit.max_health, 1)
            if hasattr(cell, '_hp_lbl'):
                cell._hp_lbl.text = f'HP:{unit.current_health}/{unit.max_health}'
                cell._hp_lbl.color = (0.3, 1, 0.3, 1) if hp_pct > 0.3 else (1, 0.3, 0.3, 1)
            if hasattr(cell, '_atk_lbl'):
                cell._atk_lbl.text = f'ATK:{unit.attack} SPD:{unit.speed}'
            if hasattr(cell, '_atb_lbl'):
                ab = min(unit.action_bar / max_bar, 1.0) if max_bar > 0 else 0
                cell._atb_lbl.text = f'ATB:{ab*100:.0f}%'
            if not unit.is_alive:
                cell.opacity = 0.25

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
        self._unit_cells = {}

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
        reward_text = f'奖励: +{gacha_reward} +{mat_reward}'
        self._reward_box.add_widget(Label(text=reward_text, color=(1, 1, 0.6, 1)))

    def add_log(self, msg):
        self._log.add_widget(Label(text=str(msg), size_hint_y=None, height=dp(20),
                                    font_size=dp(11), color=(0.8, 0.8, 0.8, 1)))
