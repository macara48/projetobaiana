class Nivel():
  def __init__(self, nivel_id: int, corNivel: str):
    self.nivel_id = nivel_id
    self.corNivel = corNivel
  
  def __str__(self):
    return f"{self.nivel_id} | {self.corNivel}"
