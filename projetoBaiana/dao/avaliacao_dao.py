"""
DAO (Data Access Object) para operações de banco de dados da tabela avaliacao
"""

from bd.database import DatabaseConnection
from model.avaliacao_class import Avaliacao

class AvaliacaoDAO:
    def __init__(self, db: DatabaseConnection):
        self.__db = db
    
    def salvar(self, avaliacao: Avaliacao):
        cur = self.__db.cursor()
        
        # Converter boolean para integer (SQLite)
        if avaliacao.id is None:
            # INSERT
            cur.execute("""
                INSERT INTO avaliacao (data, examinador, aluno, nivel, evento, obs)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (avaliacao.data, avaliacao.examinador, avaliacao.aluno, avaliacao.nivel, avaliacao.evento, avaliacao.obs))

            avaliacao.id = cur.lastrowid
        else:
            # UPDATE
            cur.execute("""
                UPDATE avaliacao SET data = ?, examinador = ?, aluno = ?, nivel = ?, evento = ?, obs = ?
                WHERE id = ?;
            """, (avaliacao.data, avaliacao.examinador, avaliacao.aluno, avaliacao.nivel, avaliacao.evento, avaliacao.obs))
        
        return avaliacao.id
    
    def buscarPorId(self, id: int):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM avaliacao WHERE id = ?;", (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def buscarPorNome(self, nome: str):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM avaliacao WHERE nome LIKE ?;", (f'%{nome}%',))
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def listarTodos(self):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM avaliacao ORDER BY data;")
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def criarDeRow(self, row):
        return Avaliacao(
            id=row['id'],
            data=row['data'],
            examinador=row['examinador'],
            aluno=row['aluno'],
            nivel=row['nivel'],
            evento=row['evento'],
            obs=row['obs']
        )
    
    def deletar(self, avaliacao: Avaliacao):        
        cur = self.__db.cursor()
        cur.execute("DELETE FROM avaliacao WHERE id = ?;", (avaliacao.id,))

        return cur.rowcount > 0
    
    