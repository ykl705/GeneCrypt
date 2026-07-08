from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from functools import partial


class GachaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        title = Label(text='基因抽卡', size_hint_y=0.06, bold=True, color=(1, 1, 1, 1))
        main.add_widget(title)
        self._currency_lbl = Label(text='🧬 抽卡货币: 0', size_hint_y=0.04, color=(1, 1, 0.6, 1))
        main.add_widget(self._currency_lbl)
        self._mat_lbl = Label(text='🧱 战斗材料: 0', size_hint_y=0.04, color=(0.6, 1, 0.6, 1))
        main.add_widget(self._mat_lbl)

        content = BoxLayout(orientation='horizontal', spacing=dp(10))
        left = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=dp(5))
        left.add_widget(Label(text='卡池选择', size_hint_y=0.08, color=(0.8, 0.8, 0.8, 1)))
        self._pool_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(3))
        self._pool_list.bind(minimum_height=self._pool_list.setter('height'))
        sv_pools = ScrollView()
        sv_pools.add_widget(self._pool_list)
        left.add_widget(sv_pools)
        content.add_widget(left)

        right = BoxLayout(orientation='vertical', size_hint_x=0.7, spacing=dp(5))
        self._pool_info = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=dp(3), padding=dp(5))
        self._pool_info.add_widget(Label(text='选择卡池查看详情', color=(0.8, 0.8, 0.8, 1)))
        right.add_widget(self._pool_info)
        self._pull_btns = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=dp(10))
        right.add_widget(self._pull_btns)

        sv_result = ScrollView(size_hint_y=0.6)
        self._result_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self._result_list.bind(minimum_height=self._result_list.setter('height'))
        sv_result.add_widget(self._result_list)
        right.add_widget(sv_result)
        content.add_widget(right)
        main.add_widget(content)
        self.add_widget(main)
        self._selected_pool = None

    def on_enter(self):
        self._refresh()

    def _refresh(self):
        app = App.get_running_app()
        game = app.game
        self._currency_lbl.text = f'🧬 抽卡货币: {game.gacha_currency}'
        self._mat_lbl.text = f'🧱 战斗材料: {game.battle_materials}'
        self._pool_list.clear_widgets()
        for pid, pool in app.game.GACHA_POOLS.items():
            unlocked = game.max_stage >= pool['unlock_stage']
            name = pool['name']
            cost = pool.get('cost', 100)
            btn = Button(text=f'{pool.get("icon", "")} {name} ({cost}🧬)',
                         size_hint_y=None, height=dp(50),
                         background_color=self._hex(pool.get('theme_bg', '#1a1a2e')),
                         on_press=lambda _, p=pid: self._select_pool(p))
            if not unlocked:
                btn.text = f'🔒 {name} (需要通关第{pool["unlock_stage"]}关)'
                btn.background_color = (0.2, 0.2, 0.2, 1)
            self._pool_list.add_widget(btn)
        if self._selected_pool:
            self._select_pool(self._selected_pool)

    def _hex(self, h):
        return tuple(int(h[i:i+2], 16)/255 for i in (1, 3, 5)) + (1,)

    def _select_pool(self, pid):
        self._selected_pool = pid
        app = App.get_running_app()
        pool = app.game.GACHA_POOLS.get(pid)
        if not pool:
            return
        self._pool_info.clear_widgets()
        color = pool.get('theme_color', '#00d9ff')
        bg = pool.get('theme_bg', '#1a1a2e')
        sec = pool.get('theme_secondary', '#0a0a1a')
        self._pool_info.add_widget(Label(text=f'{pool.get("icon","")} {pool["name"]}', bold=True, color=(1, 1, 1, 1),
                                         size_hint_y=0.2))
        self._pool_info.add_widget(Label(text=pool.get('description', ''), color=(0.8, 0.8, 0.8, 1),
                                         size_hint_y=0.15))
        self._pool_info.add_widget(Label(text=pool.get('flavor', ''), color=(0.6, 0.6, 0.6, 1),
                                         size_hint_y=0.2))
        cost = pool.get('cost', 100)
        self._pool_info.add_widget(Label(text=f'每次抽取: {cost} 🧬', color=(1, 1, 0.6, 1), size_hint_y=0.15))
        with self._pool_info.canvas.before:
            Color(*self._hex(bg))
            self._pool_info.rect = Rectangle(pos=self._pool_info.pos, size=self._pool_info.size)
        self._pool_info.bind(pos=lambda _, v: setattr(self._pool_info, 'rect', Rectangle(pos=v, size=self._pool_info.size))
                             if hasattr(self._pool_info, 'rect') else None)

        self._pull_btns.clear_widgets()
        pull1 = Button(text=f'抽取1次 ({cost}🧬)', on_press=lambda _: self._do_pull(pid, 1))
        pull10 = Button(text=f'抽取10次 ({cost*10}🧬)', on_press=lambda _: self._do_pull(pid, 10))
        self._pull_btns.add_widget(pull1)
        self._pull_btns.add_widget(pull10)

    def _do_pull(self, pid, count):
        app = App.get_running_app()
        result = app.game.gacha_pull(pid, count)
        if result.get('success'):
            cards = result.get('cards', [])
            for card in cards:
                from widgets.card_widget import CardWidget
                cw = CardWidget(card=card)
                cw.height = dp(60)
                self._result_list.add_widget(cw)
            self._refresh()
            app.game.save_game()
            app.refresh_breeding_combos()
        else:
            from kivy.uix.popup import Popup
            popup = Popup(title='抽卡失败', content=Label(text=result.get('msg', '未知错误')),
                          size_hint=(0.5, 0.3))
            popup.open()
