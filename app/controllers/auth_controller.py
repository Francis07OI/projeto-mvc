from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.auth import hash_senha, verificar_senha, criar_token


# APIROUTER agrupa as rotas desse arquivo com o prefixo /auth
router = APIRouter(prefix="/auth", tags=["Atenticação"])

#configurar para renderizar os templates HTML 
templates = Jinja2Templates(directory="app/templates")


#Rotas para tela de cadastro 
@router.get("/cadastro")
def tela_cadastro(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/cadastro.html",
        {"request": request}
    )

# Tela login 
@router.get("/login")
def tela_cadastro(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/login.html",
        {"request": request}
    )

# Rota para criar um usuario no banco de dados 

@router.post("/cadastro")
def fazer_cadastro(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)

):
    
    #Verificar o email do usuario 
    user_existente = db.query(Usuario).filter_by(email=email,).first()

    if user_existente:
        return templates.TemplateResponse(
            request,
            "auth/cadastro.html",
            {"request": request, "erro": "Este e-mail já está cadastrado"}
        )


    #Cria o novo usuario 
    novo_usuaio = Usuario(nome=nome, email=email, senha_hash=hash_senha(senha))
    db.add(novo_usuaio)
    db.commit()

    return RedirectResponse(url="/auth/login?cadastro=ok", status_code=302)




    



