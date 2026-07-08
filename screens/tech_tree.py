from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.core.window import Window


class TechTreeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        title = Label(text='科技树', size_hint_y=0.06, bold=True, color=(1, 1, 1, 1))
        main.add_widget(title)

        self._info_bar = BoxLayout(orientation='horizontal', size_hint_y=0.04, spacing=dp(10))
        self._info_bar.add_widget(Label(text='分支:', color=(0.8, 0.8, 0.8, 1)))
        self._branch_lbl = Label(text='', color=(0.8, 0.8, 0.8, 1))
        self._info_bar.add_widget(self._branch_lbl)
        self._info_bar.add_widget(Label(text='材料:', color=(0.6, 1, 0.6, 1)))
        self._mat_lbl = Label(text='🧱 0', color=(0.6, 1, 0.6, 1))
        self._info_bar.add_widget(self._mat_lbl)
        self._info_bar.add_widget(Label(text='货币:', color=(1, 1, 0.6, 1)))
        self._cur_lbl = Label(text='🧬 0', color=(1, 1, 0.6, 1))
        self._info_bar.add_widget(self._cur_lbl)
        main.add_widget(self._info_bar)

        sv = ScrollView(do_scroll_x=True, do_scroll_y=True)
        self._tree_box = BoxLayout(orientation='vertical', size_hint=(None, None), spacing=dp(10), padding=dp(20))
        self._tree_box.bind(minimum_width=self._tree_box.setter('width'),
                            minimum_height=self._tree_box.setter('height'))
        sv.add_widget(self._tree_box)
        main.add_widget(sv)
        self.add_widget(main)

    def on_enter(self):
        self._refresh()

    def _refresh(self):
        self._tree_box.clear_widgets()
        app = App.get_running_app()
        game = app.game
        self._mat_lbl.text = f'🧱 {game.battle_materials}'
        self._cur_lbl.text = f'🧬 {game.gacha_currency}'
        from tech_config import TREE_BRANCHES
        for branch_name, branch_info in TREE_BRANCHES.items():
            branch_box = BoxLayout(orientation='vertical', size_hint=(None, None), spacing=dp(3),
                                    padding=dp(5))
            branch_box.add_widget(Label(text=f'【{branch_info.get("name", branch_name)}】',
                                        size_hint_y=None, height=dp(25), bold=True, color=(0, 0.85, 1, 1)))
            for tech_name in branch_info.get('techs', []):
                node = game.tech_tree.get(tech_name)
                if not node:
                    continue
                level = node.get('level', 0)
                unlocked = node.get('unlocked', False)
                max_lv = node.get('max_level', 5)
                costs = node.get('costs', {})
                next_cost = costs.get(level + 1, {})
                txt = f'{node.get("name", tech_name)} Lv.{level}/{max_lv}'
                if level >= max_lv:
                    txt += ' [MAX]'

                tech_box = BoxLayout(orientation='horizontal', size_hint=(None, None),
                                     size=(dp(500), dp(40)), spacing=dp(5))
                btn = Button(text=txt, size_hint_x=0.5,
                             background_color=(0.1, 0.5, 0.1, 1) if level > 0 else (0.3, 0.3, 0.3, 1))
                if level < max_lv and unlocked:
                    cost_text = ''
                    for res, amt in next_cost.items():
                        if res == 'battle_materials':
                            cost_text += f'🧱{amt} '
                        elif res == 'gacha_currency':
                            cost_text += f'🧬{amt} '
                    if cost_text:
                        btn.text += f' | {cost_text}'
                    btn.bind(on_press=lambda _, tn=tech_name: self._upgrade(tn))
                tech_box.add_widget(btn)

                desc = node.get('description', '')
                next_effect = node.get('effects', {}).get(level + 1, node.get('effect', ''))
                detail = f'{desc} | 下级效果: {next_effect}' if next_effect else desc
                detail_lbl = Label(text=detail, size_hint_x=0.5, color=(0.7, 0.7, 0.7, 1),
                                   halign='left', text_size=(dp(280), None))
                tech_box.add_widget(detail_lbl)
                branch_box.add_widget(tech_box)
            if branch_box.children:
                self._tree_box.add_widget(branch_box)

    def _upgrade(self, tech_name):
        app = App.get_running_app()
        result = app.game.upgrade_tech(tech_name)
        if result.get('success'):
            app.game.save_game()
            self._refresh()
        else:
            from kivy.uix.popup import Popup
            popup = Popup(title='升级失败', content=Label(text=result.get('msg', '未知错误')),
                          size_hint=(0.5, 0.3))
            popup.open()
