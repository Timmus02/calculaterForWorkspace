import workspaceEverX
from laodFile import main
IMode = input("Lesen oder Generieren? <1|2>")

if IMode == "2":
    IsaveMode = input("Daten speichern? <true/false>:")
    if IsaveMode == "" or IsaveMode == "false" or IsaveMode == "0":
        save = False
    if IsaveMode == "true" or IsaveMode == "1":
        save = True
    if save == True:
        IfileName = input("Name der Datei:")
        print(IfileName)
        workspaceEverX.calc(save, IfileName)
    if save == False:
        workspaceEverX.calc(save, "")
if IMode == "1":
    IfileName = IfileName = input("Name der Datei:")
    main(IfileName + ".csv")