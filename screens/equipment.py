from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.metrics import dp
from gene_config import EQUIPMENT_SLOTS, EQUIPMENT_SLOT_NAMES, EQUIPMENT_RARITY, SET_BONUSES, AFFIX_CODE_NAMES
import os


class EquipmentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        main.add_widget(Label(text='卡牌装备', size_hint_y=0.05, bold=True, color=(1,0.6,0,1)))
        self._card_btn = Button(text='选择卡牌', size_hint_y=0.06,
                                 on_press=lambda _: self._select_card())
        main.add_widget(self._card_btn)
        body = BoxLayout(orientation='horizontal', spacing=dp(8), size_hint_y=1)
        left = BoxLayout(orientation='vertical', size_hint_x=0.45, spacing=dp(3))
        left.add_widget(Label(text='装备槽', size_hint_y=None, height=dp(22), color=(0.8,0.8,0.8,1)))
        self._slot_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self._slot_box.bind(minimum_height=self._slot_box.setter('height'))
        sv1 = ScrollView(size_hint_y=1)
        sv1.add_widget(self._slot_box)
        left.add_widget(sv1)
        body.add_widget(left)
        right = BoxLayout(orientation='vertical', size_hint_x=0.55, spacing=dp(3))
        right.add_widget(Label(text='库存装备', size_hint_y=None, height=dp(22), color=(0.8,0.8,0.8,1)))
        self._inv_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self._inv_box.bind(minimum_height=self._inv_box.setter('height'))
        sv2 = ScrollView(size_hint_y=1)
        sv2.add_widget(self._inv_box)
        right.add_widget(sv2)
        body.add_widget(right)
        main.add_widget(body)
        self.add_widget(main)
        self._card = None

    def on_enter(self):
        self._refresh()

    def _select_card(self):
        app = App.get_running_app()
        content = BoxLayout(orientation='vertical', spacing=dp(3))
        sv = ScrollView()
        inner = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        inner.bind(minimum_height=inner.setter('height'))
        for card in app.game.cards:
            if not card.is_alive: continue
            btn = Button(text=f'{card.name} ATK:{card.traits.get("attack",0)}',
                         size_hint_y=None, height=dp(36))
            btn.bind(on_press=lambda _, c=card: self._pick(c))
            inner.add_widget(btn)
        sv.add_widget(inner)
        content.add_widget(sv)
        popup = Popup(title='选择卡牌', content=content, size_hint=(0.7,0.7))
        popup.open()

    def _pick(self, card):
        self._card = card
        self._card_btn.text = f'已选: {card.name}'
        self._refresh()

    def _refresh(self):
        try:
            self._refresh_impl()
        except Exception as e:
            Popup(title='错误', content=Label(text=f'装备页面错误:\n{str(e)[:200]}'),
                  size_hint=(0.7, 0.4)).open()

    def _refresh_impl(self):
        self._slot_box.clear_widgets()
        self._inv_box.clear_widgets()
        app = App.get_running_app()
        if not self._card:
            return
        card = self._card
        for slot in EQUIPMENT_SLOTS:
            item = card.equipment.get(slot)
            sname = EQUIPMENT_SLOT_NAMES.get(slot, slot)
            if item:
                name = item.get('name', item.get('id','?'))
                rarity = item.get('rarity', 'common')
                rinfo = next((r for r in EQUIPMENT_RARITY if r['id'] == rarity), {'color':(0.6,1,0.6,1)})
                txt = f'[{sname}] {name}'
                clr = rinfo['color']
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(34), spacing=dp(4))
                img_path = os.path.join('assets', 'equipment', f'{slot}_{rarity}.png')
                if os.path.exists(img_path):
                    from kivy.uix.image import Image as KivyImg
                    row.add_widget(KivyImg(source=img_path, size_hint_x=None, width=dp(28)))
                row.add_widget(Label(text=txt, color=clr, size_hint_x=0.7))
                btn = Button(text='卸下', size_hint_x=0.3, on_press=lambda _, s=slot: self._safe_unequip(s))
                row.add_widget(btn)
                self._slot_box.add_widget(row)
            else:
                btn = Button(text=f'[{sname}] 空', color=(0.4,0.4,0.4,1),
                             size_hint_y=None, height=dp(36))
            self._slot_box.add_widget(btn)

        for inv_id, inv_entry in app.game.equipment_inventory.items():
            if isinstance(inv_entry, int):
                continue
            if inv_entry.get('count', 0) <= 0: continue
            item = inv_entry.get('data', {})
            slot = item.get('slot', inv_id.split('_')[0])
            rarity = item.get('rarity', inv_id.split('_')[1] if len(inv_id.split('_'))>1 else 'common')
            rinfo = next((r for r in EQUIPMENT_RARITY if r['id'] == rarity), {'name':'?','color':(0.5,0.5,0.5,1)})
            sname = EQUIPMENT_SLOT_NAMES.get(slot, slot)
            name = item.get('name', f'{rinfo["name"]}装备')
            txt = f'[{rinfo["name"]}] {name} x{inv_entry["count"]}'
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(34), spacing=dp(4))
            img_path = os.path.join('assets', 'equipment', f'{slot}_{rarity}.png')
            if os.path.exists(img_path):
                from kivy.uix.image import Image as KivyImg
                row.add_widget(KivyImg(source=img_path, size_hint_x=None, width=dp(28)))
            row.add_widget(Label(text=txt, color=rinfo['color'], size_hint_x=0.55))
            btn = Button(text='装备', size_hint_x=0.2,
                         on_press=lambda _, i=inv_id: self._safe_equip(i))
            info_btn = Button(text='?', size_hint_x=0.08,
                               on_press=lambda _, i=inv_id: self._show_item_detail(i))
            row.add_widget(btn)
            row.add_widget(info_btn)
            row.add_widget(btn)
            self._inv_box.add_widget(row)

    def _safe_equip(self, item_id):
        try:
            self._equip(item_id)
        except Exception as e:
            Popup(title='错误', content=Label(text=f'装备失败:\n{str(e)[:200]}'),
                  size_hint=(0.7, 0.4)).open()

    def _safe_unequip(self, slot):
        try:
            self._unequip(slot)
        except Exception as e:
            Popup(title='错误', content=Label(text=f'卸装备失败:\n{str(e)[:200]}'),
                  size_hint=(0.7, 0.4)).open()

    def _equip(self, item_id):
        app = App.get_running_app()
        success, msg = app.game.equip_item(self._card, item_id)
        app.game.save_game()
        self._refresh()

    def _unequip(self, slot):
        app = App.get_running_app()
        app.game.unequip_item(self._card, slot)
        app.game.save_game()
        self._refresh()

    def _show_item_detail(self, inv_id):
        try:
            app = App.get_running_app()
            inv_entry = app.game.equipment_inventory.get(inv_id)
            if not inv_entry:
                return
            if isinstance(inv_entry, int):
                return
            item = inv_entry.get('data', {})
            rarity = item.get('rarity', 'common')
            rinfo = next((r for r in EQUIPMENT_RARITY if r['id'] == rarity), {'name':'?','color':(0.5,0.5,0.5,1)})
            lines = [item.get('name', '?')]
            lines.append(f'稀有度: {rinfo["name"]}')
            lines.append(f'部位: {EQUIPMENT_SLOT_NAMES.get(item.get("slot",""),"?")}')
            lines.append('--- 词条 ---')
            for aff in item.get('affixes', []):
                code = aff.get('code', '?')
                cname = AFFIX_CODE_NAMES.get(code, code)
                v = aff['value']
                s = '%' if aff.get('is_pct') else ''
                lines.append(f'  {cname}: +{v}{s}')
            popup = Popup(title='装备详情', content=Label(text='\n'.join(lines)),
                          size_hint=(0.6, 0.5))
            popup.open()
        except Exception as e:
            Popup(title='错误', content=Label(text=f'详情错误:\n{str(e)[:200]}'),
                  size_hint=(0.7, 0.4)).open()
