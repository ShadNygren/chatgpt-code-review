import os
import display

# Function to save recommendations to a markdown file, for CLI and Lambda use
def save_markdown(recommendations, file_path="chatgpt_recommendations.md"):
    if recommendations:
        markdown_content = display.generate_markdown(recommendations)
        with open(file_path, "w") as md_file:
            md_file.write(markdown_content)
        print(f"Markdown file saved to {file_path}")
    else:
        print("No recommendations to save.")

# Conditional function to either download or save markdown based on the environment
def handle_markdown(recommendations, web=False):
    if web:
        # This part assumes the presence of Streamlit, use only in a web context
        try:
            import streamlit as st
            if recommendations:
                st.download_button(
                    "Download Markdown",
                    data=display.generate_markdown(recommendations),
                    file_name="chatgpt_recommendations.md",
                    mime="text/markdown",
                )
            else:
                st.download_button(
                    "Download Markdown",
                    data="",
                    file_name="chatgpt_recommendations.md",
                    mime="text/markdown",
                    disabled=True,
                )
        except ImportError:
            print("Streamlit is not installed. Running in a non-web environment.")
    else:
        # For CLI or Lambda, save the markdown to a file
        save_markdown(recommendations)
