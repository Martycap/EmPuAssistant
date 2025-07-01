from gradio.themes.base import Base

def get_dark_blue_theme():
    return Base(
        primary_hue="blue",
        neutral_hue="slate",
        font=["Inter", "sans-serif"],
    ).set(
        body_background_fill="#0D1B2A",
        body_text_color="#FFFFFF",
        input_background_fill="#1B263B",
        input_border_color="#415A77",
        block_background_fill="#1B263B",
        block_title_text_color="#E0E1DD",
        border_color_primary="#778DA9",
    )
