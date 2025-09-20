import json
import os

import requests
from langchain_community.document_loaders import JSONLoader
from langchain_core.documents import Document


def _check_file_exist(path: str) -> bool:
    return os.path.exists(path)


def download_file(
    file_hash: str = "b5c001cbcd72b919e9b05e3281cc4e4914fee0748b3d81954772975630233a6e",
) -> str:
    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
    save_path = f"data/virustotal_report_{file_hash}.json"
    if _check_file_exist(path=save_path):
        print("File exists")
        return save_path

    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"

    try:
        response = requests.get(
            url, headers={"x-apikey": VIRUSTOTAL_API_KEY, "Accept": "application/json"}
        )

        if response.status_code == 200:
            report = response.json()

            # 將 JSON 報告存檔
            with open(save_path, "w") as f:
                json.dump(report, f, indent=4)
            print(f"成功下載報告，已儲存為 virustotal_report_{file_hash}.json")

        elif response.status_code == 404:
            print(f"錯誤：找不到此檔案雜湊值 {file_hash} 的報告。")
        else:
            print(f"API 請求失敗，狀態碼：{response.status_code}")
            print(f"回應內容：{response.text}")

    except requests.exceptions.RequestException as e:
        print(f"發生網路錯誤: {e}")
    return save_path


# Define the metadata extraction function.
def metadata_func(record: dict, metadata: dict) -> dict:
    columns = [
        "rule_level",
        "rule_id",
        "rule_source",
        "rule_title",
        "rule_description",
        "rule_author",
        "match_context",
    ]
    for column in columns:
        metadata[column] = record.get(column)
    return metadata


def load_json(
    file_path: str,
    jq_schema: str,
    content_key: str,
) -> list[Document]:
    loader = JSONLoader(
        file_path=file_path,
        jq_schema=jq_schema,
        content_key=content_key,
        metadata_func=metadata_func,
    )

    return loader.load()
