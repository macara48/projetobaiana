"""
DAO (Data Access Object) para operações de banco de dados da tabela examinador
"""

from bd.database import DatabaseConnection
from model.examinador_class import Examinador

class ExaminadorDAO:
    def __init__(self, db: DatabaseConnection):
        self.__db = db
    
    def salvar(self, examinador: Examinador):
        cur = self.__db.cursor()
        
        # Converter boolean para integer (SQLite)
        if examinador.id is None:
            # INSERT
            cur.execute("""
                INSERT INTO examinador (nome, contato)
                VALUES (?, ?);
            """, (examinador.nome, examinador.contato))

            examinador.id = cur.lastrowid
        else:
            # UPDATE
            cur.execute("""
                UPDATE examinador SET nome = ?, contato = ?
                WHERE id = ?;
            """, (examinador.nome, examinador.contato))
        
        return examinador.id
    
    def buscarPorId(self, id: int):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM examinador WHERE id = ?;", (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def buscarPorNome(self, nome: str):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM examinador WHERE nome LIKE ?;", (f'%{nome}%',))
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def listarTodos(self):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM examinador ORDER BY nome;")
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def criarDeRow(self, row):
        return Examinador(
            id=row['id'],
            nome=row['nome'],
            contato=row['contato']
        )
    
    def deletar(self, examinador: Examinador):        
        cur = self.__db.cursor()
        cur.execute("DELETE FROM examinador WHERE id = ?;", (examinador.id,))

        return cur.rowcount > 0

