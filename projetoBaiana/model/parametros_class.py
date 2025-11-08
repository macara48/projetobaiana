from model.nivel_class import Nivel
from model.estiloDanca_class import EstiloDanca

class Parametros():
  def __init__(self, parametro_id: int, parametro: str, tipoConducao: str, estilo: EstiloDanca, nivel: Nivel):
    self.parametro_id = parametro_id
    self.parametro = parametro
    self.tipoConducao = tipoConducao
    self.estilo = estilo
    self.nivel = nivel

  def __str__(self):
    return f"{self.parametro_id} | {self.parametro} | {self.tipoConducao} | {self.estilo} | {self.nivel}"