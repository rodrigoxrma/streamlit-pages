import streamlit as st
import os
import base64

dns_name = os.getenv('DNS_NAME')
port = os.getenv('PORT')
USER_PAGES_DIR = "./pages"
DEFAULT_PAGES_DIR = "./default_pages"

def load_pages(num_cols, PAGES_DIR):
    pages = os.listdir(PAGES_DIR)
    for i in range(0,len(pages),num_cols):
        if i >= len(pages):
            break

        cols = st.beta_columns(num_cols)
        for j in range(0,num_cols):
            if (i+j) >= len(pages):
                break
            
            if pages[i+j] == "default":
                page_path = ""
            else:
                page_path = pages[i+j]

            with open("{}/{}/thumb.png".format(PAGES_DIR,pages[i+j]), "rb") as img_file:
                b64_image = base64.b64encode(img_file.read()).decode('utf-8')

            cols[j].markdown("[![Image description](data:image/png;base64,{})](http://{}:{}/{}) {}".format(b64_image,dns_name,port,page_path,pages[i+j].capitalize()))

            print("Page added to list: {}".format(pages[i+j]))

                

st.markdown("""
# Streamlit pages: Main menu

Here will be presented all of the pages stored in the 'pages' folder.

For more information, visit this page: <http://{}:{}/howto>

""".format(dns_name,port))

num_cols = 4


st.markdown("## System pages available")
load_pages(num_cols,DEFAULT_PAGES_DIR)

st.markdown("## User pages available")
load_pages(num_cols,USER_PAGES_DIR)