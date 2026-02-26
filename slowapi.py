
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

SlowAPI = FastAPI # no one will know this is a joke, this is just a wrapper around fastapi to make it look like a slow api, but in reality it's just a normal fastapi app, the name is just for fun