from model.nivel_class import Nivel
from model.estiloDanca_class import EstiloDanca

class Parametros:
  def __init__(self, id: int, nome: str, tipoConducao: str, estilo: EstiloDanca, nivel: Nivel):
    self.__id = id
    self.__nome = nome
    self.__tipoConducao = tipoConducao
    self.__estilo = estilo
    self.__nivel = nivel

  @property
  def id(self):
    return self.__id
  
  @id.setter
  def id(self, value):
    self.__id = value
  
  @property
  def nome(self):
    return self.__nome
  
  @nome.setter
  def nome(self, value):
    self.__nome = value

  @property
  def tipoConducao(self):
    return self.__tipoConducao
  
  @tipoConducao.setter
  def tipoConducao(self, value):
    self.__tipoConducao = value

  @property
  def estilo(self):
    return self.__estilo
  
  @estilo.setter
  def estilo(self, value):
    self.__estilo = value

  @property
  def nivel(self):
    return self.__nivel
  
  @nivel.setter
  def nivel(self, value):
    self.__nivel = value

  def __str__(self):
    return (f"Parametros(id={self.__id}, nome='{self.__nome}', tipoConducao='{self.__tipoConducao}', estilo='{self.__estilo}', nivel='{self.__nivel}')")