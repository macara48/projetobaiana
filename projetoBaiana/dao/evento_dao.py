"""
DAO (Data Access Object) para operações de banco de dados da tabela evento
"""

from bd.database import DatabaseConnection
from model.evento_class import Evento

class EventoDAO:
    def __init__(self, db: DatabaseConnection):
        self.__db = db
    
    def salvar(self, evento: Evento):
        cur = self.__db.cursor()
        
        # Converter boolean para integer (SQLite)
        if evento.id is None:
            # INSERT
            cur.execute("""
                INSERT INTO evento (nome, dataEvento, homenageado)
                VALUES (?, ?, ?);
            """, (evento.nome, evento.dataEvento, evento.homenageado))

            evento.id = cur.lastrowid
        else:
            # UPDATE
            cur.execute("""
                UPDATE evento SET nome = ?, dataEvento = ?, homenageado = ?
                WHERE id = ?;
            """, (evento.nome, evento.dataEvento, evento.homenageado))
        
        return evento.id
    
    def buscarPorId(self, id: int):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM evento WHERE id = ?;", (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def buscarPorNome(self, nome: str):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM evento WHERE nome LIKE ?;", (f'%{nome}%',))
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def listarTodos(self):
        cur = self.__db.cursor()
        cur.execute("SELECT * FROM evento ORDER BY dataEvento;")
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def criarDeRow(self, row):
        return Evento(
            id=row['id'],
            nome=row['nome'],
            dataEvento=row['dataEvento'],
            homenageado=row['homenageado']
        )
    
    def deletar(self, evento: Evento):        
        cur = self.__db.cursor()
        cur.execute("DELETE FROM evento WHERE id = ?;", (evento.id,))

        return cur.rowcount > 0

