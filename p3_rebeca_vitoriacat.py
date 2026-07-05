# %% Importando bibliotecas/módulos necessários:
import os 
# --> Criará uma pasta de Resultados.
import sys 
# --> Encerra o programa caso haja erro. 
import time  
# --> Medirá o tempo da simulação. 
import numpy as np  
# --> Operações Matemáticas. 
import pandas as pd
#  --> Gera dataframe/CSV.
import argparse  
#  -- > Interação com o usuário. 
import plotly 
#  -->  Gráfico interativo.

#Biblioteca Progress ainda precisa ser adicionada (Barra de Progresso)

# %% Classe correspondente ao habitat da população:
class Ambiente:
    tipos = {
        1: ('Aquático','Presa: Anchova','Predador: Tubarão'),
        2: ('Terrestre', 'Presa: Lebre','Predador: Raposa')
    }
    def __init__(self_ambiente, tipo):
        if tipo not in self_ambiente.tipos:
            raise ValueError(
                "Ambiente inválido!\n"
                "Escolha [1] para Aquático OU [2] para Terrestre."
            )
        self_ambiente.tipo = self_ambiente.tipos[tipo]
#%% Classe correspondente ao modelo Predador-Presa:
class PredadorPresa:
    def __init__(self, alpha, beta, gamma, delta, x0, y0):
        '''Os valores devem ser maiores do que 0, pois se forem igual a 0, não iremos conseguir definir o valor inicial da população.'''
        if alpha > 0 and beta > 0 and gamma > 0 and delta > 0:
            self.alpha = alpha
            self.beta = beta
            self.gamma = gamma
            self.delta = delta
            '''Os parâmetros a seguir definem o estado inicial das populações'''
            self.x0 = x0 
            self.y0 = y0
            print(f"{alpha}, {beta}, {gamma} e {delta} são números válidos!")
        else:
            raise ValueError('As taxas devem ser números reais positivos de acordo com a Equação de Lotka-Volterra.')
    def predador (self, x, y):
       predadortax = (f'Valor de Delta:{self.delta*x*y}\n'
                       f'Valor de Gamma:{self.gamma*y}\n'
                       f'Taxa de Predadores:{self.delta*x*y - self.gamma*y}') 
       return predadortax
    def presa (self, x, y):
        presatax = (f'Valor de Alpha:{self.alpha*x}\n'
                       f'Valor de Beta:{self.beta*x*y}\n'
                       f'Taxa de Presas:{self.alpha*x - self.beta*x*y}') 
        return presatax
        
    @staticmethod
    def grafico(historico, ambiente):
        tempos = [p[0] for p in historico]
        presas = [p[1] for p in historico]
        predadores = [p[2] for p in historico]

        plt.figure(figsize=(10, 5))
        plt.plot(tempos, presas, label=ambiente.tipo[1], linestyle='--')
        plt.plot(tempos, predadores, label=ambiente.tipo[2], linestyle='-')
        plt.xlabel('Tempo')
        plt.ylabel('População')
        plt.title('Dinâmica Predador-Presa (Lotka-Volterra)')
        plt.legend()
        plt.grid(True)
        plt.show()
        return historico

# %% Criando menu Argpase:
def criando_menu ():
    prog = "DINAMIPY"
    description = "..."
    epilogue = "..."
    menu = argparse.ArgumentParser(prog=prog,
                                  description=description,
                                  epilog=epilogue)

    # Podemos adicionar ao menu um grupo de opções
    reqmenu = menu.add_argument_group('Argumentos obrigatórios com flag:')

    # Temos também a opção de tornar um argumento obrigatório com required=True
    reqmenu.add_argument('-hab', type=int, help='Ambiente\n 1:Aquático\n 2:Terrestre', required=True)
    reqmenu.add_argument('-alpha', type=float, help='Taxa de crescimento da presa (alpha)', required=True)
    reqmenu.add_argument('-beta', type=float, help='Taxa de mortalidade da presa em relação ao predador (beta)', required=True)
    reqmenu.add_argument('-gamma', type=float, help='Taxa de mortalidade natural do predador (gamma)', required=True)
    reqmenu.add_argument('-delta', type=float, help='Taxa de crescimento do predador em relação à presa (delta)', required=True)
    reqmenu.add_argument('-perturbacao', type=float, help='Perturbação inicial em relação ao equilíbrio (ex: 1.5)', required=True)

    return menu.parse_args()

if __name__ == '__main__':
    args = criando_menu()
    ambiente = Ambiente(tipo=args.hab)
    modelo = PredadorPresa(alpha=args.alpha,
                           beta=args.beta,
                           gamma=args.gamma,
                           delta=args.delta)
    print(ambiente.tipo)
    modelo.predador(modelo.x0, modelo.y0)
    modelo.presa(modelo.x0, modelo.y0)

    if __name__ == '__main__':
        args = criando_menu()
        ambiente = Ambiente(tipo=args.hab)
        modelo = PredadorPresa(alpha=args.alpha,
                           beta=args.beta,
                           gamma=args.gamma,
                           delta=args.delta)
    print(*ambiente.tipo, sep='\n')
    modelo.predador(modelo.x0, modelo.y0)
    modelo.presa(modelo.x0, modelo.y0)
    historico = modelo.evolucao()
    historico = modelo.evolucao(perturbacao=args.perturbacao)
    PredadorPresa.grafico(historico, ambiente)