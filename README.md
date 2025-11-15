# 🎓 Sistema de Avaliação para a **Escola de Dança Baianá** – **Projeto Back-End Python Orientado a Objetos: Bolsa Futuro Digital**  
---
<div style= 'text-align: justify'>A escola de dança Baianá possui o propósito de divulgar o ensino do forró na região e preservar a história dessa dança tradicional. No entanto, observou-se que os processos de avaliação e organização de eventos na escola são realizados manualmente, sem nenhum sistema automatizado, o que dificulta a gestão das informações. Nesse contexto, este projeto foi desenvolvido para solucionar este problema, criou-se um banco de dados estruturado, para registrar informações sobre os alunos e suas atividades, contribuindo para a preservação da memória da escola e, consequentemente, da identidade cultural nordestina.</div>
---

**Como instalar esse projeto?**

## 👥 Equipe
- Iandra Santos Lacerda
- Maria Clara dos Santos Pires
- Tarcísio Côrtes Viana
- Yuri Lima

**Orientador:** Prof. Cláudio Rodolfo Sousa de Oliveira

---


# 📄 Documentação do Modelo de Domínio: Sistema de Avaliação de Dança

Este documento descreve o **Modelo de Entidade-Relacionamento (ERD)** e as **Regras de Negócio** subjacentes ao sistema de avaliação, conforme representado no diagrama conceitual. Ele é essencial para a implementação e manutenção do banco de dados e da lógica de negócio da aplicação.

---

## 1. 🎨 Diagrama de Classes/Entidades

O diagrama ilustra as entidades principais do sistema e as associações entre elas, usando as seguintes convenções de cor para as relações:

<img width="970" height="556" alt="Captura de tela 2025-11-14 222047" src="https://github.com/user-attachments/assets/3b06210a-59de-4309-acf5-97a2bdef4fae" />

* **⚫ Preto:** Relação de **Agregação** (Associação fraca - as entidades podem existir de forma independente).
* **🔴 Vermelho:** Relação de **Composição** (Associação forte - a entidade parte não existe sem a entidade todo).



---

## 2. 📚 Dicionário de Dados (Entidades e Atributos)

Abaixo estão as tabelas (Entidades) e suas respectivas colunas (Atributos), incluindo as chaves primárias (PK) e estrangeiras (FK).

| Entidade | Atributo (Coluna) | Tipo de Chave | Descrição e Notas |
| :--- | :--- | :--- | :--- |
| **nivel** | `nivel_id` | PK | Identificador único do nível (Ex: Básico, Avançado). |
| | `confNivel` | | Nome do nível. |
| **estiloDanca** | `estilo_id` | PK | Identificador único do estilo de dança. |
| | `estilo` | | Nome do estilo. |
| **evento** | `evento_id` | PK | Identificador único do evento de avaliação. |
| | `dataEvento` | | Data de realização do evento. |
| **examinador** | `examinador_id` | PK | Identificador único do examinador/juiz. |
| | `nome` | | Nome completo do examinador. |
| **aluno** | `aluno_id` | PK | Identificador único do aluno. |
| | `nome` | | Nome completo do aluno. |
| | `nivel_id` | FK | Liga ao nível do aluno. |
| | `estilo_id` | FK | Liga ao estilo principal do aluno. |
| **parametros** | `parametro_id` | PK | Identificador único do critério de avaliação (Ex: Ritmo, Técnica). |
| | `parametro` | | Nome do parâmetro. |
| | `estilo_id` | FK | Liga ao estilo de dança. |
| | `nivel_id` | FK | Liga ao nível de dificuldade. |
| **avaliacao** | `ava_id` | PK | Identificador único da avaliação. |
| | `data` | | Data da avaliação. |
| | `aluno_id` | FK | Liga ao aluno avaliado. |
| | `examinador_id` | FK | Liga ao examinador responsável. |
| | `evento_id` | FK | Liga ao evento. |
| **itmAvaliacao** | `ava_id`, `parametro_id` | PK (Composta) | Identifica um item de avaliação (nota específica). |
| | `nota` | | Nota ou pontuação dada para o parâmetro. |

