from pathlib import Path
from typing import List
import glob
import xml.etree.ElementTree as ET
import random

def random_cut (xml_file: Path, num_deleted_entry: int) -> None:
    # Cut the half number of <entry>
    tree = ET.parse(xml_file)
    benchmark = tree.getroot()

    all_entry = List()
    for entries in benchmark:
        for entry in entries:
            all_entry.append(entry)

    if len(all_entry) <= num_deleted_entry:
        return
    
    entry_to_delete = random.sample(all_entry, num_deleted_entry)

    for entries in benchmark:
        for entry in entries:
            if entry in entry_to_delete:
                entries.remove(entry)
    
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

def count_num_entry (pdf_file: Path) -> int:
    num_entry = 0
    tree = ET.parse(pdf_file)
    benchmark = tree.getroot()
    for entries in benchmark:
        if entries.tag == "entries":
            num_entry += len(entries)
    
    return num_entry

data_root = Path("release_v3.0/en/train")
num_sub_folders = 7

for i in range(1, num_sub_folders + 1):
    data_path = data_root / f"{i}triples"

    if not data_path.exists():
        print(f"Folder {data_path} does not exist, skip")
        continue
    
    xml_files = List(data_path.glob("*.xml"))

    for xml_file in xml_files:
        num_deleted_entry = count_num_entry(xml_file) // 2
        random_cut(xml_file, num_deleted_entry)

print("Data cutting completed")
