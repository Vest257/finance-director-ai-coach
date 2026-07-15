"""Streamlit Community Cloud entrypoint for the FinanceOS pilot surfaces."""

import streamlit as st

from finance_director_coach.practice_ui import run_practice_app
from finance_director_coach.streamlit_ui import run_app


def main() -> None:
    st.set_page_config(
        page_title="FinanceOS | Finance Director Scenario Coach",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    page = st.navigation(
        [
            st.Page(run_app, title="Scenario Coach", icon=":material/account_balance:"),
            st.Page(run_practice_app, title="Practice", icon=":material/calculate:"),
        ],
        position="sidebar",
    )
    page.run()


if __name__ == "__main__":
    main()
