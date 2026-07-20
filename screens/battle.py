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
        if self._battle_running and self._battle_system:
            self._update_all_cells()

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
        content = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(6))
        content.add_widget(Label(text='点击卡牌选中，再点击格子放置',
                                 size_hint_y=None, height=dp(24), color=(0.8, 0.8, 0.8, 1)))
        self._pending_lbl = Label(text='', size_hint_y=None, height=dp(20), color=(0.4, 1, 0.4, 1))
        content.add_widget(self._pending_lbl)

        two_col = BoxLayout(orientation='horizontal', size_hint_y=1, spacing=dp(8))

        left = BoxLayout(orientation='vertical', size_hint_x=0.45, spacing=dp(2))
        left.add_widget(Label(text='出战阵型', size_hint_y=None, height=dp(20), color=(1, 1, 1, 1)))
        self._grid_btns = {}
        grid = GridLayout(cols=3, spacing=dp(3), size_hint_y=None, height=dp(165))
        for pos in range(9):
            card_at = self._team.get(pos)
            txt = f'{pos+1}:{card_at.name[:3]}' if card_at else f'{pos+1}:空'
            clr = (0.3, 0.8, 1, 1) if card_at else (0.4, 0.4, 0.4, 1)
            btn = Button(text=txt, size_hint=(1, None), height=dp(50),
                         background_color=clr, halign='center', font_size=dp(10))
            btn._pos = pos
            btn.bind(on_press=self._on_grid_cell)
            grid.add_widget(btn)
            self._grid_btns[pos] = btn
        left.add_widget(grid)
        two_col.add_widget(left)

        right = BoxLayout(orientation='vertical', size_hint_x=0.55, spacing=dp(2))
        right.add_widget(Label(text='可用卡牌', size_hint_y=None, height=dp(20), color=(1, 1, 1, 1)))
        sv = ScrollView(size_hint_y=1, do_scroll_x=False, bar_width=dp(6),
                        scroll_type=['bars', 'content'])
        inner = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        inner.bind(minimum_height=inner.setter('height'))
        for card in app.game.cards:
            if not card.is_alive:
                continue
            in_t = card.id in [c.id for c in self._team.values() if c]
            prefix = '[上阵]' if in_t else ''
            atk = card.traits.get('attack', 0)
            hp = card.traits.get('health', 0)
            lbl = Label(text=f'{prefix}{card.name} ATK:{atk} HP:{hp}',
                         size_hint_y=None, height=dp(30), color=(1, 1, 1, 1),
                         halign='left', valign='middle', font_size=dp(11))
            lbl._card = card
            if in_t:
                lbl.color = (0.3, 0.8, 1, 1)
            with lbl.canvas.before:
                from kivy.graphics import Color as GfxColor, Rectangle
                GfxColor(0.2, 0.2, 0.25, 1)
                lbl._bg = Rectangle(pos=lbl.pos, size=lbl.size)
            lbl.bind(pos=lambda c, v: setattr(c._bg, 'pos', v) if hasattr(c, '_bg') else None,
                      size=lambda c, v: setattr(c._bg, 'size', v) if hasattr(c, '_bg') else None)
            lbl.bind(on_touch_down=self._on_card_label_touch)
            inner.add_widget(lbl)
        sv.add_widget(inner)
        right.add_widget(sv)
        two_col.add_widget(right)

        content.add_widget(two_col)

        btn_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        confirm = Button(text='确认编队')
        clear = Button(text='清空全部')
        btn_row.add_widget(confirm)
        btn_row.add_widget(clear)
        content.add_widget(btn_row)

        popup = Popup(title='选择队伍', content=content, size_hint=(0.9, 0.85))
        confirm.bind(on_press=lambda _: popup.dismiss())
        clear.bind(on_press=lambda _: self._do_clear_team())
        popup.open()

    def _on_card_label_touch(self, lbl, touch):
        if lbl.collide_point(*touch.pos):
            self._pending_card = getattr(lbl, '_card', None)
            if self._pending_card:
                self._pending_lbl.text = f'已选中: {self._pending_card.name}'
        return False

    def _on_grid_cell(self, btn):
        pos = getattr(btn, '_pos', -1)
        if pos < 0:
            return
        if self._pending_card:
            if len(self._team) >= 5:
                popup = Popup(title='错误', content=Label(text='最多上阵5张卡牌'),
                              size_hint=(0.5, 0.25))
                popup.open()
                return
            existing_ids = [c.id for c in self._team.values()]
            if self._pending_card.id in existing_ids:
                popup = Popup(title='错误', content=Label(text='该卡牌已上阵'),
                              size_hint=(0.5, 0.25))
                popup.open()
                return
            self._team[pos] = self._pending_card
            self._pending_card = None
            self._pending_lbl.text = ''
            self._refresh_grid_btns()
            self._team_btn.text = f'队伍: {len(self._team)}/5'
        elif pos in self._team:
            del self._team[pos]
            self._refresh_grid_btns()
            self._team_btn.text = f'队伍: {len(self._team)}/5'

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
        if stage_num >= 50:
            traited = [e for e in self._battle_system.enemies if getattr(e, '_traits', [])]
            if traited:
                from gene_config import ENEMY_TRAITS
                tdesc = []
                for e in traited:
                    for tid in e._traits:
                        if tid in ENEMY_TRAITS:
                            tdesc.append(f'{e.name}: [{ENEMY_TRAITS[tid]["name"]}] {ENEMY_TRAITS[tid]["desc"]}')
                hint_text = '敌人特质!\n' + '\n'.join(tdesc[:4])
                popup = Popup(title='敌人特质', content=Label(text=hint_text, size_hint_y=None, height=dp(200)),
                              size_hint=(0.7, 0.5))
                popup.open()
        Clock.schedule_interval(self._battle_tick, 0.3)

    def _render_battle_grid(self):
        self._battle_area.clear_widgets()
        self._unit_cells = {}
        bs = self._battle_system

        player_gs = 3
        enemy_gs = bs.enemy_grid_size

        grid_container = BoxLayout(orientation='horizontal', spacing=dp(12))

        player_side = BoxLayout(orientation='vertical', size_hint_x=0.45, spacing=dp(2))
        player_side.add_widget(Label(text='我方', color=(0.3, 0.8, 1, 1), size_hint_y=None, height=dp(20)))
        pg = GridLayout(cols=player_gs, spacing=dp(2), size_hint_y=0.95)
        pmap = {u.position: u for u in bs.player_team}
        for i in range(player_gs * player_gs):
            unit = pmap.get(i)
            cell = self._make_cell(unit, is_player=True)
            pg.add_widget(cell)
            if unit:
                self._unit_cells[unit.id] = cell
        player_side.add_widget(pg)
        grid_container.add_widget(player_side)

        enemy_side = BoxLayout(orientation='vertical',
                               size_hint_x=0.55 if enemy_gs > 3 else 0.5, spacing=dp(2))
        enemy_side.add_widget(Label(text='敌方', color=(1, 0.3, 0.3, 1), size_hint_y=None, height=dp(20)))
        spacing = dp(2) if enemy_gs <= 3 else dp(1)

        from kivy.uix.floatlayout import FloatLayout
        enemy_wrap = FloatLayout(size_hint_y=0.95)
        eg = GridLayout(cols=enemy_gs, spacing=spacing,
                        size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        emap = {}
        bosses = []
        for u in bs.enemies:
            ops = u.occupied_positions if u.occupied_positions else [u.position]
            for op in ops:
                emap[op] = u
            if u.width > 1 or u.height > 1:
                bosses.append(u)
        for i in range(enemy_gs * enemy_gs):
            unit = emap.get(i)
            is_boss_tile = unit is not None and (unit.width > 1 or unit.height > 1)
            cell = self._make_cell(unit if not is_boss_tile else None, is_player=False)
            eg.add_widget(cell)
            if unit is not None and i == unit.position:
                self._unit_cells[unit.id] = cell
        enemy_wrap.add_widget(eg)

        for boss in bosses:
            self._place_boss_overlay(enemy_wrap, boss, enemy_gs, spacing)

        enemy_side.add_widget(enemy_wrap)
        grid_container.add_widget(enemy_side)

        self._battle_area.add_widget(grid_container)

    def _place_boss_overlay(self, wrap, boss, gs, spacing):
        import os
        c, r, w, h = boss.col, boss.row, boss.width, boss.height
        tkey = getattr(boss, 'template_key', '')
        boss_img_path = os.path.join('assets', 'enemies', f'{tkey}_0.png') if tkey else ''

        from kivy.uix.image import Image as KivyImage
        from kivy.graphics import Color as GfxColor, Rectangle as GfxRect

        boss_cell = BoxLayout(orientation='vertical',
                               pos=(0, 0), size=(100, 100),
                               size_hint=(None, None))
        with boss_cell.canvas.before:
            GfxColor(1, 0.15, 0.15, 0.4)
            boss_cell._bg = GfxRect(pos=boss_cell.pos, size=boss_cell.size)
        boss_cell.bind(pos=lambda c, v: setattr(c._bg, 'pos', v) if hasattr(c, '_bg') else None,
                       size=lambda c, v: setattr(c._bg, 'size', v) if hasattr(c, '_bg') else None)
        if os.path.exists(boss_img_path):
            img = KivyImage(source=boss_img_path, size_hint_y=0.55,
                            allow_stretch=True, keep_ratio=True, fit_mode='contain')
            boss_cell.add_widget(img)
        boss_cell.add_widget(Label(text=boss.name[:8], font_size=dp(8), bold=True,
                                    color=(1, 0.3, 0.3, 1), size_hint_y=0.15))
        boss_cell._hp_lbl = Label(text=f'HP{boss.current_health}/{boss.max_health}',
                                   font_size=dp(7), color=(1, 1, 1, 1), size_hint_y=0.12)
        boss_cell.add_widget(boss_cell._hp_lbl)
        boss_cell.add_widget(Label(text=f'ATK{boss.attack} DEF{boss.defense}',
                                    font_size=dp(7), color=(0.8, 0.8, 0.8, 1), size_hint_y=0.13))
        boss_cell._boss = boss
        wrap.add_widget(boss_cell)
        self._unit_cells[boss.id] = boss_cell

        def _do_place(*a):
            if wrap.width <= 0 or wrap.height <= 0:
                return
            ew = (wrap.width - spacing * (gs - 1)) / gs
            eh = (wrap.height - spacing * (gs - 1)) / gs
            boss_cell.pos = (c * (ew + spacing), wrap.height - (r + h) * (eh + spacing) + spacing)
            boss_cell.size = (w * ew + (w - 1) * spacing, h * eh + (h - 1) * spacing)

        wrap.bind(size=lambda *a: _do_place(*a))
        _do_place()

    def _make_cell(self, unit, is_player):
        from kivy.graphics import Color as GfxColor, Rectangle
        import os
        cell = BoxLayout(orientation='vertical', spacing=dp(0), padding=dp(1))
        cell.size_hint = (1, None)
        gs = self._battle_system.enemy_grid_size if not is_player else 3
        cell_h = dp(58) if gs >= 4 else dp(72)
        cell.height = cell_h
        font_s = dp(6) if gs >= 4 else dp(7)
        name_s = dp(7) if gs >= 4 else dp(8)

        with cell.canvas.before:
            if unit is None:
                GfxColor(0.08, 0.08, 0.12, 1)
            else:
                nc = (0.2, 0.7, 1, 1) if is_player else (1, 0.3, 0.3, 1)
                GfxColor(nc[0] * 0.25, nc[1] * 0.25, nc[2] * 0.25, 1)
            cell._bg_rect = Rectangle(pos=cell.pos, size=cell.size)
        cell.bind(pos=self._update_cell_bg, size=self._update_cell_bg)

        if unit is None:
            cell.add_widget(Label(text='', color=(0.05, 0.05, 0.08, 1)))
            cell._hp_bar = None
            cell._hp_lbl = None
            cell._atb_bar = None
            cell._atb_lbl = None
            return cell

        nc = (0.2, 0.7, 1, 1) if is_player else (1, 0.3, 0.3, 1)

        hp_pct = unit.current_health / max(unit.max_health, 1)
        if hp_pct > 0.5:
            hp_c = (0.2, 0.9, 0.2, 1)
        elif hp_pct > 0.25:
            hp_c = (1, 0.8, 0.2, 1)
        else:
            hp_c = (1, 0.2, 0.2, 1)

        if not is_player:
            tkey = getattr(unit, 'template_key', '')
            if tkey:
                img_path = os.path.join('assets', 'enemies', f'{tkey}_0.png')
                if os.path.exists(img_path):
                    from kivy.uix.image import Image as KivyImage
                    img = KivyImage(source=img_path, size_hint_y=0.45, allow_stretch=True,
                                    keep_ratio=True, fit_mode='contain')
                    cell.add_widget(img)

        row1 = BoxLayout(orientation='horizontal', size_hint_y=0.17, spacing=dp(2))
        row1.add_widget(Label(text=unit.name[:5], color=nc, font_size=name_s, bold=True,
                              size_hint_x=0.55, halign='left', valign='middle'))
        row1.add_widget(Label(text=f'SPD{unit.speed}', color=(0.7, 0.7, 0.7, 1),
                              font_size=font_s, size_hint_x=0.45, halign='right'))
        cell.add_widget(row1)

        row2 = BoxLayout(orientation='horizontal', size_hint_y=0.14, spacing=dp(2))
        cell._hp_lbl = Label(text=f'HP{unit.current_health}/{unit.max_health}',
                             font_size=font_s, color=hp_c, size_hint_x=0.55, halign='left')
        row2.add_widget(cell._hp_lbl)
        row2.add_widget(Label(text=f'ATK{unit.attack}', color=(1, 0.7, 0.3, 1),
                              font_size=font_s, size_hint_x=0.45, halign='right'))
        cell.add_widget(row2)

        bar1 = BoxLayout(size_hint_y=0.06, spacing=dp(0))
        cell._hp_bar = bar1
        with bar1.canvas.before:
            GfxColor(0.2, 0.2, 0.2, 1)
            bar1._bg = Rectangle(pos=bar1.pos, size=bar1.size)
            GfxColor(*hp_c[:3], 1)
            bar1._fill = Rectangle(pos=bar1.pos, size=(bar1.width * hp_pct, bar1.height))
        bar1.bind(pos=self._update_bar, size=self._update_bar)
        cell.add_widget(bar1)

        row3 = BoxLayout(orientation='horizontal', size_hint_y=0.14, spacing=dp(2))
        d = unit.defense if hasattr(unit, 'defense') else 0
        row3.add_widget(Label(text=f'DEF{d}', color=(0.5, 0.7, 1, 1),
                              font_size=font_s, size_hint_x=0.55, halign='left'))
        max_bar = BATTLE_CONFIG['action_bar_max']
        ab = min(unit.action_bar / max_bar, 1.0) if max_bar > 0 else 0
        cell._atb_lbl = Label(text=f'ATB{ab*100:.0f}%', font_size=font_s,
                              color=(0.7, 0.7, 0, 1), size_hint_x=0.45, halign='right')
        row3.add_widget(cell._atb_lbl)
        cell.add_widget(row3)

        bar2 = BoxLayout(size_hint_y=0.06, spacing=dp(0))
        cell._atb_bar = bar2
        with bar2.canvas.before:
            GfxColor(0.2, 0.2, 0.2, 1)
            bar2._bg = Rectangle(pos=bar2.pos, size=bar2.size)
            GfxColor(0.6, 0.6, 0, 1)
            bar2._fill = Rectangle(pos=bar2.pos, size=(bar2.width * ab, bar2.height))
        bar2.bind(pos=self._update_bar, size=self._update_bar)
        cell.add_widget(bar2)

        skills_text = ','.join(unit.skills[:2]) if unit.skills else '-'
        traits = getattr(unit, '_traits', [])
        if traits:
            from gene_config import ENEMY_TRAITS
            tnames = [ENEMY_TRAITS[t]['name'] for t in traits[:2] if t in ENEMY_TRAITS]
            skills_text = '/'.join(tnames) if tnames else skills_text
        statuses = []
        for k in unit.status_effects:
            if k in ('poison', 'burn', 'bleed', 'freeze', 'paralyze', 'sleep'):
                statuses.append(k[:1].upper())
        st_text = ' '.join(statuses) if statuses else ''
        cell.add_widget(Label(text=f'{skills_text}  {st_text}', font_size=dp(5) if gs >= 4 else dp(6),
                              color=(0.5, 0.5, 0.5, 1), size_hint_y=0.16))

        return cell

    def _update_cell_bg(self, instance, value):
        if hasattr(instance, '_bg_rect'):
            instance._bg_rect.pos = instance.pos
            instance._bg_rect.size = instance.size

    def _update_bar(self, instance, value):
        if hasattr(instance, '_bg'):
            instance._bg.pos = instance.pos
            instance._bg.size = instance.size
        if hasattr(instance, '_fill'):
            instance._fill.pos = instance.pos
            pw = max(instance.width, 1)
            instance._fill.size = (instance._fill.size[0], instance.height)

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
            if hp_pct > 0.5:
                hp_c = (0.2, 0.9, 0.2, 1)
            elif hp_pct > 0.25:
                hp_c = (1, 0.8, 0.2, 1)
            else:
                hp_c = (1, 0.2, 0.2, 1)
            if hasattr(cell, '_hp_lbl') and cell._hp_lbl:
                cell._hp_lbl.text = f'HP{unit.current_health}/{unit.max_health}'
                cell._hp_lbl.color = hp_c
            if hasattr(cell, '_atb_lbl') and cell._atb_lbl:
                ab = min(unit.action_bar / max_bar, 1.0) if max_bar > 0 else 0
                cell._atb_lbl.text = f'ATB{ab*100:.0f}%'
            for bar_attr in ('_hp_bar', '_atb_bar'):
                bar = getattr(cell, bar_attr, None)
                if bar is None:
                    continue
                fill = getattr(bar, '_fill', None)
                if fill is None:
                    continue
                bw = max(bar.width, 1)
                if bar_attr == '_hp_bar':
                    fill.size = (bw * hp_pct, bar.height)
                else:
                    ab = min(unit.action_bar / max_bar, 1.0) if max_bar > 0 else 0
                    fill.size = (bw * ab, bar.height)
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
        self._unit_cells = {}

    def _handle_victory(self):
        app = App.get_running_app()
        stage_num = self._selected_stage
        gacha_reward = 5 + stage_num // 2
        mat_reward = 2 * (5 + stage_num // 2)
        essence_reward = 1 + stage_num // 10
        app.game.gacha_currency += gacha_reward
        app.game.battle_materials += mat_reward
        app.game.gene_essence += essence_reward
        next_stage = stage_num + 1
        from battle_config import STAGES
        if next_stage in STAGES and next_stage not in app.game.unlocked_stages:
            app.game.unlocked_stages.append(next_stage)
            app.game.max_stage = max(app.game.max_stage, next_stage)
        alive_players = [u for u in self._battle_system.player_team if u.is_alive]
        if len(alive_players) == len(self._battle_system.player_team):
            app.game.no_loss_stages.add(stage_num)
        for u in self._battle_system.enemies:
            etype = getattr(u, '_etype', u.name)
            app.game.enemy_kills[etype] = app.game.enemy_kills.get(etype, 0) + 1
            width = getattr(u, 'width', 1)
            height = getattr(u, 'height', 1)
            if width > 1 or height > 1:
                app.game.enemy_kills['__boss__'] = app.game.enemy_kills.get('__boss__', 0) + 1
        app.game._check_all_quests()
        app.game.save_game()
        app.refresh_breeding_combos()
        self._reward_box.clear_widgets()
        reward_text = f'奖励: +{gacha_reward} +{mat_reward} +{essence_reward}精华'
        self._reward_box.add_widget(Label(text=reward_text, color=(1, 1, 0.6, 1)))
        ci = getattr(self, '_challenge_info', None)
        if ci:
            import time
            elapsed = int(time.time() - ci['start_time'])
            mins, secs = divmod(elapsed, 60)
            score_entry = {
                'points': ci['points'],
                'time_str': f'{mins:02d}:{secs:02d}',
                'elapsed': elapsed,
            }
            tid = ci['theme_id']
            old = app.game.challenge_scores.get(tid)
            if not old or ci['points'] > old.get('points', 0):
                app.game.challenge_scores[tid] = score_entry
            app.game.save_game()
            self.add_log(f'[挑战] 完成! 得分:{ci["points"]} 用时:{mins:02d}:{secs:02d}')

    def add_log(self, msg):
        self._log.add_widget(Label(text=str(msg), size_hint_y=None, height=dp(20),
                                    font_size=dp(11), color=(0.8, 0.8, 0.8, 1)))
        sv = self._log.parent
        if sv and hasattr(sv, 'scroll_y'):
            sv.scroll_y = 0
