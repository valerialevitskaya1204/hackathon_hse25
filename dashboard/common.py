import streamlit as st

class Page:
    url: str
    title: str
    def render(self, **kwargs):
        ...
    def page(self, **kwargs) -> st.Page:
        def render_with_args():
            self.render(**kwargs)
        return st.Page(render_with_args, title=self.title, url_path=self.url)