import tarfile
import os

names = ["Miss Islington",
         "Sir Bors",
         "Tim the Enchanter",
         "Dragon of Angnor",
         "Brother Maynard",
         "Sir Bedevere",
         "Sir Robin",
         "Zoot",
         "Squire Concorde",
         "Green Knight",
         "Trojan Rabbit",
         "Chicken of Bristol",
         "Roger the Shrubber",
         "Bridge Keeper",
         "Sir Gawain",
         "Legendary Black Beast of Argh",
         "A Famous Historian",
         "Sir Lancelot",
         "Lady of the Lake",
         "Rabbit of Caerbannog",
         "Sir Not-Appearing-in-this-Film",
         "Prince Herbert",
         "King Arthur",
         "Inspector End Of Film",
         "Sir Ector",
         "Squire Patsy",
         "Dennis the Peasant",
         "Dinky",
         "Black Knight",
         "Sir Gallahad"]

for name in names:
    # 文件夹
    if not os.path.isfile("./"+name):
        t = tarfile.open("./"+name+"/layer.tar")
        t.extractall("./result/")
