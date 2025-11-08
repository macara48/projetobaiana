class Examinador():
  def __init__(self, examinador_id: int, examinador: str, contato: str):
    self.examinador_id = examinador_id
    self.examinador = examinador
    self.contato = contato

  def __str__(self):
    return f"{self.examinador_id} | {self.examinador} | {self.contato}"