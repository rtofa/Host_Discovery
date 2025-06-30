# Scanner de Rede Local com Scapy e Nmap 🕵️‍♂️

![Banner do Projeto](https://i.imgur.com/rSCTgE2.png)

> ⚠️ **AVISO LEGAL: PROJETO PARA FINS EDUCACIONAIS** ⚠️  
> Este projeto foi desenvolvido com **fins estritamente educacionais**. O objetivo é demonstrar a aplicação de programação de redes com Python, Scapy e Nmap em um ambiente controlado.  
>  
> O uso desta ferramenta para escanear redes nas quais você não tenha **permissão explícita** é ilegal e antiético. Atividades de scan não autorizadas podem violar leis de privacidade e de crimes cibernéticos. O autor não se responsabiliza por qualquer uso indevido do código ou das informações aqui apresentadas.  
>  
> **Use com responsabilidade e apenas em redes de sua propriedade.**

---

## 🚀 Funcionalidades Principais

* **Descoberta de Hosts Ativos:** Identifica todos os dispositivos conectados na rede, retornando seus endereços IP e MAC.
* **Scan de Portas Otimizado:** Utiliza o Nmap para verificar portas abertas nos hosts encontrados. O scan é feito em lote para máxima velocidade.
* **Modos de Scan Flexíveis:** Permite escolher entre um scan rápido (top 100 portas) e um scan completo (portas 1-1000).
* **Controle de Timeout:** Evita que o script fique "preso" em um host lento ou que não responde.
* **Geração Automática de Relatórios:** Salva um relatório detalhado em formato `.txt` a cada execução.
* **Histórico Organizado:** Cria uma pasta `relatorios_scan` e armazena os relatórios com nomes únicos baseados na data e hora, garantindo que nenhum dado seja perdido.

---

## 🛠️ Tecnologias Utilizadas

O projeto é construído com as seguintes ferramentas e bibliotecas:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  
![Scapy](https://img.shields.io/badge/Scapy-003B6D?style=for-the-badge&logo=python&logoColor=white)  
![Nmap](https://img.shields.io/badge/Nmap-005A9C?style=for-the-badge&logo=nmap&logoColor=white)

---

## 📋 Pré-requisitos

Antes de executar, certifique-se de que você tem o ambiente necessário configurado.

1. **Python 3.8+**
2. **Bibliotecas Python:** Instale as dependências com o pip.
    ```bash
    pip install scapy python-nmap
    ```
3. **Nmap:** O programa Nmap precisa estar instalado no seu sistema e acessível através do PATH.

    * **Linux (Debian/Ubuntu):**
      ```bash
      sudo apt-get install nmap
      ```
    * **Linux (Fedora/CentOS):**
      ```bash
      sudo yum install nmap
      ```
    * **macOS (Homebrew):**
      ```bash
      brew install nmap
      ```
    * **Windows:** Baixe o instalador em [nmap.org](https://nmap.org/download.html) e certifique-se de que a opção "Add to Path" esteja marcada durante a instalação.

---

## ⚙️ Como Usar

1. **Clone o repositório** ou apenas salve o arquivo `scan_rede.py` em uma pasta.
2. **Navegue até a pasta** onde o script está localizado.
3. **Execute o script** através do terminal:
    ```bash
    python scan_rede.py
    ```
4. (Opcional) Você pode **especificar a rede alvo** como um argumento na linha de comando. Caso contrário, ele usará o valor padrão definido no script.
    ```bash
    python scan_rede.py 192.168.1.1/24
    ```

---

## 📊 Saída do Script

Após a execução, você verá uma saída detalhada no console e um novo arquivo de relatório será criado.

### Exemplo de Saída no Console

[] [FASE 1/3] Buscando hosts ativos na rede 192.168.5.1/24...
[] Encontrados 4 hosts ativos.
[] [FASE 2/3] Verificando portas abertas em todos os hosts de uma só vez...
[] Usando modo de scan rápido (-F)...
[] Executando Nmap com os argumentos: -F -n -T4 --host-timeout 180s --min-rate 50
[] Scan do Nmap concluído. Processando os resultados...

[] [FASE 3/3] Gerando e salvando o relatório final...
[] Relatório salvo com sucesso em: relatorios_scan\relatorio_2025-06-30_17-23-05.txt

shell
Copiar
Editar

### Exemplo de Relatório

================================================================== RELATÓRIO DE SCAN DE REDE
Data e Hora do Scan: 30/06/2025 17:23:05
Rede Alvo: 192.168.5.1/24

IP: 192.168.5.1 MAC Address: a0:b1:c2:d3:e4:f5 Portas Abertas: 53, 80, 443
IP: 192.168.5.102 MAC Address: 11:22:33:44:55:66 Portas Abertas: 8080
IP: 192.168.5.130
MAC Address: ab:cd:ef:12:34:56
Portas Abertas: Nenhuma encontrada (conforme scan).

yaml
Copiar
Editar

---

### Estrutura dos Arquivos

A cada execução, a estrutura de pastas ficará assim:

Scapy_Learn/
├── relatorios_scan/
│ ├── relatorio_2025-06-30_17-18-15.txt
│ └── relatorio_2025-06-30_17-23-05.txt <-- Novo relatório
└── hostDiscovery.py

yaml
Copiar
Editar

---

## 📄 Licença

Este projeto está sob a licença MIT.