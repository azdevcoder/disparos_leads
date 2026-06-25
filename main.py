import csv
import webbrowser
import time
import pyautogui
import urllib.parse

# 1. Caminho do seu arquivo CSV
file_path = "dataset_google-maps-extractor_2026-06-22_12-59-41.csv"

def carregar_dados_seguro(caminho):
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(caminho, 'r', encoding=encoding) as f:
                primeira_linha = f.readline()
                delimiter = ';' if primeira_linha.count(';') > primeira_linha.count(',') else ','
                
                f.seek(0)
                reader = csv.DictReader(f, delimiter=delimiter)
                headers_originais = reader.fieldnames
                rows = list(reader)
                
                if rows and headers_originais:
                    # Limpa aspas ou espaços invisíveis dos cabeçalhos originais
                    headers_limpos = [str(h).strip().replace('"', '').replace("'", "") for h in headers_originais]
                    
                    dados_limpos = []
                    for r in rows:
                        # Normaliza as linhas para bater com os cabeçalhos limpos
                        linha_normalizada = {str(k).strip().replace('"', '').replace("'", ""): v for k, v in r.items() if k}
                        dados_limpos.append(linha_normalizada)
                    
                    print(f"[Sucesso] Planilha carregada! Delimitador: '{delimiter}' | Encoding: {encoding}")
                    return dados_limpos, headers_limpos, delimiter, encoding
        except Exception:
            continue
    return None, None, None, None

def salvar_progresso_csv(caminho, dados, cabecalhos, delimitador, codificacao):
    """Reescreve o arquivo CSV salvando as atualizações de status de envio."""
    try:
        with open(caminho, 'w', encoding=codificacao, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=cabecalhos, delimiter=delimitador)
            writer.writeheader()
            writer.writerows(dados)
    except Exception as e:
        print(f"⚠️ Alerta: Não foi possível salvar o arquivo agora (pode estar aberto no Excel). Erro: {e}")

# Executa a carga dos dados capturando as configurações do arquivo original
contatos, headers, delimiter, encoding_usado = carregar_dados_seguro(file_path)

if not contatos:
    print("❌ Erro: Não foi possível ler o arquivo. Verifique se ele está na mesma pasta do script.")
    exit()

print(f"📊 {len(contatos)} registros encontrados na planilha.")
print("🚀 O disparo começará em 5 segundos... Clique na tela do seu WhatsApp Web!")
time.sleep(5)

# 2. Execução dos disparos com validação de status
for index, row in enumerate(contatos):
    nome_empresa = row.get('title') or 'Cliente'
    
    # 🔍 VALIDAÇÃO DA COLUNA "ENVIADO"
    status_enviado = str(row.get('Enviado', '')).strip().lower()
    if status_enviado == 'sim':
        print(f"⏭️ [{index + 1}/{len(contatos)}] Já enviado para '{nome_empresa}'. Pulando...")
        continue

    # Busca estritamente nas colunas de telefone
    telefone_cru = row.get('phone') or row.get('phoneUnformatted') or ''
    telefone = ''.join(c for c in str(telefone_cru) if c.isdigit())
    
    if not telefone:
        print(f"⏩ [{index + 1}/{len(contatos)}] Pulando '{nome_empresa}': Sem número cadastrado.")
        continue
        
    if not telefone.startswith('55'):
        telefone = '55' + telefone

    # Filtro para ignorar números fixos comerciais
    if len(telefone) != 13:
        print(f"⏩ [{index + 1}/{len(contatos)}] Pulando '{nome_empresa}' ({telefone_cru}): Telefone fixo.")
        continue

    # Sua mensagem comercial
    mensagem = """Bom dia tudo bem?
Me chamo André da AzDev Coder
visitei sua empresa no google e vi que tem excelentes avaliações dos seus produtos, mas vi que não tem um site ainda, gostaria de apresentar algumas opções para alavancar suas vendas, sem compromisso"""

    mensagem_codificada = urllib.parse.quote(mensagem)
    link_whatsapp = f"https://web.whatsapp.com/send?phone={telefone}&text={mensagem_codificada}"
    
    print(f"📲 [{index + 1}/{len(contatos)}] Abrindo conversa para: {nome_empresa} ({telefone})...")
    
    webbrowser.open(link_whatsapp)
    
    # Gerenciamento do tempo de carregamento da página
    if index == 0:
        time.sleep(18)  
    else:
        time.sleep(12)  
        
    # Pressiona "Enter" para disparar o envio
    pyautogui.press('enter')
    time.sleep(3)
    
    # Fecha a aba atual do navegador
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(1)
    
    # 💾 ATUALIZAÇÃO E EXPORTAÇÃO EM TEMPO REAL
    row['Enviado'] = 'sim'
    salvar_progresso_csv(file_path, contatos, headers, delimiter, encoding_usado)
    print(f"💾 Status de '{nome_empresa}' atualizado para 'sim' no arquivo CSV.")

print("\n🎉 Todos os disparos pendentes foram processados e salvos!")
