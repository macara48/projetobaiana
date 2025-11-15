"""
DAO (Data Access Object) para operações de banco de dados da tabela itemAvaliacao
"""

from bd.database import DatabaseConnection
from model.itemAvaliacao_class import ItemAvaliacao

class ItemAvaliacaoDAO:
    def __init__(self, db: DatabaseConnection):
        self.__db = db
    
    def salvar(self, itemAvaliacao: ItemAvaliacao):
        cur = self.__db.cursor()
        
        # Converter boolean para integer (SQLite)
        if itemAvaliacao.id is None:
            # INSERT
            cur.execute("""
                INSERT INTO itemAvaliacao (parametro_id, avaliacao_id, nota)
                VALUES (?, ?, ?);
            """, (itemAvaliacao.parametro_id, itemAvaliacao.avaliacao_id, itemAvaliacao.nota))

            itemAvaliacao.id = cur.lastrowid
        else:
            # UPDATE
            cur.execute("""
                UPDATE itemAvaliacao SET parametro_id = ?, avaliacao_id = ?, nota = ?
                WHERE id = ?;
            """, (itemAvaliacao.parametro_id, itemAvaliacao.avaliacao_id, itemAvaliacao.nota))
        
        return itemAvaliacao.id
    
    def buscarPorId(self, id: int):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM itemAvaliacao WHERE id = ?;", (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def listarTodos(self):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM itemAvaliacao ORDER BY avaliacao_id;")
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def criarDeRow(self, row):
        return ItemAvaliacao(
            id=row['id'],
            parametro=row['parametro_id'],
            avaliacao=row['avaliacao_id'],
            nota=row['nota']
        )
    
    def deletar(self, itemAvaliacao: ItemAvaliacao):        
        cur = self.__db.cursor()
        cur.execute("DELETE FROM itemAvaliacao WHERE id = ?;", (itemAvaliacao.id,))

        return cur.rowcount > 0