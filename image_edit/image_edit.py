"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
import asyncio
import reflex as rx
from typing import List
import os

options: List[str] = [
    "LAB",
    "HSV",
    "Greyscale",
    "LUV",
    "YUV",
    "BayerGBRG",
    "NV21"
]
def image_box(filename: str):
    return rx.center(
        rx.vstack(
            rx.image(src=filename, width="120px", height="auto"), #so far hardcoded, in the for each need to add path for image
            rx.box(rx.text(filename), bg="white"),            
        ),
        padding="2em",
    )
class State(rx.State):
    """The app state."""
    is_uploading: bool
    option: str = "No selection yet."
    uploaded_images: list
    img : list[str]

    @rx.var
    def file_list(self) -> str:
        """Get the names of each file as a list of strings."""
        self.uploaded_images = os.listdir(rx.get_asset_path())
        return os.listdir(rx.get_asset_path())

    async def handle_upload(self, files: List[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_asset_path(file.filename)


            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)
            self.img.append(file.filename)
    
    async def stop_upload(self):
        """Stop the file upload."""
        await asyncio.sleep(1)
        self.is_uploading = False


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.color_mode_button(rx.color_mode_icon(), float="right"),
            rx.heading("Welcome to Image Theory!", font_size="2em"),
            rx.text("What does your image look like in another color space?"),
                rx.responsive_grid(
                    rx.foreach(State.file_list, image_box),
                    columns=[2, 4, 6],
                ),
            rx.upload(
                    rx.button(
                            "Select File(s)",
                            color="purple",
                            bg="white",
                            text_align="center",
                            border="1px dotted black",
                            padding="1.0em",
                            margin_top = "0.5em",
                            margin_bottom = "0.5em"
                        ),
            text_align="center",
            ),
            rx.button(
                "Upload",
                height="70px",
                width="200px",
                on_click=lambda: State.handle_upload(rx.upload_files()),
                padding="1.5em",
                margin_bottom="2em",
            ),
            rx.select(
                options,
                placeholder="Select a color space.",
                value=State.option,
                on_change=State.set_option, #we havent define this, so does it do anything? update_image
            ),
            rx.text(State.option),  
            spacing="1.5em",
            font_size="2em",
            padding_top="10%",
        )
    )


# Add state and page to the app.
app = rx.App(state=State)
app.add_page(index)
app.compile()
