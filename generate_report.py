import json
import sys
sys.path.insert(0, '.')
from gene_config import GENE_TEMPLATES, CHROMOSOME_LAYOUT, GENE_REGIONS, SKILL_TRAITS
from gene_enhance_config import STAT_ENHANCE_REGIONS, STAT_TRAITS

def wrap_text(text, width=50):
    return '\n'.join(text[i:i+width] for i in range(0, len(text), width))

def generate_report(card_data):
    lines = []
    cid = card_data.get('id', '?')
    name = card_data.get('name', '?')
    gender = card_data.get('gender', '?')
    gender_symbol = '♂' if gender == 'male' else '♀'
    alive = card_data.get('is_alive', True)
    skills = card_data.get('skills', [])
    traits = card_data.get('traits', {})
    chromosomes = card_data.get('chromosomes', {})

    lines.append(f"卡牌ID: {cid}")
    lines.append(f"名称: {name}")
    lines.append(f"性别: {gender_symbol}{'雄性' if gender == 'male' else '雌性'}")
    lines.append(f"存活: {'是' if alive else '否'}")
    lines.append(f"技能: {', '.join(skills) if skills else '无'}")
    lines.append('')

    lines.append('=== 性状 ===')
    for k, v in traits.items():
        lines.append(f"  {k}: {v}")
    lines.append('')

    total_bp = sum(
        len(h.get('genome', ''))
        for chrid in ['chr1','chr2','chr3','chrX']
        for h in chromosomes.get(chrid, [])
    )
    lines.append(f'=== 基因组序列（正链，每条同源体一条连续序列，共{total_bp}bp）===')
    lines.append('')

    for chrid in ['chr1','chr2','chr3','chrX']:
        homs = chromosomes.get(chrid, [])
        if not homs:
            continue
        chr_len = len(homs[0].get('genome', ''))
        lines.append(f'--- {chrid} ({chr_len}bp) ---')
        for i, h in enumerate(homs):
            genome = h.get('genome', '')
            lines.append(f'  同源体{i+1}:')
            if genome:
                lines.append('    ' + wrap_text(genome, 50).replace('\n', '\n    '))
        lines.append('')

    lines.append('=== 基因区域（坐标 + 序列精简）===')
    lines.append('')
    for chrid in ['chr1','chr2','chr3','chrX']:
        homs = chromosomes.get(chrid, [])
        regions = GENE_REGIONS.get(chrid, [])
        if not homs or not regions:
            continue
        lines.append(f'--- {chrid} ---')
        for i, (gene_name, start, end) in enumerate(regions):
            tmpl = GENE_TEMPLATES.get(gene_name, {})
            seq_len = end - start
            seqs = []
            for h in homs:
                g = h.get('genome', '')
                if start < len(g):
                    seg = g[start:end]
                    if len(seg) > 30:
                        seg = seg[:30] + '...'
                    seqs.append(seg)
                else:
                    seqs.append('（超出范围）')
            if len(seqs) == 1:
                seqs.append('...')
            seq_display = ' / '.join(seqs)
            lines.append(f'  {gene_name} ({start}-{end}, {seq_len}bp): {seq_display}')
        lines.append('')

    lines.append('=== 基因组增强区域 ===')
    lines.append('')
    for trait_name in STAT_TRAITS:
        regions = STAT_ENHANCE_REGIONS.get(trait_name, [])
        if not regions:
            continue
        trait_val = traits.get(trait_name, '?')
        lines.append(f'--- {trait_name} (当前值: {trait_val}) ---')
        for i, reg in enumerate(regions):
            chrid = reg['chr']
            start = reg['start']
            end = reg['end']
            add_str = ', '.join(f'{b}:{v:+d}' for b, v in sorted(reg.get('add', {}).items())) if reg.get('add') else '无'
            mul_str = ', '.join(f'{b}:{v}' for b, v in reg.get('mul', {}).items()) if reg.get('mul') else '无'
            seqs = []
            homs = chromosomes.get(chrid, [])
            for h in homs:
                g = h.get('genome', '')
                if start < len(g):
                    seg = g[start:end]
                    seqs.append(seg[:20] + '...' if len(seg) > 20 else seg)
                else:
                    seqs.append('（超）')
            seq_display = ' / '.join(seqs)
            lines.append(f'  区域{i+1}: {chrid}({start}-{end}, {end-start}bp)')
            lines.append(f'    加算: {{{add_str}}}  乘算: {{{mul_str}}}')
            lines.append(f'    序列: {seq_display}')
        lines.append('')
    return '\n'.join(lines)

def main():
    with open('gene_game_save.json', 'r', encoding='utf-8') as f:
        save = json.load(f)
    cards = save.get('cards', [])
    report_parts = []
    for i, card in enumerate(cards):
        r = generate_report(card)
        report_parts.append(r)
        if i > 0:
            separator = '\n' + '='*70 + '\n'
            report_parts = [report_parts[0]] + [separator + r for r in report_parts[1:]]
    full_report = report_parts[0] if len(report_parts) == 1 else report_parts[0] + ''.join(report_parts[1:])
    with open('个体基因报告.txt', 'w', encoding='utf-8') as f:
        f.write(full_report)
    print(f"报告已生成: {len(cards)} 张卡牌, {len(full_report)} 字符")

if __name__ == '__main__':
    main()
