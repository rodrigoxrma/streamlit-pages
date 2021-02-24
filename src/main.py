import subprocess
import os
import time
import signal

class StreamlitPages():

    def __init__(self, CONFIG_DIR, DEFAULT_PAGES_DIR, PAGES_DIR, BASE_PORT):
        self.CONFIG_DIR = CONFIG_DIR
        self.DEFAULT_PAGES_DIR = DEFAULT_PAGES_DIR
        self.PAGES_DIR = PAGES_DIR
        self.BASE_PORT = BASE_PORT
        self.processes = []
        self.pages = {}
        self.LAST_PORT = 0
        self.CURRENT_PAGES = []
        self.page_locations = []

        self.location_base = """location /$PAGE_NAME {
                    rewrite /$PAGE_NAME/(.*) /$1  break;
                    $REWRITE_TRAILING_SLASH
                    proxy_pass http://localhost:$PAGE_PORT;
                    proxy_http_version 1.1;
                    proxy_set_header Upgrade $http_upgrade;
                    proxy_set_header Connection $connection_upgrade;
                }
                
                """

    def kill_child(self):
        for process in self.processes:
            if process.pid is None:
                pass
            else:
                os.kill(process.pid, signal.SIGTERM)


    def start_pages(self, pages, directory):
        locations = []
        BASE_PORT = self.BASE_PORT if self.LAST_PORT == 0 else self.LAST_PORT + 1
        port = 0
        # Loading pages with streamlit
        for i, page in enumerate(pages):
            page_path = os.path.join(directory,page,"main.py")
            port = BASE_PORT+i

            # Create um subprocess for each folder
            self.processes.append(subprocess.Popen(["streamlit","run",
                                            "--server.port", str(port),
                                            "--server.headless","true", 
                                            "--browser.gatherUsageStats", "false",
                                            "--browser.serverAddress", os.getenv('DNS_NAME'),
                                             page_path],))
                                            #  stdout=subprocess.PIPE))

            print("Opened to page {} on port {}".format(page, port))
            print("PID for {}: {}".format(page,self.processes[-1].pid))
            self.pages[page] = (self.processes[-1].pid, port)
            
            # Keeping the main page at the / location
            rewrite = "" if page == "default" else "rewrite /$PAGE_NAME $1/  break;"
            page = page if page != "default" else ""

            locations.append(self.location_base.replace("$PAGE_PORT",str(port)).replace("$REWRITE_TRAILING_SLASH",rewrite).replace("$PAGE_NAME",page))
        
        if port > 0:
            self.LAST_PORT = port

        return locations

    def update_nginx(self, locations):

        os.system("service nginx stop")

        # Writing the nginx file based on these pages
        with open('./config/nginx-base.conf') as reader:
            nginx_config = reader.read()

        os.system("rm /etc/nginx/nginx.conf")

        with open('/etc/nginx/nginx.conf',"w") as writer:
            writer.writelines(nginx_config.replace("$LOCATIONS","".join(locations)).replace("$BASE_PORT",str(self.BASE_PORT)))


        time.sleep(5)

        os.system("service nginx start")
        
    
    def check_new_pages(self,page_locations_base, PAGES_DIR):
        available_pages = os.listdir(PAGES_DIR)

        removed_pages = list(set(self.CURRENT_PAGES)-set(available_pages))
        new_pages = list(set(available_pages)-set(self.CURRENT_PAGES))
        old_pages = list(set(available_pages)-set(new_pages))

        print("New Pages")
        print(new_pages)
        print("Removed Pages")
        print(removed_pages)

        if new_pages != []:
            self.page_locations = page_locations_base
            self.page_locations += self.start_pages(new_pages, PAGES_DIR)

            for page in old_pages:
                self.page_locations.append(self.location_base.replace("$PAGE_PORT",str(self.pages[page][1])).replace("$REWRITE_TRAILING_SLASH","rewrite /$PAGE_NAME $1/  break;").replace("$PAGE_NAME",page))

            self.update_nginx(self.page_locations)
            self.CURRENT_PAGES = available_pages

        return removed_pages


def main():
    CONFIG_DIR = "./config"
    DEFAULT_PAGES_DIR = "./default_pages"
    USER_PAGES_DIR = "./pages"
    BASE_PORT = 8501

    st_pages = StreamlitPages(CONFIG_DIR, DEFAULT_PAGES_DIR, USER_PAGES_DIR, BASE_PORT)

    # System pages
    page_locations_base = st_pages.start_pages(os.listdir(DEFAULT_PAGES_DIR), DEFAULT_PAGES_DIR)

    # User pages
    st_pages.CURRENT_PAGES = os.listdir(USER_PAGES_DIR)
    st_pages.page_locations = page_locations_base + st_pages.start_pages(os.listdir(USER_PAGES_DIR), USER_PAGES_DIR)

    st_pages.update_nginx(st_pages.page_locations)


    # Loop to watch updates on folder
    while True:
        time.sleep(15)
        pages_to_remove = st_pages.check_new_pages(page_locations_base, USER_PAGES_DIR)
        print("----")
        for page in pages_to_remove:
            try:
                os.kill(st_pages.pages[page][0], signal.SIGTERM)
                print("Removed page {}, process {}.".format(page, st_pages.pages[page][0]))
            except:
                print("Cound not remove page {}".format(page))
                pass


if __name__ == "__main__" : main()