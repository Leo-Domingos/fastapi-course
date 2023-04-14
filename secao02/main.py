from fastapi import FastAPI

app = FastAPI()

@app.get('/msg')
async def mensagem():
    return {'msg': 'FastAPI na Geek University'}

#uvicorn main:app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host = '127.0.0.1', port  = 8000, 
    log_level = 'info', reload = True)

# Quando coloca host = "0.0.0.0" permite o acesso de qualquer pessoa através do seu ip
# Só colocar o ip da rede no lugar do host