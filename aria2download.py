import aria2p

# initialization, these are the default values
def login_aria2():
    aria2 = aria2p.API(
        aria2p.Client(
            host="http://192.168.1.2",
            port=6800,
            secret="zyj"
        )
    )
    return aria2 


def add_download_task(aria2,magnet_uri):
# add downloads
    download = aria2.add_magnet(magnet_uri)
    print('Download task'+magnet_uri+' has been added ')


def print_download_task(aria2):
# list downloads
    downloads = aria2.get_downloads()
    for download in downloads:
        print(download.name, download.download_speed)