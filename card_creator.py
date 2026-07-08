import tkinter as tk
from tkinter import ttk, messagebox
import sys, os, random, copy
sys.path.insert(0, '.')
from gene_game import Card, Game, GENE_TEMPLATES, GENE_REGIONS, CHROMOSOME_LENGTH, CHROMOSOME_LAYOUT, BASES
from gene_enhance_config import STAT_ENHANCE_REGIONS

BG = "#1a1a2e"
FG = "#ffffff"
ACCENT = "#00d9ff"
FRAME_BG = "#16213e"

SKILL_ENTRIES = []
for gname, tmpl in sorted(GENE_TEMPLATES.items()):
    if tmpl.get('category') == 'skill':
        chrom = next((c for c, gl in GENE_REGIONS.items() if any(g == gname for g, _, _ in gl)), '?')
        SKILL_ENTRIES.append({
            'gene': gname, 'name': tmpl.get('skill_name', gname),
            'desc': tmpl.get('description', ''), 'chromosome': chrom,
        })

PASSIVE_ENTRIES = []
for gname, tmpl in sorted(GENE_TEMPLATES.items()):
    if tmpl.get('category') == 'passive':
        chrom = next((c for c, gl in GENE_REGIONS.items() if any(g == gname for g, _, _ in gl)), '?')
        PASSIVE_ENTRIES.append({
            'gene': gname, 'name': tmpl.get('passive_name', gname),
            'desc': tmpl.get('description', ''), 'chromosome': chrom,
        })

ENHANCED_TRAITS = ['health', 'stamina', 'defense', 'dodge_rate', 'attack', 'speed', 'critical_rate']

TRAIT_LABELS = {
    'health': '生命(HP)', 'stamina': '耐力', 'defense': '防御(DEF)',
    'dodge_rate': '闪避', 'attack': '攻击(ATK)', 'speed': '速度(SPD)',
    'critical_rate': '暴击率',
}


def neutral_base_for_region(region):
    forbidden = set(region.get('add', {}).keys()) | set(region.get('mul', {}).keys())
    for b in 'ATGC':
        if b not in forbidden:
            return b
    return 'G'


def fill_region(region, length, add_pct, mul_pct):
    nb = neutral_base_for_region(region)
    add = region.get('add', {})
    mul = region.get('mul', {})

    has_add, has_mul = bool(add), bool(mul)
    if has_add and not has_mul:
        pct = add_pct
    elif has_mul and not has_add:
        pct = mul_pct
    else:
        pct = (add_pct + mul_pct) / 2.0

    if pct == 50:
        return nb * length

    beneficial, detrimental = None, None
    if add:
        beneficial = max(add, key=add.get)
        detrimental = min(add, key=add.get)
    if mul:
        best_mul, worst_mul = None, None
        for b, f in mul.items():
            if f > 1.0 and (best_mul is None or f > mul[best_mul]):
                best_mul = b
            if f < 1.0 and (worst_mul is None or f < mul[worst_mul]):
                worst_mul = b
        if best_mul:
            beneficial = best_mul
        if worst_mul:
            detrimental = worst_mul

    if pct > 50:
        base = beneficial or nb
        ratio = (pct - 50) * 2 / 100.0
    else:
        base = detrimental or nb
        ratio = (50 - pct) * 2 / 100.0

    n = max(0, min(length, int(length * ratio)))
    return base * n + nb * (length - n)


def gene_strategy(gname, h_idx, active_skills, active_passives):
    tmpl = GENE_TEMPLATES.get(gname, {})
    dom_seq = tmpl.get('sequence', '')
    rec_seq = tmpl.get('recessive_sequence', '')
    cat = tmpl.get('category', '')
    if cat == 'vital':
        return (dom_seq, True)
    if cat == 'passive':
        if gname in active_passives:
            return (dom_seq, True)
        return (rec_seq, False)
    if cat in ('special', 'recessive'):
        return (dom_seq, True)
    if cat == 'skill':
        if gname in active_skills:
            return (dom_seq, True)
        return (dom_seq, True) if h_idx == 0 else (rec_seq, False)
    return (dom_seq, True)


