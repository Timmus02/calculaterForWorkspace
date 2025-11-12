import workspaceEverX
from laodFile import main
IMode = input("Lesen oder Generieren? <1|2>")

if IMode == "2":
    IfileName = input("Name der Datei:")
    print(IfileName)
    workspaceEverX.calc(IfileName)
if IMode == "1":
    IfileName = IfileName = input("Name der Datei:")
    main(IfileName + ".csv")