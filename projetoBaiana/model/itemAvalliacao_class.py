from parametros_class import Parametros

class ItemAvaliacao():
  def __init__(self, ava_id: int, nota: int, parametro: Parametros):
    self.ava_id = ava_id
    self.nota =  nota
    self.parametro = Parametros
  
  def __str__(self):
    return f"{self.ava_id} | {self.nota} | {self.parametro}"