def build_chromosomes(active_skills, active_passives, trait_pcts):
    chromosomes = {}
    for chr_id in ['chr1', 'chr2', 'chr3', 'chrX']:
        regions = GENE_REGIONS.get(chr_id if chr_id != 'chrX' else 'chrX', [])
        target = CHROMOSOME_LENGTH.get(chr_id, 1000)

        for h_idx in (0, 1):
            parts, dom_map = [], []
            for gname, gs, ge in regions:
                tmpl = GENE_TEMPLATES.get(gname, {})
                seqlen = ge - gs
                s, dom = gene_strategy(gname, h_idx, active_skills, active_passives)
                s = (s or 'A'*seqlen)[:seqlen].ljust(seqlen, 'A')
                parts.append(s)
                dom_map.append({'gene': gname, 'is_dominant': dom})

            gene_region = ''.join(parts)
            pad_start = len(gene_region)
            pad_len = target - pad_start
            if pad_len <= 0:
                genome = gene_region
            else:
                padding = ['N'] * pad_len
                for tname, enh_regions in STAT_ENHANCE_REGIONS.items():
                    tp = trait_pcts.get(tname, {'add': 50, 'mul': 50})
                    for reg in enh_regions:
                        if reg['chr'] != chr_id:
                            continue
                        lo = max(reg['start'], pad_start)
                        hi = min(reg['end'], target)
                        if lo >= hi:
                            continue
                        length = hi - lo
                        bases = fill_region(reg, length, tp['add'], tp['mul'])
                        pad_lo = lo - pad_start
                        for i in range(length):
                            if pad_lo + i < pad_len:
                                padding[pad_lo + i] = bases[i % len(bases)]
                for tname, enh_regions in STAT_ENHANCE_REGIONS.items():
                    for reg in enh_regions:
                        if reg['chr'] != chr_id:
                            continue
                        lo = max(reg['start'], pad_start)
                        hi = min(reg['end'], target)
                        if lo >= hi:
                            continue
                        nb = neutral_base_for_region(reg)
                        pad_lo = lo - pad_start
                        for i in range(hi - lo):
                            if pad_lo + i < pad_len and padding[pad_lo + i] == 'N':
                                padding[pad_lo + i] = nb
                for i in range(pad_len):
                    if padding[i] == 'N':
                        padding[i] = 'A'
                genome = gene_region + ''.join(padding)

            if chr_id == 'chrX':
                chromosomes.setdefault('chrX', [])
                chromosomes['chrX'].append({'type': 'X', 'genome': genome, 'is_dominant': {d['gene']: d['is_dominant'] for d in dom_map}})
            else:
                chromosomes.setdefault(chr_id, [])
                chromosomes[chr_id].append({'genome': genome, 'is_dominant': {d['gene']: d['is_dominant'] for d in dom_map}})
    return chromosomes


