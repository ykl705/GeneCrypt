from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.dropdown import DropDown


class BreedingLabScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        title = Label(text='繁殖实验室', size_hint_y=0.06, bold=True, color=(1, 1, 1, 1))
        main.add_widget(title)

        self._speed_lbl = Label(text='繁殖速度: 1.0x', size_hint_y=0.04, color=(0.8, 0.8, 1, 1))
        main.add_widget(self._speed_lbl)

        select = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=dp(5))
        select.add_widget(Label(text='父本:', color=(0.6, 0.8, 1, 1)))
        self._male_btn = Button(text='选择雄性', on_press=lambda _: self._show_dropdown('male'))
        select.add_widget(self._male_btn)
        select.add_widget(Label(text='母本:', color=(1, 0.6, 0.8, 1)))
        self._female_btn = Button(text='选择雌性', on_press=lambda _: self._show_dropdown('female'))
        select.add_widget(self._female_btn)
        main.add_widget(select)

        btn_row = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=dp(10))
        self._breed_btn = Button(text='开始繁殖', on_press=lambda _: self._start_breed())
        btn_row.add_widget(self._breed_btn)
        self._auto_btn = Button(text='自动繁殖: OFF', on_press=lambda _: self._toggle_auto())
        btn_row.add_widget(self._auto_btn)
        main.add_widget(btn_row)

        ivf = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=dp(5))
        ivf.add_widget(Button(text='提取精子', on_press=lambda _: self._extract_gamete('male')))
        ivf.add_widget(Button(text='提取卵子', on_press=lambda _: self._extract_gamete('female')))
        ivf.add_widget(Button(text='体外受精', on_press=lambda _: self._fuse_gametes()))
        main.add_widget(ivf)
        self._ivf_lbl = Label(text='IVF: 未提取', size_hint_y=0.04, color=(0.8, 0.8, 0.8, 1))
        main.add_widget(self._ivf_lbl)

        sv = ScrollView()
        self._info = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self._info.bind(minimum_height=self._info.setter('height'))
        sv.add_widget(self._info)
        main.add_widget(sv)

        self.add_widget(main)
        self._male_card = None
        self._female_card = None
        self._male_dropdown = None
        self._female_dropdown = None

    def on_enter(self):
        self._refresh()

    def update_combos(self):
        pass

    def _refresh(self):
        app = App.get_running_app()
        game = app.game
        self._speed_lbl.text = f'繁殖速度: {game.breed_speed_multiplier:.1f}x | 育种强化: {game.breed_speed_multiplier:.1f}x'
        self._male_btn.text = self._male_card.name if self._male_card else '选择雄性'
        self._female_btn.text = self._female_card.name if self._female_card else '选择雌性'

        info_text = ''
        if game.breeding_queue:
            for task in game.breeding_queue:
                remaining = task.get('remaining_time', 0)
                info_text += f'繁殖中: {task.get("name", "?")} - 剩余 {remaining:.0f}s\n'
        else:
            info_text = '无进行中的繁殖'
        self._info.clear_widgets()
        self._info.add_widget(Label(text=info_text.strip(), color=(0.8, 0.8, 0.8, 1)))
        if game.auto_breeding:
            self._auto_btn.text = '自动繁殖: ON'

    def _show_dropdown(self, gender):
        app = App.get_running_app()
        game = app.game
        dropdown = DropDown()
        compatible = [c for c in game.cards if c.is_alive and c.gender == gender]
        for card in compatible:
            btn = Button(text=f'{card.name} [{card.id}]', size_hint_y=None, height=dp(40))
            btn.bind(on_release=lambda b, c=card: self._select_card(c, gender, dropdown))
            dropdown.add_widget(btn)
        target = self._male_btn if gender == 'male' else self._female_btn
        dropdown.open(target)

    def _select_card(self, card, gender, dropdown):
        if gender == 'male':
            self._male_card = card
            self._male_btn.text = card.name
        else:
            self._female_card = card
            self._female_btn.text = card.name
        dropdown.dismiss()

    def _start_breed(self):
        if not self._male_card or not self._female_card:
            from kivy.uix.popup import Popup
            popup = Popup(title='错误', content=Label(text='请选择父母本'), size_hint=(0.5, 0.3))
            popup.open()
            return
        app = App.get_running_app()
        result = app.game.breeding(self._male_card, self._female_card)
        if isinstance(result, dict) and 'error' in result:
            from kivy.uix.popup import Popup
            popup = Popup(title='繁殖失败', content=Label(text=result['error']), size_hint=(0.5, 0.3))
            popup.open()
        else:
            app.refresh_breeding_combos()
            self._refresh()

    def _toggle_auto(self):
        app = App.get_running_app()
        app.game.auto_breeding = not app.game.auto_breeding
        self._auto_btn.text = '自动繁殖: ON' if app.game.auto_breeding else '自动繁殖: OFF'
        app.game.save_game()

    def _extract_gamete(self, gender):
        app = App.get_running_app()
        card = self._male_card if gender == 'male' else self._female_card
        if not card:
            from kivy.uix.popup import Popup
            popup = Popup(title='错误', content=Label(text=f'请先选择{"雄性" if gender == "male" else "雌性"}卡片'),
                          size_hint=(0.5, 0.3))
            popup.open()
            return
        result = app.game.extract_gamete(card, gender)
        if result.get('success'):
            self._ivf_lbl.text = f'IVF: {result.get("msg", "提取成功")}'
        else:
            from kivy.uix.popup import Popup
            popup = Popup(title='提取失败', content=Label(text=result.get('msg', '未知错误')), size_hint=(0.5, 0.3))
            popup.open()

    def _fuse_gametes(self):
        app = App.get_running_app()
        result = app.game.fuse_gametes()
        if result.get('success'):
            app.refresh_breeding_combos()
            self._refresh()
        else:
            from kivy.uix.popup import Popup
            popup = Popup(title='受精失败', content=Label(text=result.get('msg', '未知错误')), size_hint=(0.5, 0.3))
            popup.open()
