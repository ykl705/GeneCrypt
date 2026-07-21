from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.metrics import dp
from gene_config import ACHIEVEMENTS, BLOODLINES, ENEMY_TRAITS


class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        main.add_widget(Label(text='数据面板', size_hint_y=0.06, bold=True, color=(0.3, 0.8, 1, 1)))
        sv = ScrollView(size_hint_y=1)
        self._content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self._content.bind(minimum_height=self._content.setter('height'))
        sv.add_widget(self._content)
        main.add_widget(sv)
        self.add_widget(main)

    def on_enter(self):
        self._refresh()

    def _section(self, title):
        self._content.add_widget(Label(text=title, size_hint_y=None, height=dp(26), bold=True,
                                        color=(1, 0.85, 0, 1)))

    def _line(self, text, color=(0.8, 0.8, 0.8, 1)):
        self._content.add_widget(Label(text=text, size_hint_y=None, height=dp(22), color=color, halign='left'))

    def _refresh(self):
        self._content.clear_widgets()
        app = App.get_running_app()
        game = app.game

        self._section('战斗统计')
        total_wins = game.max_stage
        boss_kills = game.enemy_kills.get('__boss__', 0)
        no_loss = len(game.no_loss_stages)
        max_stage = game.max_stage
        self._line(f'  最高关卡: {max_stage}    击败BOSS: {boss_kills}    无伤通关: {no_loss}关')

        self._section('最强卡牌')
        if game.cards:
            top_atk = max(game.cards, key=lambda c: c.traits.get('attack', 0))
            top_hp = max(game.cards, key=lambda c: c.traits.get('health', 0))
            top_spd = max(game.cards, key=lambda c: c.traits.get('speed', 0))
            self._line(f'  最高ATK: {top_atk.name} [{top_atk.traits.get("attack",0)}]')
            self._line(f'  最高HP:  {top_hp.name} [{top_hp.traits.get("health",0)}]')
            self._line(f'  最高SPD: {top_spd.name} [{top_spd.traits.get("speed",0)}]')

        self._section('养成进度')
        bl_collected = len(set(getattr(c, 'bloodline', None) for c in game.cards if c.bloodline))
        star5 = sum(1 for c in game.cards if getattr(c, 'star', 1) >= 5)
        breeds = game.breed_counter
        self._line(f'  血脉: {bl_collected}/{len(BLOODLINES)}  5星卡: {star5}  繁殖次数: {breeds}')

        self._section('图鉴进度')
        seen = set()
        from battle_config import STAGES
        for snum, stage in STAGES.items():
            if not isinstance(snum, int): continue
            for e in stage.get('enemies', []):
                seen.add(e.get('name', ''))
        self._line(f'  敌人发现: {len(seen)}种')

        self._section('成就')
        done = sum(1 for a in ACHIEVEMENTS if a['id'] in game.achievements)
        total = len(ACHIEVEMENTS)
        self._line(f'  完成: {done}/{total} - 请到"成就"页面查看详情', color=(0.4, 1, 0.4, 1))

        self._section('挑战记录')
        if game.challenge_scores:
            for theme_id, hs in game.challenge_scores.items():
                theme_names = {
                    'subject_rampage': '实验体暴乱', 'abandoned_lab': '废弃实验室',
                    'ancient_ruins': '远古遗迹', 'elemental_cycle': '元素轮回', 'blind_box_war': '盲盒战争'
                }
                tname = theme_names.get(theme_id, theme_id)
                self._line(f'  {tname}: {hs["points"]}分 ({hs["time_str"]})', color=(1, 0.85, 0, 1))
        else:
            self._line('  暂无记录', color=(0.5, 0.5, 0.5, 1))

        self._section('资源')
        self._line(f'  基因密钥: {game.gacha_currency}  战斗材料: {game.battle_materials}')
        self._line(f'  基因精华: {game.gene_essence}  芯片: {sum(game.chip_inventory.values())}种  模组: {sum(game.module_inventory.values())}个')
