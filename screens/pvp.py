from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp
import random


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
        main = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(10))
        main.add_widget(Label(text='PvP对决', size_hint_y=0.06, bold=True, color=(1,0.6,0,1)))
        main.add_widget(Label(text='导出队伍代码', size_hint_y=None, height=dp(24), color=(0.8,0.8,0.8,1)))
        btn_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(8))
        self._export_btn = Button(text='生成代码', on_press=lambda _: self._export_team())
        btn_row.add_widget(self._export_btn)
        main.add_widget(btn_row)
        self._export_lbl = Label(text='', size_hint_y=None, height=dp(40), color=(0.4,1,0.4,1))
        main.add_widget(self._export_lbl)
        main.add_widget(Label(text='粘贴对手代码', size_hint_y=None, height=dp(24), color=(0.8,0.8,0.8,1)))
        self._code_input = TextInput(text='', multiline=False, size_hint_y=None, height=dp(40),
                                      hint_text='粘贴队伍代码...')
        main.add_widget(self._code_input)
        self._import_btn = Button(text='导入并模拟', size_hint_y=None, height=dp(40),
                                   on_press=lambda _: self._import_and_sim())
        main.add_widget(self._import_btn)
        self._result_lbl = Label(text='', size_hint_y=1, color=(1,1,0.6,1))
        main.add_widget(self._result_lbl)
        self.add_widget(main)

    def _export_team(self):
        app = App.get_running_app()
        bs = app._screen_refs.get('战斗')
        if not bs or not bs._team:
            popup = Popup(title='错误', content=Label(text='请先在战斗页编好队伍'),
                          size_hint=(0.5,0.25))
            popup.open()
            return
        code = encode_team(bs._team)
        self._export_lbl.text = f'代码: {code}'
        from kivy.base import Clipboard
        try:
            Clipboard.put('code', code)
        except:
            pass

    def _import_and_sim(self):
        code = self._code_input.text.strip()
        if not code:
            return
        try:
            team = decode_team(code)
        except ValueError as e:
            self._result_lbl.text = f'[错误] {e}'
            return
        from battle_config import STAGES
        stage = STAGES.get(50, STAGES.get(1))
        ed = [dict(e) for e in stage.get('enemies', [])]
        if not ed:
            ed = [{'name':'对手','health':300,'attack':30,'defense':15,'speed':15,
                   'skills':['火焰吐息'],'passive_abilities':[],'width':1,'height':1,'position':0}]
        detail = '\n'.join(f'  位置{p}: 血脉={t["bloodline"] or "无"} 星={t["star"]} 技能={t["skills"]}' 
                          for p, t in sorted(team.items()))
        result = self._sim_battle(team)
        self._result_lbl.text = f'队伍解析成功!\n{detail}\n\n{result}'

    def _sim_battle(self, opponent_team):
        app = App.get_running_app()
        my_team = app._screen_refs.get('战斗')
        if not my_team or not my_team._team:
            return '[需要先在战斗页编队]'

        from gene_game import Card, BattleSystem
        import random, time

        my_cards = list(my_team._team.values())
        opp_cards = []
        for pos, t in sorted(opponent_team.items()):
            c = Card(f'对手{pos}', random.choice(['male', 'female']))
            star = t.get('star', 1)
            c.star = star
            c.traits['attack'] = 50 + star * 30
            c.traits['health'] = 200 + star * 100
            c.traits['defense'] = 20 + star * 10
            c.traits['speed'] = 10 + star * 5
            c.traits['critical_rate'] = 5 + star * 2
            c.traits['dodge_rate'] = 5
            c.skills = t.get('skills', [])
            opp_cards.append(c)

        my_ed = [{'name': '模拟对手', 'health': sum(c.traits['health'] for c in opp_cards),
                   'attack': max(c.traits['attack'] for c in opp_cards),
                   'defense': max(c.traits['defense'] for c in opp_cards),
                   'speed': max(c.traits['speed'] for c in opp_cards),
                   'skills': sum((c.skills for c in opp_cards), []),
                   'passive_abilities': [], 'width': 1, 'height': 1, 'position': 0}]

        my_grid = {i: c for i, c in enumerate(my_cards)}
        bs = BattleSystem(my_grid, my_ed, stage_num=1, skill_enhance_level=0)
        bs.is_running = True
        ticks = 0
        while ticks < 200:
            bs.update_action_bars_frame()
            if bs.check_winner():
                break
            unit = bs.get_next_unit()
            if unit:
                bs.execute_turn(unit, None)
            ticks += 1
        if bs.winner == 'player':
            return f'[胜利!] 我方在{ticks}回合内击败对手!'
        return f'[失败] 对手实力太强...'

