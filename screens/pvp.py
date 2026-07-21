from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
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
        if pos < 0 or pos > 8: raise ValueError(f'Bad position: {pos}')
        if star < 1 or star > 5: raise ValueError(f'Bad star: {star}')
        team[pos] = {'bloodline': bl if bl != 'XX' else '', 'star': star, 'skills': skills}
    return team


class PvPScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(10))
        main.add_widget(Label(text='PvP对决', size_hint_y=0.05, bold=True, color=(1,0.6,0,1)))

        main.add_widget(Label(text='我的队伍代码', size_hint_y=None, height=dp(20), color=(0.8,0.8,0.8,1)))
        r1 = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(38), spacing=dp(5))
        self._my_code = TextInput(text='', multiline=False, size_hint_x=0.7, hint_text='点击生成导出代码...')
        r1.add_widget(self._my_code)
        r1.add_widget(Button(text='生成', size_hint_x=0.3, on_press=lambda _: self._export_team()))
        main.add_widget(r1)

        main.add_widget(Label(text='对手A代码', size_hint_y=None, height=dp(20), color=(1,0.5,0.5,1)))
        self._code_a = TextInput(text='', multiline=False, size_hint_y=None, height=dp(38))
        main.add_widget(self._code_a)

        main.add_widget(Label(text='对手B代码', size_hint_y=None, height=dp(20), color=(0.5,0.5,1,1)))
        self._code_b = TextInput(text='', multiline=False, size_hint_y=None, height=dp(38))
        main.add_widget(self._code_b)

        btn_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(44), spacing=dp(10))
        btn_row.add_widget(Button(text='A vs B 对决!', on_press=lambda _: self._start_pvp()))
        main.add_widget(btn_row)
        self._result_lbl = Label(text='', size_hint_y=1, color=(1,1,0.6,1))
        main.add_widget(self._result_lbl)
        self.add_widget(main)

    def _export_team(self):
        app = App.get_running_app()
        bs = app._screen_refs.get('战斗')
        if not bs or not bs._team:
            Popup(title='错误', content=Label(text='请先在战斗页编好队伍'), size_hint=(0.5,0.25)).open()
            return
        code = encode_team(bs._team)
        self._my_code.text = code
        try:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(code)
        except:
            pass

    def _start_pvp(self):
        ca = self._code_a.text.strip()
        cb = self._code_b.text.strip()
        if not ca or not cb:
            self._result_lbl.text = '请填写双方代码'
            return
        try:
            team_a = decode_team(ca)
            team_b = decode_team(cb)
        except ValueError as e:
            self._result_lbl.text = f'代码错误: {e}'
            return
        result = self._sim_battle(team_a, team_b)
        self._result_lbl.text = result

    def _sim_battle(self, team_a, team_b):
        from gene_game import Card, BattleSystem
        def _make_team(tm):
            cards = []
            for pos, t in sorted(tm.items()):
                c = Card(f'单位{pos}', random.choice(['male','female']))
                c.star = t.get('star', 1)
                c.traits['attack'] = 40 + c.star * 25
                c.traits['health'] = 150 + c.star * 80
                c.traits['defense'] = 15 + c.star * 8
                c.traits['speed'] = 8 + c.star * 5
                c.traits['critical_rate'] = 5
                c.traits['dodge_rate'] = 5
                c.traits['stamina'] = 50
                c.skills = t.get('skills', [])
                cards.append(c)
            return cards

        a_cards = _make_team(team_a)
        b_cards = _make_team(team_b)
        b_stats = {'total_hp': sum(c.traits['health'] for c in b_cards),
                   'avg_atk': sum(c.traits['attack'] for c in b_cards)//max(1,len(b_cards)),
                   'avg_def': sum(c.traits['defense'] for c in b_cards)//max(1,len(b_cards)),
                   'avg_spd': sum(c.traits['speed'] for c in b_cards)//max(1,len(b_cards)),
                   'all_skills': sum((c.skills for c in b_cards), [])}

        enemy_data = [{'name': f'B队', 'health': b_stats['total_hp'],
                       'attack': b_stats['avg_atk'], 'defense': b_stats['avg_def'],
                       'speed': b_stats['avg_spd'], 'skills': b_stats['all_skills'][:6],
                       'passive_abilities': [], 'width': 1, 'height': 1, 'position': 0}]

        my_grid = {i: c for i, c in enumerate(a_cards[:5])}
        bs = BattleSystem(my_grid, enemy_data, stage_num=1, skill_enhance_level=0)
        bs.is_running = True
        ticks = 0
        while ticks < 300:
            bs.update_action_bars_frame()
            bs.update_status_damage()
            if bs.check_winner(): break
            unit = bs.get_next_unit()
            if unit: bs.execute_turn(unit, None)
            ticks += 1
        el = bs.winner
        if el == 'player':
            return f'A队胜利! ({ticks}回合)'
        return f'B队胜利! ({ticks}回合)'
