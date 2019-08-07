from abc import ABC, abstractmethod

class Consulta(ABC):
    @abstractmethod
    def __init__(self, response, segmento, subsegmento, anotacoes):
        self.response = response
        self.segmento = segmento
        self.subsegmento = subsegmento
        self.anotacoes = anotacoes

    @abstractmethod
    def captura_faixa(self):
        pass

    @abstractmethod
    def captura_tarifas(self):
         pass