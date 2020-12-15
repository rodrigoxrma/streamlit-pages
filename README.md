# Streamlit pages

This docker-compose file creates a nginx container that serves multiple streamlit pages which. The application updates its nginx config file when new streamlit pages are added. 

## Building the image

Run the script 'build-image.sh'.

## Deploying containers

Run 'docker-compose up' to create the app container and the nginx container, which will route the apges correctly.

Remember to mount the folder 'pages' on the host the be able to add your own pages to the app!

