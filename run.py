from app import create_app

app = create_app()

if __name__ == "__main__":
    # use_reloader=False: sem isso o Flask abre o programa 2 vezes
    # e as tabelas seriam criadas 2 vezes. Assim roda uma vez só.
    app.run(debug=True, use_reloader=False)
