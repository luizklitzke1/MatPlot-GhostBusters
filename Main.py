#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString

import PySimpleGUI as sg


class TelaPython:
    def __init__(self):
        layout = [
            [sg.Text("X Fantasma"), sg.Input(size = (10,0), key = "Xfantasma")],
            [sg.Text("Y Fantasma"), sg.Input(size = (10,0), key = "Yfantasma")],
            [sg.Text("A1"), sg.Input(size = (10,0), key = "A1")],
            [sg.Text("B1"), sg.Input(size = (10,0), key = "B1")],
            [sg.Text("C1"), sg.Input(size = (10,0), key = "C1")],
            [sg.Text("Tipo da função")],
            [sg.Radio("Seno", "tipoA", key = "tipoASen"), sg.Radio("Cosseno", "tipoA", key = "tipoACos")],
            
            [sg.Text("A1"), sg.Input(size = (10,0), key = "A2")],
            [sg.Text("B2"), sg.Input(size = (10,0), key = "B2")],
            [sg.Text("C2"), sg.Input(size = (10,0), key = "C2")],
    
            [sg.Text("Tipo da função")],
            [sg.Radio("Seno", "tipoB", key = "tipoBSen"), sg.Radio("Cosseno", "tipoB", key = "tipoBCos")],
                
            [sg.Button("Gerar gráfico")]
        ]
        
        #Cria janela
        self.janela = sg.Window("Dados pra o Gráfico").layout(layout)
        
        
        
    def Iniciar(self):
        while True:
            #Pega os dados
            self.button, self.values = self.janela.Read()
            print(self.values)

#np.sqrt(5)  np.pi  pow(x,y)

tela = TelaPython()
tela.Iniciar()

def GeraFuncao(x, a, b, c, tipo):
    #Gerando outra tupla para eixo Y, multiplicando por todos os valores da tupla X
    if tipo == "sen":
        FuncaoY = a + b * np.sin(c * x)
    else:
        FuncaoY = a + b * np.cos(c * x)
        
    return FuncaoY

Continuar = 1

while Continuar == 1:
    
    #Recebe a posicao do fantasma
    XFantasma = eval(input("Informe o X do Fantasma: "))
    YFantasma = eval(input("Informe o Y do Fantasma: "))
    
    #Recebe os dados da primera função (f)
    a = eval(input("Informe o valor de A: "))
    b = eval(input("Informe o valor de B: "))
    c = eval(input("Informe o valor de C: "))
    tipo = input("Gostaria de utilizar seno (sen) ou cosseno (cos): ")
    if c != 0:
        periodo = 2 * np.pi/c
    else:
        periodo = 3  
        c = 3  
    
    #Tupla Eixo X |start end    step|    Sempre baseado na primeira função
    x = np.arange(0, XFantasma, .001)
    
    f = GeraFuncao(x, a, b, c, tipo)   
    
    titulo = ("f(x) = " + str(a) + " * " + str(b) + "* " + tipo + "(" + str(c)+ " * X)")
    
    #Recebe os dados da segunda função (g)
    a = eval(input("Informe o valor de A: "))
    b = eval(input("Informe o valor de B: "))
    c = eval(input("Informe o valor de C: "))
    tipo = input("Gostaria de utilizar seno (sen) ou cosseno (cos): ")
    
    #Tupla Eixo X |start           end        step|         Sempre baseado na primeira função
    g = GeraFuncao(x, a, b, c, tipo)    
    
    titulo += ("  |  g(x) = " + str(a) + " * " + str(b) + "* " + tipo + "(" + str(c)+ " * X)")

    #Subplot das linhas de referencias do cartesiano e configurações
    fig = plt.figure()
    minimg = np.min(f)
    maximg = np.max(f)
    amplitude = (maximg - minimg) / 2
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.spines['left'].set_color('orange')
    ax1.spines['left'].set_linewidth(1)
    ax1.spines['bottom'].set_color('orange')
    ax1.spines['bottom'].set_linewidth(1)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.set_ylim([0, YFantasma + maximg + 1])
    plt.subplots_adjust(left = 0.08, right = 0.95, wspace = 0.2, hspace = 0.2)
    
    #Plot principal
    plt.ylabel("Posição na linha")
    plt.grid(color = "gray")
    plt.xlabel("Distância")
    plt.title(titulo)          
    plt.plot(x, f)
    plt.plot(x, g)
    plt.plot(XFantasma, YFantasma, "X", markersize = 20)
    
    #Calcula os pontos de encontro das funções
    first_line = LineString(np.column_stack((x, f)))
    second_line = LineString(np.column_stack((x, g)))
    intersection = first_line.intersection(second_line)

    if intersection.geom_type == 'MultiPoint':
        plt.plot(*LineString(intersection).xy, 'o')
    elif intersection.geom_type == 'Point':
        plt.plot(*intersection.xy, 'o')
 
    Batem = True
 
    try:
        XInterseccao, YInterseccao = x, y = LineString(intersection).xy
    except:
        try:
            XInterseccao, YInterseccao = intersection.xy
        except:
            Batem = False
    
    #print(XInterseccao)
    #print(YInterseccao)
        
    if (Batem):
        print ("Eles batem antes de encontrar o fantasma!")
    else:
        print ("Boa! Eles não batem antes do fantasma!")
    
        if (abs(f[-1]) - YFantasma <= 3):
            print ("Sucesso! Você acertou o fanstasma!")
        else:
            print ("Droga!! Você errou o fanstasma!")
    
    plt.show()

    Continuar = int(input("Gostaria de Continuar a executar o programa?   1- Sim   0 - Não      "))
    print("\n\n\n\n")