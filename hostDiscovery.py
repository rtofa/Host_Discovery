from scapy.all import *
import sys
import nmap
import time
import os  # <--- NOVO: Para criar pastas e manipular caminhos
from datetime import datetime  # <--- NOVO: Para pegar data e hora

# --- CONFIGURAÇÕES ---
USAR_SCAN_RAPIDO = False

# --- PASSO 1: DEFINIR O ALVO ---
if len(sys.argv) > 1:
    rede_alvo = sys.argv[1]
else:
    rede_alvo = "192.168.5.1/24" 

# --- PASSO 2: DESCOBRIR HOSTS ATIVOS COM SCAPY ---
print(f"[*] [FASE 1/3] Buscando hosts ativos na rede {rede_alvo}...")
pacote_arp = ARP(pdst=rede_alvo)
quadro_ethernet = Ether(dst="ff:ff:ff:ff:ff:ff")
pacote_final = quadro_ethernet / pacote_arp
respostas, _ = srp(pacote_final, timeout=3, verbose=0)

if not respostas:
    print("[!] Nenhum host ativo encontrado. Encerrando.")
    sys.exit()

dispositivos_encontrados = []
ips_ativos = []
for enviado, recebido in respostas:
    dispositivo = {
        'ip': recebido.psrc,
        'mac': recebido.hwsrc,
        'portas_abertas': []
    }
    dispositivos_encontrados.append(dispositivo)
    ips_ativos.append(recebido.psrc)

print(f"[*] Encontrados {len(ips_ativos)} hosts ativos.")

# --- PASSO 3: VERIFICAR PORTAS ABERTAS COM NMAP (EM LOTE) ---
print("[*] [FASE 2/3] Verificando portas abertas em todos os hosts de uma só vez...")
alvos_str = " ".join(ips_ativos)

try:
    nm = nmap.PortScanner()
except nmap.PortScannerError:
    print("[!] Erro: Nmap não encontrado no sistema.")
    print("[!] Por favor, instale o Nmap e adicione-o ao PATH do sistema.")
    sys.exit()

if USAR_SCAN_RAPIDO:
    print("[*] Usando modo de scan rápido (-F)...")
    port_range_arg = '-F'
else:
    print("[*] Usando modo de scan completo (-p 1-1000)...")
    port_range_arg = '-p 1-1000'

argumentos_nmap = f'{port_range_arg} -n -T4 --host-timeout 180s --min-rate 50'
print(f"[*] Executando Nmap com os argumentos: {argumentos_nmap}")
nm.scan(hosts=alvos_str, arguments=argumentos_nmap)

# --- PASSO 4: PROCESSAR OS RESULTADOS DO SCAN EM LOTE ---
print("[*] Scan do Nmap concluído. Processando os resultados...")
for host in dispositivos_encontrados:
    ip_alvo = host['ip']
    if ip_alvo in nm.all_hosts() and nm[ip_alvo].state() == 'up':
        for proto in nm[ip_alvo].all_protocols():
            if proto == 'tcp':
                portas = nm[ip_alvo][proto].keys()
                for porta in portas:
                    if nm[ip_alvo][proto][porta]['state'] == 'open':
                        host['portas_abertas'].append(porta)

# --- PASSO 5: GERAR, SALVAR E EXIBIR O RELATÓRIO FINAL ---
print("\n[*] [FASE 3/3] Gerando e salvando o relatório final...")

# 1. Preparar nomes de pasta e arquivo
pasta_relatorios = "relatorios_scan"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nome_arquivo = f"relatorio_{timestamp}.txt"
caminho_completo_arquivo = os.path.join(pasta_relatorios, nome_arquivo)

# 2. Criar a pasta de relatórios, se ela não existir
os.makedirs(pasta_relatorios, exist_ok=True)

# 3. Construir o conteúdo do relatório como uma grande string
conteudo_relatorio = [] # Usar uma lista para performance
agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

conteudo_relatorio.append("==================================================================\n")
conteudo_relatorio.append(f"          RELATÓRIO DE SCAN DE REDE\n")
conteudo_relatorio.append("==================================================================\n")
conteudo_relatorio.append(f"Data e Hora do Scan: {agora}\n")
conteudo_relatorio.append(f"Rede Alvo: {rede_alvo}\n\n")

for dispositivo in dispositivos_encontrados:
    conteudo_relatorio.append("------------------------------------------------------------------\n")
    conteudo_relatorio.append(f"IP: \t\t{dispositivo['ip']}\n")
    conteudo_relatorio.append(f"MAC Address: \t{dispositivo['mac']}\n")
    
    if dispositivo['portas_abertas']:
        portas_str = ', '.join(map(str, sorted(dispositivo['portas_abertas'])))
        conteudo_relatorio.append(f"Portas Abertas: {portas_str}\n")
    else:
        conteudo_relatorio.append("Portas Abertas: Nenhuma encontrada (conforme scan).\n")

relatorio_final_str = "".join(conteudo_relatorio)

# 4. Salvar o relatório no arquivo de texto
try:
    with open(caminho_completo_arquivo, 'w', encoding='utf-8') as f:
        f.write(relatorio_final_str)
    print(f"[*] Relatório salvo com sucesso em: {caminho_completo_arquivo}")
except IOError as e:
    print(f"[!] ERRO AO SALVAR ARQUIVO: {e}")

# 5. Exibir o relatório no console
print("\n" + relatorio_final_str)