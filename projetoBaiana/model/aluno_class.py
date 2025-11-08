from model.nivel_class import Nivel
from model.parametros_class import Parametros

class Aluno():
    
  
  def __init__(self, aluno_id: int, nome: str, contato: str, nivel: Nivel, tipoConducao: Parametros, ativo: bool = True):
    self.aluno_id = aluno_id
    self.nome = nome
    self.contato = contato
    self.nivel = nivel
    self.tipoConducao = tipoConducao
    self.ativo = ativo

  def __str__(self):
    return f"{self.aluno_id} | {self.nome} | {self.contato} | {self.ativo} | {self.nivel} | {self.contato} | {self.tipoConducao}"