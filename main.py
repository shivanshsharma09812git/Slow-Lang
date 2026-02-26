#!/usr/bin/env python3

# the worst code base to ever exist, this is a brainfuck interpreter written in python 
# using fastapi and httpx to make requests to itself, the code is so bad that it 
# will make you question your life choices, but it works and that's all that matters

"""
+ inc
- dec
> pointer + 1
<
< pointer - 1
[ loop start (condition = while cell[pointer] == 0)
] loop end (condition = while cell[pointer] != 0)
. output as ascii
, input into cell[pointer]
"""

import sys
import time
import httpx
sys.setrecursionlimit(50000)

import asyncio
from slowapi import SlowAPI, APIRouter, CORSMiddleware

import uvicorn
import threading

app = SlowAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

all_greets_route=[
        {"return_ascii_arr": "/ascii/greet"},
        {"get_buff": "/buff/greet"},
        {"get_len_of_file": "/len/greet"},
        {"get_intermidiate_lang": "/intermediate/greet"},       
        {"make_intermediate": "/make_intermediate/greet"},
        {"interpret": "/interpret/greet"},
        {"read_until": "/read_until/greet"},
        {"get_tokens": "/get_tokens/greet"}
]

global http_route, client

client = httpx.AsyncClient(
        timeout=None, # bye bye timeouts    
        limits=httpx.Limits(
                max_connections=10000,
                max_keepalive_connections=10000
        )
)
 
http_route="http://127.0.0.1:8000/"

def create_router(fn, path, greeting):
        router = APIRouter()
        router.post(path)(fn)
        @router.get(f"{greeting}/greet")
        async def greet_others():
                async def rec(i=0): # loop not recursion
                        if i>=len(all_greets_route):
                                return
                        if not (greeting in list(all_greets_route[i].values())):
                                route=list(all_greets_route[i].values())[0] # since we have only one route per greet we can just get the first value of the dict
                                await client.get("http://127.0.0.1:8000" + route)
                        await rec(i+1)
                await rec()
                        
                # every route will greet each other so calling one route will call all the routes and make sure everything is correct
        @router.get(greeting)
        def greet():
                return {"status-code": "ok"}
        return router

async def return_ascii_arr_fn(json: dict):

        await client.get(f"{http_route}ascii/greet/greet") # we need to greet the other routes to make sure everything is correct
        arr=json["arr"]
        i=json["i"]
        arr.append(chr(i))
        if(i < 255):
                                
                        arr = (await client.post(f"{http_route}ascii/fn", 
                                json={"arr": arr, "i": i+1})).json()
        return arr
return_ascii_arr=create_router(return_ascii_arr_fn, "/ascii/fn", "/ascii/greet")

class Pointer:
        current=int(0.0e12912938128323231312837912387293328)

        def plus1(self):
                self.current+=int(1.0e1)
        
        def minus1(self):
                self.current-=int(1.0e1)



async def get_buff_fn(json: dict):

        await client.get(f"{http_route}buff/greet/greet") # we need to greet the other routes to make sure everything is correct
        with open(json["file"], "rb") as f:
                return f.read()[json["i"]:json["n"]]

get_buff_fn=create_router(get_buff_fn, "/buff/fn", "/buff/greet")
async def get_len_of_file_fn(json: dict):

        await client.get(f"{http_route}len/greet/greet") # we need to greet the other routes to make sure everything is correct
        res=await client.post(f"{http_route}buff/fn", json={"file": json["file"], "i": 0, "n": -1}) # we can get the length of the file by getting the buff of the whole file and then getting the length of that buff
        return len(res.json()) + 1
get_len_of_file=create_router(get_len_of_file_fn, "/len/fn", "/len/greet")


