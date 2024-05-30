document.getElementById('analyze-button').addEventListener('click', function() {
    const text = document.getElementById('input-text').value.trim();

    if (!text) {
        alert('Por favor, escribe algún texto para analizar.');
        return;
    }

    const maxTokens = 1000;
    if (text.split(/\s+/).length > maxTokens) {
        alert(`El texto no debe exceder los ${maxTokens} tokens.`);
        return;
    }

    fetch(`http://127.0.0.1:3001/recomendacion?texto=${encodeURIComponent(text)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json();
        })
        .then(data => {
            if (data.sentimiento && data.puntaje !== undefined && data.publicar !== undefined) {
                document.getElementById('sentiment').innerText = `Sentimiento: ${data.sentimiento}`;
                document.getElementById('score').innerText = `Puntaje: ${data.puntaje}`;
                document.getElementById('publish').innerText = `Recomendación de Publicación: ${data.publicar ? 'Sí' : 'No'}`;
            } else {
                throw new Error('Estructura de datos inesperada');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un problema con la solicitud. Por favor, intenta de nuevo.');
        });
});

// Función para actualizar los comentarios analizados
function actualizarComentarios() {
    fetch('http://127.0.0.1:3001/comentarios_analizados')
        .then(response => response.json())
        .then(data => {
            const comentariosDiv = document.getElementById('comentarios');
            comentariosDiv.innerHTML = ''; // Limpiar comentarios anteriores
            data.forEach(comentario => {
                const comentarioElement = document.createElement('div');
                comentarioElement.classList.add('comentario');
                comentarioElement.innerHTML = `
                    <p><strong>Usuario:</strong> ${comentario.usuario}</p>
                    <p><strong>Comentario:</strong> ${comentario.comentario}</p>
                    <p><strong>Sentimiento:</strong> ${comentario.sentimiento}</p>
                    <p><strong>Puntaje:</strong> ${comentario.puntaje.toFixed(2)}</p>
                `;
                comentariosDiv.appendChild(comentarioElement);
            });
        })
        .catch(error => {
            console.error('Error al obtener los comentarios:', error);
        });
}


setInterval(actualizarComentarios, 20000);
document.addEventListener('DOMContentLoaded', actualizarComentarios);
