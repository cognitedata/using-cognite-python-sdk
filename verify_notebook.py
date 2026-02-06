import json

with open('notebooks/Get_Cognite_Groups.ipynb', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Total cells: {len(data["cells"])}\n')
for i in range(8, len(data['cells'])):
    cell = data['cells'][i]
    cell_type = cell.get('cell_type', 'unknown')
    source = ''.join(cell['source'])
    preview = source[:70].replace('\n', ' ')
    print(f'Cell {i} ({cell_type}): {preview}...')

