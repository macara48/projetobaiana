"""
Serviço para interação do usuário via linha de comando com a entidade Categoria
"""
import sys
import os

# Adicionar o diretório pai ao path para permitir imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bd.database import DatabaseConnection
from dao.nivel_dao import NivelDAO
from model.nivel_class import Nivel

class NivelService:
    def __init__(self, db: DatabaseConnection):
        self.db = db
        self.nivelDao = NivelDAO(db)
    
    def exibirMenu(self):
        """Exibe o menu principal de opções"""
        print("\n" + "="*50)
        print("  SISTEMA DE GERENCIAMENTO DE NIVEIS")
        print("="*50)
        print("1. Criar nivel")
        print("2. Listar todos os niveis")
        print("3. Buscar nivel por ID")
        print("4. Buscar nivel por nome")
        print("5. Atualizar nivel")
        print("6. Deletar nivel")
        print("0. Sair")
        print("="*50)

    def criarNivel(self):
        """Solicita dados do usuário e cria um novo nivel"""
        print("\n--- CRIAR NIVEL ---")
        nome = input("Digite o nome do nivel: ").strip()
        
        if not nome:
            print("❌ Erro: O nome do nivel não pode ser vazio!")
            return
        
        try:
            # Verificar se já existe um nivel com esse nome
            nivelExistente = self.nivelDao.buscarPorNome(nome)
            if nivelExistente:
                print(f"❌ Erro: Já existe um nivel com o nome '{nome}' (ID: {nivelExistente.nivel_id})")
                return
            
            # Criar novo nivel
            nivel = Nivel(nivel_id=None, corNivel=nome)
            nivelId = self.nivelDao.salvar(nivel)
            print(f"✅ Nivel criado com sucesso!")
            print(f"   ID: {nivelId}")
            print(f"   Nome: {nivel.corNivel}")
        
        except Exception as e:
            print(f"❌ Erro ao criar nível: {e}")

    def listarNiveis(self):
        """Lista todas as categorias cadastradas"""
        print("\n--- LISTAR TODOS OS NÍVEIS ---")
        
        try:
            niveis = self.nivelDao.listarTodas()
            
            if not niveis:
                print("⚠️  Nenhum nível cadastrado.")
                return
            
            print(f"\nTotal de níveis: {len(niveis)}")
            print("\n" + "-"*50)
            print(f"{'ID':<5} | {'Nome':<30}")
            print("-"*50)
            
            for nivel in niveis:
                print(f"{nivel.nivel_id:<5} | {nivel.corNivel:<30}")
            
            print("-"*50)
        
        except Exception as e:
            print(f"❌ Erro ao listar níveis: {e}")

    def buscarPorId(self):
        """Solicita um ID e busca a nivel correspondente"""
        print("\n--- BUSCAR NÍVEL POR ID ---")
        
        try:
            idStr = input("Digite o ID do nivel: ").strip()
            nivelId = int(idStr)
            
            nivel = self.nivelDao.buscarPorId(nivelId)
            
            if nivel:
                print("\n✅ Nivel encontrada:")
                print(f"   ID: {nivel.nivel_id}")
                print(f"   Nome: {nivel.corNivel}")
            else:
                print(f"⚠️  Nivel com ID {nivelId} não encontrada.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao buscar nível: {e}")

    def buscarPorNome(self):
        """Solicita um nome e busca a categoria correspondente"""
        print("\n--- BUSCAR NIVEL POR NOME ---")
        
        nome = input("Digite o nome do nivel: ").strip()
        
        if not nome:
            print("❌ Erro: O nome não pode ser vazio!")
            return
        
        try:
            nivel = self.nivelDao.buscarPorNome(nome)
            
            if nivel:
                print("\n✅ Nível encontrado:")
                print(f"   ID: {nivel.nivel_id}")
                print(f"   Nome: {nivel.corNivel}")
            else:
                print(f"⚠️  Nível '{nome}' não encontrado.")
        
        except Exception as e:
            print(f"❌ Erro ao buscar nível: {e}")

    def atualizarNivel(self):
        """Solicita dados do usuário e atualiza um nível existente"""
        print("\n--- ATUALIZAR NÍVEL ---")
        
        try:
            idStr = input("Digite o ID do nível a atualizar: ").strip()
            nivelId = int(idStr)
            
            # Buscar o nível existente
            nivel = self.nivelDao.buscarPorId(nivelId)
            
            if not nivel:
                print(f"⚠️  Nivel com ID {nivelId} não encontrado.")
                return
            
            print(f"\nNível atual:")
            print(f"   ID: {nivel.nivel_id}")
            print(f"   Nome: {nivel.corNivel}")
            
            novoNome = input("\nDigite o novo nome do nível (ou Enter para manter): ").strip()
            
            if not novoNome:
                print("⚠️  Operação cancelada. Nome não foi alterado.")
                return
            
            # Verificar se já existe outro nível com esse nome
            nivelExistente = self.nivelDao.buscarPorNome(novoNome)
            if nivelExistente and nivelExistente.nivel_id != nivelId:
                print(f"❌ Erro: Já existe outro nivel com o nome '{novoNome}' (ID: {nivelExistente.nivel_id})")
                return
            
            # Atualizar nivel
            nivel.corNivel = novoNome
            self.nivelDao.salvar(nivel)
            print(f"\n✅ Nível atualizado com sucesso!")
            print(f"   ID: {nivel.nivel_id}")
            print(f"   Nome: {nivel.corNivel}")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao atualizar nivel: {e}")

    def deletarNivel(self):
        """Solicita um ID e deleta o nível correspondente"""
        print("\n--- DELETAR NÍVEL ---")
        
        try:
            idStr = input("Digite o ID do nível a deletar: ").strip()
            nivelId = int(idStr)
            
            # Buscar o nível existente
            nivel = self.nivelDao.buscarPorId(nivelId)
            
            if not nivel:
                print(f"⚠️  Nível com ID {nivelId} não encontrado.")
                return
            
            print(f"\nNível a ser deletada:")
            print(f"   ID: {nivel.nivel_id}")
            print(f"   Nome: {nivel.corNivel}")
            
            confirmacao = input("\n⚠️  Tem certeza que deseja deletar este nível? (S/N): ").strip().lower()
            
            if confirmacao != 's':
                print("❌ Operação cancelada.")
                return
            
            sucesso = self.nivelDao.deletar(nivel)
            
            if sucesso:
                print(f"\n✅ Nível deletado com sucesso!")
            else:
                print(f"\n❌ Erro ao deletar nível.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao deletar nível: {e}")

    def executar(self):
        """Método principal que executa o loop do menu"""
        try:
            while True:
                self.exibirMenu()
                opcao = input("\nEscolha uma opção: ").strip()
                
                if opcao == '0':
                    print("\n👋 Encerrando o sistema...")
                    break
                elif opcao == '1':
                    self.criarNivel()
                elif opcao == '2':
                    self.listarNiveis()
                elif opcao == '3':
                    self.buscarPorId()
                elif opcao == '4':
                    self.buscarPorNome()
                elif opcao == '5':
                    self.atualizarNivel()
                elif opcao == '6':
                    self.deletarNivel()
                else:
                    print("❌ Opção inválida! Tente novamente.")
                
                input("\nPressione Enter para continuar...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Função principal para executar o serviço"""
    db = DatabaseConnection('exemplo_bd.db')
    
    try:
        # Conectar ao banco
        db.conectar()
        
        # Garantir que as tabelas existam
        db.criarTabelas()
        
        # Criar e executar o serviço
        service = NivelService(db)
        service.executar()
    
    except Exception as e:
        print(f"❌ Erro ao inicializar o sistema: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.fechar()
        print("✓ Conexão com banco de dados encerrada.")


if __name__ == "__main__":
    main()