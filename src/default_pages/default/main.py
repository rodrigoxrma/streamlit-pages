import streamlit as st
import os
import base64
import json

DNS_NAME = os.getenv('DNS_NAME')
port = os.getenv('PORT')
USER_PAGES_DIR = "./pages"
DEFAULT_PAGES_DIR = "./default_pages"


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url,width):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" width={width} />
        </a>'''
    return html_code

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

            try:
                with open(os.path.join(PAGES_DIR,pages[i+j],"config.json")) as json_file:
                    app_config = json.load(json_file)
                
                if "PREFERRED_DNS" in app_config:
                    DNS_NAME = app_config["PREFERRED_DNS"]
                else:
                    DNS_NAME = os.getenv('DNS_NAME')
            except:
                DNS_NAME = os.getenv('DNS_NAME')

            img_html = get_img_with_href("{}/{}/thumb.png".format(PAGES_DIR,pages[i+j]), 'http://{}:{}/{}'.format(DNS_NAME,port,page_path),"107px")

            cols[j].markdown(img_html, unsafe_allow_html=True)
            cols[j].text(pages[i+j].capitalize())

            print("Page added to list: {}".format(pages[i+j]))

DNS_NAME = os.getenv('DNS_NAME')   

st.markdown("""
# Streamlit pages: Main menu

Here will be presented all of the pages stored in the 'pages' folder.

For more information, visit this page: <http://{}:{}/howto>

""".format(DNS_NAME,port))

num_cols = 4


st.markdown("## System pages available")
load_pages(num_cols,DEFAULT_PAGES_DIR)

st.markdown("## User pages available")
load_pages(num_cols,USER_PAGES_DIR)