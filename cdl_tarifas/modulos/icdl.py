from abc import ABC, abstractmethod

class Cdl(ABC):
    @abstractmethod
    def __init__(self, nome):
        self.nome = nome
        self.lista_consultas = []