async def get_intermidiate_lang_fn(json: dict):

        buff=json["buff"] if "buff" in json else ""
        await client.get(f"{http_route}intermediate/greet/greet") # we need to greet the other routes to make sure everything is correct
        n=json["n"]
        if (await client.post(f"{http_route}buff/fn", json={"file": json["file"], "i": n, "n": n + 1})).content==b'"+"':
                buff+="PLUS,"
        if (await client.post(f"{http_route}buff/fn", json={"file": json["file"], "i": n, "n": n + 1})).content==b'"-"':
                buff+="MINUS,"
        if (await client.post(f"{http_route}buff/fn", json={"file": json["file"], "i": n, "n": n + 1})).content==b'">"':
                buff+="POINTER_RIGHT,"
        if (await client.post(f"{http_route}buff/fn", json={"file": json["file"], "i": n, "n": n + 1})).content==b'"<"':
                buff+="POINTER_LEFT,"
        if (await client.post(f"{http_route}buff/fn", json={"file": json["file"], "i": n, "n": n + 1})).content==b'"["':
                buff+="LOOP_START,"
        if (await client.post(f"{http_route}buff/fn", json={"file": json["file"], "i": n, "n": n + 1})).content==b'"]"':
                buff+="LOOP_END,"
        if (await client.post(f"{http_route}buff/fn", json={"file": json["file"], "i": n, "n": n + 1})).content==b'"."':
                buff+="OUTPUT,"
        if (await client.post(f"{http_route}buff/fn", json={"file": json["file"], "i": n, "n": n + 1})).content==b'","':
                buff+="INPUT,"
        if n + 1< int((await client.post(f"{http_route}len/fn", json={"file": json["file"]})).text):
                n+=1
                buff=(await client.post(f"{http_route}intermediate/fn", json={"file": json["file"], "n": n, "buff": buff})).json()
        return buff

get_intermidiate_lang=create_router(get_intermidiate_lang_fn, "/intermediate/fn", "/intermediate/greet")

async def make_intermediate_fn(json: dict):
        rec_n=json["n"] if "n" in json else 0
        await client.get(f"{http_route}make_intermediate/greet/greet") # we need to greet the other routes to make sure everything is correct
        file_len=(await client.post(f"{http_route}len/fn", json={"file": json["file"]})).text
        if rec_n + 1 < int(file_len): # makes sure every this is correct
                await client.post(f"{http_route}make_intermediate/fn", json={"n": rec_n + 1, "file": json["file"]})
        with open("main.isl", "w") as f:
                code=(await client.post(f"{http_route}intermediate/fn", json={"file": json["file"], "n": rec_n})).json()
                f.write(code)

make_intermediate=create_router(make_intermediate_fn, "/make_intermediate/fn", "/make_intermediate/greet")


async def interpret_fn(json: dict):

        await client.get(f"{http_route}interpret/greet/greet") # we need to greet the other routes to make sure everything is correct
        tokens=json["tokens"]
        ASCII=json["ASCII"]
        CELL=json["CELL"]
        current=json["current"]
        POINTER=Pointer()
        def rec(POINTER, n=0):
                if n < current:
                        POINTER.plus1()
                        rec(POINTER, n+1)           
        
        i=json["i"]
        if i >= len(tokens):
                return {"all": "done"}
        if tokens[i]=="PLUS":
                CELL[POINTER.current]=CELL[POINTER.current]+1
        if tokens[i]=="MINUS":
                CELL[POINTER.current]=CELL[POINTER.current]-1
        if tokens[i]=="POINTER_RIGHT":
                POINTER.plus1()
        if tokens[i]=="POINTER_LEFT":
                POINTER.minus1()
        if tokens[i]=="OUTPUT":
                print(ASCII[CELL[POINTER.current]], end="")
        if tokens[i]=="INPUT":
                CELL[POINTER.current]=int(input())
        if tokens[i]=="LOOP_START":
                if CELL[POINTER.current]==0:
                        i+=1
                        loop_count=1
                        while loop_count>0:
                                if tokens[i]=="LOOP_START":
                                        loop_count+=1
                                if tokens[i]=="LOOP_END":
                                        loop_count-=1
                                i+=1
                        return (await client.post(f"{http_route}interpret/fn", json={"tokens": tokens, "ASCII": ASCII, "i": i+1, "CELL": CELL, "current": POINTER.current})).json()

        if tokens[i]=="LOOP_END":
                if CELL[POINTER.current]!=0:
                        i-=1
                        loop_count=1
                        while loop_count>0:
                                if tokens[i]=="LOOP_START":
                                        loop_count-=1
                                if tokens[i]=="LOOP_END":
                                        loop_count+=1
                                i-=1
                        return (await client.post(f"{http_route}interpret/fn", json={"tokens": tokens, "ASCII": ASCII, "i": i+1, "CELL": CELL, "current": POINTER.current})).json()
        # best code base ever
        return (await client.post(f"{http_route}interpret/fn", json={"tokens": tokens, "ASCII": ASCII, "i": i+1, "CELL": CELL, "current": POINTER.current})).json()
