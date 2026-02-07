"""
Detecção automática de ambiente (Local vs Docker)
e configuração inteligente do banco de dados.

Estratégias de detecção (em ordem de prioridade):
1. Variável de ambiente ENVIRONMENT (pode ser definida no docker-compose)
2. Arquivo /.dockerenv (presente em containers Docker)
3. Arquivo /proc/self/cgroup (contém 'docker' ou 'podman')
4. Hostname do container (diferente da máquina local)
"""
import os
import socket
from app.config.config_logger import setup_logger

logger = setup_logger()


def is_in_docker() -> bool:
    """
    Detecta se a aplicação está rodando dentro de um container Docker.

    Estratégias usadas:
    1. Variável ENVIRONMENT=docker (define explicitamente no docker-compose)
    2. Arquivo /.dockerenv (indicador padrão do Docker)
    3. Cgroup contendo 'docker' ou 'podman'
    4. Hostname diferente (container tem hostname único)

    Returns:
        bool: True se está em Docker, False caso contrário
    """

    # Estratégia 1: Variável de ambiente explícita (MAIS CONFIÁVEL)
    # Define no docker-compose: ENVIRONMENT=docker
    environment = os.getenv('ENVIRONMENT', '').lower()
    if environment == 'docker':
        logger.info("🐳 Ambiente detectado: DOCKER (variável ENVIRONMENT=docker)")
        return True

    # Estratégia 2: Arquivo específico do Docker
    if os.path.exists('/.dockerenv'):
        logger.info("🐳 Ambiente detectado: DOCKER (/.dockerenv presente)")
        return True

    # Estratégia 3: Cgroup do Docker/Podman
    try:
        with open('/proc/self/cgroup', 'r') as cgroup_file:
            content = cgroup_file.read()
            if 'docker' in content.lower() or 'podman' in content.lower() or 'lxc' in content.lower():
                logger.info("🐳 Ambiente detectado: DOCKER (cgroup detectado)")
                return True
    except (FileNotFoundError, IOError):
        # Normal em Windows/macOS - prossegue para próxima verificação
        pass

    # Estratégia 4: Hostname diferente (container Docker tem hostname aleatório)
    try:
        hostname = socket.gethostname()
        # Containers Docker geralmente têm hostnames hexadecimais ou específicos
        # Máquinas locais geralmente têm nomes legíveis
        if len(hostname) == 12 and all(c in '0123456789abcdef' for c in hostname.lower()):
            logger.info(f"🐳 Ambiente detectado: DOCKER (hostname Docker: {hostname})")
            return True
    except Exception as e:
        logger.debug(f"Erro ao verificar hostname: {e}")

    # Se chegou aqui, está em ambiente local
    logger.info("💻 Ambiente detectado: LOCAL")
    return False


def detect_db_host() -> str:
    """
    Detecta automaticamente o host do banco de dados baseado no ambiente.

    Returns:
        str: 'mysql' para Docker, 'localhost' para local
    """
    # Primeiro, tenta usar variável de ambiente se definida explicitamente
    db_host = os.getenv('DB_HOST')
    if db_host:
        logger.info(f"🗄️  DB_HOST obtido da variável de ambiente: {db_host}")
        return db_host

    # Se não definida, detecta automaticamente
    if is_in_docker():
        # Em Docker, usar o nome do serviço
        db_host = 'mysql'
        logger.info(f"🗄️  DB_HOST automático (Docker): {db_host}")
    else:
        # Em local, usar localhost
        db_host = 'localhost'
        logger.info(f"🗄️  DB_HOST automático (Local): {db_host}")

    return db_host


def detect_db_port() -> str:
    """
    Detecta automaticamente a porta do banco de dados baseado no ambiente.

    Returns:
        str: '3306' para Docker, '3305' para local
    """
    # Primeiro, tenta usar variável de ambiente se definida
    db_port = os.getenv('DB_PORT')
    if db_port:
        logger.info(f"🗄️  DB_PORT obtido da variável de ambiente: {db_port}")
        return db_port

    # Se não definida, detecta automaticamente
    if is_in_docker():
        # Em Docker, usar a porta interna
        db_port = '3306'
        logger.info(f"🗄️  DB_PORT automático (Docker): {db_port}")
    else:
        # Em local, usar a porta mapeada
        db_port = '3305'
        logger.info(f"🗄️  DB_PORT automático (Local): {db_port}")

    return db_port


def detect_localstack_endpoint() -> str:
    """
    Detecta automaticamente o endpoint do LocalStack baseado no ambiente.

    Returns:
        str: 'http://localstack:4566' para Docker, 'http://localhost:4566' para local
    """
    # Primeiro, tenta usar variável de ambiente se definida
    endpoint = os.getenv('LOCALSTACK_ENDPOINT')
    if endpoint:
        logger.info(f"☁️  LOCALSTACK_ENDPOINT obtido da variável de ambiente: {endpoint}")
        return endpoint

    # Se não definida, detecta automaticamente
    if is_in_docker():
        # Em Docker, usar o nome do serviço
        endpoint = 'http://localstack:4566'
        logger.info(f"☁️  LOCALSTACK_ENDPOINT automático (Docker): {endpoint}")
    else:
        # Em local, usar localhost
        endpoint = 'http://localhost:4566'
        logger.info(f"☁️  LOCALSTACK_ENDPOINT automático (Local): {endpoint}")

    return endpoint


def test_db_connectivity(host: str, port: str) -> bool:
    """
    Testa se é possível conectar ao banco de dados via socket.

    Args:
        host (str): Hostname do banco
        port (str): Porta do banco

    Returns:
        bool: True se conectar, False caso contrário
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, int(port)))
        sock.close()

        if result == 0:
            logger.debug(f"✅ Socket conectado: {host}:{port}")
            return True
        else:
            logger.debug(f"❌ Socket não conectou: {host}:{port}")
            return False
    except Exception as e:
        logger.debug(f"❌ Erro ao testar socket: {e}")
        return False


def get_database_config() -> dict:
    """
    Retorna a configuração completa do banco de dados com auto-detecção.

    Returns:
        dict: Dicionário com DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
    """
    config = {
        'DB_HOST': detect_db_host(),
        'DB_PORT': detect_db_port(),
        'DB_USER': os.getenv('DB_USER', 'spring'),
        'DB_PASS': os.getenv('DB_PASS', 'spring123'),
        'DB_NAME': os.getenv('DB_NAME', 'minha_base'),
    }

    logger.info("=" * 60)
    logger.info("📦 Configuração do Banco de Dados")
    logger.info("=" * 60)
    for key, value in config.items():
        if 'PASS' in key:
            logger.info(f"  {key}: {'*' * 8}")
        else:
            logger.info(f"  {key}: {value}")
    logger.info("=" * 60)

    return config

