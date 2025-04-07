# Load the files from the given paths and return their content
def loadFiles(filesPaths):
    filesContent = []
    for path in filesPaths:
        with open(path, "r", encoding="utf-8") as f:
            filesContent.append(f.read())
    return filesContent