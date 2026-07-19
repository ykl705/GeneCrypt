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
        ivf.add_widget(Button(text='提取精子', on_press=lambda _: self._extract_gamete(True)))
        ivf.add_widget(Button(text='提取卵子', on_press=lambda _: self._extract_gamete(False)))
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
        self._stored_sperm = None
        self._stored_egg = None

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
        import time
        if game.breeding_queue:
            for task in game.breeding_queue:
                if task.get('completed'):
                    continue
                c1 = task.get('card1')
                c2 = task.get('card2')
                elapsed = time.time() - task.get('start_time', 0)
                dur = task.get('duration', 60)
                remaining = max(0, dur - elapsed)
                info_text += f'{c1.name}x{c2.name} 剩余{remaining:.0f}s\n'
        if not info_text:
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
        if self._male_card.gender != 'male' or self._female_card.gender != 'female':
            from kivy.uix.popup import Popup
            popup = Popup(title='错误', content=Label(text='性别不匹配，需要一雄一雌'), size_hint=(0.5, 0.3))
            popup.open()
            return
        male = self._male_card
        female = self._female_card
        def _on_complete():
            child_chr, child_gender = app.game.breeding(male, female)
            if child_chr:
                name = f'{male.name[:2]}{female.name[:2]}子代{len(app.game.cards)+1}'
                card = app.game.create_card(name, child_gender, chromosomes=child_chr)
                if card:
                    app.game._check_all_quests()
                    app.game.save_game()
            self._refresh()
        app.game.add_breeding_task(male, female, _on_complete)
        app.game.save_game()
        self._refresh()

    def _toggle_auto(self):
        app = App.get_running_app()
        app.game.auto_breeding = not app.game.auto_breeding
        self._auto_btn.text = '自动繁殖: ON' if app.game.auto_breeding else '自动繁殖: OFF'
        app.game.save_game()

    def _extract_gamete(self, as_male):
        app = App.get_running_app()
        card = self._male_card if as_male else self._female_card
        if not card:
            from kivy.uix.popup import Popup
            popup = Popup(title='错误', content=Label(text=f'请先选择{"雄性" if as_male else "雌性"}卡牌'),
                          size_hint=(0.5, 0.3))
            popup.open()
            return
        result = app.game.extract_gamete(card, as_male)
        gamete, msg = result
        if gamete:
            if as_male:
                self._stored_sperm = gamete
            else:
                self._stored_egg = gamete
            self._ivf_lbl.text = f'IVF: {msg}'
        else:
            from kivy.uix.popup import Popup
            popup = Popup(title='提取失败', content=Label(text=msg), size_hint=(0.5, 0.3))
            popup.open()

    def _fuse_gametes(self):
        if not self._stored_sperm or not self._stored_egg:
            from kivy.uix.popup import Popup
            popup = Popup(title='受精失败', content=Label(text='请先提取精子和卵子'), size_hint=(0.5, 0.3))
            popup.open()
            return
        app = App.get_running_app()
        child_chr, child_gender = app.game.fuse_gametes(self._stored_sperm, self._stored_egg)
        if child_chr:
            child_name = f'IVF体{len(app.game.cards)+1}'
            card = app.game.create_card(child_name, child_gender, chromosomes=child_chr)
            if card:
                self._stored_sperm = None
                self._stored_egg = None
                self._ivf_lbl.text = 'IVF: 受精成功！'
                app.refresh_breeding_combos()
                self._refresh()
            else:
                from kivy.uix.popup import Popup
                popup = Popup(title='受精失败', content=Label(text='卡牌创建失败，可能已满'), size_hint=(0.5, 0.3))
                popup.open()
        else:
            from kivy.uix.popup import Popup
            popup = Popup(title='受精失败', content=Label(text='配子融合失败'), size_hint=(0.5, 0.3))
            popup.open()
