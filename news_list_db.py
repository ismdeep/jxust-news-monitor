import pickle


class NewsListDB:
    news_set = set()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(NewsListDB, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    @staticmethod
    def has(__item__):
        news_list_db = NewsListDB()
        for news in news_list_db.news_set:
            if news == __item__:
                return True
        return False

    @staticmethod
    def add(__item__):
        news_list_db = NewsListDB()
        news_list_db.news_set.add(__item__)

    @staticmethod
    def save():
        pickle.dump(NewsListDB.news_set, open('news-list.db', 'wb'))

    @staticmethod
    def load():
        try:
            NewsListDB.news_set = pickle.load(open('news-list.db', 'rb'))
        except:
            NewsListDB.news_set = set()