class CardCreatorGUI:
    def __init__(self):
        self.game = Game(load_save=True)
        self.root = tk.Tk()
        self.root.title("基因卡牌创建器")
        self.root.geometry("880x950")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background=BG, foreground=FG, font=('微软雅黑', 10))
        style.configure('TFrame', background=BG)
        style.configure('TLabelframe', background=BG, foreground=ACCENT, font=('微软雅黑', 10, 'bold'))
        style.configure('TLabelframe.Label', background=BG, foreground=ACCENT, font=('微软雅黑', 10, 'bold'))
        style.configure('TButton', font=('微软雅黑', 10), background='#0f3460', foreground=FG)
        style.configure('TCheckbutton', background=BG, foreground=FG, font=('微软雅黑', 9))
        self._build_ui()

    def _build_ui(self):
        # Outer canvas for full scrollability
        outer_canvas = tk.Canvas(self.root, bg=BG, highlightthickness=0)
        outer_sb = ttk.Scrollbar(self.root, orient='vertical', command=outer_canvas.yview)
        outer_canvas.configure(yscrollcommand=outer_sb.set)
        outer_canvas.pack(side='left', fill='both', expand=True)
        outer_sb.pack(side='right', fill='y')

        main = ttk.Frame(outer_canvas)
        main.bind('<Configure>', lambda e: outer_canvas.configure(scrollregion=outer_canvas.bbox('all')))
        outer_canvas.create_window((0, 0), window=main, anchor='nw')
        outer_canvas.bind_all('<MouseWheel>', lambda e: outer_canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))

        # Title
        title = ttk.Label(main, text="基因卡牌创建器", font=('微软雅黑', 16, 'bold'), foreground=ACCENT)
        title.pack(pady=(15, 10))

        # ── Name & Gender ──
        nf = ttk.Frame(main)
        nf.pack(fill='x', pady=5, padx=20)
        ttk.Label(nf, text="卡牌名称:").pack(side='left')
        self.name_var = tk.StringVar(value="新个体")
        ttk.Entry(nf, textvariable=self.name_var, font=('微软雅黑', 10), width=30).pack(side='left', padx=10)
        ttk.Label(nf, text="性别:").pack(side='left', padx=(20, 0))
        self.gender_var = tk.StringVar(value="female")
        ttk.Radiobutton(nf, text="雌性", variable=self.gender_var, value="female").pack(side='left', padx=5)
        ttk.Radiobutton(nf, text="雄性", variable=self.gender_var, value="male").pack(side='left', padx=5)

        # ── Skills ──
        skill_box = ttk.LabelFrame(main, text="技能选择", padding=10)
        skill_box.pack(fill='x', pady=8, padx=20)
        self.skill_vars = {}
        skill_canvas = tk.Canvas(skill_box, bg=FRAME_BG, highlightthickness=0, height=160)
        skill_sb = ttk.Scrollbar(skill_box, orient='vertical', command=skill_canvas.yview)
        skill_frame = ttk.Frame(skill_canvas)
        skill_frame.bind('<Configure>', lambda e: skill_canvas.configure(scrollregion=skill_canvas.bbox('all')))
        skill_canvas.create_window((0, 0), window=skill_frame, anchor='nw')
        skill_canvas.configure(yscrollcommand=skill_sb.set)

        for idx, ent in enumerate(SKILL_ENTRIES):
            var = tk.BooleanVar(value=False)
            self.skill_vars[ent['gene']] = var
            r, c = idx // 3, idx % 3
            ttk.Checkbutton(skill_frame, text=f"{ent['name']} ({ent['chromosome']})", variable=var).grid(row=r, column=c, sticky='w', padx=5, pady=2)
        skill_canvas.pack(side='left', fill='both', expand=True)
        skill_sb.pack(side='right', fill='y')

        # ── Passive Skills ──
        passive_box = ttk.LabelFrame(main, text="被动技能选择（勾选激活）", padding=10)
        passive_box.pack(fill='x', pady=8, padx=20)
        self.passive_vars = {}
        if PASSIVE_ENTRIES:
            for ent in PASSIVE_ENTRIES:
                var = tk.BooleanVar(value=False)
                self.passive_vars[ent['gene']] = var
                cb = ttk.Checkbutton(passive_box, text=f"{ent['name']} ({ent['chromosome']})", variable=var)
                cb.pack(anchor='w', padx=5, pady=2)
        else:
            ttk.Label(passive_box, text="无可用被动技能", foreground='#888888').pack(anchor='w', padx=5)

        # ── Per-Stat Sliders ──
        sl_box = ttk.LabelFrame(main, text="数值属性 (0% = 最弱, 50% = 中性, 100% = 最强)", padding=15)
        sl_box.pack(fill='x', pady=8, padx=20)

        self.trait_vars = {}
        for tname in ENHANCED_TRAITS:
            label = TRAIT_LABELS.get(tname, tname)
            row_f = ttk.Frame(sl_box)
            row_f.pack(fill='x', pady=4)

            ttk.Label(row_f, text=label, width=12, anchor='w').pack(side='left')

            add_var = tk.DoubleVar(value=50.0)
            mul_var = tk.DoubleVar(value=50.0)
            self.trait_vars[tname] = {'add': add_var, 'mul': mul_var}

            ttk.Label(row_f, text="加算", font=('微软雅黑', 8)).pack(side='left', padx=(5, 0))
            add_lbl = ttk.Label(row_f, text="50%", width=4, font=('Consolas', 8))
            add_lbl.pack(side='left')
            tk.Scale(row_f, from_=0, to=100, orient='horizontal', variable=add_var, length=160,
                     bg=FRAME_BG, fg=FG, troughcolor='#0f3460', highlightbackground=BG, font=('Consolas', 7),
                     command=lambda v, l=add_lbl: l.configure(text=f"{int(float(v))}%")).pack(side='left', padx=3)

            ttk.Label(row_f, text="乘算", font=('微软雅黑', 8)).pack(side='left', padx=(10, 0))
            mul_lbl = ttk.Label(row_f, text="50%", width=4, font=('Consolas', 8))
            mul_lbl.pack(side='left')
            tk.Scale(row_f, from_=0, to=100, orient='horizontal', variable=mul_var, length=160,
                     bg=FRAME_BG, fg=FG, troughcolor='#0f3460', highlightbackground=BG, font=('Consolas', 7),
                     command=lambda v, l=mul_lbl: l.configure(text=f"{int(float(v))}%")).pack(side='left', padx=3)

        ttk.Label(sl_box, text="← 0% = 最弱   50% = 中性   100% = 最强 →",
                  font=('微软雅黑', 8), foreground='#888888').pack(pady=(5, 0))

        # ── Preview ──
        pb = ttk.LabelFrame(main, text="数值预览", padding=10)
        pb.pack(fill='x', pady=8, padx=20)
        self.preview_text = tk.Text(pb, height=8, width=80, bg=FRAME_BG, fg=FG, font=('Consolas', 9), highlightbackground='#0f3460')
        self.preview_text.pack(fill='x')
        self.preview_text.insert('1.0', "调整参数后点击下方按钮预览或创建")

        # ── Buttons ──
        bf = ttk.Frame(main)
        bf.pack(pady=15)
        ttk.Button(bf, text="预览数值", command=self.preview_card).pack(side='left', padx=8)
        tk.Button(bf, text="确定创建", command=self.create_card,
                  bg='#00d9ff', fg='#1a1a2e', font=('微软雅黑', 12, 'bold'), padx=30, pady=6, cursor='hand2').pack(side='left', padx=8)
        ttk.Button(bf, text="关闭", command=self.root.destroy).pack(side='left', padx=8)

    def _active_skills(self):
        return {g for g, v in self.skill_vars.items() if v.get()}

    def _active_passives(self):
        return {g for g, v in self.passive_vars.items() if v.get()}

    def _trait_pcts(self):
        return {
            tname: {
                'add': self.trait_vars[tname]['add'].get(),
                'mul': self.trait_vars[tname]['mul'].get(),
            }
            for tname in ENHANCED_TRAITS
        }

    def _temp_card(self):
        name = self.name_var.get() or "未命名"
        act = self._active_skills()
        ap = self._active_passives()
        return Card(name, chromosomes=build_chromosomes(act, ap, self._trait_pcts()))

    def preview_card(self):
        card = self._temp_card()
        self.preview_text.delete('1.0', 'end')
        if not card.is_alive:
            self.preview_text.insert('1.0', "卡牌死亡(关键基因缺失)")
            return
        lines = [f"名称: {card.name}  |  {'雄性' if card.gender == 'male' else '雌性'}  |  存活: {card.is_alive}",
                 f"技能: {', '.join(card.skills) if card.skills else '无'}",
                 f"被动: {', '.join(f'{k}({v}%反伤)' if isinstance(v, int) else f'{k}激活' for k, v in card.passive_skills.items()) if card.passive_skills else '无'}",
                 f"{'─'*60}"]
        for k in ENHANCED_TRAITS:
            lines.append(f"  {TRAIT_LABELS.get(k, k)}: {card.traits.get(k, 0)}")
        lines.append(f"{'─'*60}")
        for k, v in sorted(card.traits.items()):
            if k not in ENHANCED_TRAITS:
                lines.append(f"  {k}: {v}")
        self.preview_text.insert('1.0', '\n'.join(lines))

    def create_card(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("警告", "请输入卡牌名称")
            return
        card = self._temp_card()
        if not card.is_alive:
            messagebox.showerror("错误", "卡牌死亡，请调整参数")
            return
        tp = self._trait_pcts()
        summary_lines = [
            f"名称: {card.name}  {'雄性' if card.gender == 'male' else '雌性'}",
            f"技能({len(card.skills)}个): {', '.join(card.skills) if card.skills else '无'}",
            f"{'─'*40}",
        ]
        for k in ENHANCED_TRAITS:
            v = card.traits.get(k, 0)
            a = tp[k]['add']
            m = tp[k]['mul']
            summary_lines.append(f"  {TRAIT_LABELS.get(k, k)}: {v}  (加算{a:.0f}% 乘算{m:.0f}%)")
        summary_lines.append(f"{'─'*40}")
        ok = messagebox.askyesno("确认创建", '\n'.join(summary_lines) + "\n确认创建？")
        if not ok:
            return
        card.id = f"CARD{Card.card_count:04d}"
        self.game.cards.append(card)
        self.game.save_game()
        messagebox.showinfo("创建成功",
            f"卡牌 {card.id}「{card.name}」已创建！\n"
            f"技能: {', '.join(card.skills) if card.skills else '无'}\n"
            f"速度:{card.traits.get('speed',0)} 攻击:{card.traits.get('attack',0)} "
            f"生命:{card.traits.get('health',0)} 防御:{card.traits.get('defense',0)}")
        self.preview_card()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    CardCreatorGUI().run()
