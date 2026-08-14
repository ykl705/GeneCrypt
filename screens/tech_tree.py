from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.metrics import dp

BRANCH_ORDER = ['root', 'breeding', 'mutation', 'editing', 'enhance', 'logistics']


class TechTreeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        title = Label(text='科技树', size_hint_y=0.06, bold=True, color=(1, 1, 1, 1))
        main.add_widget(title)

        self._info_bar = BoxLayout(orientation='horizontal', size_hint_y=0.04, spacing=dp(10))
        self._info_bar.add_widget(Label(text='材料:', color=(0.6, 1, 0.6, 1)))
        self._mat_lbl = Label(text='🧱 0', color=(0.6, 1, 0.6, 1))
        self._info_bar.add_widget(self._mat_lbl)
        self._info_bar.add_widget(Label(text='密钥:', color=(1, 1, 0.6, 1)))
        self._cur_lbl = Label(text='🧬 0', color=(1, 1, 0.6, 1))
        self._info_bar.add_widget(self._cur_lbl)
        self._info_bar.add_widget(Label(text='点击科技节点升级', color=(0.6, 0.6, 0.6, 1)))
        main.add_widget(self._info_bar)

        sv = ScrollView(do_scroll_x=False, do_scroll_y=True)
        self._tree_box = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=dp(6), padding=dp(8))
        self._tree_box.bind(minimum_height=self._tree_box.setter('height'))
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
        from tech_config import TECH_TREE, TREE_BRANCHES
        for branch in BRANCH_ORDER:
            binfo = TREE_BRANCHES.get(branch, {'name': branch})
            techs = [(tn, td) for tn, td in TECH_TREE.items() if td.get('branch') == branch]
            techs.sort(key=lambda kv: (kv[1].get('tree_radius', 0), kv[1].get('tree_angle', 0)))
            if not techs:
                continue
            branch_box = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=dp(3), padding=dp(4))
            branch_box.bind(minimum_height=branch_box.setter('height'))
            hdr = Label(text=f'◆ {binfo.get("name", branch)}', size_hint_y=None, height=dp(28),
                        bold=True, color=(0, 0.85, 1, 1), halign='left')
            hdr.bind(size=lambda *_: setattr(hdr, 'text_size', hdr.size))
            branch_box.add_widget(hdr)

            for tech_name, tpl in techs:
                node = game.tech_tree.get(tech_name)
                if not node:
                    continue
                level = node.get('level', 0)
                unlocked = node.get('unlocked', False)
                max_lv = node.get('max_level', 5)
                costs = node.get('costs', {})
                next_cost = costs.get(level + 1, {})
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(58), spacing=dp(5))

                txt = f'{node.get("name", tech_name)} Lv.{level}/{max_lv}'
                if level >= max_lv:
                    txt += ' [MAX]'
                    bg = (0.15, 0.45, 0.15, 1)
                elif unlocked:
                    cost_text = ''
                    for res, amt in next_cost.items():
                        if res == 'battle_materials':
                            cost_text += f' 🧱{amt}'
                        elif res == 'gacha_currency':
                            cost_text += f' 🧬{amt}'
                    txt += f' | 升{cost_text}' if cost_text else ''
                    bg = (0.2, 0.45, 0.2, 1)
                else:
                    txt += ' [未解锁]'
                    bg = (0.35, 0.35, 0.35, 1)
                btn = Button(text=txt, size_hint_x=0.38, font_size=dp(13),
                             background_color=bg)
                btn.bind(on_press=lambda _, tn=tech_name: self._upgrade(tn))
                row.add_widget(btn)

                desc = node.get('description', '')
                next_effect = node.get('effects', {}).get(level + 1, '')
                if level >= max_lv:
                    detail = node.get('effects', {}).get(level, desc)
                elif not unlocked:
                    req = node.get('unlock_requirement')
                    req_name = ''
                    if req:
                        from tech_config import TECH_TREE as TT
                        req_name = TT.get(req[0], {}).get('name', req[0]) if isinstance(req, (tuple, list)) else str(req)
                    detail = f'{desc} | 解锁需要: {req_name} Lv.{req[1] if isinstance(req, (tuple, list)) else "?"}'
                else:
                    detail = f'{desc} | 下级: {next_effect}' if next_effect else desc
                detail_lbl = Label(text=detail, size_hint_x=0.62, color=(0.75, 0.75, 0.75, 1),
                                   halign='left', valign='middle', font_size=dp(12))
                detail_lbl.bind(size=lambda *_: setattr(detail_lbl, 'text_size', detail_lbl.size))
                row.add_widget(detail_lbl)
                branch_box.add_widget(row)
            self._tree_box.add_widget(branch_box)

    def _upgrade(self, tech_name):
        app = App.get_running_app()
        success, msg = app.game.upgrade_tech(tech_name)
        if success:
            app.game.save_game()
            app.game._check_all_quests()
            self._refresh()
        else:
            from kivy.uix.popup import Popup
            popup = Popup(title='升级失败', content=Label(text=msg or '未知错误'),
                          size_hint=(0.7, 0.35))
            popup.open()
