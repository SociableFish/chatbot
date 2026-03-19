import PIL.Image
import streamlit as st


LOGO: PIL.Image.Image = PIL.Image.open("./JVA Logo.png")


def main() -> None:
    st.image(LOGO)
    st.title("JVA Math 0.1.0")
    st.text("This app is currently in progress. Come back later.")


if __name__ == "__main__":
    main()
