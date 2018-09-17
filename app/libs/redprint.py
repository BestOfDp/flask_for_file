class Redprint:

    def __init__(self, name):
        self.name = name
        self.o = []

    def route(self, rule, **options):
        def decorator(f):
            # 保存需要注册到蓝图的信息
            self.o.append((f, rule, options))
            return f

        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        for f, rule, options in self.o:
            endpoint = options.pop("endpoint", self.name + '_' + f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
