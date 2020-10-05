from flask import Flask
from kl_designs import create_app, Config

app = create_app()

if __name__ == '__main__':
    app.run()
