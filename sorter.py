from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH, exceptions
import click
import os

@click.command()
@click.option('-s', '--src-dir', type=str, prompt="Source directory", help="Source directory")
@click.option('-d', '--dst-dir', type=str, prompt="Destination directory", help="Destination directory")
def sort(src_dir, dst_dir):
    file = open("log.txt", "w")
    work_dir = os.chdir(src_dir)
    directory = os.listdir(work_dir)
    if os.path.exists(dst_dir):
        for el in directory:
            try:
                audio = MP3File(el)
                audio.set_version(VERSION_1)
                try:
                    title = audio.song
                    if title is None:
                        title = el
                    title = checkOsError(title.strip())
                except AttributeError:
                    print("Нет названия для трека...")
                    title = el
                    title = checkOsError(title.strip())
                try:
                    artist = audio.artist
                    artist = checkOsError(artist.strip())
                    album = audio.album
                    album = checkOsError(album.strip())
                    # Сортировка
                    try:
                        os.mkdir(dst_dir+"/"+artist)
                    except FileExistsError:
                        continue
                    try:
                        os.mkdir(dst_dir+"/"+artist+"/"+album)
                    except FileExistsError or FileNotFoundError:
                        if FileExistsError:
                            continue
                        elif FileNotFoundError:
                            os.mkdir(dst_dir+"/"+artist+"/"+album)
                    try:
                        os.rename(src_dir+"/"+el, src_dir+"/"+str(title)+"-"+str(artist)+"-"+str(album)+".mp3")
                        el = str(title)+"-"+str(artist)+"-"+str(album)+".mp3"
                        os.replace(src_dir+"/"+el, dst_dir+"/"+artist+"/"+album+"/"+el)
                        file.write(src_dir+"/"+el+" ---> "+dst_dir+"/"+artist+"/"+album+"/"+el+"\n")
                        file.write("Done"+"\n")
                    except FileExistsError or PermissionError:
                        print("FileExistError")
                except AttributeError:
                            print("Нет названия альбома или имени исполнителя для трека: "+el)
            except exceptions.MP3OpenFileError:
                file.write(el+"Это не .mp3 файл..."+"\n")
                file.write("Done"+"\n")      
    else:
        file.write("Нет такого каталога: "+dst_dir+"\n")
        file.write("Done"+"\n")
    file.close()

def checkOsError(seq):
    check = ["/", "*", ":", '"', "<", ">", "|", "?"]
    for item in seq:
        for row in range(len(check)):
            if item == check[row]:
                seq = seq.replace(check[row], "")
    print(seq)
    return seq
    
if __name__ == '__main__':
    sort()