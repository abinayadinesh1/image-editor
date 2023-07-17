"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
import asyncio
import reflex as rx
from typing import List
import os
from localStoragePy import localStoragePy
import json   

localStorage = localStoragePy('image_edit', 'storage_backend')
localStorage.setItem('images', [])
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
def cvt_str_to_list(initStr) -> List[str]:
    parsed = initStr.strip('][').split(', ')
    for i in range(0, len(parsed)):
        parsed[i] = parsed[i].replace(" ", "")
    print("parsed", parsed)
    return parsed

class State(rx.State):
    mode: bool = True
    is_uploading: bool
    option: str = "No selection yet."
    img: str = "ex_gfp_fungi.jpg"
    imgsFromLocalStorage = localStorage.getItem("images")
    imgs: List[str]

    # this is a computed var that cant be modified
    @rx.var
    def file_list(self) -> str:
        """Get the names of each file as a list of strings."""
        return os.listdir(rx.get_asset_path())
    @rx.var
    def get_imgs_for_responsive_grid(self) -> List[str]:
        """Get the list of images from local storage.images, which is a string that looks like a list."""
        storedList = cvt_str_to_list(self.imgsFromLocalStorage)
        print(storedList)
        print(type(storedList))
        return storedList
    
    #helpful button to clear local storage
    def clear_local_storage(self):
        # localStorage.clear()
        return
    
    #helpful button to display local storage
    def update_local_storage(self):
        return 
    
    #dummy func
    def dummy(self):
        print(State.imgsFromLocalStorage)
        return 
    
    # @rx.var
    # def get_local_storage_dir(self) -> str:
    #     return "\n\n".join(self.all_image_paths)
    
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
        oldList = self.imgsFromLocalStorage
        print("old list", oldList)
        print("new file", file.filename)
        oldList.append(file.filename)
        # try: 
        #     print("old list", oldList)
        #     oldList.append(file.filename)
        # except: #when oldList starts out as empty
        #     print("must start tempList from scratch")
        #     print("thing to add:", file.filename)
        #     oldList = [file.filename]
        print("dump the whole list u are about to update it with, should have the new one", json.dumps(oldList)) #templist is updating properly
        localStorage.setItem("images", json.dumps(oldList))
        print("imgs from local storage state variable", self.imgsFromLocalStorage) #has this updated?
    
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
                rx.heading("Image Theory!", font_size="5em"),
                rx.image(src="text4.png", width = "auto", height = "auto"),
                padding_top="2%",
            ),
            #upload image and change color space left and right
            rx.text(State.get_imgs_for_responsive_grid),
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
                rx.heading("Image Theory", font_size="5em"),
                rx.image(src="dark_text2.png", width = "auto", height = "auto"),
                padding_top="2%"
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
