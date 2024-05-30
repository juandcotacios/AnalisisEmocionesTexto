from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from faker import Faker
import random

clasificador = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


faker = Faker('es_ES')


def mapear_sentimiento(label: str):
    sentimiento_mapping = {
        '1 star': 'triste',
        '2 stars': 'decepcionado',
        '3 stars': 'neutral',
        '4 stars': 'satisfecho',
        '5 stars': 'feliz'
    }
    return sentimiento_mapping.get(label, 'desconocido')


comentarios_ejemplos = [
    "El ambiente de estudio en la Universidad Konrad Lorenz es excelente.",
    "Los profesores son muy atentos y siempre dispuestos a ayudar.",
    "Me encanta la biblioteca, tiene una gran cantidad de recursos.",
    "Las instalaciones deportivas son de primera calidad.",
    "Estoy muy satisfecho con el plan de estudios de mi carrera.",
    "El proceso de matrícula fue muy sencillo y rápido.",
    "Hay muchas oportunidades para participar en proyectos de investigación.",
    "El campus es muy bonito y bien cuidado.",
    "El servicio de cafetería ofrece una buena variedad de alimentos.",
    "Las actividades extracurriculares son muy variadas e interesantes."
]


def generar_comentarios_mock():
    comentarios = []
    for _ in range(15):
        comentario = random.choice(comentarios_ejemplos)
        usuario = faker.user_name()
        comentarios.append({"usuario": usuario, "comentario": comentario})
    return comentarios


@app.get("/comentarios_analizados")
def obtener_comentarios_analizados():
    comentarios = generar_comentarios_mock()
    comentarios_analizados = []
    for comentario in comentarios:
        resultado = clasificador(comentario['comentario'])
        sentimiento = mapear_sentimiento(resultado[0]['label'])
        comentarios_analizados.append({
            "usuario": comentario['usuario'],
            "comentario": comentario['comentario'],
            "sentimiento": sentimiento,
            "puntaje": resultado[0]['score']
        })
    return comentarios_analizados

@app.get("/recomendacion")
def recomendar_publicacion(texto: str = Query(..., description="Texto para analizar y recomendar")):
    if not isinstance(texto, str):
        raise HTTPException(status_code=400, detail="El input debe ser una cadena de texto.")
    
 
    max_tokens = 1000
    if len(texto.split()) > max_tokens:
        raise HTTPException(status_code=400, detail=f"El texto no debe exceder los {max_tokens} tokens.")
    
    resultado = clasificador(texto)
    puntaje = resultado[0]['score']
    sentimiento = mapear_sentimiento(resultado[0]['label'])

   
    publicar = sentimiento in ['satisfecho', 'feliz', 'neutral']
    
    return {
        "texto": texto,
        "sentimiento": sentimiento,
        "puntaje": puntaje,
        "publicar": publicar
    }


