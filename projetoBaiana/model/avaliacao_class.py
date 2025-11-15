from model.examinador_class import Examinador
from model.aluno_class import Aluno
from model.nivel_class import Nivel
from model.evento_class import Evento

class Avaliacao:
  def __init__(self, id: int, data: str, examinador: Examinador, aluno: Aluno, nivel: Nivel, evento: Evento, obs: str | None = None):
    self.__id = id
    self.__data = data
    self.__examinador = examinador
    self.__aluno = aluno
    self.__nivel = nivel
    self.__evento = evento
    self.__obs = obs

  @property
  def id(self):
    return self.__id
  
  @id.setter
  def id(self, value):
    self.__id = value
  
  @property
  def data(self):
    return self.__data
  
  @data.setter
  def data(self, value):
    self.__data = value

  @property
  def examinador(self):
    return self.__examinador
  
  @examinador.setter
  def examinador(self, value):
    self.__examinador = value
  
  @property
  def aluno(self):
    return self.__aluno
  
  @aluno.setter
  def aluno(self, value):
    self.__aluno = value
  
  @property
  def nivel(self):
    return self.__nivel
  
  @nivel.setter
  def nivel(self, value):
    self.__nivel = value
  
  @property
  def evento(self):
    return self.__evento
  
  @evento.setter
  def evento(self, value):
    self.__evento = value

  @property
  def obs(self):
    return self.__obs
  
  @obs.setter
  def obs(self, value):
    self.__obs = value

  def __str__(self):
    return (f"Avaliacao(id={self.__id}, data='{self.__data}', examinador='{self.__examinador}', aluno='{self.__aluno}', evento='{self.__evento}', aluno='{self.__aluno}', nivel='{self.__nivel}')")