# 🧪 Guia Prático de Testes - DevOps Study

**Última Atualização:** 2026-01-03

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Estrutura de Testes](#estrutura)
4. [Executando Testes](#executando)
5. [Escrevendo Novos Testes](#escrevendo)
6. [CI/CD Integration](#cicd)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral {#visão-geral}

O projeto possui **50+ testes unitários** cobrindo:

| Componente | Testes | Cobertura |
|-----------|--------|-----------|
| **TradingService** | 32 | Indicadores, Decisões, Insights |
| **SnapshotAcao** | 10 | Mapeamento, Validação |
| **AggregatorService** | 12 | Agregação, Cálculos |
| **E2E Flow** | 5+ | Fluxo Completo |
| **TOTAL** | **59** | ✅ |

---

## 💻 Instalação {#instalação}

### Pré-requisitos

```bash
# Python 3.11+
python --version

# Pip
pip --version
```

### Instalar Dependências

```bash
# Navegar para o diretório
cd gerar-insights

# Instalar requirements
pip install -r requirements.txt

# Instalar ferramentas de teste
pip install pytest pytest-mock pytest-cov
```

### Verificar Instalação

```bash
# Verificar pytest
pytest --version

# Verificar imports do projeto
python -c "from app.core.service.trading_service import TradingService; print('✅ OK')"
```

---

## 📂 Estrutura de Testes {#estrutura}

```
gerar-insights/
└── tests/
    ├── conftest.py                    # Fixtures compartilhadas
    ├── test_trading_service.py        # 32 testes
    ├── test_snapshot_mapper.py        # 10 testes
    ├── test_aggregator_service.py     # 12 testes
    └── test_e2e_flow.py              # 5+ testes
```

### Convenções

```python
# Nomes de arquivos de teste
test_<module>.py

# Nomes de classes de teste
Test<Feature>

# Nomes de funções de teste
def test_<funcionalidade>_<esperado>():
    """Descrição clara do teste"""

# Exemplo
def test_calcular_indicadores_returns_dict():
    """Testa se calcular_indicadores retorna um dicionário"""
```

---

## 🚀 Executando Testes {#executando}

### Executar Todos os Testes

```bash
# Modo simples
pytest tests/

# Modo verboso (recomendado)
pytest tests/ -v

# Com output detalhado
pytest tests/ -v -s
```

### Executar Arquivo Específico

```bash
# Todos os testes de trading_service
pytest tests/test_trading_service.py -v

# Todos os testes de mapper
pytest tests/test_snapshot_mapper.py -v
```

### Executar Teste Específico

```bash
# Teste individual
pytest tests/test_trading_service.py::TestTradingService::test_decisao_comprar -v

# Com output
pytest tests/test_trading_service.py::TestTradingService::test_decisao_comprar -v -s
```

### Executar por Padrão

```bash
# Testes de decisão
pytest tests/ -k "decisao" -v

# Testes que retornam algo
pytest tests/ -k "retorna" -v

# Testes de ativo buy
pytest tests/ -k "buy" -v
```

### Executar com Coverage

```bash
# Coverage geral
pytest tests/ --cov=app --cov-report=term-missing

# Gerar relatório HTML
pytest tests/ --cov=app --cov-report=html
# Abrir: htmlcov/index.html
```

### Executar com Timeout

```bash
# Timeout de 10s por teste
pytest tests/ -v --timeout=10
```

---

## ✍️ Escrevendo Novos Testes {#escrevendo}

### Estrutura Básica

```python
import pytest
from app.core.service.trading_service import TradingService

class TestMinhaFuncionalidade:
    """Agrupa testes relacionados"""
    
    @pytest.fixture
    def service(self):
        """Setup compartilhado"""
        return TradingService()
    
    def test_meu_teste(self, service):
        """Testa algo específico"""
        # Arrange
        ativo = {"symbol": "PETR4", ...}
        
        # Act
        resultado = service.processar_ativo(ativo)
        
        # Assert
        assert resultado is not None
```

### Fixtures Úteis

```python
# Fixture simples
@pytest.fixture
def ativo_completo():
    return {
        "symbol": "PETR4",
        "regularMarketPrice": 30.0,
        ...
    }

# Fixture com setup/teardown
@pytest.fixture
def database():
    # Setup
    db = DatabaseService()
    db.connect()
    
    yield db  # Teste usa db aqui
    
    # Teardown
    db.disconnect()

# Fixture de parametrização
@pytest.fixture(params=[10, 20, 30])
def quantidade(request):
    return request.param
```

### Assertions Comuns

```python
# Igualdade
assert resultado == esperado
assert len(lista) == 5

# Tipo
assert isinstance(resultado, dict)
assert isinstance(insights, list)

# Conteúdo
assert "COMPRAR" in decisoes
assert any("barata" in i for i in insights)

# Comparação
assert resultado > 0
assert resultado >= 12

# None
assert resultado is not None
assert resultado is None

# Exceções
with pytest.raises(ValueError):
    funcao_invalida()
```

---

## 🔄 CI/CD Integration {#cicd}

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd gerar-insights
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        cd gerar-insights
        pytest tests/ -v --cov=app
```

### Local Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
cd gerar-insights
pytest tests/ --tb=short
if [ $? -ne 0 ]; then
    echo "❌ Testes falharam! Não é permitido fazer commit."
    exit 1
fi
```

---

## 🔧 Troubleshooting {#troubleshooting}

### Erro: "No module named 'pytest'"

```bash
# Solução
pip install pytest
```

### Erro: "ModuleNotFoundError: No module named 'app'"

```bash
# Solução: Execute do diretório correto
cd gerar-insights
pytest tests/ -v
```

### Erro: "ImportError: cannot import name 'TradingService'"

```bash
# Verificar se o arquivo existe
ls -la app/core/service/trading_service.py

# Verificar __init__.py
ls -la app/__init__.py
ls -la app/core/__init__.py
```

### Testes Lentos

```bash
# Executar testes rápidos apenas
pytest tests/ -m "not slow" -v

# Medir tempo de execução
pytest tests/ -v --durations=10
```

### Falha em Teste Aleatório

```bash
# Registrar seed de aleatoriedade
pytest tests/ -v --randomly-seed=12345

# Usar seed específico
pytest tests/ -v --randomly-seed=12345
```

---

## 📊 Exemplos de Testes

### ✅ Teste Bem-Escrito

```python
def test_decisao_comprar_com_earnings_yield_alto(self, service, sample_ativo_buy):
    """
    Testa decisão COMPRAR quando earnings_yield > 12%
    
    Contexto:
        - Ativo com P/L baixo (8.0) e LPA alto (4.0)
        - Preço atual: 30.0
        - Esperado: earnings_yield = 13.33%
    
    Resultado esperado:
        - Decisão deve ser "COMPRAR"
    """
    indicadores = service.calcular_indicadores(sample_ativo_buy)
    decisao = service.calcular_decisao(indicadores)
    
    assert indicadores["earnings_yield"] > 12
    assert decisao == "COMPRAR"
```

### ❌ Teste Mal-Escrito

```python
def test_service(self):
    # ❌ Não está claro o que está testando
    # ❌ Sem descrição
    # ❌ Sem dados de exemplo
    # ❌ Sem assertions claras
    x = TradingService()
    y = x.processar_ativo({})
    assert y is not None
```

---

## 📈 Métricas de Teste

### Executar com Metricas

```bash
# Coverage percentage
pytest tests/ --cov=app --cov-report=term-missing

# Duração de testes
pytest tests/ -v --durations=5
```

### Target de Coverage

| Componente | Target | Atual |
|-----------|--------|-------|
| **trading_service.py** | 90% | ✅ |
| **aggregator_service.py** | 85% | ✅ |
| **snapshot_mapper.py** | 95% | ✅ |
| **Overall** | 80% | ✅ |

---

## 🎓 Recursos Adicionais

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [unittest vs pytest](https://docs.pytest.org/en/6.2.x/unittest.html)

---

## 📝 Checklist Antes de Fazer Push

- [ ] Todos os testes passam: `pytest tests/ -v`
- [ ] Coverage está aceitável: `pytest tests/ --cov=app`
- [ ] Sem warnings: `pytest tests/ -v --tb=short`
- [ ] Código segue padrão: `flake8 app/`
- [ ] Type hints corretos: `mypy app/`

---

**Última atualização:** 2026-01-03  
**Mantido por:** GitHub Copilot

