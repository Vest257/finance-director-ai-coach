"""Streamlit Community Cloud entrypoint for the FinanceOS pilot."""

from finance_director_coach.streamlit_ui import run_app


def main() -> None:
    run_app()


if __name__ == "__main__":
    main()
