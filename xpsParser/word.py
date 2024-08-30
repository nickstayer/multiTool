import win32com.client


class Word:
    def __init__(self):
        self.word = win32com.client.Dispatch("Word.Application")
        self.word.Visible = False
        self.doc = None

    def open(self, docx_file):
        self.doc = self.word.Documents.Open(docx_file)

    def save_as(self, docx_file):
        self.doc.SaveAs(docx_file)

    def close(self):
        self.doc.Close()

    def quit(self):
        self.word.Quit()

    def insert_text_after_line(self, target_line, new_line):
        for paragraph in self.doc.Paragraphs:
            if paragraph.Range.Text.strip() == target_line:
                paragraph.Range.Text = paragraph.Range.Text.strip() + " " + new_line + "\r\n"
                break

    def insert_text_in_table(self, table_index, row_index, col_index, text):
        try:
            table = self.doc.Tables(table_index)
            if row_index <= table.Rows.Count and col_index <= table.Columns.Count:
                table.Cell(row_index, col_index).Range.Text = text
        except Exception as e:
            print(f"Произошла ошибка: {e}")
