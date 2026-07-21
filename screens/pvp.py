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
        app = App.get_running_app()
        bs = app._screen_refs.get('战斗')
        if bs is None:
            return
        from gene_game import Card, BattleSystem
        import random
        def _build_cards(tm):
            cards = {}
            for pos, t in tm.items():
                c = Card(f'PvP-{pos}', random.choice(['male','female']))
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
        bs._render_battle_grid()
        bs.add_log('[PvP] 对决开始!')
        Clock.schedule_interval(bs._battle_tick, 0.3)
        for tab in app.root.tab_list:
            if tab.text == '战斗':
                app.root.switch_to(tab)
                break
