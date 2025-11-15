"""
DAO (Data Access Object) para operações de banco de dados da tabela estiloDanca
"""

from bd.database import DatabaseConnection
from model.estiloDanca_class import EstiloDanca

class EstiloDancaDAO:
    def __init__(self, db: DatabaseConnection):
        self.__db = db
    
    def salvar(self, estiloDanca: EstiloDanca):
        cur = self.__db.cursor()
        
        # Converter boolean para integer (SQLite)
        if estiloDanca.id is None:
            # INSERT
            cur.execute("""
                INSERT INTO estiloDanca (nome)
                VALUES (?);
            """, (estiloDanca.nome))

            estiloDanca.id = cur.lastrowid
        else:
            # UPDATE
            cur.execute("""
                UPDATE estiloDanca SET nome = ?
                WHERE id = ?;
            """, (estiloDanca.nome))
        
        return estiloDanca.id
    
    def buscarPorId(self, id: int):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM estiloDanca WHERE id = ?;", (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def buscarPorNome(self, nome: str):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM estiloDanca WHERE nome LIKE ?;", (f'%{nome}%',))
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def listarTodos(self):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM estiloDanca ORDER BY nome;")
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def criarDeRow(self, row):
        return EstiloDanca(
            id=row['id'],
            nome=row['nome']
        )
    
    def deletar(self, estiloDanca: EstiloDanca):        
        cur = self.__db.cursor()
        cur.execute("DELETE FROM estiloDanca WHERE id = ?;", (estiloDanca.id,))

        return cur.rowcount > 0
    