---

## 3. ⚖️ Regras de Negócio e Relacionamentos

As regras de negócio definem as restrições e a lógica de persistência do sistema.

### 3.1. Relações de Composição (🔴 Associação Forte)

A Composição implica uma dependência de ciclo de vida: a "parte" é removida se o "todo" for removido (**Exclusão em Cascata**).

| Relacionamento (Todo $\rightarrow$ Parte) | Cardinalidade | Regra de Negócio |
| :--- | :--- | :--- |
| **`aluno`** $\rightarrow$ **`avaliacao`** | 1 $\rightarrow$ (0, n) | Uma avaliação **pertence estritamente** a um aluno. Se um aluno for excluído, **todas** as suas avaliações históricas devem ser removidas do sistema. |
| **`avaliacao`** $\rightarrow$ **`itmAvaliacao`** | 1 $\rightarrow$ (0, n) | Um item de avaliação (nota) **existe apenas** no contexto de uma avaliação. A exclusão de uma avaliação implica na remoção de **todos** os seus itens detalhados. |
| **`nivel/estilo`** $\rightarrow$ **`parametros`** | 1 $\rightarrow$ (0, n) | Um parâmetro é **definido** para um nível e estilo específicos. A exclusão de um `nivel` ou `estiloDanca` deve resultar na exclusão dos `parametros` exclusivos relacionados. |

### 3.2. Relações de Agregação (⚫ Associação Fraca)

A Agregação indica que as entidades podem existir de forma independente. A remoção do "todo" **não** causa a remoção da "parte".

| Relacionamento (Todo $\rightarrow$ Parte) | Cardinalidade | Regra de Negócio |
| :--- | :--- | :--- |
| **`evento`** $\rightarrow$ **`avaliacao`** | 1 $\rightarrow$ (0, n) | Um evento **fornece o contexto** para a avaliação. Se um evento for excluído, as avaliações associadas **devem ser mantidas** para fins históricos, e o campo `evento_id` pode ser definido como `NULL`. |
| **`examinador`** $\rightarrow$ **`avaliacao`** | 1 $\rightarrow$ (0, n) | Um examinador é uma entidade independente que **realiza** avaliações. Se um examinador for removido do cadastro, as avaliações que ele conduziu **devem ser preservadas**. |
| **`aluno`** $\rightarrow$ **`nivel/estiloDanca`** | (0, n) $\rightarrow$ (1, 1) | Embora o aluno possa mudar de nível ou estilo, o sistema **exige** que ele sempre esteja associado a um Nível e Estilo de Dança válidos (Obrigatório). |

### 3.3. Regras de Integridade de Chave Composta

* **Unicidade do Item de Avaliação:** Para a entidade **`itmAvaliacao`**, a combinação de (`ava_id`, `parametro_id`) é única. Isso garante que um examinador só pode atribuir **uma única nota** para um parâmetro dentro de uma avaliação específica.
* **Unicidade do Parâmetro:** Para a entidade **`parametros`**, a combinação de (`estilo_id`, `nivel_id`, `parametro`) deve ser única, garantindo que não haja critérios de avaliação duplicados para o mesmo contexto.

  # 🏆 Sistema de Gerenciamento de Avaliação de Dança

## 🌟 Resumo do Projeto

Este projeto consiste em um sistema back-end para **gerenciar, registrar e consultar avaliações de performances de dança** em eventos e escolas.

O objetivo principal é fornecer uma plataforma estruturada para:

1.  **Modelagem e Cadastro** de entidades chave: **Alunos**, **Examinadores**, **Níveis**, **Estilos de Dança** e **Eventos**.
2.  **Criação de Avaliações Detalhadas**: Permitindo que Examinadores registrem notas (`itmAvaliacao`) para múltiplos **Parâmetros** (critérios como Ritmo, Técnica, Expressão), que são específicos para cada **Nível** e **Estilo de Dança**.
3.  **Garantia da Integridade dos Dados**: O sistema foi construído com regras de **Composição** e **Agregação** estritas (conforme detalhado no ERD), garantindo que os dados de performance histórica sejam rastreáveis e consistentes.