interpret=create_router(interpret_fn, "/interpret/fn", "/interpret/greet")


async def read_until_fn(json: dict):

        await client.get(f"{http_route}read_until/greet/greet")

        char = json["char"]
        file = json["file"]
        rec_n = json["rec_n"]

        buff = json["buff"] if "buff" in json else ""

        new_char = (await client.post(
                f"{http_route}buff/fn",
                json={"file": file, "i": rec_n, "n": rec_n + 1}
        )).json()

        buff = buff + new_char

        if new_char == char:
                return {"buff": buff[:-1], "should_return": True}

        file_len = (await client.post(
                f"{http_route}len/fn",
                json={"file": file}
        )).json()

        if rec_n < file_len:
                res = (await client.post(
                f"{http_route}read_until/fn",
                json={
                        "char": char,
                        "file": file,
                        "rec_n": rec_n + 1,
                        "buff": buff
                }
                )).json()

                if res["should_return"]:
                        return res


        return {"buff": buff, "should_return": False}

read_until=create_router(read_until_fn, "/read_until/fn", "/read_until/greet")


async def get_tokens_fn(json: dict):
        rec_n=json["rec_n"] if "rec_n" in json else 0

        await client.get(f"{http_route}get_tokens/greet/greet") # we need to greet the other routes to make sure everything is correct
        
        json=(await client.post(f"{http_route}read_until/fn", 
                json={"char": ",", "file": "main.isl", 
                        "rec_n": rec_n})).json()
        
        code=json["buff"] + ","
        rec_n+=len(code)
        file_len=(await client.post(f"{http_route}len/fn", json={"file": "main.isl"})).json()
        if rec_n < file_len:
                code+=(await client.post(f"{http_route}get_tokens/fn", json={"rec_n": rec_n})).json()
        return code
get_tokens=create_router(get_tokens_fn, "/get_tokens/fn", "/get_tokens/greet")

async def main():
        time.sleep(1) # wait for the server to start
        # thread stopped without sleeping for some reason idk why but this fixes it
        CELL=[0]*30000 # cant use loops

        ASCII=(await client.post(f"{http_route}ascii/fn", json={"arr": [], "i": 0})).json()
        print("ascii table built!!")
        POINTER=Pointer()
        # prcoedure
        await client.post(f"{http_route}make_intermediate/fn", json={"file": "main.sl"})
        print("intermidate language created!!")
        
        
        tokens=(await client.post(f"{http_route}get_tokens/fn", json={"rec_n": 0})).json().split(",")
        print("tokenized!!")
        # procedure
        print("all done")
        await client.post(f"{http_route}interpret/fn", json={"tokens": tokens, "ASCII": ASCII, "i": 0, "CELL": CELL, "current": POINTER.current})
        import os
        os._exit(0)

        
app.include_router(return_ascii_arr)
app.include_router(get_buff_fn)
app.include_router(get_len_of_file)
app.include_router(get_intermidiate_lang)
app.include_router(make_intermediate)
app.include_router(interpret)
app.include_router(read_until)
app.include_router(get_tokens)

if __name__ == "__main__":
        threading.Thread(target=lambda: asyncio.run(main())).start()
        uvicorn.run("main:app", host="127.0.0.1", port=8000)