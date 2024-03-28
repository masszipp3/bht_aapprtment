from waitress import serve
from bht_appartment.wsgi import application  # Replace 'myproject' with your actual project name

if __name__ == "__main__":
    serve(application, host='0.0.0.0', port=8000)  # Adjust the host and port as needed
    