class NewsModel:
    title = None
    url = None

    def __init__(self, __title__, __url__):
        self.title = __title__
        self.url = __url__

    def __str__(self):
        return '''["%s", "%s"]''' % (self.title, self.url)
