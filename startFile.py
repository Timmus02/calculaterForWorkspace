import workspaceEverX
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
