def add_routes(router, prefix, routes):
    for route in routes:
        name = route[0]
        viewset = route[1]
        basename = None
        if len(route) > 2:
            basename = route[2]

        path = f'{prefix}{name}'
        router.register(path, viewset, basename=basename)
