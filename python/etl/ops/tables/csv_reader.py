from ...graph import Op
import csv

class CSVReader(Op):
    def __init__(self, file, delimiter=',', quotechar='|', batch_size=-1):
        super(CSVReader, self).__init__(file=file, delimiter=delimiter, quotechar=quotechar, batch_size=batch_size)

    def open_stream(self):
        if hasattr(self, 'file_stream'):
            self.file_stream.close()
        self.file_stream = open(self.file, 'r')
        self.csv_stream = csv.reader(self.file_stream, delimiter=self.delimiter, quotechar=self.quotechar)

    def execute(self, inputs=None):
        if not hasattr(self, 'csv_stream'):
            self.open_stream()
        batch_size = self.batch_size
        csv = self.csv_stream
        if batch_size == -1:
            batch = [row for row in csv]
            self.open_stream()
            return batch
        batch = []
        for _ in range(batch_size):
            try:
                batch.append(csv.next())
            except StopIteration:
                self.open_stream()
                return batch
        return batch
