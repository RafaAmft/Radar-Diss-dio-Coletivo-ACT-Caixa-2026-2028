import pandas as pd
import re
import openpyxl

# Load data
df1 = pd.read_excel('dissidios_coletivos_estatais_2016_2026.xlsx', sheet_name='Estatal Suscitante')
df2 = pd.read_excel('dissidios_coletivos_estatais_2016_2026.xlsx', sheet_name='Estatal Suscitada')

def get_year(cnj):
    m = re.search(r'\.(\d{4})\.5\.', str(cnj))
    return int(m.group(1)) if m else 0

df1['ano_proc'] = df1['número CNJ'].apply(get_year)
df2['ano_proc'] = df2['número CNJ'].apply(get_year)

# Filter 2016 to 2026
df1 = df1[(df1['ano_proc'] >= 2016) & (df1['ano_proc'] <= 2026)].copy()
df2 = df2[(df2['ano_proc'] >= 2016) & (df2['ano_proc'] <= 2026)].copy()

UNION_WORDS = ['sindicato', 'federacao', 'federação', 'confederacao', 'confederação', 'associacao', 'associação', 'fenadsef', 'fentect', 'fup', 'fnte', 'sindipetro', 'sintect']

# Move any row from df1 where Suscitante is clearly a union to df2
rows_to_move_to_tab2 = []
rows_tab1_clean = []

for idx, r in df1.iterrows():
    susc = str(r['suscitante']).strip()
    suscd = str(r['suscitado(s)']).strip()
    
    # Check if suscitante is a union
    is_union_susc = any(w in susc.lower() for w in UNION_WORDS)
    
    # Check if suscitante is corrupted/long text
    if len(susc) > 120 or 'cláusula' in susc.lower() or 'clausula' in susc.lower() or 'também se mostra' in susc.lower() or 'conhece-se' in susc.lower():
        # Clean up
        if 'emgerpi' in susc.lower() or 'emgerpi' in suscd.lower():
            susc = "Empresa de Gestão de Recursos do Estado do Piauí - EMGERPI"
            is_union_susc = False
        elif 'cepar' in susc.lower() or 'celepar' in susc.lower():
            susc = "Companhia de Tecnologia da Informação e Comunicação do Paraná - CELEPAR"
            is_union_susc = False
        else:
            is_union_susc = True # Treat as union appeal
    
    if is_union_susc or susc == 'Entidade Sindical Profissional':
        # Swap or move to Tab 2
        r_copy = r.to_dict()
        rows_to_move_to_tab2.append(r_copy)
    else:
        r_dict = r.to_dict()
        # Clean known name representations
        if 'correios' in susc.lower() or 'ect' in susc.lower():
            r_dict['suscitante'] = 'Empresa Brasileira de Correios e Telégrafos (ECT)'
        elif 'petrobras' in susc.lower() and 'transpetro' in susc.lower():
            r_dict['suscitante'] = 'Petrobras Transporte S.A. - TRANSPETRO'
        elif 'petrobras' in susc.lower():
            r_dict['suscitante'] = 'Petróleo Brasileiro S.A. - PETROBRAS'
        elif 'eletrobras' in susc.lower() or 'centrais eletricas brasileiras' in susc.lower():
            r_dict['suscitante'] = 'Centrais Elétricas Brasileiras S.A. - ELETROBRAS'
        elif 'furnas' in susc.lower():
            r_dict['suscitante'] = 'Furnas Centrais Elétricas S.A.'
        elif 'ebserh' in susc.lower() or 'hospitalares' in susc.lower():
            r_dict['suscitante'] = 'Empresa Brasileira de Serviços Hospitalares (EBSERH)'
        elif 'cptm' in susc.lower():
            r_dict['suscitante'] = 'Companhia Paulista de Trens Metropolitanos (CPTM)'
        elif 'cbtu' in susc.lower():
            r_dict['suscitante'] = 'Companhia Brasileira de Trens Urbanos (CBTU)'
        elif 'serpro' in susc.lower():
            r_dict['suscitante'] = 'Serviço Federal de Processamento de Dados (SERPRO)'
        elif 'dataprev' in susc.lower():
            r_dict['suscitante'] = 'Empresa de Tecnologia e Informações da Previdência (DATAPREV)'
        elif 'metrô' in susc.lower() and ('distrito federal' in susc.lower() or 'df' in susc.lower()):
            r_dict['suscitante'] = 'Companhia do Metropolitano do Distrito Federal (Metrô DF)'
        elif 'metrô' in susc.lower() and 'são paulo' in susc.lower():
            r_dict['suscitante'] = 'Companhia do Metropolitano de São Paulo (Metrô SP)'
        elif 'imbel' in susc.lower():
            r_dict['suscitante'] = 'Indústria de Material Bélico do Brasil (IMBEL)'
        elif 'ebc' in susc.lower() or 'brasil de comunicacao' in susc.lower():
            r_dict['suscitante'] = 'Empresa Brasil de Comunicação S.A. (EBC)'
        elif 'casa da moeda' in susc.lower() or 'cmb' in susc.lower():
            r_dict['suscitante'] = 'Casa da Moeda do Brasil (CMB)'
        elif 'telebras' in susc.lower():
            r_dict['suscitante'] = 'Telecomunicações Brasileiras S.A. (TELEBRAS)'
        elif 'valec' in susc.lower() or 'infra s.a.' in susc.lower():
            r_dict['suscitante'] = 'Infra S.A. / VALEC'
        
        # Clean suscitado
        if not r_dict['suscitado(s)'] or r_dict['suscitado(s)'] == 'Entidades Sindicais' or len(str(r_dict['suscitado(s)'])) < 5:
            r_dict['suscitado(s)'] = 'Entidades Sindicais Representativas da Categoria Profissional'
        elif len(str(r_dict['suscitado(s)'])) > 250:
            r_dict['suscitado(s)'] = str(r_dict['suscitado(s)'])[:240] + '...'
            
        rows_tab1_clean.append(r_dict)

