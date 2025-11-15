class Examinador:
  def __init__(self, id: int, nome: str, contato: str):
    self.__id = id
    self.__nome = nome
    self.__contato = contato

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

  def __str__(self):
    return (f"Evento(id={self.__id}, nome='{self.__nome}', contato='{self.__contato}')")
