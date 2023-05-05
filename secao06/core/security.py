from passlib.context import CryptContext

CRIPTO = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

def verificar_senha(senha: str, hash_senha: str) -> bool:
    """
    Função para verificar se a senha está correta, 
    comparando a senha informada em texto puro e o hash salvo.
    """
    return CRIPTO.verify(senha, hash_senha)

def gerar_hash_senha(senha: str) -> str:
    """
    Função para criar e retornar o hash da senha
    """
    return CRIPTO.hash(senha)