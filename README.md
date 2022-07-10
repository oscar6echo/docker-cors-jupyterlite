# FastApi CORS Proxy Server

## Principe

FastApi server to **replace** any server header `Access-Control-Allow-Origin` with header `Access-Control-Allow-Origin: $http_origin` for requests to `[protocol]://[hostname]/<targetURL>` where `[protocol]` and `[hostname]` are those of the FastApi CORS proxy server.

Additionally if params `_proxy_usename` and `_proxy_password` are in url, and env variables `$PROXY_HOST` and `$PROXY_PORT` exist in server then they are used as params to use the following proxy:

- `http://{_proxy_usename}:{_proxy_password}@{PROXY_HOST}:{PROXY_PORT}`.  
  _NOTE_: `_proxy_password` needs be url encoded.

## Example

A client sent request to `https://localhost:8086/cors/<targetURL>`, the FastApi CORS proxy server (CPS) makes the same the request to `<targetURL>`, and when the CPS receives the response from `<targetURL>`, the CPS sets header `Access-Control-Allow-Origin: $http_origin` on the response, after suppressing that header coming from `<targetURL>`, and pass it back to client.

If the client is a browser this allows to avoid [CORS errors](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors).

## Certificates

You need serve the CPS over `https` if the client is a web page served over `https`.  
Then you need create certificates first.  
For a dev environment, [mkcert](https://github.com/FiloSottile/mkcert) is very convenient.

## Test

Run the following in sequence:

- Certificates:

  ```sh
  # create local dev certificate
  run_create_cert.sh
  ```

- Build:

  ```sh
  # in folder /scripts
  run_docker_build.sh
  ```

- Run:

  ```sh
  # in folder /scripts
  run_docker_run_https.sh

  curl -H 'Origin: http://192.168.0.33' -vI -X GET https://localhost:8443/cors/https://example.com

  curl -H 'Origin: http://192.168.0.34' -vI -X GET https://localhost:8443/cors/https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv

  ```

See demo notebook [test-cors.ipynb](./test/test-cors.ipynb).
