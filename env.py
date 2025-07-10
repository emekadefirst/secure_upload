import os
from dotenv import load_dotenv

load_dotenv()



S3_ACCESS_KEY = str(os.environ["S3_ACCESS_KEY"])
S3_SECRET_KEY = str(os.environ["S3_SECRET_KEY"])
S3_ENDPOINT = str(os.getenv("S3_ENDPOINT"))
S3_BUCKET = str(os.environ["S3_BUCKET"])