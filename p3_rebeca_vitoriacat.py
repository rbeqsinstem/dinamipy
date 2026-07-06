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
# O dicionário a seguir corresponde aos ambientes que serão oferecidos ao usuário.
    tipos = {
        1: ('Aquático','Presa: Anchova','Predador: Tubarão'),
        2: ('Terrestre', 'Presa: Lebre','Predador: Raposa')
    }
    def __init__(self, tipo):
        #Verifica se o ambiente está dentro das opções oferecidas
        if tipo not in self.tipos:
            raise ValueError(
                "Ambiente inválido!\n"
                "Escolha [1] para Aquático OU [2] para Terrestre."
            )
        self.nome, self.presa, self.predador = self.tipos[tipo] #Desempacotando o dicionário e atribuindo ao objeto ambiente.
#%% Classe correspondente ao modelo Predador-Presa:
class PredadorPresa:
    def __init__(self, alpha, beta, gamma, delta, x0, y0):

        #Os valores devem ser maiores do que 0.
        if alpha > 0 and beta > 0 and gamma > 0 and delta > 0:
            self.alpha = alpha
            self.beta = beta
            self.gamma = gamma
            self.delta = delta
            parametros = (self.alpha, self.beta, self.gamma, self.delta)
            print(f"{parametros} são números válidos!")
        else:
            raise ValueError('As taxas devem ser números reais positivos e maiores do que 0.')
        
        #Os parâmetros a seguir definem o estado inicial das populações.
        if x0 <= 0 or y0 <= 0:
            raise ValueError("As populações iniciais devem ser maiores que zero.")
        self.x0 = x0
        self.y0 = y0
        
    def taxa_presapredador (self, x, y):
        taxa_presa = self.alpha*x - self.beta*x*y
        taxa_predador = self.delta*x*y - self.gamma*y
        return taxa_presa, taxa_predador

    @staticmethod #Esse método/função não utiliza nenhum atributo da classe, então é estático.
    def extincao (x,y):
        if x <= 1:
            return "As presas entraram em extinção !!" #Caso a população x alcance menos que 1, retornará isto.
        if y <= 1:
            return "Os predadores entraram em extinção !!" #Caso a população y alcance menos que 1, retornará isto.
        return "Parabéns! Todos estão vivos."  #Caso nenhuma população entre em extinção, retornará isto.
    def evolucao (self, anos):
        dt = 1
        x = self.x0
        y = self.y0
        historico = []
        historico.append (((0,x,y)))
        for ano in range(anos):
            taxa_x, taxa_y = self.taxa_presapredador (x,y)
            dx = taxa_x * dt
            dy = taxa_y * dt
            x += dx
            y += dy
            historico.append((ano + 1, x, y))
            extinto = self.extincao(x, y)
            if extinto:
                print(extinto)
                break
        return historico

# %% Criando menu Argpase:
def criando_menu ():
    prog = "DINAMIPY" #Nome do programa.
    description = "Dinamipy é um jogo de tentativa-erro que simula a dinâmica populacional de predadores e presas." #Descrevendo o programa.
    epilogue = "O objetivo do jogo é que ambas populações sobrevivam!" #Definindo o objetivo final do programa.
    menu = argparse.ArgumentParser(prog=prog,
                                  description=description,
                                  epilog=epilogue)
    
    menu.add_argument ("Ambiente", type = int, help = "Digite [1] para Aquático OU [2] para Terrestre.")
    menu.add_argument ("")