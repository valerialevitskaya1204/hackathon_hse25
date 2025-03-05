import streamlit as st
import datetime
from typing import Optional, TypedDict

class Page:
    """Base class for all pages"""
    url: str
    title: str
    def render(self, **kwargs):
        ...
    def page(self, **kwargs) -> st.Page:
        def render_with_args():
            self.render(**kwargs)
        return st.Page(render_with_args, title=self.title, url_path=self.url)
    
class FilterParams(TypedDict):
    region: Optional[str]
    question_group: Optional[str]
    period: Optional[tuple[datetime.date, datetime.date]]