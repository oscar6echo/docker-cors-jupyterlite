import os

import requests as rq
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse

os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["no_proxy"] = ""

PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = os.getenv("PROXY_PORT")
CORS_ORIGINS = os.getenv("CORS_ORIGINS")


app = FastAPI()


if CORS_ORIGINS is None:
    origins = [
        # official demo
        "https://jupyterlite.readthedocs.io",
    ]
else:
    origins = CORS_ORIGINS.split(",")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


user_guide: HTMLResponse = f"""
     <html>
        <body>
            <h3>CORS Proxy Server</h3>
            <p>Expected request:</p>
            <ul>
            <li>- methods: GET/POST/PUT/PATCH/DELETE</li>
            <li>- url: https://[cors-server-hostname]:[cors-server-port]/cors/[target_url]</li>
            </ul>
            <p>See doc: TBD/README.md</p>
            <p>Only for origins: {origins}</p>                
            </p>
        </body>
    </html>
    """


@app.get("/cors/{path:path}")
@app.post("/cors/{path:path}")
@app.patch("/cors/{path:path}")
@app.delete("/cors/{path:path}")
async def root(req: Request):
    """"""
    url_target = req.path_params["path"]
    print(f"DEBUG ----- catch_url: {url_target}")

    if (
        (url_target == "")
        or not url_target.startswith("http")
        or not url_target.startswith("https")
    ):
        url = app.url_path_for("")
        response = RedirectResponse(url=url)
        return response

    if "?" in url_target:
        url_target, _ = url_target.split("?")

    method = req.method

    params = None
    proxies = None
    if req.query_params is not None:
        params = req.query_params._dict
        key_user = "_proxy_username"
        key_pwd = "_proxy_password"
        if PROXY_HOST and PROXY_PORT and key_user in params and key_pwd in params:
            username = params.pop(key_user)
            pwd_encoded = params.pop(key_pwd)
            p = f"http://{username}:{pwd_encoded}@{PROXY_HOST}:{PROXY_PORT}"
            proxies = {"http": p, "https": p}

    headers = None
    if req.headers is not None:
        headers = [list(e) for e in req.headers._list]
        dic = {}
        for e in headers:
            key = e[0].decode("utf-8")
            val = e[1].decode("utf-8")
            if not key in ["host"]:
                dic[key] = val
        headers = dic

    body = None
    if req.body is not None:
        body = await req.body()

    dic_request = {
        "url": url_target,
        "method": method,
        "headers": headers,
        "params": params,
        "data": body,
        "proxies": proxies,
    }
    print(f"DEBUG ----- dic_request")
    print(dic_request)
    print(f"END DEBUG -----")

    try:
        res = rq.request(**dic_request)
        media_type = res.raw.getheaders().get("content-type")
        return Response(content=res.content, media_type=media_type)

    except Exception as e:
        return {
            "error": str(e),
            "details": {
                "url": url_target,
                "method": method,
            },
        }


@app.get("/{catch_all:path}", response_class=HTMLResponse)
async def root(catch_all: str):
    """"""
    print(f"DEBUG ----- catch_all: {catch_all}")
    return user_guide
