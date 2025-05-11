from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    title: str
    summary: str
    link: str
    date: str
    source: str = 'BBC Technology'
    
    @property
    def to_dict(self):
        return {
            'title': self.title,
            'summary': self.summary,
            'link': self.link,
            'date': self.date,
            'source': self.source
        }