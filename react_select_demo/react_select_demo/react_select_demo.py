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

    @rx.event
    def set_focus(self, target_id):
        return rx.call_script(f'document.getElementById("{target_id}").focus();')


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
                dark_mode_toggle(),
                spacing="2",
                direction="column",
            ),
            rx.cond(
                # rx.State.is_hydrated,  # without this rx.memo causes exception
                True,  # The above is always returning false now!
                form_with_selections(),
            ),
            direction="column",
            spacing="6",
            width="100%",
            padding_top="2em",
        ),
    )


@rx.memo
def form_with_selections() -> rx.Component:
    return rx.form.root(
        rx.vstack(
            rx.form.field(
                rx.form.label(
                    "Street Address",
                    size="4",
                    weight="medium",
                ),
                react_select(
                    input_id="selected_street_id",
                    name="selected_street",
                    placeholder="Select street address",
                    options=StreetState.streets,
                    on_input_change=StreetState.on_input_change,
                    no_options_message=rx.vars.FunctionStringVar(
                        """(select_object) => {
                        return select_object.inputValue.length < 2 ?
                            "Provide at least the first 2 digits of your house number \
                             to get a list of street addresses to choose from" :
                            `No street addresses start with: ${select_object.inputValue}`;}"""
                    ),
                    width="20em",
                    on_mount=StreetState.set_focus("selected_street_id"),
                    # on_mount=rx.set_focus(
                    #     "selected_street_id"
                    # ),  # never finds the id although you can see it is there on the element
                ),
                key="selected_street_key",
            ),
            rx.form.field(
                rx.form.label(
                    "Desired foods",
                    size="4",
                    weight="medium",
                ),
                react_select(
                    input_id="desired_foods_id",
                    name="desired_foods",
                    placeholder="Select foods desired ",
                    is_multi=True,
                    close_menu_on_select=False,
                    options=food_options,
                    no_options_message=rx.vars.FunctionStringVar(
                        "(select_object) => `No options include: ${select_object.inputValue}`"
                    ),
                    width="20em",
                ),
                key="desired_foods_key",
            ),
            rx.form.field(
                rx.form.label(
                    "Most desired food",
                    size="4",
                    weight="medium",
                ),
                react_select(
                    input_id="most_desired_food_id",
                    name="most_desired_food",
                    placeholder="Select most desired food ",
                    options=food_options,
                    max_menu_height=100,
                    is_searchable=False,
                    is_clearable=False,
                    width="20em",
                ),
                key="most_desired_food_key",
            ),
            rx.button(
                "Select Desired Foods",
                on_click=StreetState.set_focus("desired_foods_id"),
            ),
            align="center",
            direction="column",
            spacing="7",
        ),
    )


app = rx.App()
app.add_page(index)
