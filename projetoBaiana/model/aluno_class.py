from model.nivel_class import Nivel
from model.parametros_class import Parametros

class Aluno:
  def __init__(self, id: int, nome: str, contato: str, nivel: Nivel, tipoConducao: Parametros, ativo: bool = True):
    self.__id = id
    self.__nome = nome
    self.__contato = contato
    self.__nivel = nivel
    self.__tipoConducao = tipoConducao
    self.__ativo = ativo

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
  def contato(self):
    return self.__contato
  
  @contato.setter
  def contato(self, value):
    self.__contato = value
  
  @property
  def nivel(self):
    return self.__nivel
  
  @nivel.setter
  def nivel(self, value):
    self.__nivel = value

  @property
  def tipoConducao(self):
    return self.__tipoConducao
  
  @tipoConducao.setter
  def tipoConducao(self, value):
    self.__tipoConducao = value

  @property
  def ativo(self):
    return self.__ativo
  
  @ativo.setter
  def ativo(self, value):
    self.__ativo = value

  def __str__(self):
    return (f"Aluno(id={self.__id}, nome='{self.__nome}', tipoConducao='{self.__tipoConducao}', "
                f"contato='{self.__contato}', "
                f"nivel_id={self.__nivel.id})")