from model.examinador_class import Examinador
from model.aluno_class import Aluno
from model.nivel_class import Nivel
from model.evento_class import Evento

class Avaliacao():
  def __init__(self, ava_id: int, data: str, examinador: Examinador, aluno: Aluno, nivel: Nivel, evento: Evento, obs: str | None = None):
    self.ava_id = ava_id
    self.data = data
    self.obs = obs
    self.examinador = examinador
    self.aluno = aluno
    self.nivel = nivel
    self.evento = evento
 
  def __str__(self):
    return f"{self.ava_id} | {self.nome} | {self.contato} | {self.nivel} | {self.tipoConducao}"