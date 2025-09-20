from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(
        default="Give me a short and precise summary about the report.",
        title="Query for Cyber Threat Intelligence",
    )


class QueryResponse(BaseModel):
    query: str = Field(
        default="Give me a short and precise summary about the report.",
        title="Query for Cyber Threat Intelligence",
    )
    answer: str = Field(
        default="The report outlines detections related to potential malicious activities associated with Microsoft Office applications. It identifies file creation in the Windows startup directory, which may indicate persistence. Additionally, it detects the svchost process spawning Office applications, potentially indicating the creation of malicious Office documents with macros. Another detection involves the dropping of a script file by Winword.exe in the startup location, as well as potential DLL sideloading of 'wwlib.dll.'",
        title="Answer for Cyber Threat Intelligence query",
    )
