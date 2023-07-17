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
# must fix style for buttons
light_style = {
    "background_image": "light_mode.png", 
    "font_family": "Comic Sans MS",
    "color": "black",
}
dark_style = {
    "background_image": "dark_mode.png", 
    "font_family": "Comic Sans MS",
    "color": "white",
}

class State(rx.State):
    mode: bool = True
    is_uploading: bool
    option: str = "No selection yet."
    img: str = "ex_gfp_fungi.jpg"
    imgs: List[str] = [
        "another_random.jpg",
    ]
    all_image_paths : str

    # this is a computed var that cant be modified
    @rx.var
    def file_list(self) -> str:
        """Get the names of each file as a list of strings."""
        return os.listdir(rx.get_asset_path())
    
    #helpful button to clear local storage
    def clear_local_storage(self):
        # localStorage.clear()
        return
    
    #helpful button to display local storage
    def update_local_storage(self):
        return 
    
    #dummy func
    def dummy(self):
        return 
    
    @rx.var
    def get_local_storage_dir(self) -> str:
        return "\n\n".join(self.all_image_paths)
    
    # @rx.var
    # def get_local_storage_dir_list(self) -> List[str]:
    #     return

    async def handle_upload(self, files: List[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_asset_path(file.filename)

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)
    
    def update_image_list(self):
        storedList = localStorage.getItem("images")
    def toggle_mode(self):
        if self.mode == True:
            self.mode = False
        else:
            self.mode = True

    async def stop_upload(self):
        """Stop the file upload."""
        await asyncio.sleep(1)
        self.is_uploading = False
def index():
    return rx.cond(
        State.mode,
        rx.center(
        rx.vstack(
            #main header (3)
            rx.vstack(                
                rx.button("dark", 
                            background_image="moon.png",
                            on_click=State.toggle_mode()),
                rx.heading("Welcome to Image Theory!", font_size="5em"),
                rx.text("What does your image look like in another color space?",
                        background_image="linear-gradient(271.3deg, #4500FF 15%, #FF0000 30%, #FFD100 30%, #00FFEE 70%, #FF00FB 15%)",
                        background_clip="text",
                        font_size="3em"
                ),
                padding_top="5%"
            ),
            #upload image and change color space left and right
            rx.hstack(
                #upload image left stack
                rx.vstack(
                    rx.image(src=State.img, width="auto", height="300px"),
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
                    padding_right = "30%"
                ),
                
                #change diff color space right stack
                rx.vstack(
                    rx.select(
                        options,
                        placeholder="Select a color space.",
                        value=State.option,
                        on_change=State.set_option, #we havent define this, so does it do anything? update_image
                        width = "200px", 
                        height = "auto",
                    
                    ),
                        rx.text(State.option),  
                        spacing="1.5em",
                        font_size="1.5em",
                        padding_bottom="10%",
                ),
            ),

            #see grid view of all images
            rx.center(
                rx.vstack(            
                    rx.text("All uploaded images", font_size="3em"),
                    # rx.responsive_grid(
                    #     rx.foreach(State.imgs, image_box),
                    #     columns=[2, 4, 6],
                    # ),
                ),
                padding_top = "5%"
            ),
            #helpful buttons
            rx.hstack(
                rx.vstack(
                    rx.text("Something not working? Try clearing your local storage"),
                                rx.button(
                            "Clear local storage",
                            height="70px",
                            width="200px",
                            on_click=State.dummy,
                            padding="1.5em",
                            margin_bottom="2em",
                        ),
                        border="1px dotted black",
                        padding="1.5em",
                ), 
                rx.vstack(
                    rx.text("Going back to an old pic? Find the full list here then copy/paste the filename to the editor."),
                    rx.button(
                        "Check local storage",
                        height="70px",
                        width="200px",
                        on_click=State.dummy,
                        padding="1.5em",
                        margin_bottom="2em",
                    ),
                    border="1px dotted black",
                    padding="1.5em",
                ),
                padding_bottom="0.5em"
            ),
        ),
        style=light_style
    ),
        rx.center(
        rx.vstack(
            #main header (3)
            rx.vstack(                
                rx.button("light", 
                            background_image="sun.png",
                            on_click=State.toggle_mode()),
                rx.heading("Welcome to Image Theory!", font_size="5em"),
                rx.text("What does your image look like in another color space?",
                        background_image="linear-gradient(271.3deg, #4500FF 15%, #FF0000 30%, #FFD100 30%, #00FFEE 70%, #FF00FB 15%)",
                        background_clip="text",
                        font_size="3em"
                ),
                padding_top="5%"
            ),
            #upload image and change color space left and right
            rx.hstack(
                #upload image left stack
                rx.vstack(
                    rx.image(src=State.img, width="auto", height="300px"),
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
                    padding_right = "30%"
                ),
                
                #change diff color space right stack
                rx.vstack(
                    rx.select(
                        options,
                        placeholder="Select a color space.",
                        value=State.option,
                        on_change=State.set_option, #we havent define this, so does it do anything? update_image
                        width = "200px", 
                        height = "auto",
                    
                    ),
                        rx.text(State.option),  
                        spacing="1.5em",
                        font_size="1.5em",
                        padding_bottom="10%",
                ),
            ),

            #see grid view of all images
            rx.center(
                rx.vstack(            
                    rx.text("All uploaded images", font_size="3em"),
                    # rx.responsive_grid(
                    #     rx.foreach(State.imgs, image_box),
                    #     columns=[2, 4, 6],
                    # ),
                ),
                padding_top = "5%"
            ),
            #helpful buttons
            rx.hstack(
                rx.vstack(
                    rx.text("Something not working? Try clearing your local storage"),
                                rx.button(
                            "Clear local storage",
                            height="70px",
                            width="200px",
                            on_click=State.dummy,
                            padding="1.5em",
                            margin_bottom="2em",
                        ),
                        border="1px dotted black",
                        padding="1.5em",
                ), 
                rx.vstack(
                    rx.text("Going back to an old pic? Find the full list here then copy/paste the filename to the editor."),
                    rx.button(
                        "Check local storage",
                        height="70px",
                        width="200px",
                        on_click=State.dummy,
                        padding="1.5em",
                        margin_bottom="2em",
                    ),
                    border="1px dotted black",
                    padding="1.5em",
                ),
                padding_bottom="0.5em"
            ),
        ),
        style=dark_style
    )
            )

app = rx.App(state=State)
app.add_page(index)
app.compile()
