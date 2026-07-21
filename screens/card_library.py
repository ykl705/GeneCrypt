from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.popup import Popup
from widgets.card_widget import CardWidget, CardDetailPopup


class CardLibraryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        main = BoxLayout(orientation='horizontal', spacing=dp(10), padding=dp(10))
        left = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=dp(5))
        left.add_widget(Label(text='卡牌库', size_hint_y=0.06, bold=True, color=(1, 1, 1, 1)))
        self._count_lbl = Label(text='卡牌: 0/20', size_hint_y=0.04, color=(0.8, 0.8, 0.8, 1))
        left.add_widget(self._count_lbl)
        sv = ScrollView()
        self._card_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self._card_list.bind(minimum_height=self._card_list.setter('height'))
        sv.add_widget(self._card_list)
        left.add_widget(sv)
        main.add_widget(left)

        right = BoxLayout(orientation='vertical', size_hint_x=0.6, spacing=dp(5))
        right.add_widget(Label(text='卡牌详情', size_hint_y=0.06, bold=True, color=(1, 1, 1, 1)))
        sv2 = ScrollView()
        self._detail = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self._detail.bind(minimum_height=self._detail.setter('height'))
        sv2.add_widget(self._detail)
        right.add_widget(sv2)
        self._action_bar = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=dp(5))
        right.add_widget(self._action_bar)
        main.add_widget(right)
        self.add_widget(main)
        self._selected_card = None

    def on_enter(self):
        self._refresh()

    def _refresh(self):
        app = App.get_running_app()
        game = app.game
        self._count_lbl.text = f'卡牌: {len(game.cards)}/{game.effective_max_cards}'
        self._card_list.clear_widgets()
        cards = sorted(game.cards, key=lambda c: (not getattr(c, 'favorite', False), c.name))
        for card in cards:
            cw = CardWidget(card=card)
            cw.bind(on_release=lambda _, c=card: self._on_card_select(c))
            self._card_list.add_widget(cw)
        if self._selected_card and self._selected_card in game.cards:
            self._show_detail(self._selected_card)
        else:
            self._detail.clear_widgets()
            self._action_bar.clear_widgets()

    def _on_card_select(self, card):
        self._selected_card = card
        self._show_detail(card)

    def _show_detail(self, card):
        self._detail.clear_widgets()
        self._action_bar.clear_widgets()
        c = card
        gender_color = '#4a90d9' if c.gender == 'male' else '#d94a8a'
        alive_str = '' if c.is_alive else ' [已死亡]'
        title = f'{c.name} [{c.id}]{alive_str}'
        self._detail.add_widget(Label(text=title, bold=True, color=(1, 1, 1, 1), size_hint_y=None, height=dp(30)))
        self._detail.add_widget(Label(text=f'性别: {"♂ 雄性" if c.gender == "male" else "♀ 雌性"} | '
                                           f'代系: {len(c.parent_ids)} | 寿命: {c.traits.get("lifespan", "?")}',
                                     size_hint_y=None, height=dp(25), color=(0.8, 0.8, 0.8, 1)))
        t = c.traits
        stats_grid = GridLayout(cols=4, size_hint_y=None, height=dp(100), spacing=dp(2))
        stats = [
            ('攻击', t.get('attack', 0)), ('生命', t.get('health', 0)),
            ('防御', t.get('defense', 0)), ('速度', t.get('speed', 0)),
            ('体力', t.get('stamina', 0)), ('暴击', t.get('critical_rate', 0)),
            ('闪避', t.get('dodge_rate', 0)), ('寿命', t.get('lifespan', 0)),
        ]
        for name, val in stats:
            stats_grid.add_widget(Label(text=f'{name}:', color=(0.8, 0.8, 0.8, 1), font_size=dp(11)))
            stats_grid.add_widget(Label(text=str(val), color=(1, 1, 1, 1), font_size=dp(11)))
        self._detail.add_widget(stats_grid)
        skills_text = ', '.join(c.skills) if c.skills else '无'
        self._detail.add_widget(Label(text=f'技能: {skills_text}', color=(0.6, 1, 0.6, 1), size_hint_y=None, height=dp(25)))
        passive_text = ', '.join(c.passive_skills) if c.passive_skills else '无'
        self._detail.add_widget(Label(text=f'被动: {passive_text}', color=(0.6, 0.8, 1, 1), size_hint_y=None, height=dp(25)))
        if c.is_alive:
            mutate_btn = Button(text='射线变异', on_press=lambda _: self._mutate_card(c))
            self._action_bar.add_widget(mutate_btn)
            star_btn = Button(text=f'升星({c.star}/5)', on_press=lambda _: self._star_up(c))
            self._action_bar.add_widget(star_btn)
            train_btn = Button(text='训练', on_press=lambda _: self._train_card(c))
            self._action_bar.add_widget(train_btn)
            equip_btn = Button(text='装备', on_press=lambda _: self._show_equipment(c))
            self._action_bar.add_widget(equip_btn)
        clone_btn = Button(text='克隆', on_press=lambda _: self._clone_card(c))
        self._action_bar.add_widget(clone_btn)
        fav_text = '★取消收藏' if getattr(c, 'favorite', False) else '☆收藏'
        fav_btn = Button(text=fav_text, on_press=lambda _: self._toggle_favorite(c))
        self._action_bar.add_widget(fav_btn)
        report_btn = Button(text='基因报告', on_press=lambda _: self._show_report(c))
        self._action_bar.add_widget(report_btn)
        delete_btn = Button(text='删除', on_press=lambda _: self._del_card_check(c))
        delete_btn.background_color = (0.8, 0.2, 0.2, 1)
        self._action_bar.add_widget(delete_btn)
        if c.is_alive:
            mod_btn = Button(text='模组', on_press=lambda _: self._manage_modules(c))
            self._action_bar.add_widget(mod_btn)
            chip_btn = Button(text='芯片', on_press=lambda _: self._manage_chips(c))
            self._action_bar.add_widget(chip_btn)

    def _star_up(self, card):
        app = App.get_running_app()
        success, msg = app.game.star_up_card(card)
        popup = Popup(title='升星', content=Label(text=msg), size_hint=(0.5, 0.3))
        btn = Button(text='确定', on_press=popup.dismiss, size_hint_y=None, height=dp(40))
        content = BoxLayout(orientation='vertical', padding=dp(10))
        content.add_widget(Label(text=msg))
        content.add_widget(btn)
        popup.content = content
        popup.open()
        app.game.save_game()
        app.refresh_breeding_combos()
        self._show_detail(card)

    def _train_card(self, card):
        from kivy.uix.gridlayout import GridLayout
        app = App.get_running_app()
        content = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        content.add_widget(Label(text=f'训练 {card.name} | 精华:{app.game.gene_essence} 材料:{app.game.battle_materials}',
                                  size_hint_y=None, height=dp(24), color=(0.8, 0.8, 0.8, 1)))
        stats = GridLayout(cols=2, size_hint_y=None, height=dp(160), spacing=dp(3))
        for stat_key in ('attack', 'health', 'defense', 'speed'):
            done = card.training.get(stat_key, 0)
            max_s = card.star * 8
            stats.add_widget(Label(text=f'{stat_key}: {done}/{max_s}', color=(1, 1, 1, 1)))
            btn = Button(text=f'训练', size_hint_y=None, height=dp(32),
                         on_press=lambda _, sk=stat_key: self._do_train(card, sk))
            stats.add_widget(btn)
        content.add_widget(stats)
        close_btn = Button(text='关闭', size_hint_y=None, height=dp(36))
        content.add_widget(close_btn)
        popup = Popup(title='训练', content=content, size_hint=(0.6, 0.5))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _do_train(self, card, stat_key):
        app = App.get_running_app()
        success, msg = app.game.train_card(card, stat_key)
        from kivy.uix.popup import Popup
        popup = Popup(title='训练结果', content=Label(text=msg), size_hint=(0.5, 0.25))
        popup.open()
        app.game.save_game()

    def _delete_card(self, card):
        if getattr(card, 'favorite', False):
            popup = Popup(title='错误', content=Label(text='无法删除收藏卡牌，请先取消收藏'),
                          size_hint=(0.5, 0.25))
            popup.open()
            return
        app = App.get_running_app()
        app.game.cards.remove(card)
        app.game.save_game()
        self._selected_card = None
        app.refresh_breeding_combos()
        self._refresh()

    def _del_card_check(self, card):
        self._delete_card(card)

    def _toggle_favorite(self, card):
        card.favorite = not getattr(card, 'favorite', False)
        App.get_running_app().game.save_game()
        self._show_detail(card)
        self._refresh()

    def _show_equipment(self, card):
        try:
            from screens.equipment import EquipmentScreen
            content = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
            sv = ScrollView(size_hint_y=1)
            inner = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(3))
            inner.bind(minimum_height=inner.setter('height'))
            self._eq_card = card
            self._fill_equipment_ui(inner)
            sv.add_widget(inner)
            content.add_widget(sv)
            close_btn = Button(text='关闭', size_hint_y=None, height=dp(36))
            content.add_widget(close_btn)
            popup = Popup(title=f'{card.name} - 装备', content=content, size_hint=(0.85, 0.8))
            close_btn.bind(on_press=lambda _: (popup.dismiss(), self._show_detail(self._eq_card)))
            popup.open()
        except Exception as e:
            import traceback
            Popup(title='错误', content=Label(text=f'装备页错误:\n{str(e)[:200]}'),
                  size_hint=(0.7, 0.4)).open()

    def _fill_equipment_ui(self, inner):
        card = self._eq_card
        app = App.get_running_app()
        from gene_config import EQUIPMENT_SLOTS, EQUIPMENT_SLOT_NAMES, EQUIPMENT_RARITY, AFFIX_CODE_NAMES
        import os
        inner.add_widget(Label(text='[装备槽]', size_hint_y=None, height=dp(22), bold=True, color=(0.8,0.8,0.8,1)))
        for slot in EQUIPMENT_SLOTS:
            item = card.equipment.get(slot)
            sname = EQUIPMENT_SLOT_NAMES.get(slot, slot)
            if item and isinstance(item, dict):
                name = item.get('name', '?')
                rarity = item.get('rarity', 'common')
                rinfo = next((r for r in EQUIPMENT_RARITY if r['id'] == rarity), {'color':(0.6,1,0.6,1)})
                txt = f'[{sname}] {name}'
                row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(4))
                img_path = os.path.join('assets', 'equipment', f'{slot}_{rarity}.png')
                if os.path.exists(img_path):
                    from kivy.uix.image import Image as KivyImg
                    row.add_widget(KivyImg(source=img_path, size_hint_x=None, width=dp(24)))
                row.add_widget(Label(text=txt, color=rinfo['color'], size_hint_x=0.7))
                row.add_widget(Button(text='卸', size_hint_x=0.15, on_press=lambda _, s=slot: self._do_unequip(s)))
                inner.add_widget(row)
            else:
                inner.add_widget(Label(text=f'[{sname}] 空', color=(0.4,0.4,0.4,1),
                                        size_hint_y=None, height=dp(24)))
        inner.add_widget(Label(text='', size_hint_y=None, height=dp(4)))
        inner.add_widget(Label(text='[库存装备]', size_hint_y=None, height=dp(22), bold=True, color=(0.8,0.8,0.8,1)))
        for inv_id, inv_entry in app.game.equipment_inventory.items():
            if isinstance(inv_entry, int): continue
            if inv_entry.get('count', 0) <= 0: continue
            item = inv_entry.get('data', {})
            slot = item.get('slot', '?')
            rarity = item.get('rarity', 'common')
            rinfo = next((r for r in EQUIPMENT_RARITY if r['id'] == rarity), {'name':'?','color':(0.5,0.5,0.5,1)})
            name = item.get('name', '?')
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(4))
            img_path = os.path.join('assets', 'equipment', f'{slot}_{rarity}.png')
            if os.path.exists(img_path):
                from kivy.uix.image import Image as KivyImg
                row.add_widget(KivyImg(source=img_path, size_hint_x=None, width=dp(24)))
            row.add_widget(Label(text=f'[{rinfo["name"]}] {name}', color=rinfo['color'], size_hint_x=0.55))
            row.add_widget(Button(text='装', size_hint_x=0.12, on_press=lambda _, i=inv_id: self._do_equip(i)))
            detail_btn = Button(text='?', size_hint_x=0.08)
            detail_btn.bind(on_press=lambda _, i=inv_id: self._show_eq_detail(i))
            row.add_widget(detail_btn)
            inner.add_widget(row)

    def _do_equip(self, inv_id):
        card = self._eq_card
        app = App.get_running_app()
        try:
            app.game.equip_item(card, inv_id)
            app.game.save_game()
        except Exception as e:
            import traceback
            Popup(title='错误', content=Label(text=str(e)), size_hint=(0.5,0.25)).open()
            return
        self._refresh_eq_popup()

    def _do_unequip(self, slot):
        card = self._eq_card
        app = App.get_running_app()
        try:
            app.game.unequip_item(card, slot)
            app.game.save_game()
        except Exception as e:
            Popup(title='错误', content=Label(text=str(e)), size_hint=(0.5,0.25)).open()
            return
        self._refresh_eq_popup()

    def _refresh_eq_popup(self):
        if not hasattr(self, '_eq_popup') or not self._eq_popup:
            return
        content = self._eq_popup.content
        children = [c for c in content.children if isinstance(c, ScrollView)]
        if children:
            sv = children[0]
            if sv.children:
                inner = sv.children[0]
                if inner:
                    inner.clear_widgets()
                    self._fill_equipment_ui(inner)

    def _show_eq_detail(self, inv_id):
        app = App.get_running_app()
        inv_entry = app.game.equipment_inventory.get(inv_id)
        if not inv_entry or isinstance(inv_entry, int): return
        item = inv_entry.get('data', {})
        rarity = item.get('rarity', 'common')
        rinfo = next((r for r in EQUIPMENT_RARITY if r['id'] == rarity), {'name':'?','color':(0.5,0.5,0.5,1)})
        lines = [item.get('name', '?')]
        lines.append(f'稀有度: {rinfo["name"]}')
        from gene_config import EQUIPMENT_SLOT_NAMES, AFFIX_CODE_NAMES
        lines.append(f'部位: {EQUIPMENT_SLOT_NAMES.get(item.get("slot",""),"?")}')
        lines.append('--- 词条 ---')
        for aff in item.get('affixes', []):
            code = aff.get('code', '?')
            cname = AFFIX_CODE_NAMES.get(code, code)
            v = aff['value']
            s = '%' if aff.get('is_pct') else ''
            lines.append(f'  {cname}: +{v}{s}')
        Popup(title='装备详情', content=Label(text='\n'.join(lines)), size_hint=(0.6, 0.5)).open()

    def _mutate_card(self, card):
        from kivy.uix.textinput import TextInput
        app = App.get_running_app()
        popup = Popup(title='射线变异', size_hint=(0.6, 0.4))
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text=f'对 {card.name} 进行射线照射？\n这将随机改变基因序列，可能有益也可能有害。'))
        btn_box = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.3)
        confirm = Button(text='确认照射')
        cancel = Button(text='取消')
        btn_box.add_widget(confirm)
        btn_box.add_widget(cancel)
        content.add_widget(btn_box)
        popup.content = content
        confirm.bind(on_press=lambda _: self._do_mutate(card, popup))
        cancel.bind(on_press=popup.dismiss)
        popup.open()

    def _do_mutate(self, card, popup):
        app = App.get_running_app()
        app.game.radiation_mutation(card)
        app.game.save_game()
        popup.dismiss()
        self._show_detail(card)

    def _clone_card(self, card):
        app = App.get_running_app()
        result = app.game.clone_card(card)
        if isinstance(result, str):
            from kivy.uix.popup import Popup
            popup = Popup(title='克隆失败', content=Label(text=result), size_hint=(0.5, 0.3))
            popup.open()
        else:
            app.refresh_breeding_combos()
            self._refresh()

    def _show_report(self, card):
        popup = Popup(title=f'{card.name} - 基因报告', size_hint=(0.8, 0.8))
        sv = ScrollView()
        inner = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2), padding=dp(10))
        inner.bind(minimum_height=inner.setter('height'))
        inner.add_widget(Label(text=f'名称: {card.name}', color=(1, 1, 1, 1), size_hint_y=None, height=dp(25)))
        inner.add_widget(Label(text=f'ID: {card.id}', color=(1, 1, 1, 1), size_hint_y=None, height=dp(25)))
        inner.add_widget(Label(text=f'性别: {"♂ 雄性" if card.gender == "male" else "♀ 雌性"}',
                               size_hint_y=None, height=dp(25), color=(1, 1, 1, 1)))
        inner.add_widget(Label(text=f'亲代: {", ".join(card.parent_ids) if card.parent_ids else "无"}',
                               size_hint_y=None, height=dp(25), color=(0.8, 0.8, 0.8, 1)))
        inner.add_widget(Label(text=f'存活: {"是" if card.is_alive else "否"}',
                               size_hint_y=None, height=dp(25), color=(0.3, 1, 0.3, 1) if card.is_alive else (1, 0.3, 0.3, 1)))
        for chr_id, homologs in card.chromosomes.items():
            inner.add_widget(Label(text=f'--- {chr_id} ---', bold=True, size_hint_y=None, height=dp(25), color=(0, 0.85, 1, 1)))
            for i, h in enumerate(homologs):
                genome = h.get('genome', '')[:60]
                dom = h.get('is_dominant', {})
                inner.add_widget(Label(text=f'  同源{i+1}: {genome}...', size_hint_y=None, height=dp(25),
                                        color=(0.6, 0.6, 0.6, 1)))
        for gname, gdata in card.genes.items():
            a1d = gdata.get('allele1', {}).get('is_dominant', False)
            a2d = gdata.get('allele2', {}).get('is_dominant', False)
            inner.add_widget(Label(text=f'  {gname}: {"显" if a1d else "隐"}/{"显" if a2d else "隐"}',
                                   size_hint_y=None, height=dp(20), color=(0.8, 0.8, 1, 1)))
        close_btn = Button(text='关闭', size_hint_y=None, height=dp(40))
        inner.add_widget(close_btn)
        sv.add_widget(inner)
        popup.content = sv
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _manage_modules(self, card):
        app = App.get_running_app()
        game = app.game
        from gene_config import MODULE_POOLS
        content = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(8))
        slots = 1 if card.star < 3 else (2 if card.star < 5 else 3)
        content.add_widget(Label(text=f'{card.name} 模组 ({len(card.modules)}/{slots})',
                                  size_hint_y=None, height=dp(24), color=(0.8, 0.8, 0.8, 1)))
        for mid, count in game.module_inventory.items():
            if count <= 0: continue
            md = MODULE_POOLS.get(mid, {})
            if not md: continue
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(4))
            row.add_widget(Label(text=f'{md["name"]} x{count}', size_hint_x=0.5, color=(1,1,1,1)))
            row.add_widget(Button(text='装备', size_hint_x=0.25,
                                  on_press=lambda _, m=mid: self._do_mod_eq(card, m)))
            if md['level'] < 3:
                row.add_widget(Button(text='合成', size_hint_x=0.25,
                                      on_press=lambda _, m=mid: self._do_mod_merge(m)))
            content.add_widget(row)
        for mid in list(card.modules):
            md = MODULE_POOLS.get(mid, {})
            if md:
                content.add_widget(Button(text=f'卸下 {md["name"]}',
                                          on_press=lambda _, m=mid: self._do_mod_rm(card, m)))
        close_btn = Button(text='关闭', size_hint_y=None, height=dp(36))
        content.add_widget(close_btn)
        popup = Popup(title='模组管理', content=content, size_hint=(0.7, 0.7))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _do_mod_eq(self, card, mid):
        App.get_running_app().game.equip_module(card, mid)
        App.get_running_app().game.save_game()
        self._show_detail(card)

    def _do_mod_rm(self, card, mid):
        App.get_running_app().game.remove_module(card, mid)
        App.get_running_app().game.save_game()
        self._show_detail(card)

    def _do_mod_merge(self, mid):
        App.get_running_app().game.merge_modules(mid)
        App.get_running_app().game.save_game()

    def _manage_chips(self, card):
        app = App.get_running_app()
        game = app.game
        from gene_config import CHIP_POOLS
        content = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(8))
        content.add_widget(Label(text=f'{card.name} 芯片 ({len(card.chips)}/{card.chip_slots})',
                                  size_hint_y=None, height=dp(24), color=(0.8,0.8,0.8,1)))
        for cid, count in game.chip_inventory.items():
            if count <= 0: continue
            cp = CHIP_POOLS.get(cid, {})
            if not cp: continue
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(32), spacing=dp(4))
            row.add_widget(Label(text=f'{cp["name"]}({cp["skill"]}) x{count}',
                                 size_hint_x=0.7, color=(0.6,1,0.6,1)))
            row.add_widget(Button(text='装备', size_hint_x=0.3,
                                  on_press=lambda _, c=cid: self._do_chip_eq(card, c)))
            content.add_widget(row)
        for i, ci in enumerate(list(card.chips)):
            content.add_widget(Button(text=f'移除 {ci.get("skill_name","?")}',
                                      on_press=lambda _, idx=i: self._do_chip_rm(card, idx)))
        close_btn = Button(text='关闭', size_hint_y=None, height=dp(36))
        content.add_widget(close_btn)
        popup = Popup(title='芯片管理', content=content, size_hint=(0.7, 0.6))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _do_chip_eq(self, card, cid):
        App.get_running_app().game.equip_chip(card, cid)
        App.get_running_app().game.save_game()
        self._show_detail(card)

    def _do_chip_rm(self, card, idx):
        App.get_running_app().game.remove_chip(card, idx)
        App.get_running_app().game.save_game()
        self._show_detail(card)
