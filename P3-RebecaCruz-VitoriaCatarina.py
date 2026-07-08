#%% README
'''
CFB017 - Programação para biociências
Instituto de Biofísica Carlos Chagas Filho
Universidade Federal do Rio de Janeiro
Prof. Pedro Torres

=== TRABALHO FINAL ===
Dupla: Rebeca Cruz e Vitória Catarina

DINAMIPY é um jogo de tentativa-erro baseado na Equação de Lotka-Volterra.

    1. O jogador escolhe um ambiente (Aquático ou Terrestre) e define os parâmetros
        da simulação (taxas de crescimento, mortalidade, predação e
        populações iniciais). O objetivo é manter as duas populações VIVAS durante
        todo o período de anos simulado, sem que nenhuma delas seja extinta.
        O jogador tem até 3 tentativas para vencer. 

    2. Os resultados são salvos em um arquivo CSV (na pasta 'Resultados') 
        e um gráfico interativo é gerado, mostrando a variação das
        populações de presas e predadores ao longo do tempo.

    3. Para rodar o programa, os parâmetros podem ser digitados diretamente no
    terminal (via argparse) ou informados durante a execução, quando solicitados.

Observação: Recomendamos que realize um "git clone" do nosso repositório pelo terminal.
| -->  1. No terminal, localize sua pasta ""Documentos."
| -->  2. Digite: git clone https://github.com/rbeqsinstem/dinamipy.git
| -->  3. Você terá uma pasta chamada "dinamipy" com o programa.
'''
# %% Importando bibliotecas/módulos necessários:
import os
# --> Criará uma pasta de Resultados.
import pandas as pd
#  --> Gera dataframe/CSV.
import argparse
#  -- > Interação com o usuário.
import plotly.graph_objects as go
#  -->  Gráfico interativo. 
#%% Ambiente da população:
'''
Há dois ambientes disponíveis acompanhados de populações pré-definidas para cada tipo de dictambiente.
Escolha e se divirta!
'''
#Dicionário de tuplas contendo os ambientes oferecidos.
dictambiente = {
    1: ("Aquático", "Anchova", "Tubarão"),
    2: ("Terrestre", "Lebre", "Raposa")
}
class Ambiente:
 def __init__(self, tipo):
        #Verifica se o "tipo" está dentro das opções oferecidas em dictambiente.
        if tipo not in dictambiente:
            raise ValueError(
                "Ambiente inválido!\n"
                "Escolha [1] para Aquático OU [2] para Terrestre."
            )
        dados = dictambiente[tipo]
        self.nome = dados[0]
        self.presa = dados[1]
        self.predador = dados[2]
#%% Equação de Lotka-Volterra:
''' 
A classe predador-presa representa a Equação de Lotka-Volterra. 
Clique aqui para saber mais: https://scipy-cookbook.readthedocs.io/items/LoktaVolterraTutorial.html
Os parâmetros são:
    x = presa
    y = predador
    alpha = taxa de crescimento natural das presas, quando não há predadores.
    beta = taxa de mortalidade de presas, devido à predação.
    delta = taxa de crescimento dos predadores após predação.
    gamma = taxa de mortalidade natural de predadores.
'''
class PredadorPresa:
    def __init__(self, alpha, beta, gamma, delta, x0, y0): #Esta função define os parâmetros iniciais da classe.
        #Todos os parâmetros devem ser maiores do que 0 de acordo com a Equação de Lotka-Volterra.
        if alpha < 0 or beta < 0 or gamma < 0 or delta < 0:
            raise ValueError("Todos os valores tem que ser maior que zero!")
        if x0 < 0 or y0 < 0:
            raise ValueError("A População inicial tem que ser maior que zero!")

        self.alpha = alpha 
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.x0 = x0
        self.y0 = y0
        print("Todos os parâmetros são aceitos! Vamos continuar.")

    def calculotaxa(self, x, y):
        # Essa é a fórmula do Lotka-Volterra
        taxa_x = self.alpha * x - self.beta * x * y
        taxa_y = self.delta * x * y - self.gamma * y
        return taxa_x, taxa_y

    def extincao (self, x, y):
        #Define o que faz a população de presas (x) e de predadores (y) entrar em extinção.
        if x < 1: #Se o x for menor do que 1 as presas são extintas.
            return "As presas entraram em extinção !!"
        elif y < 1: #Se o y for menor do 1 os predadores são extintos.
            return "Os predadores entraram em extinção !!"
        else:
            return None
        
    def simulacao(self, anos, dt=0.01):
        '''
        Esta função é essencial, pois define a simulação dos dados.
        Neste caso, definimos que a contagem de instante será em anos.
        o "dt" seria a variação do instante, quanto menor mais devagar, mas mais preciso!
            |--> O valor de 0.01 será usado como padrão, pois funciona na maioria dos casos.
        '''
        x = self.x0 #Atribui o valor do parâmetro na variável de simulação.
        y = self.y0 #Atribui o valor do parâmetro na variável de simulação.
        instante = 0 #O instante inicial é 0
        historico = [] #No histórico será armazenado o valor de presas e predadores em cada instante de tempo (dt) da simulação.
        ganhou = True 

        while instante <= anos: #Continua simulando até completar o total de anos.
            historico.append((instante, x, y)) #Guarda o estado atual da simulação.

            taxa_x, taxa_y = self.calculotaxa(x, y) #Calcula a taxa de variação de presas e predadores.

            x = x + taxa_x * dt #Atualiza a população de presas em cada instante de tempo.
            y = y + taxa_y * dt #Atualiza a população de predadores em cada instante de tempo.

            if x < 0: 
                x = 0
            if y < 0:
                y = 0
            # |--> A equação pode gerar um valor negativo e população não pode ser negativa. 
            # O programa condiciona o número negativo para 0.
            verificar_extincao = self.extincao (x, y)
            if verificar_extincao is not None:
                print("Você perdeu... ⚠︎ Tente novamente !") #Esta função verifica se houve extinção, se sim, aparece esta mensagem.
                historico.append((instante + dt, x, y))
                ganhou = False
                break

            instante = instante + dt #Loop do instante de tempo 

        return historico, ganhou

