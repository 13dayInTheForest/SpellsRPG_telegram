tempo_stats = {None: 'hi', 'hp': [{'expired': 231}, {'expired': 34}]}

tempo_stats.get('asd')
enemy_hp_effects = sorted(tempo_stats.get('hp', [{'expired': 2}, {'expired': 1}]), key=lambda x: x['expired'])

print(tempo_stats[None])