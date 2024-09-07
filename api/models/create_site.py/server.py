from http.server import HTTPServer, CGIHTTPRequestHandler
server_address = ("#адрес нашего сервака", "номер порта, прокинутого на сервер") #подключаем сервер наш
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
httpd.serve_forever()

