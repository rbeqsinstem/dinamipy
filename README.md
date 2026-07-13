# DINAMIPY

DINAMIPY é um jogo de tentativa e erro baseado no modelo predador-presa de Lotka-Volterra, desenvolvido para a disciplina **CFB017 - Programação para Biociências (UFRJ)**.

## Autoras

- Rebeca Cruz
- Vitória Catarina

## Requisitos

- Python 3.10 ou superior
- pandas
- plotly

Instale as dependências com:

```bash
pip install pandas plotly
```

## Como executar

Clone o repositório:

```bash
git clone https://github.com/rbeqsinstem/dinamipy.git
cd dinamipy
```

Execute o programa:

```bash
python P3-RebecaCruz-VitoriaCatarina1.py
```

Ou informe os parâmetros diretamente pelo terminal:

```bash
python P3-RebecaCruz-VitoriaCatarina1.py -amb 1 -anos 50 -a 0.6 -b 0.03 -x 40 -d 0.02 -g 0.4 -y 12
```

## Parâmetros

| Argumento | Descrição |
|-----------|-----------|
| `-amb` | Ambiente (1 = Aquático, 2 = Terrestre) |
| `-anos` | Tempo de simulação |
| `-a` | Taxa de crescimento das presas (α) |
| `-b` | Taxa de predação (β) |
| `-g` | Taxa de mortalidade dos predadores (γ) |
| `-d` | Taxa de reprodução dos predadores (δ) |
| `-x` | População inicial das presas |
| `-y` | População inicial dos predadores |

Caso algum parâmetro não seja informado, o programa solicitará sua entrada durante a execução.

## Como jogar

1. Escolha um dos ambientes disponíveis.
2. Defina os parâmetros da simulação.
3. O objetivo é manter as populações de presas e predadores vivas durante todo o período simulado.
4. O jogador possui até três tentativas.

## Saídas

Ao final da execução, o programa gera:

- um gráfico interativo da evolução das populações;
- um arquivo CSV na pasta `Resultados` contendo os parâmetros utilizados e os resultados das tentativas.
