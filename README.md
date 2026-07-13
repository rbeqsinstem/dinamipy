<p align="center">
  <img src="midias/entrada.png" alt="Logo do DINAMIPY" width="750">
</p>

# O que é o DINAMIPY?
DINAMIPY é um jogo de tentativa e erro baseado no modelo predador-presa de **Lotka-Volterra**, desenvolvido como trabalho final da disciplina **CFB017 – Programação para Biociências (UFRJ)**.
O objetivo é encontrar um conjunto de parâmetros capaz de manter as populações de presas e predadores vivas durante todo o período da simulação.

## Requisitos do programa:

- Python 3.10 ou superior
- pandas
- plotly

Instale as dependências:

```bash
pip install pandas plotly
```

## Instalando o programa:

Clone o repositório:

```bash
git clone https://github.com/rbeqsinstem/dinamipy.git
cd dinamipy
```

## Execução

Execute o programa no modo interativo:

```bash
python P3-RebecaCruz-VitoriaCatarina1.py
```

Ou informe todos os parâmetros diretamente pelo terminal:

```bash
python P3-RebecaCruz-VitoriaCatarina1.py -amb 1 -anos 50 -a 0.6 -b 0.03 -x 40 -d 0.02 -g 0.4 -y 12
```

Caso algum parâmetro não seja informado, o programa solicitará sua entrada durante a execução.

## Parâmetros de entrada

### Ambientes disponíveis

| Ambiente | Presa | Predador |
|----------|-------|----------|
| 🌊 Aquático | Anchova | Tubarão |
| 🌳 Terrestre | Lebre | Raposa |

### Parâmetros

| Parâmetro | Descrição |
|-----------|-----------|
| **α (alpha)** | Taxa de crescimento natural das presas |
| **β (beta)** | Taxa de predação das presas |
| **γ (gamma)** | Taxa de mortalidade natural dos predadores |
| **δ (delta)** | Taxa de crescimento dos predadores após a predação |
| **x** | População inicial de presas |
| **y** | População inicial de predadores |

### Regras

- Todos os parâmetros devem ser maiores que **0**.
- As populações iniciais também devem ser maiores que **0**.
- O programa verifica automaticamente se o ponto de equilíbrio do sistema é viável antes da simulação.
- Uma população é considerada extinta quando seu tamanho fica menor que **1**.
- O jogador possui até **3 tentativas** para encontrar uma solução.

## Modelo matemático

O programa utiliza o modelo de Lotka-Volterra, resolvido numericamente pelo método de Euler.

```text
dx/dt = αx − βxy

dy/dt = δxy − γy
```

onde:

- **x** = população de presas;
- **y** = população de predadores;
- **α** = taxa de crescimento das presas;
- **β** = taxa de predação;
- **γ** = taxa de mortalidade natural dos predadores;
- **δ** = taxa de crescimento dos predadores após a predação.

## Resultados gerados

Ao final da execução, o programa gera:

- 📈 um gráfico interativo com a evolução das populações;
- 📄 um arquivo CSV contendo todas as tentativas realizadas e os parâmetros utilizados;
- 📁 uma pasta `Resultados`, criada automaticamente para armazenar os arquivos gerados.
