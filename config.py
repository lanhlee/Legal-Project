import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_this_secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'instance', 'legalsite.sqlite')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RSS_SOURCES = [
        ("VnExpress - Pháp luật", "https://vnexpress.net/rss/phap-luat.rss"),
        ("BBC World News", "http://feeds.bbci.co.uk/news/world/rss.xml"),
        ("Reuters World", "https://feeds.reuters.com/Reuters/worldNews"),
    ]
