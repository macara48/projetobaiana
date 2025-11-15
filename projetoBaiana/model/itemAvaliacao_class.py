from parametros_class import Parametros
from avaliacao_class import Avaliacao

class ItemAvaliacao:
  def __init__(self, id: int, parametro: Parametros, avaliacao: Avaliacao, nota: int):
    self.__id = id
    self.__parametro = parametro
    self.__avaliacao = avaliacao
    self.__nota = nota

  @property
  def id(self):
    return self.__id
  
  @id.setter
  def id(self, value):
    self.__id = value
  
  @property
  def parametro(self):
    return self.__parametro
  
  @parametro.setter
  def parametro(self, value):
    self.__parametro = value

  @property
  def parametro(self):
    return self.__parametro
  
  @parametro.setter
  def parametro(self, value):
    self.__parametro = value

  @property
  def avaliacao(self):
    return self.__avaliacao
  
  @avaliacao.setter
  def avaliacao(self, value):
    self.__avaliacao = value

  @property
  def nota(self):
    return self.__nota
  
  @nota.setter
  def nota(self, value):
    self.__nota = value

  def __str__(self):
    return (f"ItemAvaliacao(id={self.__id}, parametro='{self.__parametro}', avaliacao='{self.__avaliacao}', nota='{self.__nota}')")
