import psycopg2

def conectar_bd(host, port, database, user, password):
    """Função para estabelecer conexão com o banco PostgreSQL usando as credenciais fornecidas."""
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        return conn
    except Exception as e:
        raise Exception(f"Erro na conexão com o banco: {e}")
