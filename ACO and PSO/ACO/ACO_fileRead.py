import vrplib

class FileRead():
    def __init__(self, path):
        self.path = path


    def instanceTaker(self):
        vrplib.download_instance(self.path, "actual.vrp")
        instance = vrplib.read_instance("actual.vrp")

        return instance


# fileInst = FileRead("A-n60-k9")
# a = fileInst.instanceTaker()
# print(a["capacity"])
