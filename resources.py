import json
import os


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)

        for e in self.entries:
            e.print_entries(indent=indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': [e.json() for e in self.entries]
        }
        return res

    @classmethod
    def from_json(cls, value):
        new_entry = cls(title=value['title'])
        for item in value.get('entries', []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    def save(self, path):
        content = self.json()
        full_path = os.path.join(path, f'{self.title}.json')
        with open(full_path, 'w', encoding='utf-8') as file:
            json.dump(content, file)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            content = json.load(file)
            e = cls.from_json(content)
        return e


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for item in os.listdir(self.data_path):
            if item.endswith('.json'):
                entry = Entry.load(os.path.join(self.data_path, item))
                self.entries.append(entry)

    def add_entry(self, title: str):
        new_entry = Entry(title)
        self.entries.append(new_entry)

def print_with_indent(val, indent=0):
    ind = "\t" * indent
    print(ind + str(val))



# e = Entry("cat")
# # e_m = EntryManager("./files/smth.py")
# # e_m.add_entry("kitten")
# e1 = Entry("kitten")
# e2 = Entry("an old cat")
# e.add_entry(e1)
# e.add_entry(e2)
# j = e.json()
# print(j)
# print(Entry.from_json(j))


