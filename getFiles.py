from getLinks import getDropdownNames
import os, json, requests

baseUrl = "https://urnik.fov.um.si/Program/calendars/"
calendarsDir = "calendars"
metaPath = "calendarsMeta.json"

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

def loadMeta():
    if os.path.exists(metaPath):
        with open(metaPath, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def saveMeta(meta):
    tmp = metaPath + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    os.replace(tmp, metaPath)

def writeFile(path, contentIter):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        for chunk in contentIter:
            if chunk:
                f.write(chunk)
    os.replace(tmp, path)

def saveFiles():
    names = list(dict.fromkeys(getDropdownNames()))
    meta = loadMeta()
    os.makedirs(calendarsDir, exist_ok=True)

    for name in names:
        url = f"{baseUrl}{name}.ics"

        prev = meta.get(name, {})
        headers = {}
        if prev.get("etag"):
            headers["If-None-Match"] = prev["etag"]
        if prev.get("lastModified"):
            headers["If-Modified-Since"] = prev["lastModified"]

        resp = session.get(url, headers=headers, stream=True, timeout=20)

        if resp.status_code == 304:
            print(f"[unchanged] {name}")
            continue

        resp.raise_for_status()

        outPath = os.path.join(calendarsDir, f"{name}.ics")
        writeFile(outPath, resp.iter_content(8192))

        meta[name] = {
            "etag": resp.headers.get("ETag"),
            "lastModified": resp.headers.get("Last-Modified"),
        }
        print(f"[updated] {name}")

    saveMeta(meta)

if __name__ == "__main__":
    saveFiles()