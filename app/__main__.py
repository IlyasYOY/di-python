from app import create_app

app = create_app()

app.run(host=app.host, port=app.port)