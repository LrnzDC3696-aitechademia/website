from dotenv import load_dotenv

import os

from src import create_app

DEV_MODE = os.environ["DEV_MODE"] == "True"

app = create_app()

if __name__ == "__main__":
    app.run(debug=DEV_MODE)
