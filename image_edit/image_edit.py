"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
import asyncio
import reflex as rx
from typing import List
import os
from localStoragePy import localStoragePy
import json

localStorage = localStoragePy('image_edit', 'storage_backend')

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
    imgs : List[str] = localStorage.getItem("images")
    img : list[str]
    option: str = "No selection yet."

    color: List[str] = [
        "red",
        "green",
        "blue",
        "yellow",
        "orange",
        "purple",
    ]

    imgs: List[str] = [
        "another_random.jpg",
    ]
    img: str = ""
    @rx.var
    def file_list(self) -> str:
        """Get the names of each file as a list of strings."""
        self.uploaded_images = os.listdir(rx.get_asset_path())
        return os.listdir(rx.get_asset_path())
    @rx.var
    def get_imgs(self) -> List[str]:
        return self.imgs

        """
        when u handle upload, get everything from local storage and add urs to the list
        reput to local storage
        the state var should update automatically
        """
    
    def update_image_list(self):
        print("old: ", self.imgs)
        print("localStorage", localStorage.getItem("images"))
        storedList = localStorage.getItem("images")
        res = storedList.strip('][').split(', ')
        newItem = res[-1]
        newItem = newItem.replace('"', '')
        self.img = newItem
        self.imgs.append(newItem)

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
            tempList = self.imgs
            try: 
                print("old list", tempList)
                tempList.append(file.filename)
            except: 
                print("must start tempList from scratch")
                tempList = [file.filename]
            print("new templist", print)
            print("dump it allll", json.dumps(tempList)) #templist is updating properly
            localStorage.setItem("images", json.dumps(tempList))
            State.imgs = localStorage.getItem("images")
    
    async def stop_upload(self):
        """Stop the file upload."""
        await asyncio.sleep(1)
        self.is_uploading = False


def colored_box(color: str):
    return rx.box(rx.text(color))

def index() -> rx.Component:
    return rx.center(
        rx.button(
                "Check local storage",
                height="70px",
                width="200px",
                on_click=State.update_image_list,
                padding="1.5em",
                margin_bottom="2em",
            ),
        rx.vstack(
            rx.color_mode_button(rx.color_mode_icon(), float="right"),
            rx.heading("Welcome to Image Theory!", font_size="2em"),
            rx.text("What does your image look like in another color space?"),
            rx.image(src=State.img, width="auto", height="200px"),
    rx.responsive_grid(
                rx.foreach(State.imgs, image_box),
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
