# 1. Hast e verificação de senhas com bcrypt
# 2. Geração de token JWT
# 3. Leitura e validação de token vindo do cookie


from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import requests, HTTPException, status
from dotenv import load_dotenv
import os 


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACESS_TOKEN_EXPIRE_MINUTES")



#CryptContext - configura o bcrypt como algoritimo de hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#teste de hash

senha = "1234"
senha_hash = pwd_context.hash(senha)

print(senha_hash)


verificar_senha = pwd_context.hash(senha)

print(senha_hash)

senha_atual = "testeteste"
verificar_senha = pwd_context.verify(senha_atual, senha_hash)
print(verificar_senha)


# função de senha 
def hash_senha(senha: str):
    return pwd_context.hash(senha)
  
def verificar_senha (senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)


# Funções do token - JWT

def criar_token(data: dict):
    payload = data.copy()

    #Define quando o token vai inspirar
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expira})

    #Criar o token jwt 
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token 

def decodificar_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload 


#Dependencias do FastAPI
def get_usuario_logado(request: Request):
     
    token = request.cookies.get("acess_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="não autenticado"

        )

    try:
        payload = decodificar_token(token)
        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token invalido ou expirado"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )

def get_usuario_opcional(request: Request):

    try:
        return get_usuario_logado( request)
    except get_usuario_logado(request)
        return None
