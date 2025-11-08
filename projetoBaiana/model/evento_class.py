class Evento():
  def __init__(self, evento_id: int, evento: str, dataEvento: str, homenageado: str):
    self.evento_id = evento_id
    self.evento = evento
    self.dataEvento = dataEvento
    self.homenageado = homenageado

  def __str__(self):
    return f"{self.evento_id} | {self.evento} | {self.dataEvento} | {self.homenageado}"
