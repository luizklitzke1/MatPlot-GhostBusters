#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import LineString

import PySimpleGUI as sg
class TelaPython:
    def __init__(self):
        
        self.tentativa = 0
        
        sg.theme("DefaultNoMoreNagging")
        
        frame_Fanstasma = [
                    [sg.Text("x"), sg.Input(size = (15,0), key = "Xfantasma")],
                    [sg.Text("y"), sg.Input(size = (15,0), key = "Yfantasma")],
        ]
        
        frame_Funcao1 = [
                    [sg.Text("a"), sg.Input(size = (15,0), key = "A1")],
                    [sg.Text("b"), sg.Input(size = (15,0), key = "B1")],
                    [sg.Text("c"), sg.Input(size = (15,0), key = "C1")],
                    [sg.Text("Tipo da função")],
                    [sg.Radio("Seno", "tipoA", key = "tipoASen", default = True), sg.Radio("Cosseno", "tipoA", key = "tipoACos")],
        ]           
        
        frame_Funcao2 = [
                    [sg.Text("a"), sg.Input(size = (15,0), key = "A2")],
                    [sg.Text("b"), sg.Input(size = (15,0), key = "B2")],
                    [sg.Text("c"), sg.Input(size = (15,0), key = "C2")],
            
                    [sg.Text("Tipo da função")],
                    [sg.Radio("Seno", "tipoB", key = "tipoBSen", default = True), sg.Radio("Cosseno", "tipoB", key = "tipoBCos")],
        ]
        
        layout = [
            
            [sg.Frame("Dados do fantasma       ", frame_Fanstasma)],
            
            [sg.Frame("Dados da primeira função", frame_Funcao1), sg.Frame("Dados da segunda função", frame_Funcao2)],

            [sg.Text("*O  programa  encerra   automaticamente\n caso algum campo for deixado em branco")],
            
            [sg.Submit("Gerar gráfico"), sg.Cancel("Fechar")],
            
            [sg.Text("Resultados")],
            [sg.Output(size = (50,15))]
        ]
        
        #Cria janela
        self.janela = sg.Window("Trab Mat - Gerador de Funções").layout(layout)
        
    def GeraFuncao(self, x = 0, a = 0, b = 0, c = 0, tipo = "sen"):
        #Gerando outra tupla para eixo Y, multiplicando por todos os valores da tupla X
        if tipo == "sen":
            Funcao = a + b * np.sin(c * x)
        else:
            Funcao = a + b * np.cos(c * x)
        
        return Funcao
        
    def Iniciar(self):
        while True:
            
            self.tentativa += 1
                        
            #Pega os dados
            self.button, self.values = self.janela.Read()
            #print(self.values)
            
            #Recebe a posicao do fantasma
            XFantasma = float(self.values["Xfantasma"])
            YFantasma = float(self.values["Yfantasma"])
            
            #Recebe os dados da primera função (f)
            a = float(self.values["A1"])
            b = float(self.values["B1"])
            c = float(self.values["C1"])
            
            if (self.values["tipoASen"]):
                tipo = "sen"
            else:
                tipo = "cos"
                
            if c != 0:
                periodo = 2 * np.pi/c
            else:
                periodo = 3  
                c = 3  
            
            #Tupla Eixo X |start end    step|    Sempre baseado na primeira função
            x = np.arange(0, XFantasma, .001)
            
            f = self.GeraFuncao(x, a, b, c, tipo)   
            
            titulo = ("f(x) = " + str(a) + " * " + str(b) + "* " + tipo + "(" + str(c)+ " * X)")
            
            #Recebe os dados da segunda função (g)
            a = float(self.values["A2"])
            b = float(self.values["B2"])
            c = float(self.values["C2"])
            
            if (self.values["tipoBSen"]):
                tipo = "sen"
            else:
                tipo = "cos"
            
            #Tupla Eixo X |start           end        step|         Sempre baseado na primeira função
            g = self.GeraFuncao(x, a, b, c, tipo)    
            
            titulo += ("  |  g(x) = " + str(a) + " * " + str(b) + "* " + tipo + "(" + str(c)+ " * X)")

            #Subplot das linhas de referencias do cartesiano e configurações
            fig = plt.figure("Gráfico das funções")
            minimg = np.min(f)
            maximg = np.max(f)
            amplitude = (maximg - minimg) / 2
            ax1 = fig.add_subplot(1, 1, 1)
            ax1.spines["left"].set_color("orange")
            ax1.spines["left"].set_linewidth(1)
            ax1.spines["bottom"].set_color("orange")
            ax1.spines["bottom"].set_linewidth(1)
            ax1.spines["right"].set_visible(False)
            ax1.spines["top"].set_visible(False)
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

            if intersection.geom_type == "MultiPoint":
                plt.plot(*LineString(intersection).xy, "o")
            elif intersection.geom_type == "Point":
                plt.plot(*intersection.xy, "o")
        
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
                
            print (f"[{self.tentativa} tentativa ]")
                
            if (Batem):
                print ("Eles batem antes de encontrar o fantasma!")
            else:
                print ("Boa! Eles não batem antes do fantasma!")
            
                if (abs(f[-1]) - YFantasma <= 3):
                    print ("Sucesso! Você acertou o fanstasma!")
                else:
                    print ("Droga!! Você errou o fanstasma!")        
            
            print ("\n")        
            
            plt.show()
            plt.clf()

tela = TelaPython()
tela.Iniciar() 