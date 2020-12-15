import streamlit as st
import os
dns_name = os.getenv('DNS_NAME')
port = os.getenv('PORT')

st.write("""
# Streamlit pages: How to


## Creating a new page

Add a new folder on the 'pages' directory and include a file named 'main.py' which will be your streamlit aplication.
Any other resource can be added inside this folder.

## Accessing my page

You can access your page directly by its url (<http://{}:{}/your-page-name>) or acessing the main menu (<http://{}:{}/>) where it will shown in a grid for selection.


""".format(dns_name,port,dns_name,port))

