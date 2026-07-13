"""Console input validation and application entry point."""

from __future__ import annotations

from collections.abc import Callable, Mapping

from finance_director_coach.session import Scenario001Session, SessionResult

InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]


class TerminalInteraction:
    def __init__(
        self,
        input_fn: InputFunction = input,
        output_fn: OutputFunction = print,
    ) -> None:
        self._input = input_fn
        self._output = output_fn

    def write(self, text: str = "") -> None:
        self._output(text)

    def ask_number(self, prompt: str) -> float:
        while True:
            raw = self._input(prompt).strip()
            try:
                return float(raw)
            except ValueError:
                self.write("Please enter a valid number, for example 3.35 or -0.20.")

    def choose_one(self, prompt: str, options: Mapping[str, str]) -> str:
        keys = list(options)
        while True:
            self.write(f"\n{prompt}")
            for index, key in enumerate(keys, start=1):
                self.write(f"  {index}. {options[key]}")
            raw = self._input("Selection: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(keys):
                return keys[int(raw) - 1]
            self.write(f"Choose one number from 1 to {len(keys)}.")

    def choose_many(self, prompt: str, options: Mapping[str, str]) -> frozenset[str]:
        keys = list(options)
        while True:
            self.write(f"\n{prompt}")
            for index, key in enumerate(keys, start=1):
                self.write(f"  {index}. {options[key]}")
            self.write("Enter one or more numbers separated by commas, such as 1,3,4. Enter 'all' to select all.")
            raw = self._input("Selections: ").strip().lower()
            if raw == "all":
                return frozenset(keys)
            try:
                selections = {int(item.strip()) for item in raw.split(",") if item.strip()}
            except ValueError:
                selections = set()
            if selections and all(1 <= selection <= len(keys) for selection in selections):
                return frozenset(keys[selection - 1] for selection in selections)
            self.write(f"Choose comma-separated numbers between 1 and {len(keys)}.")

    def ask_text(self, prompt: str) -> str:
        while True:
            response = self._input(prompt).strip()
            if response:
                return response
            self.write("Please enter a response. Its wording will not be automatically scored.")


def main(
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
) -> SessionResult | None:
    interaction = TerminalInteraction(input_fn, output_fn)
    interaction.write("FinanceOS | Finance Director Scenario Coach")
    interaction.write("Phase 1 CLI learning experience")
    action = interaction.choose_one(
        "Start a scenario:",
        {
            "scenario_001": "Scenario 001 - Growth With Falling Cash",
            "exit": "Exit",
        },
    )
    if action == "exit":
        interaction.write("Session ended.")
        return None
    return Scenario001Session(interaction).run()