# Add moved rows to Tab 2
rows_tab2_clean = []
for idx, r in df2.iterrows():
    rows_tab2_clean.append(r.to_dict())

for r in rows_to_move_to_tab2:
    rows_tab2_clean.append(r)

# Clean Tab 2
cleaned_tab2 = []
for r in rows_tab2_clean:
    susc = str(r.get('suscitante', '')).strip()
    suscd = str(r.get('suscitado(s)', '')).strip()
    if len(susc) > 250:
        susc = susc[:240] + '...'
    if len(suscd) > 250:
        suscd = suscd[:240] + '...'
    r['suscitante'] = susc
    r['suscitado(s)'] = suscd
    cleaned_tab2.append(r)

# Deduplicate both tabs by CNJ
def dedup(rows):
    unique = {}
    for r in rows:
        c = r['número CNJ']
        if c not in unique:
            unique[c] = r
    return list(unique.values())

final_tab1 = dedup(rows_tab1_clean)
final_tab2 = dedup(cleaned_tab2)

df_final_tab1 = pd.DataFrame(final_tab1)
df_final_tab2 = pd.DataFrame(final_tab2)

cols = [
    'número CNJ', 'tribunal', 'classe', 'data de ajuizamento',
    'suscitante', 'suscitado(s)', 'tipo (greve, econômico, jurídico, revisional)',
    'relator', 'situação/resultado (acordo, sentença normativa, extinto, pendente)',
    'ano de vigência do ACT/DC', 'fonte (URL)',
    'nível de confiança (confirmado em fonte primária / só notícia / não verificado)'
]

df_final_tab1_export = df_final_tab1[cols].copy()
df_final_tab2_export = df_final_tab2[cols].copy()

# Sort by CNJ / Year
df_final_tab1_export['ano_temp'] = df_final_tab1_export['número CNJ'].apply(get_year)
df_final_tab1_export = df_final_tab1_export.sort_values(by=['ano_temp', 'número CNJ'], ascending=[False, True]).drop(columns=['ano_temp'])

df_final_tab2_export['ano_temp'] = df_final_tab2_export['número CNJ'].apply(get_year)
df_final_tab2_export = df_final_tab2_export.sort_values(by=['ano_temp', 'número CNJ'], ascending=[False, True]).drop(columns=['ano_temp'])

# Sanitize
def sanitize(val):
    if not isinstance(val, str): return val
    val = ''.join(ch for ch in val if ord(ch) >= 32 or ch in '\n\r\t')
    return re.sub(r'\s+', ' ', val).strip()

for c in cols:
    df_final_tab1_export[c] = df_final_tab1_export[c].apply(sanitize)
    df_final_tab2_export[c] = df_final_tab2_export[c].apply(sanitize)

# Export Excel
excel_paths = [
    'scraping_dissidio_coletivo_greve/dissidios_coletivos_estatais_2016_2026.xlsx',
    'dissidios_coletivos_estatais_2016_2026.xlsx'
]
for ep in excel_paths:
    with pd.ExcelWriter(ep, engine='openpyxl') as writer:
        df_final_tab1_export.to_excel(writer, sheet_name='Estatal Suscitante', index=False)
        df_final_tab2_export.to_excel(writer, sheet_name='Estatal Suscitada', index=False)

# Export CSVs
df_final_tab1_export.to_csv('scraping_dissidio_coletivo_greve/dissidios_estatais_suscitantes.csv', index=False, encoding='utf-8-sig', sep=';')
df_final_tab2_export.to_csv('scraping_dissidio_coletivo_greve/dissidios_estatais_suscitadas.csv', index=False, encoding='utf-8-sig', sep=';')
df_final_tab1_export.to_csv('dissidios_estatais_suscitantes.csv', index=False, encoding='utf-8-sig', sep=';')
df_final_tab2_export.to_csv('dissidios_estatais_suscitadas.csv', index=False, encoding='utf-8-sig', sep=';')

print(f"CONSOLIDAÇÃO FINALIZADA COM SUCESSO!")
print(f"Tab 1 (Estatal como Suscitante): {len(df_final_tab1_export)} processos únicos verificados")
print(f"Tab 2 (Estatal como Suscitada):  {len(df_final_tab2_export)} processos únicos verificados")

print("\n--- DISTRIBUIÇÃO TAB 1 (ESTATAL COMO SUSCITANTE) POR ENTIDADE ---")
print(df_final_tab1_export['suscitante'].value_counts().to_string())

df_final_tab1_export['ano_filing'] = df_final_tab1_export['número CNJ'].apply(get_year)
print("\n--- DISTRIBUIÇÃO TAB 1 POR ANO DE AJUIZAMENTO ---")
print(df_final_tab1_export['ano_filing'].value_counts().sort_index().to_string())

print("\n--- DISTRIBUIÇÃO TAB 1 POR TRIBUNAL ---")
print(df_final_tab1_export['tribunal'].value_counts().to_string())

print("\n--- DISTRIBUIÇÃO TAB 1 POR TIPO ---")
print(df_final_tab1_export['tipo (greve, econômico, jurídico, revisional)'].value_counts().to_string())

print("\n--- DISTRIBUIÇÃO TAB 1 POR SITUAÇÃO/RESULTADO ---")
print(df_final_tab1_export['situação/resultado (acordo, sentença normativa, extinto, pendente)'].value_counts().to_string())
