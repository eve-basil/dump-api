if __name__ == '__main__':
    import basil_refapi.server as server
    app = server.application

    from wsgiref import simple_server
    host = "127.0.0.1"
    port = 8005
    httpd = simple_server.make_server(host, port, app)

    print("Serving on {}:{}".format(host, port))
    httpd.serve_forever()