# %% Menu Argpase: Definindo parâmetros de classe.
def criando_menu():
    '''
    O argpase será uma opção para usuários optarem à passar os valores de forma rápida.
    Ideal para quem já sabe os valores que irão dar certo.
    '''

    menu = argparse.ArgumentParser(prog="DINAMIPY", description="Um jogo de tentativa e erro," \
    "focado em simular a interação predador-presa.")
    #Adicionando argumentos iniciais.
    menu.add_argument('-amb', type=int, help= 'Escolha o ambiente! Digite [1] para Aquático OU [2] para Terrestre.', default=None)
    menu.add_argument('-anos', type=int, help= 'Digite a quantidade de anos a serem analizados',  default=None)
    #Grupo de argumentos para as presas.
    presa_menu = menu.add_argument_group('Presa:')
    presa_menu.add_argument('-a', type=float, help='alpha = Digite um valor para taxa de crescimento natural das presas, quando não há predadores.', default=None) #Argumento para alpha.
    presa_menu.add_argument('-b', type=float, help='beta = Digite um valor para taxa de mortalidade de presas, devido à predação.', default=None) #Argumento para beta.
    presa_menu.add_argument('-x', type=int, help='x = Digite um valor para o número inicial de presas', default=None) #Argumento para número inicial de presas.
    #Grupo de argumentos para os predadores.
    predador_menu = menu.add_argument_group('Predador:')
    predador_menu.add_argument('-d', type=float, help='delta = Digite um valor para taxa de crescimento dos predadores após predação.',  default=None)
    predador_menu.add_argument('-g', type=float, help='gamma = Digite um valor para a taxa de mortalidade natural de predadores.', default=None)
    predador_menu.add_argument('-y', type=int,help=' y = Digite um valor para o número inicial de predadores.' , default=None)

    return menu

# %% Tratamento de erros utilizando try/except.
''' 
--> Para caso o usuário queira digitar separadamente os valores ou esquecer de digitar os valores dos parâmetros no argpase, 
terá o método 'input()'. A seguir se encontra um tratamento de erros para o método.
'''
def pergambiente():
    while True:
        resposta = input("Escolha o ambiente [1]: Aquático ou [2]: Terrestre: ")
        try:
            valor = int(resposta)
        except:
            print("Digite [1] para Aquático ou [2] para Terrestre")
            continue

        if valor == 1 or valor == 2:
            return valor
        else:
            print("Opção Inválida!\n" \
            "Tente novamente: Digite [1] ou [2].")


def perginteiro (texto):
    while True:
        resposta = input(texto)
        try:
            valor = int(resposta)
        except:
            print("Não é um número inteiro. Tente novamente!"\
            "Exemplo: 1")
            continue

        if valor <= 0:
            print("Digite um número MAIOR que 0.")
        else:
            return valor


def pergdecimal (texto):
    while True:
        resposta = input(texto)
        try:
            valor = float(resposta)
        except:
            print("Não é um número válido. Tente novamente!" \
            "Exemplo: 0.5")
            continue

        if valor < 0:
            print("Digite um número MAIOR que 0.")
        else:
            return valor


