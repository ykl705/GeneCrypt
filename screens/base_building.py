from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp
from gene_config import BASE_BUILDINGS


class BaseBuildingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        main.add_widget(Label(text='基地建设', size_hint_y=0.06, bold=True, color=(1,0.85,0,1)))
        sv = ScrollView(size_hint_y=1)
        self._content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(6))
        self._content.bind(minimum_height=self._content.setter('height'))
        sv.add_widget(self._content)
        main.add_widget(sv)
        self.add_widget(main)

    def on_enter(self):
        self._refresh()

    def _refresh(self):
        self._content.clear_widgets()
        app = App.get_running_app()
        game = app.game
        from kivy.graphics import Color as GfxColor, Rectangle

        self._content.add_widget(Label(text=f'材料: {game.battle_materials}  精华: {game.gene_essence}',
                                        size_hint_y=None, height=dp(24), color=(0.8,0.8,0.8,1)))

        for bld in BASE_BUILDINGS:
            lv = game.base_buildings.get(bld['id'], 0)
            bonus = bld['per_lv'] * lv
            maxed = lv >= bld['max_lv']
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(75),
                              spacing=dp(2), padding=dp(6))
            with card.canvas.before:
                c = (0.1, 0.3, 0.1, 1) if lv > 0 else (0.2, 0.2, 0.25, 1)
                GfxColor(*c)
                card._bg = Rectangle(pos=card.pos, size=card.size)
            card.bind(pos=lambda c,v:setattr(c._bg,'pos',v), size=lambda c,v:setattr(c._bg,'size',v))

            head = BoxLayout(orientation='horizontal', size_hint_y=0.35)
            head.add_widget(Label(text=f'{bld["name"]}  Lv.{lv}/{bld["max_lv"]}',
                                   color=(1,1,1,1), bold=True, size_hint_x=0.55))
            head.add_widget(Label(text=bld['desc'].format(bonus=bonus),
                                   color=(0.6,1,0.6,1), size_hint_x=0.45, halign='right'))
            card.add_widget(head)

            if maxed:
                card.add_widget(Label(text='已满级', color=(0.5,0.5,0.5,1), size_hint_y=0.3))
            else:
                cost_m = 50 + lv * 30
                cost_e = 5 + lv * 3
                btn = Button(text=f'升级 [{cost_m}材料/{cost_e}精华]', size_hint_y=0.3,
                             on_press=lambda _, bid=bld['id']: self._upgrade(bid))
                card.add_widget(btn)
            self._content.add_widget(card)

    def _upgrade(self, bid):
        app = App.get_running_app()
        success, msg = app.game.upgrade_building(bid)
        if success:
            app.game.save_game()
        popup = Popup(title='基建', content=Label(text=msg), size_hint=(0.5, 0.25))
        popup.open()
        self._refresh()
