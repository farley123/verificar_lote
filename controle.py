class Controle:
    lista_de_controles=[]
    def __init__(self,hora:str,data:str,padrao:str,valor_identificado:str,comentario:str):
        self.hora:str=hora
        self.data:str=data
        self.padrao:str=padrao
        self.valor_identificado:str=valor_identificado
        self.comentario:str=comentario
    def __str__(self):
        return f'{self.hora} {self.data} {self.padrao} {self.valor_identificado} {self.comentario}'

    def adicionar_controle(self,controle):
        Controle.lista_de_controles.append(controle)

    def remover_controle(self,controle):
        Controle.lista_de_controles.remove(controle)