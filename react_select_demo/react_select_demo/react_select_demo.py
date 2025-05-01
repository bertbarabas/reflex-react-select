import reflex as rx
from reflex.style import set_color_mode, color_mode

from reflex_react_select import react_select

with open("react_select_demo/test_data/2_000 Street Addresses.txt", "r") as file:
    street_address_lines = file.readlines()

food_options = [
    {"value": "chocolate", "label": "Chocolate"},
    {"value": "strawberry", "label": "Strawberry"},
    {"value": "vanilla", "label": "Vanilla"},
    {"value": "pudding", "label": "Pudding"},
    {"value": "bacon", "label": "Bacon"},
    {"value": "toast", "label": "Toast"},
    {"value": "fish", "label": "Fish"},
    {"value": "steak", "label": "Steak"},
    {"value": "salad", "label": "Salad"},
]


class StreetState(rx.State):
    entered_prefix = ""

    @rx.var
    def streets(self) -> list[dict[str, str]]:
        return (
            [
                {"value": line, "label": line}
                for line in street_address_lines
                if line.startswith(self.entered_prefix)
            ]
            if self.entered_prefix
            else []
        )

    @rx.event
    def on_input_change(self, entered_text):
        if self.entered_prefix != entered_text[:2]:
            self.entered_prefix = entered_text[:2] if len(entered_text) >= 2 else ""


def dark_mode_toggle() -> rx.Component:
    return rx.segmented_control.root(
        rx.segmented_control.item(
            rx.icon(tag="monitor", size=20),
            value="system",
        ),
        rx.segmented_control.item(
            rx.icon(tag="sun", size=20),
            value="light",
        ),
        rx.segmented_control.item(
            rx.icon(tag="moon", size=20),
            value="dark",
        ),
        on_change=set_color_mode,
        variant="classic",
        radius="large",
        value=color_mode,
    )


def index() -> rx.Component:
    return rx.vstack(
        rx.center(
            rx.center(
                rx.heading("React Select with", size="5"),
                rx.heading("Reflex Custom Component Wrapping", size="5"),
                spacing="0",
                direction="column",
            ),
            dark_mode_toggle(),
            direction="column",
            spacing="3",
            width="100%",
            padding_top="2em",
        ),
        react_select(
            name="test_dropdown_for_form",
            placeholder="Select street address",
            options=StreetState.streets,
            on_input_change=lambda info: StreetState.on_input_change(info),
            no_options_message=rx.vars.FunctionStringVar(
                """(select_object) => {
                        return select_object.inputValue.length < 2 ?
                            "Provide at least the first 2 digits of your house number \
                             to get a list of street addresses to choose from" :
                            `No street addresses start with: ${select_object.inputValue}`;}"""
            ),
            width="20em",
        ),
        react_select(
            name="test_dropdown_for_form",
            placeholder="Select foods desired ",
            is_multi=True,
            close_menu_on_select=False,
            options=food_options,
            no_options_message=rx.vars.FunctionStringVar(
                "(select_object) => `No options include: ${select_object.inputValue}`"
            ),
            width="20em",
        ),
        align="center",
        spacing="7",
        height="100vh",
    )


app = rx.App()
app.add_page(index)
