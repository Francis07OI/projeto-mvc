# instalar o requirements.txt

bash 
    pip install -r requirements.txt


# inicializar o alembic
bash
python -m alembic init migrations 


# gerar a migrations 

python -m alembic revision --autogenerate -m 
"Criar tabela  usuario"

# aplicar a migrations 

python -m alembic upgrade head 

# Rodar a migration 
bash
python -m uvicorn app.main:app --reload --port 5500
