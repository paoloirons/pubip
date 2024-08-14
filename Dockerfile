# Usa un'immagine base di Python
FROM python:3.9-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file requirements.txt e installa le dipendenze
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Installa Gunicorn
RUN pip install gunicorn

# Copia il resto del codice dell'applicazione
COPY . .

# Espone la porta su cui l'applicazione sarà in esecuzione
EXPOSE 5000

# Comando per eseguire l'applicazione con Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

