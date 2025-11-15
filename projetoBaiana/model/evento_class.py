class Evento:
  def __init__(self, id: int, nome: str, dataEvento: str, homenageado: str):
    self.__id = id
    self.__nome = nome
    self.__dataEvento = dataEvento
    self.__homenageado = homenageado

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
  def dataEvento(self):
    return self.__dataEvento
  
  @dataEvento.setter
  def dataEvento(self, value):
    self.__dataEvento = value
  
  @property
  def homenageado(self):
    return self.__homenageado
  
  @homenageado.setter
  def homenageado(self, value):
    self.__homenageado = value

  def __str__(self):
    return (f"Evento(id={self.__id}, nome='{self.__nome}', dataEvento='{self.__dataEvento}', homenageado='{self.__homenageado}')")
