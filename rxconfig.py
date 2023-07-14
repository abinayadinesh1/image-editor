import reflex as rx

class ImageeditConfig(rx.Config):
    pass

config = ImageeditConfig(
    app_name="image_edit",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)



# rx.responsive_grid(
# rx.foreach(State.file_list, image_box),
# columns=[2, 4, 6],
# ),