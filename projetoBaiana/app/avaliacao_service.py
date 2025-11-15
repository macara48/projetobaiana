"""
Serviço para interação do usuário via linha de comando com a entidade avaliacao
"""
import sys
import os

# Adicionar o diretório pai ao path para permitir imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bd.database import DatabaseConnection
from dao.avaliacao_dao import AvaliacaoDAO
from model.avaliacao_class import Avaliacao


class AvaliacaoService:
    
    def __init__(self, db: DatabaseConnection):
        self.__db = db
        self.__avaliacaoDao = AvaliacaoDAO(db)
    
    def exibirMenu(self):
        """Exibe o menu principal de opções"""
        print("\n" + "="*50)
        print("  SISTEMA DE GERENCIAMENTO DE AVALIAÇÕES")
        print("="*50)
        print("1. Criar avaliação")
        print("2. Listar todas as avaliação")
        print("3. Buscar avaliação por ID")
        print("4. Buscar avaliação por data")
        print("5. Atualizar avaliação")
        print("6. Deletar avaliação")
        print("0. Sair")
        print("="*50)
    
    def criarAvaliacao(self):
        """Solicita dados do usuário e cria uma nova avaliacao"""
        print("\n--- CRIAR AVALIAÇÕES ---")
        data = input("Digite a data da valiacao: ").strip()
        
        if not data:
            print("❌ Erro: A data da valiacao não pode ser vazio!")
            return
        
        try:
            # Verificar se já existe um parâmetro com esse data
            avaliacaoExistente = self.__avaliacaoDao.buscarPorData(data)
            if avaliacaoExistente:
                print(f"❌ Erro: Já existe uma avaliacao com o data '{data}' (ID: {avaliacaoExistente.id})")
                return
            
            # Criar nova avaliacao
            avaliacao = Avaliacao(id=None, data=data)
            avaliacaoId = self.__avaliacaoDao.salvar(avaliacao)
            print(f"✅ Avaliacao criada com sucesso!")
            print(f"   ID: {avaliacaoId}")
            print(f"   Data: {avaliacao.data}")
        
        except Exception as e:
            print(f"❌ Erro ao criar avaliacao: {e}")
    
    def listarAvaliacao(self):
        """Lista todas as avaliações cadastradas"""
        print("\n--- LISTAR TODAS AS AVALIAÇÕES ---")
        
        try:
            avaliacoes = self.__avaliacaoDao.listarTodas()
            
            if not avaliacoes:
                print("⚠️  Nenhuma avaliacao cadastrada.")
                return
            
            print(f"\nTotal de avaliacoes: {len(avaliacoes)}")
            print("\n" + "-"*50)
            print(f"{'ID':<5} | {'Data':<30}")
            print("-"*50)
            
            for avaliacao in avaliacoes:
                print(f"{avaliacao.id:<5} | {avaliacao.data:<10}")
            
            print("-"*50)
        
        except Exception as e:
            print(f"❌ Erro ao listar avaliacoes: {e}")
    
    def buscarPorId(self):
        """Solicita um ID e busca a avaliacao correspondente"""
        print("\n--- BUSCAR AVALIACAO POR ID ---")
        
        try:
            idStr = input("Digite o ID da avaliacao: ").strip()
            avaliacaoId = int(idStr)
            
            avaliacao = self.__avaliacaoDao.buscarPorId(avaliacaoId)
            
            if avaliacao:
                print("\n✅ Avaliacao encontrada:")
                print(f"   ID: {avaliacao.id}")
                print(f"   Data: {avaliacao.data}")
            else:
                print(f"⚠️  Avaliacao com ID {avaliacaoId} não encontrada.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao buscar avaliacao: {e}")
    
    def buscarPorData(self):
        """Solicita um data e busca a avaliacao correspondente"""
        print("\n--- BUSCAR AVALIACAO POR DATA ---")
        
        data = input("Digite o data do avaliacao: ").strip()
        
        if not data:
            print("❌ Erro: O data não pode ser vazio!")
            return
        
        try:
            avaliacao = self.__avaliacaoDao.buscarPorData(data)
            
            if avaliacao:
                print("\n✅ Avaliacao encontrada:")
                print(f"   ID: {avaliacao.id}")
                print(f"   Data: {avaliacao.data}")
            else:
                print(f"⚠️  Avaliacao '{data}' não encontrada.")
        
        except Exception as e:
            print(f"❌ Erro ao buscar avaliacao: {e}")
    
    def atualizarAvaliacao(self):
        """Solicita dados do usuário e atualiza uma avaliacao existente"""
        print("\n--- ATUALIZAR AVALIACAO ---")
        
        try:
            idStr = input("Digite o ID da avaliacao a atualizar: ").strip()
            avaliacaoId = int(idStr)
            
            # Buscar a avaliacao existente
            avaliacao = self.__avaliacaoDao.buscarPorId(avaliacaoId)
            
            if not avaliacao:
                print(f"⚠️  Categoria com ID {avaliacaoId} não encontrada.")
                return
            
            print(f"\nAvaliacao atual:")
            print(f"   ID: {avaliacao.id}")
            print(f"   Data: {avaliacao.data}")
            
            novaData = input("\nDigite a nova data do avaliacao (ou Enter para manter): ").strip()
            
            if not novaData:
                print("⚠️  Operação cancelada. Data não foi alterado.")
                return
            
            # Verificar se já existe outra avaliacao com esse data
            avaliacaoExistente = self.__avaliacaoDao.buscarPorData(novaData)
            if avaliacaoExistente and avaliacaoExistente.id != avaliacaoId:
                print(f"❌ Erro: Já existe outra avaliacao com o data '{novaData}' (ID: {avaliacaoExistente.id})")
                return
            
            # Atualizar avaliacao
            avaliacao.data = novaData
            self.__avaliacaoDao.salvar(avaliacao)
            print(f"\n✅ Avaliacao atualizada com sucesso!")
            print(f"   ID: {avaliacao.id}")
            print(f"   Data: {avaliacao.data}")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao atualizar avaliacao: {e}")
    
    def deletarAvaliacao(self):
        """Solicita um ID e deleta a avaliacao correspondente"""
        print("\n--- DELETAR AVALIACAO ---")
        
        try:
            idStr = input("Digite o ID da avaliacao a deletar: ").strip()
            avaliacaoId = int(idStr)
            
            # Buscar a avaliacao existente
            avaliacao = self.__avaliacaoDao.buscarPorId(avaliacaoId)
            
            if not avaliacao:
                print(f"⚠️  Avaliacao com ID {avaliacaoId} não encontrada.")
                return
            
            print(f"\nAvaliacao a ser deletada:")
            print(f"   ID: {avaliacao.id}")
            print(f"   Data: {avaliacao.data}")
            
            confirmacao = input("\n⚠️  Tem certeza que deseja deletar esta avaliacao? (s/N): ").strip().lower()
            
            if confirmacao != 's':
                print("❌ Operação cancelada.")
                return
            
            sucesso = self.__avaliacaoDao.deletar(avaliacao)
            
            if sucesso:
                print(f"\n✅ Avaliacao deletada com sucesso!")
            else:
                print(f"\n❌ Erro ao deletar avaliacao.")
        
        except ValueError:
            print("❌ Erro: ID deve ser um número inteiro!")
        except Exception as e:
            print(f"❌ Erro ao deletar avaliacao: {e}")
    
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
                    self.criarAvaliacao()
                elif opcao == '2':
                    self.listarAvaliacao()
                elif opcao == '3':
                    self.buscarPorId()
                elif opcao == '4':
                    self.buscarPorData()
                elif opcao == '5':
                    self.atualizarAvaliacao()
                elif opcao == '6':
                    self.deletarAvaliacao()
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
        service = AvaliacaoService(db)
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