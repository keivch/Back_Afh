from .models import Tool

def createCodeTool(name):
    code = ""
    initials = "".join([word[0].upper() for word in name.split()])
    toolNames = Tool.objects.filter(name__iexact=name).count()                          
    if toolNames < 1:
        code = initials + "-1"
    else:
        number = toolNames + 1
        code = f"{initials}-{number}"
    return code

def updateCodeTool(name):
    code = ""
    initials = "".join([word[0].upper() for word in name.split()])
    toolNames = Tool.objects.filter(name__iexact=name).count()
    if toolNames < 1:
        code = initials + "-1"
    else:
        number = toolNames + 1
        code = f"{initials}-{number}"
    return code