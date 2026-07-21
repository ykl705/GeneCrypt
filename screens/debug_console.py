from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
import random


class DebugConsole(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        main.add_widget(Label(text='调试控制台', size_hint_y=0.05, bold=True, color=(1,0.3,0.3,1)))
        sv = ScrollView(size_hint_y=1)
        inner = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(4), padding=dp(5))
        inner.bind(minimum_height=inner.setter('height'))

        inner.add_widget(Label(text='关卡', size_hint_y=None, height=dp(22), color=(1,0.85,0,1)))
        row1 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36), spacing=dp(5))
        self._stage_input = TextInput(text='50', multiline=False, size_hint_x=0.4)
        row1.add_widget(self._stage_input)
        row1.add_widget(Button(text='通关此关', on_press=lambda _: self._skip_stage()))
        row1.add_widget(Button(text='解锁全部', on_press=lambda _: self._unlock_all()))
        inner.add_widget(row1)

        inner.add_widget(Label(text='资源', size_hint_y=None, height=dp(22), color=(1,0.85,0,1)))
        row2 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36), spacing=dp(5))
        row2.add_widget(Button(text='+500币', on_press=lambda _: self._add('gacha', 500)))
        row2.add_widget(Button(text='+500材料', on_press=lambda _: self._add('mats', 500)))
        row2.add_widget(Button(text='+100精华', on_press=lambda _: self._add('essence', 100)))
        inner.add_widget(row2)

        inner.add_widget(Label(text='卡牌', size_hint_y=None, height=dp(22), color=(1,0.85,0,1)))
        row3 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36), spacing=dp(5))
        self._card_name = TextInput(text='调试卷袭者', multiline=False, size_hint_x=0.35)
        row3.add_widget(self._card_name)
        self._card_atk = TextInput(text='500', multiline=False, size_hint_x=0.15)
        row3.add_widget(self._card_atk)
        self._card_hp = TextInput(text='2000', multiline=False, size_hint_x=0.15)
        row3.add_widget(self._card_hp)
        row3.add_widget(Button(text='创建', on_press=lambda _: self._create_card()))
        inner.add_widget(row3)

        inner.add_widget(Label(text='科技/成就', size_hint_y=None, height=dp(22), color=(1,0.85,0,1)))
        row4 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36), spacing=dp(5))
        row4.add_widget(Button(text='解锁全科技', on_press=lambda _: self._unlock_tech()))
        row4.add_widget(Button(text='解锁全成就', on_press=lambda _: self._unlock_achievements()))
        inner.add_widget(row4)

        row5 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36), spacing=dp(5))
        row5.add_widget(Button(text='全芯片x5', on_press=lambda _: self._fill_chips()))
        row5.add_widget(Button(text='全模组x3', on_press=lambda _: self._fill_modules()))
        inner.add_widget(row5)

        inner.add_widget(Label(text='生成装备', size_hint_y=None, height=dp(22), color=(1,0.85,0,1)))
        row6 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36), spacing=dp(4))
        self._eq_slot = TextInput(text='weapon', multiline=False, size_hint_x=0.25, hint_text='部位')
        row6.add_widget(self._eq_slot)
        self._eq_rarity = TextInput(text='legend', multiline=False, size_hint_x=0.25, hint_text='稀有度')
        row6.add_widget(self._eq_rarity)
        self._eq_count = TextInput(text='1', multiline=False, size_hint_x=0.15, hint_text='数量')
        row6.add_widget(self._eq_count)
        row6.add_widget(Button(text='生成', size_hint_x=0.2, on_press=lambda _: self._gen_equip()))
        inner.add_widget(row6)
        inner.add_widget(Label(text='部位:weapon/head/body/accessory/boots/special', font_size=dp(9),
                               size_hint_y=None, height=dp(16), color=(0.5,0.5,0.5,1)))
        inner.add_widget(Label(text='稀有度:common/uncommon/rare/epic/legend/ancient/mythic/chaos', font_size=dp(9),
                               size_hint_y=None, height=dp(16), color=(0.5,0.5,0.5,1)))

        sv.add_widget(inner)
        main.add_widget(sv)
        self.add_widget(main)

    def _get_game(self):
        return App.get_running_app().game

    def _skip_stage(self):
        try:
            n = int(self._stage_input.text) if self._stage_input.text else 50
        except:
            n = 50
        game = self._get_game()
        if n > game.max_stage:
            game.max_stage = n
            game.unlocked_stages = list(range(1, n+1))
        game.gacha_currency += 50 + n
        game.battle_materials += 100 + n*2
        game.gene_essence += 2 + n//10
        game.save_game()
        self._pop(f'已跳到第{n}关')

    def _unlock_all(self):
        game = self._get_game()
        game.max_stage = 200
        game.unlocked_stages = list(range(1, 201))
        game.save_game()
        self._pop('全部关卡已解锁')

    def _add(self, key, amt):
        game = self._get_game()
        if key == 'gacha':
            game.gacha_currency += amt
        elif key == 'mats':
            game.battle_materials += amt
        elif key == 'essence':
            game.gene_essence += amt
        game.save_game()
        self._pop(f'+{amt}')

    def _create_card(self):
        name = self._card_name.text or '调试卷袭者'
        try:
            atk = int(self._card_atk.text or 500)
            hp = int(self._card_hp.text or 2000)
        except:
            atk, hp = 500, 2000
        from gene_game import Card
        card = Card(name, random.choice(['male', 'female']))
        card.traits['attack'] = atk
        card.traits['health'] = hp
        card.traits['defense'] = atk // 3
        card.traits['speed'] = atk // 5 + 20
        card.traits['stamina'] = 100
        card.traits['critical_rate'] = 15
        card.traits['dodge_rate'] = 10
        card.bloodline = random.choice(['dragon', 'phoenix', 'shadow', 'frost', 'storm', 'vital'])
        card.star = 5
        card.skills = card.skills[:5]
        game = self._get_game()
        game.cards.append(card)
        game.save_game()
        self._pop(f'创建: {name} ATK:{atk} HP:{hp}')

    def _unlock_tech(self):
        game = self._get_game()
        for tn, t in game.tech_tree.items():
            t['level'] = t.get('max_level', 5)
            t['unlocked'] = True
        game._sync_tech_effects()
        game.save_game()
        self._pop('全科技已解锁')

    def _unlock_achievements(self):
        game = self._get_game()
        from gene_config import ACHIEVEMENTS
        for a in ACHIEVEMENTS:
            game.achievements[a['id']] = True
        game.save_game()
        self._pop('全成就已解锁')

    def _fill_chips(self):
        game = self._get_game()
        from gene_config import CHIP_POOLS
        for cid in CHIP_POOLS:
            game.chip_inventory[cid] = game.chip_inventory.get(cid, 0) + 5
        game.save_game()
        self._pop('芯片+5')

    def _fill_modules(self):
        game = self._get_game()
        from gene_config import MODULE_POOLS
        for mid in MODULE_POOLS:
            game.module_inventory[mid] = game.module_inventory.get(mid, 0) + 3
        game.save_game()
        self._pop('模组+3')

    def _gen_equip(self):
        slot = self._eq_slot.text.strip() or 'weapon'
        rarity = self._eq_rarity.text.strip() or 'common'
        try: count = int(self._eq_count.text or 1)
        except: count = 1
        game = self._get_game()
        from gene_config import EQUIPMENT_SLOTS, EQUIPMENT_RARITY, EQUIPMENT_AFFIX_POOLS, EQUIPMENT_SLOT_NAMES, EQUIPMENT_NAMES
        chosen = next((r for r in EQUIPMENT_RARITY if r['id'] == rarity), EQUIPMENT_RARITY[0])
        pool = EQUIPMENT_AFFIX_POOLS.get(rarity, EQUIPMENT_AFFIX_POOLS['common'])
        min_a, max_a = chosen['affixes']
        for _ in range(count):
            n_a = __import__('random').randint(min_a, min(max_a, len(pool)))
            picked = __import__('random').sample(pool, min(n_a, len(pool)))
            affixes = [{'code': c, 'stat': s, 'value': __import__('random').randint(lo, hi), 'is_pct': bool(ip)}
                       for c, s, ip, lo, hi in picked]
            iid = f'{slot}_{rarity}_{__import__("random").randint(1000,9999)}'
            name_pool = EQUIPMENT_NAMES.get(slot, {}).get(rarity, [f'{chosen["prefix"]}{EQUIPMENT_SLOT_NAMES.get(slot,slot)}'])
            real_name = __import__('random').choice(name_pool)
            item = {'id': iid, 'slot': slot, 'rarity': rarity, 'name': real_name, 'affixes': affixes}
            if iid not in game.equipment_inventory:
                game.equipment_inventory[iid] = {'data': item, 'count': 0}
            game.equipment_inventory[iid]['count'] += 1
        game.save_game()
        self._pop(f'生成{count}件 {real_name}')

    def _pop(self, msg):
        popup = Popup(title='控制台', content=Label(text=msg), size_hint=(0.5, 0.25))
        popup.open()