def pastaresultados ():
    nome_pasta = "Resultados"
    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)
    return nome_pasta

# %% Gerando CSV dos dados digitados pelo usuário.
def gerarcsv (pasta, amb, anos, historico, params, resultado):
    ''' 
    Gera um CSV com o histórico de todas as tentativas e os parâmetros usados em cada uma.
    O intuito deste CSV é gerar a possibilidade de treinar ferramentas de ML para deixar este código com uma maior acurácia de resultados.
    '''
    if not historico:
        raise ValueError(" Histórico vazio... Não há dados de simulação para exportar.") #Se não tiver dados, irá resultar em erro.

    colunrod = [item[0] for item in historico] #Pega o item posicional 0 na lista histórico e associa a coluna da rodada.
    coluntempo = [item[1] for item in historico] #Pega o item posicional 1 na lista histórico e associa a coluna do instante.
    colunpresas = [item[2] for item in historico] #Pega o item posicional 2 na lista histórico e associa a coluna das presas.
    colunpredadores = [item[3] for item in historico] #Pega o item posicional 3 na lista histórico e associa a coluna dos predadores.

    #Busca o parâmetro correspondente à rodada daquela linha.
    colunalpha = [params[z][0] for z in colunrod]
    colunbeta = [params[z][1] for z in colunrod]
    colungamma = [params[z][2] for z in colunrod]
    colundelta = [params[z][3] for z in colunrod]
    colunx0 = [params[z][4] for z in colunrod]
    coluny0 = [params[z][5] for z in colunrod]

    #Para cada linha, busca se aquela rodada terminou em "ganhou" ou "perdeu".
    colunresult = [resultado[z] for z in colunrod]

    df = pd.DataFrame({
        "Rodada": colunrod,
        "Tempo": coluntempo,
        "Presas": colunpresas,
        "Predadores": colunpredadores,
        "Alpha": colunalpha,
        "Beta": colunbeta,
        "Gamma": colungamma,
        "Delta": colundelta,
        "x0": colunx0,
        "y0": coluny0,
        "Resultado": colunresult,
        "Ambiente" : amb.nome,
        "Anos" : anos
    })

    nomearquivo = os.path.join(pasta, f"simulacao_{amb.nome}.csv") #Salva o arquivo .CSV na pasta 'Resultados'

    try:
        df.to_csv(nomearquivo) #Transforma o DataFrame em arquivo .CSV
    except OSError as erro:
        raise OSError(f"Não foi possível salvar o CSV em '{nomearquivo}': {erro}") #Caso não seja possível salvar o arquivo, retornará esta mensagem de erro.
    return nomearquivo

