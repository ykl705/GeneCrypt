from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
import random, time


SKILL_CODES = {
    '火焰吐息':'FR','冰霜护盾':'IS','雷击':'LT','毒液攻击':'PS','自我修复':'HL','能量护盾':'ES',
    '幻觉制造':'IL','瞬移':'TP','睡眠诱导':'SL','麻痹神经':'PZ','能量吸收':'AB','召唤':'SU',
    '隐身':'IN','自爆':'EX','快速生长':'GR','观星':'OB','澎湃':'SR','甘霖':'RN',
    '冻结':'FZ','诅咒':'CR','灼烧':'BR','处决':'EXE','毒雾扩散':'AP','时光倒流':'RW',
    '亡灵复苏':'RV','剧毒新星':'TN','腐蚀之触':'CT','炼狱之火':'IF','余烬复燃':'ER',
    '永冻领域':'PF','绝对零度':'AZ','血之渴望':'BT','猩红风暴':'CS','万象终结':'OE','状态共鸣':'SR2',
}
REV_SKILL_CODES = {v:k for k,v in SKILL_CODES.items()}

from gene_config import PVP_TIERS, PVP_TIER_SKILLS
TIER_SKILLS = PVP_TIER_SKILLS


def encode_team(team):
    parts = []
    for pos, card in sorted(team.items()):
        bl = getattr(card, 'bloodline', '') or 'XX'
        st = getattr(card, 'star', 1)
        sk = ','.join(SKILL_CODES.get(s, s[:3]) for s in card.skills[:4])
        parts.append(f'{pos}|{bl[:2]:>2}|{st}|{sk}')
    return ';'.join(parts)


def decode_team(code):
    team = {}
    for p in code.split(';'):
        segs = p.split('|')
        if len(segs) != 4:
            raise ValueError(f'Invalid segment: {p}')
        try:
            pos = int(segs[0])
            bl = segs[1].strip()
            star = int(segs[2])
            skills = [REV_SKILL_CODES.get(s, s) for s in segs[3].split(',') if s]
        except:
            raise ValueError(f'Parse error: {p}')
        if pos < 0 or pos > 8:
            raise ValueError(f'Bad position: {pos}')
        if star < 1 or star > 5:
            raise ValueError(f'Bad star: {star}')
        team[pos] = {'bloodline': bl if bl != 'XX' else '', 'star': star, 'skills': skills}
    return team


class PvPScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(10))
        main.add_widget(Label(text='PvP竞技场', size_hint_y=0.05, bold=True, color=(1, 0.6, 0, 1)))
        self._rating_lbl = Label(text='', size_hint_y=None, height=dp(24), color=(1, 1, 0.6, 1))
        main.add_widget(self._rating_lbl)
        sv = ScrollView(size_hint_y=1)
        self._tier_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(6))
        self._tier_box.bind(minimum_height=self._tier_box.setter('height'))
        sv.add_widget(self._tier_box)
        main.add_widget(sv)
        self._code_btn = Button(text='代码对决 (A vs B 模拟)', size_hint_y=None, height=dp(40),
                                on_press=lambda _: self._show_code_duel())
        main.add_widget(self._code_btn)
        self.add_widget(main)

    def on_enter(self):
        self._refresh()

    def _refresh(self):
        app = App.get_running_app()
        game = app.game
        self._rating_lbl.text = f'段位分: {game.pvp_rating}  |  胜利场次: {sum(game.pvp_record.values())}'
        self._tier_box.clear_widgets()
        for tier in PVP_TIERS:
            locked = game.pvp_rating < tier['unlock_rating']
            wins = game.pvp_record.get(tier['id'], 0)
            txt = f'{tier["icon"]} {tier["name"]}段  (胜{wins})'
            if locked:
                txt += f'  [需{tier["unlock_rating"]}分解锁]'
            btn = Button(text=txt, size_hint_y=None, height=dp(46),
                         background_color=(0.6, 0.35, 0.1, 1) if not locked else (0.3, 0.3, 0.3, 1))
            if locked:
                btn.disabled = True
            else:
                btn.bind(on_press=lambda _, t=tier: self._start_ladder(t))
            self._tier_box.add_widget(btn)

    def _start_ladder(self, tier):
        app = App.get_running_app()
        bs = app._screen_refs.get('战斗')
        if bs is None:
            return
        if not bs._team:
            Popup(title='错误', content=Label(text='请先在战斗页编好队伍'), size_hint=(0.5, 0.25)).open()
            return
        from gene_game import Card, BattleSystem
        bots = []
        n_bots = 4 + PVP_TIERS.index(tier)
        skills_pool = TIER_SKILLS[PVP_TIERS.index(tier)]
        for i in range(min(n_bots, 5)):
            b = Card(f'PvP-{tier["name"]}-{i}', 'male' if i % 2 else 'female')
            b.genome_quality = tier['q']
            b.traits = b.calculate_traits()
            b.star = tier['stars']
            b.traits = b.calculate_traits()
            for k in ('attack', 'health', 'defense', 'speed'):
                b.traits[k] = int(b.traits[k] * 1.5)
            b.skills = random.sample(skills_pool, min(2, len(skills_pool)))
            bots.append({
                'name': b.name, 'health': b.traits['health'], 'attack': b.traits['attack'],
                'defense': b.traits['defense'], 'speed': b.traits['speed'],
                'skills': b.skills, 'passive_abilities': [], 'width': 1, 'height': 1, 'position': i,
            })
        bs2 = BattleSystem(dict(bs._team), bots, stage_num=30, skill_enhance_level=0)
        bs2.is_running = True
        bs._battle_system = bs2
        bs._battle_running = True
        bs._selected_stage = 30
        bs._battle_mode = 'pvp_ladder'
        bs._pvp_tier = tier
        bs._challenge_info = None
        bs._render_battle_grid()
        bs.add_log(f'[PvP] {tier["icon"]}{tier["name"]}段位战开始! 对手实力 q={tier["q"]} ★{tier["stars"]}')
        Clock.schedule_interval(bs._battle_tick, 0.3)
        app.switch_tab('战斗')

    def _show_code_duel(self):
        content = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(10))
        content.add_widget(Label(text='我的队伍代码', size_hint_y=None, height=dp(20), color=(0.8, 0.8, 0.8, 1)))
        r1 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(38), spacing=dp(5))
        my_code = TextInput(text='', multiline=False, size_hint_x=0.7, hint_text='生成导出代码...')
        r1.add_widget(my_code)
        r1.add_widget(Button(text='生成', size_hint_x=0.3, on_press=lambda _: self._export_team(my_code)))
        content.add_widget(r1)
        content.add_widget(Label(text='对手A代码', size_hint_y=None, height=dp(20), color=(1, 0.5, 0.5, 1)))
        code_a = TextInput(text='', multiline=False, size_hint_y=None, height=dp(38))
        content.add_widget(code_a)
        content.add_widget(Label(text='对手B代码', size_hint_y=None, height=dp(20), color=(0.5, 0.5, 1, 1)))
        code_b = TextInput(text='', multiline=False, size_hint_y=None, height=dp(38))
        content.add_widget(code_b)
        duel_btn = Button(text='A vs B 对决!', size_hint_y=None, height=dp(44),
                          on_press=lambda _: self._start_pvp(code_a.text.strip(), code_b.text.strip()))
        content.add_widget(duel_btn)
        popup = Popup(title='代码对决', content=content, size_hint=(0.9, 0.75))
        popup.open()

    def _export_team(self, my_code_input):
        app = App.get_running_app()
        bs = app._screen_refs.get('战斗')
        if not bs or not bs._team:
            Popup(title='错误', content=Label(text='请先在战斗页编好队伍'), size_hint=(0.5, 0.25)).open()
            return
        code = encode_team(bs._team)
        my_code_input.text = code
        try:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(code)
        except:
            pass

    def _start_pvp(self, ca, cb):
        if not ca or not cb:
            return
        try:
            team_a = decode_team(ca)
            team_b = decode_team(cb)
        except ValueError as e:
            Popup(title='错误', content=Label(text=f'代码错误: {e}'), size_hint=(0.5, 0.25)).open()
            return
        app = App.get_running_app()
        bs = app._screen_refs.get('战斗')
        if bs is None:
            return
        from gene_game import Card, BattleSystem

        def _build_cards(tm):
            cards = {}
            for pos, t in tm.items():
                c = Card(f'PvP-{pos}', random.choice(['male', 'female']))
                c.star = t.get('star', 1)
                c.traits['attack'] = 45 + c.star * 30
                c.traits['health'] = 180 + c.star * 100
                c.traits['defense'] = 18 + c.star * 10
                c.traits['speed'] = 10 + c.star * 6
                c.traits['critical_rate'] = 5
                c.traits['dodge_rate'] = 5
                c.skills = t.get('skills', [])
                cards[pos] = c
            return cards
        my_cards = _build_cards(team_a)
        opp_cards = _build_cards(team_b)
        enemy_data = []
        for pos, c in opp_cards.items():
            enemy_data.append({
                'name': f'对手{pos}', 'health': c.traits['health'],
                'attack': c.traits['attack'], 'defense': c.traits['defense'],
                'speed': c.traits['speed'], 'skills': c.skills,
                'passive_abilities': [], 'width': 1, 'height': 1, 'position': pos,
            })
        bsystem = BattleSystem(my_cards, enemy_data, stage_num=1, skill_enhance_level=0)
        bsystem.is_running = True
        bs._battle_system = bsystem
        bs._battle_running = True
        bs._selected_stage = 1
        bs._battle_mode = 'pvp'
        bs._challenge_info = None
        bs._render_battle_grid()
        bs.add_log('[PvP] 代码对决开始!')
        Clock.schedule_interval(bs._battle_tick, 0.3)
        app.switch_tab('战斗')
