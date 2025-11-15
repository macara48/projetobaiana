"""
Classe modelo para a tabela usuario (relacionamento 1:1 com Aluno)
"""
from model.aluno_class import Aluno

class Usuario:
    def __init__(self, id: int, login: str, senha: str, tipo: str, aluno: Aluno):
        self.__id = id
        self.__login = login
        self.__senha = senha
        self.__tipo = tipo
        self.__aluno = aluno
    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = value
    
    @property
    def login(self):
        return self.__login
    
    @login.setter
    def login(self, value):
        self.__login = value
    
    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, value):
        self.__senha = value
    
    @property
    def tipo(self):
        return self.__tipo
    
    @tipo.setter
    def tipo(self, value):
        self.__tipo = value
    
    @property
    def aluno(self):
        return self.__aluno
    
    @aluno.setter
    def aluno(self, value):
        self.__aluno = value
    
    def __str__(self):
        return (f"Usuario(id={self.__id}, login='{self.__login}', "
                f"tipo='{self.__tipo}', aluno_id={self.__aluno.id})")

