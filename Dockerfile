FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir streamlit google-genai pandas python-dotenv
COPY . /app
EXPOSE 8080
CMD ["streamlit", "run", "dashboard.py", "--server.port=8080", "--server.address=0.0.0.0"]