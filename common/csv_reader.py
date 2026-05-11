import csv
import logging
import os


class CSVReader:
    """CSV文件读取器"""

    def __init__(self, file_path: str, encoding="utf-8"):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV文件不存在: {file_path}")

        self.file_path = file_path
        self.encoding = encoding
        with open(self.file_path, "r", encoding=self.encoding) as f:
            reader = csv.DictReader(f)
            self.fields = reader.fieldnames
            self.data = list(reader)
        logging.debug("成功读取文件：%s", file_path)

    def get_all_data(self):
        return self.data

    def get_row(self, index: int):
        if index < 0 or index >= len(self.data):
            raise IndexError(f"行索引超出范围: {index}")
        return self.data[index]

    def get_column(self, column_name: str):
        if column_name not in self.fields:
            raise ValueError(f"列名不存在: {column_name}")
        return [row[column_name] for row in self.data]

    def get_data_by_filter(self, column: str, value: str):
        return [row for row in self.data if row.get(column) == value]

    def row_count(self) -> int:
        return len(self.data)

    def column_count(self) -> int:
        return len(self.fields) if self.fields else 0
