from secret_santa_api import create_app


app = create_app("./secret_santa_api/.env")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
