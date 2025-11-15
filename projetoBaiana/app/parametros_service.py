"""
Serviço para interação do usuário via linha de comando com a entidade parametros
"""
import sys
import os

# Adicionar o diretório pai ao path para permitir imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bd.database import DatabaseConnection
from dao.parametros_dao import ParametrosDAO
from model.parametros_class import Parametros


class ParametrosService:
    
    def __init__(self, db: DatabaseConnection):
        self.__db = db
        self.__parametrosDao = ParametrosDAO(db)
    
    def exibirMenu(self):
        """Exibe o menu principal de opções"""
        print("\n" + "="*50)
        print("  SISTEMA DE GERENCIAMENTO DE PARÂMETROS")
        print("="*50)
        print("1. Criar parâmetro")
        print("2. Listar todos os parâmetros")
        print("3. Buscar parâmetro por ID")
        print("4. Buscar parâmetro por nome")
        print("5. Atualizar parâmetro")
        print("6. Deletar parâmetro")
        print("0. Sair")
        print("="*50)
    
    def criarParametro(self):
        """Solicita dados do usuário e cria uma nova parametro"""
        print("\n--- CRIAR PARÂMETROS ---")
        nome = input("Digite o nome da parâmetro: ").strip()
        
        if not nome:
            print("❌ Erro: O nome da parâmetro não pode ser vazio!")
            return
        
        try:
            # Verificar se já existe um parâmetro com esse nome
            parametroExistente = self.__parametrosDao.buscarPorNome(nome)
            if parametroExistente:
                print(f"❌ Erro: Já existe um parametro com o nome '{nome}' (ID: {parametroExistente.id})")
                return
            
            # Criar novo parametro
            parametro = Parametros(id=None, nome=nome)
            parametroId = self.__parametrosDao.salvar(parametro)
            print(f"✅ Parametro criada com sucesso!")
            print(f"   ID: {parametroId}")
            print(f"   Nome: {parametro.nome}")
        
        except Exception as e:
            print(f"❌ Erro ao criar parametro: {e}")
    
    def listarNiveis(self):
        """Lista todas as niveis cadastradas"""
        print("\n--- LISTAR TODOS OS NIVEIS ---")
        
        try:
            parametros = self.__parametrosDao.listarTodas()
            
            if not parametros:
                print("⚠️  Nenhum parametro cadastrada.")
                return
            
            print(f"\nTotal de niveis: {len(parametros)}")
            print("\n" + "-"*50)
            print(f"{'ID':<5} | {'Nome':<30}")
            print("-"*50)
            
            for parametro in parametros:
                print(f"{parametro.id:<5} | {parametro.nome:<30}")
            
            print("-"*50)
        
        except Exception as e:
            print(f"❌ Erro ao listar parametros: {e}")
    
    def buscarPorId(self):
        """Solicita um ID e busca a parametro correspondente"""
        print("\n--- BUSCAR PARAMETRO POR ID ---")
        
        try:
            idStr = input("Digite o ID da parametro: ").strip()
            parametroId = int(idStr)
            
            parametro = self.__parametrosDao.buscarPorId(parametroId)
            
            if parametro:
                print("\n✅ Parametro encontrada:")
                print(f"   ID: {parametro.id}")
                print(f"   Nome: {parametro.nome}")
            else:
                print(f"⚠️  Parametro com ID {parametroId} não encontrada.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao buscar parametro: {e}")
    
    def buscarPorNome(self):
        """Solicita um nome e busca a parametro correspondente"""
        print("\n--- BUSCAR PARAMETRO POR NOME ---")
        
        nome = input("Digite o nome do parametro: ").strip()
        
        if not nome:
            print("❌ Erro: O nome não pode ser vazio!")
            return
        
        try:
            parametro = self.__parametrosDao.buscarPorNome(nome)
            
            if parametro:
                print("\n✅ Parametro encontrada:")
                print(f"   ID: {parametro.id}")
                print(f"   Nome: {parametro.nome}")
            else:
                print(f"⚠️  Parametro '{nome}' não encontrada.")
        
        except Exception as e:
            print(f"❌ Erro ao buscar parametro: {e}")
    
    def atualizarParametro(self):
        """Solicita dados do usuário e atualiza uma parametro existente"""
        print("\n--- ATUALIZAR PARAMETRO ---")
        
        try:
            idStr = input("Digite o ID da parametro a atualizar: ").strip()
            parametroId = int(idStr)
            
            # Buscar a parametro existente
            parametro = self.__parametrosDao.buscarPorId(parametroId)
            
            if not parametro:
                print(f"⚠️  Categoria com ID {parametroId} não encontrada.")
                return
            
            print(f"\nParametro atual:")
            print(f"   ID: {parametro.id}")
            print(f"   Nome: {parametro.nome}")
            
            novoNome = input("\nDigite o novo nome do parametro (ou Enter para manter): ").strip()
            
            if not novoNome:
                print("⚠️  Operação cancelada. Nome não foi alterado.")
                return
            
            # Verificar se já existe outra parametro com esse nome
            parametroExistente = self.__parametrosDao.buscarPorNome(novoNome)
            if parametroExistente and parametroExistente.id != parametroId:
                print(f"❌ Erro: Já existe outra parametro com o nome '{novoNome}' (ID: {parametroExistente.id})")
                return
            
            # Atualizar parametro
            parametro.nome = novoNome
            self.__parametrosDao.salvar(parametro)
            print(f"\n✅ Parametro atualizada com sucesso!")
            print(f"   ID: {parametro.id}")
            print(f"   Nome: {parametro.nome}")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao atualizar parametro: {e}")
    
    def deletarParametro(self):
        """Solicita um ID e deleta a parametro correspondente"""
        print("\n--- DELETAR PARAMETRO ---")
        
        try:
            idStr = input("Digite o ID da parametro a deletar: ").strip()
            parametroId = int(idStr)
            
            # Buscar a parametro existente
            parametro = self.__parametrosDao.buscarPorId(parametroId)
            
            if not parametro:
                print(f"⚠️  Parametro com ID {parametroId} não encontrada.")
                return
            
            print(f"\nParametro a ser deletada:")
            print(f"   ID: {parametro.id}")
            print(f"   Nome: {parametro.nome}")
            
            confirmacao = input("\n⚠️  Tem certeza que deseja deletar esta parametro? (s/N): ").strip().lower()
            
            if confirmacao != 's':
                print("❌ Operação cancelada.")
                return
            
            sucesso = self.__parametrosDao.deletar(parametro)
            
            if sucesso:
                print(f"\n✅ Parametro deletada com sucesso!")
            else:
                print(f"\n❌ Erro ao deletar parametro.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao deletar parametro: {e}")
    
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
                    self.criarParametro()
                elif opcao == '2':
                    self.listarParametros()
                elif opcao == '3':
                    self.buscarPorId()
                elif opcao == '4':
                    self.buscarPorNome()
                elif opcao == '5':
                    self.atualizarParametro()
                elif opcao == '6':
                    self.deletarParametro()
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
        service = ParametrosService(db)
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