#%% Execução principal (__main__): Lê os argumentos do menu e executa o jogo.
if __name__ == "__main__":

    menu = criando_menu() #Cria o menu de argumentos do programa.
    args = menu.parse_args() #Armazena os argumentos digitados pelo usuário no terminal.

    print("BEM VINDO AO DINAMIPY ( ˶ˆᗜˆ˵ )")
    print("Caso queira rodar o programa rapidamente, digite no seu terminal:")
    print("python nome_do_arquivo.py -amb _ -anos _ -a _ -b _ -x _ -g _ -d _ -y _")
    print("Tente manter as duas populações vivas...")
    print("Você tem 3 tentativas no total. Boa Sorte! (ദ്ദി˙ᗜ˙)")

    if args.amb is not None:  #Verifica se o ambiente foi informado pelo argparse.
        tipo = args.amb
        if tipo not in dictambiente:  #Verifica se o valor passado pelo argparse é válido.
            print("Ambiente inválido! Digite [1] para Aquático ou [2] para Terrestre.")
            tipo = pergambiente()  #Solicita o ambiente por input, já que o valor do argparse era inválido.
    else:
        tipo = pergambiente()  #Caso contrário, solicita o ambiente por input.
    dictambiente = Ambiente(tipo)

    if args.anos is not None: #Verifica se o usuário digitou "anos" no argpase.
        anos = args.anos
    else:
        anos = perginteiro ("Quantos anos quer simular?") #Caso contrário, solicita o valor por input.

    tentativa = 1
    maxtentativas = 3
    ganhou = False #Indica que o jogador ainda não venceu.

    jogotodo = []  # Armazena o histórico completo de todas as tentativas.
    paramsrod = {} # Armazena os parâmetros utilizados em cada tentativa.
    resultadorod = {} # Armazena se cada tentativa foi "Ganhou" ou "Perdeu".

    while tentativa <=  maxtentativas and ganhou == False: #Repete o jogo até vencer ou atingir o limite de tentativas.
        print("--> Tentativa", tentativa, "de", maxtentativas)

        # O valor do argpase é utilizado apenas na primeira tentativa, depois o input para outras tentativas é solicitado.
        if tentativa == 1 and args.a is not None:
            a = args.a
        else:
            a = pergdecimal ("Digite o valor para alpha:\n" \
            "Obs: É a taxa de crescimento natural das presas, quando não há predadores. ")

        if tentativa == 1 and args.b is not None:
            b = args.b
        else:
            b = pergdecimal ("Digite o valor para beta:\n" \
            "Obs: É a taxa de mortalidade de presas, devido à predação.")

        if tentativa == 1 and args.x is not None:
            x = args.x
        else:
            x = perginteiro ("População inicial de presas: ")

        if tentativa == 1 and args.d is not None:
            d = args.d
        else:
            d = pergdecimal ("Digite o valor para delta:\n" \
            "Obs: É a taxa de crescimento dos predadores após predação.")

        if tentativa == 1 and args.g is not None:
            g = args.g
        else:
            g = pergdecimal ("Digite o valor para gamma:\n" \
            "Obs: É a taxa de mortalidade natural de predadores.")
        if tentativa == 1 and args.y is not None:
            y = args.y
        else:
            y = perginteiro ("População inicial de predadores: ")
        #Verifica se o ponto de equilíbrio do sistema está de acordo com o que estabelecemos (>1) antes de simular.
        xeq = g / d
        yeq = a / b
        if xeq < 1 or yeq < 1:
            print(f"Ponto de equilíbrio inviável: (x = {xeq}, y = {yeq}). "
                  "O jogo considera extinção para populações menores que 1, escolha outros valores para continuar!!")
            args.a = args.b = args.x = args.d = args.g = args.y = None #Caso possua dados do argpase, na próxima rodada ele desconsiderará estes valores.
            continue #Volta ao início do loop utilizando o método input() para que o usuário digite novos valores.

        jogo = PredadorPresa(a, b, g, d, x, y)  #Cria um objeto da classe PredadorPresa utilizando os parâmetros informados.
        historico, ganhou = jogo.simulacao(anos)  #Executa a simulação e retorna o histórico e o resultado da tentativa.

        paramsrod[tentativa] = [a, b, g, d, x, y]  #Salva os parâmetros utilizados na tentativa atual.
        resultadorod[tentativa] = "Ganhou" if ganhou else "Perdeu"  #Salva o resultado da tentativa atual.

        for ponto in historico:
            jogotodo.append((tentativa, ponto[0], ponto[1], ponto[2])) #Adiciona cada ponto da simulação ao histórico geral.

        if ganhou:
            print("*** VOCE GANHOU O DINAMIPY! \\ ٩( ᐛ )و / ***")
            print("As duas populaçôes sobreviveram os", anos, "anos", " | Tentativa:", tentativa)
        else:
            print("Não deu certo dessa vez: Tentativa:", tentativa)
            if tentativa <  maxtentativas:
                print("Tente de novo com outros valores.")

        tenativavencedora = tentativa
        tentativa = tentativa + 1

    pasta = pastaresultados ()
    print(f"Gerando a pasta 'Resultados' dentro de dinamipy em: {os.path.abspath(pasta)}")
    '''Gerando o arquivo csv com os dados das rodadas.
    A funcionalidade do arquivo .CSV com os dados de cada rodada, é para possívelmente treinar uma ferramenta de ML.
        | --> Gerar uma maior acurácia nos resultados.
    '''
    gerarcsv (pasta, dictambiente, anos, jogotodo, paramsrod, resultadorod)

    eixotempo = []
    eixopresas = []
    eixopredadores = []

    for ponto in historico:
        eixotempo.append(ponto[0])
        eixopresas.append(ponto[1])
        eixopredadores.append(ponto[2])

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=eixotempo, y=eixopresas, mode="lines",
                              name=dictambiente.presa, line=dict(color="royalblue", width=4)))

    fig.add_trace(go.Scatter(x=eixotempo, y=eixopredadores, mode="lines",
                              name=dictambiente.predador, line=dict(color="firebrick", width=4)))

    titulo_resultado = f"Tentativa vencedora: {tenativavencedora}" if ganhou else f"Todos extintos | Última tentativa: {tenativavencedora}"

    fig.update_layout(
        title="Modelo Predador-Presa " + dictambiente.nome + " | " + titulo_resultado,
        xaxis_title="Tempo (anos)",
        yaxis_title="População",
        template="plotly_white"
    )

    fig.show()

    if not ganhou:
        print("Fim de jogo! Todos foram extintos. U ´꓃ ` U")
    print("O histórico das tentativas foi salvo no CSV | (Verifique a pasta:'Resultados').")