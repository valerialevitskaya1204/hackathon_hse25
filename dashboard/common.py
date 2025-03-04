import streamlit as st

class Page:
    url: str
    title: str
    def render(self):
        ...
    def page(self) -> st.Page:
        return st.Page(self.render, title=self.title, url_path=self.url)