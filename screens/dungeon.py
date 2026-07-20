from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp
import random


class DungeonScreen(Screen):
    DUNGEONS = [
        {'id': 'mine', 'name': '废弃矿井', 'unlock': 30, 'boss': '矿主', 'floors': 5,
         'reward_type': '矿石精华', 'enemy_tier': 1},
        {'id': 'forest', 'name': '幽暗森林', 'unlock': 50, 'boss': '森林守护者', 'floors': 6,
         'reward_type': '生命之露', 'enemy_tier': 2},
        {'id': 'frost', 'name': '冰封王座', 'unlock': 80, 'boss': '霜龙', 'floors': 7,
         'reward_type': '冰晶碎片', 'enemy_tier': 3},
        {'id': 'dragon', 'name': '龙之巢穴', 'unlock': 120, 'boss': '远古龙', 'floors': 8,
         'reward_type': '龙鳞', 'enemy_tier': 4},
        {'id': 'void', 'name': '虚空裂隙', 'unlock': 160, 'boss': '虚空之主', 'floors': 10,
         'reward_type': '虚空精华', 'enemy_tier': 5},
    ]
    ROOM_TYPES = ['战斗', '战斗', '战斗', '宝箱', '商店', '事件']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        main.add_widget(Label(text='副本探险', size_hint_y=0.06, bold=True, color=(0.3, 1, 0.3, 1)))
        sv = ScrollView(size_hint_y=1)
        self._content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self._content.bind(minimum_height=self._content.setter('height'))
        sv.add_widget(self._content)
        main.add_widget(sv)
        self.add_widget(main)
        self._map = []

    def on_enter(self):
        self._show_list()

    def _show_list(self):
        self._content.clear_widgets()
        app = App.get_running_app()
        for d in self.DUNGEONS:
            locked = app.game.max_stage < d['unlock']
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80),
                              spacing=dp(2), padding=dp(6))
            from kivy.graphics import Color as GfxColor, Rectangle
            with card.canvas.before:
                GfxColor(0.15, 0.2, 0.3, 1) if not locked else GfxColor(0.2, 0.2, 0.2, 1)
                card._bg = Rectangle(pos=card.pos, size=card.size)
            card.bind(pos=lambda c,v:setattr(c._bg,'pos',v), size=lambda c,v:setattr(c._bg,'size',v))
            h = BoxLayout(orientation='horizontal', size_hint_y=0.4)
            h.add_widget(Label(text=f'{d["name"]} ({d["floors"]}层)', size_hint_x=0.6,
                               bold=True, color=(1,1,1,1) if not locked else (0.5,0.5,0.5,1)))
            if locked:
                h.add_widget(Label(text=f'通关第{d["unlock"]}关解锁', size_hint_x=0.4, color=(0.6,0.3,0.3,1)))
            else:
                btn = Button(text='进入', size_hint_x=0.4, background_color=(0.15,0.5,0.15,1))
                btn.bind(on_press=lambda _, di=d: self._generate_map(di))
                h.add_widget(btn)
            card.add_widget(h)
            card.add_widget(Label(text=f'Boss: {d["boss"]} | 奖励: {d["reward_type"]}',
                                   color=(0.7,0.7,0.7,1), size_hint_y=0.3, halign='left'))
            self._content.add_widget(card)

    def _generate_map(self, dung):
        floors = dung['floors']
        self._map = []
        for f in range(floors):
            rooms = []
            for _ in range(3):
                rtype = random.choice(self.ROOM_TYPES)
                rooms.append({'type': rtype})
            if f == floors - 1:
                rooms[1] = {'type': 'boss', 'boss': dung['boss']}
            self._map.append(rooms)
        self._show_floor(0, dung)

    def _show_floor(self, floor_idx, dung):
        self._content.clear_widgets()
        self._content.add_widget(Label(text=f'{dung["name"]} 第{floor_idx+1}层',
                                        size_hint_y=None, height=dp(26), bold=True, color=(1,1,0,1)))
        rooms = self._map[floor_idx]
        for room in rooms:
            icons = {'战斗': '⚔️', '宝箱': '📦', '商店': '🏪', '事件': '❓', 'boss': '💀'}
            rtype = room['type']
            c = Label(text=f'{icons.get(rtype,"?")} {rtype}', size_hint_y=None, height=dp(40),
                       color=(1,1,1,1))
            if hasattr(c, '__self__'):
                pass
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(44), spacing=dp(5))
            box.add_widget(Label(text=f'{icons.get(rtype,"?")} {rtype}', color=(1,1,1,1)))
            btn = Button(text='进入', size_hint_x=0.3,
                         on_press=lambda _, r=room, f=floor_idx, d=dung: self._enter_room(r, f, d))
            box.add_widget(btn)
            self._content.add_widget(box)

    def _enter_room(self, room, floor_idx, dung):
        app = App.get_running_app()
        rtype = room['type']
        if rtype == '战斗':
            self._start_battle(room, dung)
        elif rtype == '宝箱':
            rewards = random.choice([('gene_essence', 5+dung['enemy_tier']*3),
                                       ('battle_materials', 30+dung['enemy_tier']*20),
                                       ('gacha_currency', 20+dung['enemy_tier']*10)])
            if rewards[0] == 'gene_essence':
                app.game.gene_essence += rewards[1]
            elif rewards[0] == 'battle_materials':
                app.game.battle_materials += rewards[1]
            else:
                app.game.gacha_currency += rewards[1]
            app.game.save_game()
            self._advance_floor(floor_idx, dung)
        elif rtype == '商店':
            self._show_shop(floor_idx, dung)
        elif rtype == '事件':
            events = [
                ('基因突变', '随机卡牌HP+20!', lambda g: setattr(random.choice(g.cards), 'traits',
                     {**random.choice(g.cards).traits, 'health': random.choice(g.cards).traits.get('health', 50)+20})),
                ('流浪商人', f'获得精华+{3+dung["enemy_tier"]*2}!', lambda g: setattr(g, 'gene_essence', g.gene_essence+3+dung['enemy_tier']*2)),
            ]
            evt = random.choice(events)
            evt[2](app.game)
            app.game.save_game()
            popup = Popup(title=evt[0], content=Label(text=evt[1]), size_hint=(0.6,0.3))
            popup.open()
            self._advance_floor(floor_idx, dung)
        elif rtype == 'boss':
            self._start_boss(room, dung)

    def _start_battle(self, room, dung):
        app = App.get_running_app()
        bs = app._screen_refs.get('战斗')
        if bs and bs._team:
            from battle_config import STAGES
            stage = STAGES.get(dung['unlock'], STAGES.get(1))
            ed = [dict(e) for e in stage.get('enemies', [])]
            if not ed:
                ed = [{'name':'副本敌人','health':80+dung['enemy_tier']*40,'attack':8+dung['enemy_tier']*4,
                       'defense':3+dung['enemy_tier']*2,'speed':8+dung['enemy_tier']*2,
                       'skills':[],'passive_abilities':[],'width':1,'height':1,'position':0}]
            from gene_game import BattleSystem
            bs2 = BattleSystem(dict(bs._team), ed, stage_num=dung['unlock'], skill_enhance_level=dung['enemy_tier'])
            bs2.is_running = True
            bs._battle_system = bs2
            bs._battle_running = True
            bs._selected_stage = dung['unlock']
            bs._render_battle_grid()
            bs.add_log(f'[副本] {dung["name"]}')
            from kivy.clock import Clock
            Clock.schedule_interval(bs._battle_tick, 0.3)
            bs._dungeon_info = {'dung': dung, 'floor': getattr(self, '_cur_floor', 0)}
        for tab in app.root.tab_list:
            if tab.text == '战斗':
                app.root.switch_to(tab)
                break

    def _start_boss(self, room, dung):
        app = App.get_running_app()
        bs = app._screen_refs.get('战斗')
        if bs and bs._team:
            ed = [{'name':room['boss'],'health':200+dung['enemy_tier']*120,'attack':15+dung['enemy_tier']*10,
                   'defense':8+dung['enemy_tier']*5,'speed':10+dung['enemy_tier']*4,
                   'skills':['火焰吐息'],'passive_abilities':[],'width':2,'height':2,'position':0}]
            from gene_game import BattleSystem
            bs2 = BattleSystem(dict(bs._team), ed, stage_num=dung['unlock']*2, skill_enhance_level=dung['enemy_tier']+1)
            bs2.is_running = True
            bs._battle_system = bs2
            bs._battle_running = True
            bs._selected_stage = dung['unlock']
            bs._render_battle_grid()
            bs.add_log(f'[副本BOSS] {room["boss"]}!')
            from kivy.clock import Clock
            Clock.schedule_interval(bs._battle_tick, 0.3)

    def _show_shop(self, floor_idx, dung):
        app = App.get_running_app()
        content = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        items = [
            ('精华×5', 'gene_essence', 5, 30),
            ('材料×50', 'battle_mats', 50, 20),
            ('芯片(随机)', 'chip', 1, 80),
        ]
        for name, rtype, amt, cost in items:
            if rtype == 'battle_mats' and app.game.battle_materials >= cost:
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36), spacing=dp(5))
                row.add_widget(Label(text=f'{name} [{cost}材料]', color=(1,1,1,1)))
                btn = Button(text='购买', size_hint_x=0.3,
                             on_press=lambda _, rt=rtype, a=amt, c=cost: self._buy(rt, a, c))
                row.add_widget(btn)
                content.add_widget(row)
        close_btn = Button(text='离开商店', size_hint_y=None, height=dp(36))
        content.add_widget(close_btn)
        popup = Popup(title='商店', content=content, size_hint=(0.7,0.5))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
        self._advance_floor(floor_idx, dung)

    def _buy(self, rtype, amt, cost):
        app = App.get_running_app()
        if app.game.battle_materials < cost:
            return
        app.game.battle_materials -= cost
        if rtype == 'gene_essence':
            app.game.gene_essence += amt
        elif rtype == 'battle_mats':
            app.game.battle_materials += amt
        elif rtype == 'chip':
            from gene_config import CHIP_POOLS
            cid = random.choice(list(CHIP_POOLS.keys()))
            app.game.chip_inventory[cid] = app.game.chip_inventory.get(cid, 0) + 1
        app.game.save_game()

    def _advance_floor(self, floor_idx, dung):
        if floor_idx + 1 < len(self._map):
            self._show_floor(floor_idx + 1, dung)
        else:
            self._content.clear_widgets()
            self._content.add_widget(Label(text=f'{dung["name"]} 探索完毕!', bold=True,
                                            color=(0.4, 1, 0.4, 1), size_hint_y=None, height=dp(40)))
            self._content.add_widget(Button(text='返回列表', size_hint_y=None, height=dp(40),
                                             on_press=lambda _: self._show_list()))
