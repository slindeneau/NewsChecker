import datetime
import newspaper
import bson
#NewsArticle Class
# - NewsSource: The top-level news source (String)
# - URL: The retrieval url. (String)
# - Summary: newspaper nlp summary (String)
# - Keywords: newspaper nlp keywords (list of strings)
# - Title: Title as given by news source.
# - Text: Article body (string)
# - Authors: Authors (list of strings)
# - Publish Date: Date (datetime)
# - Retrieval Date: Date (datetime)

class NewsArticle:
    def __init__(self,art):
        if isinstance(art,newspaper.Article):
            self.NewsSource     = art.source_url
            self.URL            = art.canonical_link
            self.Summary        = art.summary
            self.Keywords       = art.keywords
            self.Title          = art.title
            self.Text           = art.text
            self.Authors        = art.authors
            self.Publish_Date   = art.publish_date
            self.Retieval_Date  = datetime.datetime.now()
            self.UID            = art.link_hash
        else:
            self.NewsSource     = art.NewsSource
            self.URL            = art.URL
            self.Summary        = art.Summary
            self.Keywords       = art.Keywords
            self.Title          = art.Title
            self.Text           = art.Text
            self.Authors        = art.Authors
            self.Publish_Date   = art.Publish_Date
            self.Retieval_Date  = art.Retieval_Date
            self.UID            = art.UID
    def GetMongoDocument(self):
        return{ "NewsSource": self.NewsSource,
                "URL": self.URL,
                "Summary": self.Summary,
                "Keywords": self.Keywords,
                "Title": self.Title,
                "Text": self.Text,
                "Authors": self.Authors,
                "Publish_Date": self.Publish_Date,
                "Retieval_Date": self.Retieval_Date,
                "_id": self.UID}
