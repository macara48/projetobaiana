"""
DAO (Data Access Object) para operações de banco de dados da tabela nivel
"""
from bd.database import DatabaseConnection
from model.nivel_class import Nivel

class NivelDAO:
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def salvar(self, nivel: Nivel):
        cur = self.db.cursor()
        
        if nivel.nivel_id is None:
            # INSERT
            cur.execute("INSERT INTO nivel (corNivel) VALUES (?);", (nivel.corNivel,))
            nivel.nivel_id = cur.lastrowid
        else:
            # UPDATE
            cur.execute("UPDATE nivel SET corNivel = ? WHERE nivel_id = ?;", (nivel.corNivel, nivel.nivel_id))
        
        return nivel.nivel_id
    
    def buscarPorId(self, nivel_id: int):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM nivel WHERE id = ?;", (nivel_id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def buscarPorNome(self, corNivel: str):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM nivel WHERE corNivel = ?;", (corNivel,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def listarTodas(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM nivel ORDER BY corNivel;")
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def criarDeRow(self, row):
        return Nivel(
            nivel_id=row['id'],
            corNivel=row['Nivel']
        )
    
    def deletar(self, nivel: Nivel):
        if nivel.nivel_id is None:
            return False
        
        cur = self.db.cursor()
        cur.execute("DELETE FROM nivel WHERE id = ?;", (nivel.nivel_id,))

        return cur.rowcount > 0