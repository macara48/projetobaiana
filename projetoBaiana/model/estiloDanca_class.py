class EstiloDanca():
  def __init__(self, estilo_id: int, estilo: str):
    self.estilo_id = estilo_id
    self.estilo = estilo

  def __str__(self):
    return f"{self.estilo_id} | {self.estilo}"
