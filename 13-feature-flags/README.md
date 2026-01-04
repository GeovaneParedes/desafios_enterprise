# Day 13: Feature Flags (Toggles)

Implementação de um sistema de **Feature Flags** para desacoplar o Deploy (instalação de código) do Release (liberação de funcionalidade).

Este padrão permite ativação gradual de recursos (Canary Releases), testes A/B e Rollbacks instantâneos sem necessidade de novo deploy.

## 🚀 Funcionalidades

### 1. Estratégias de Ativação
* **Boolean:** Liga/Desliga global (ex: "Modo Manutenção").
* **User Targeting:** Liberação para usuários específicos (ex: Developers, QA, Beta Testers).
* **Percentage Rollout (Canary):** Liberação para X% da base de usuários baseada em Hash determinístico.

### 2. Determinismo (Stickiness)
* Utiliza Hash MD5 do ID do usuário para garantir que um usuário selecionado para o grupo de teste permaneça nele consistentemente, independente de reinícios do servidor.

### 3. Configuração Dinâmica
* As regras são lidas de um arquivo JSON externo (`flags.json`), simulando um painel de controle que pode ser atualizado em tempo de execução.

## 🛠️ Tecnologias

* **Python 3.11+**
* **Hashlib** (Distribuição uniforme de usuários)
* **Pytest** (Validação estatística e lógica)

## 📂 Estrutura do Projeto

```text
src/
├── manager.py     # Gerenciador que carrega configs e avalia regras
├── strategies.py  # Implementação das lógicas (Boolean, UserList, Percentage)
└── main.py        # Simulação visual de diferentes cenários
flags.json         # Arquivo de configuração das regras
tests/
└── test_flags.py  # Testes de determinismo e distribuição estatística
```

## ⚡ Como Executar

## 1. Instalação

```bash
make install
```

## 2. Simulação Visual

Veja como diferentes usuários (customer_0 a customer_19) são afetados pelas regras.

```bash
make run
```

## 3. Rodar Testes

Valida se a distribuição percentual está correta em grande escala (1000 usuários).

```bash
make test
```

