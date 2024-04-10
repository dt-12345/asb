from utils import *
import os
import io

class Sarc:
    # Takes a SARC file, directory, or raw bytes as input
    # If using raw bytes, please provide a filename
    def __init__(self, data, filename=''):
        if type(data) != bytes:
            self.filename = os.path.basename(data)
            # Convert directory into Sarc object
            if os.path.isdir(data):
                self.magic = "SARC"
                self.header_size = 0x14
                self.bom = None
                self.version = 0x100
                self.sfat_magic = "SFAT"
                self.sfat_header_size = 0x0c
                self.hash_mult = 101
                self.sfnt_magic = "SFNT"
                self.sfnt_header_size = 0x08
                self.files = []
                for root_dir, dir, files in os.walk(data):
                    for file in files:
                        file_data = {}
                        dir_path = os.path.relpath(root_dir, data)
                        file_path = os.path.join(dir_path, file)
                        file_data["Name"] = file_path
                        with open(os.path.join(data, file_path), 'rb') as f:
                            file_data["Data"] = f.read()
                        self.files.append(file_data)
                return
            elif os.path.isfile(data):
                with open(data, 'rb') as file:
                    data = file.read()
        else:
            self.filename = filename
        self.stream = ReadStream(data)

        # File header
        self.magic = self.stream.read(4).decode('utf-8')
        assert self.magic == "SARC", f"Invalid file magic, expected 'SARC' but got '{self.magic}'"
        self.stream.read(2)
        bom = self.stream.read_u16(">")
        self.bom = "<" if bom == 65534 else ">" # < is LE, > is BE (for struct)
        self.stream.seek(-4, 1)
        self.header_size = self.stream.read_u16(self.bom)
        assert self.header_size == 0x14, f"Invalid header size, expected 0x14 but but got {hex(self.header_size)}"
        self.stream.read(2)
        self.filesize = self.stream.read_u32(self.bom)
        self.data_offset = self.stream.read_u32(self.bom)
        self.version = self.stream.read_u16(self.bom)
        assert self.version == 0x100, f"Invalid version, expected 0x100 but got {hex(self.version)}"
        self.stream.read(2)

        self.stream.seek(self.data_offset)
        self.data = self.stream.read()
        self.stream.seek(self.header_size)

        # SFAT Header
        self.sfat_magic = self.stream.read(4).decode('utf-8')
        assert self.sfat_magic == "SFAT", f"Invalid SFAT magic, expected 'SFAT' but got '{self.sfat_magic}'"
        self.sfat_header_size = self.stream.read_u16(self.bom)
        assert self.sfat_header_size == 0x0c, f"Invalid SFAT header size, expected 0x0c but got {hex(self.sfat_header_size)}"
        self.file_count = self.stream.read_u16(self.bom)
        if self.file_count > 0x3FFF:
            raise ValueError("Archive contains more than the maximum amount of 16,383 files")
        self.hash_mult = self.stream.read_u32(self.bom)
        assert self.hash_mult == 101, f"Hash multiplier in official files must be 101, got {self.hash_mult}"

        nodes = []
        for i in range(self.file_count):
            node = {}
            node["Hash"] = self.stream.read_u32(self.bom)
            name_and_flags = self.stream.read_u32(self.bom)
            node["Collision Flag"] = name_and_flags >> 24
            node["Filename Offset"] = (name_and_flags & 0xffffff) * 4 # Offset is divided by 4
            node["Data Start"] = self.stream.read_u32(self.bom)
            node["Data End"] = self.stream.read_u32(self.bom)
            nodes.append(node)
        
        if self.data_offset < self.stream.tell():
            raise ValueError("Data section must come after SFNT section")
        
        # SFNT Header
        self.sfnt_magic = self.stream.read(4).decode('utf-8')
        assert self.sfnt_magic == "SFNT", f"Invalid SFNT magic, expected 'SFNT' but got '{self.sfnt_magic}'"
        self.sfnt_header_size = self.stream.read_u16(self.bom)
        assert self.sfnt_header_size == 0x08, f"Invalid SFNT header size, expected 0x08 but got {hex(self.sfnt_header_size)}"
        self.stream.read(2)

        self.name_table_offset = self.stream.tell()

        self.files = []
        for node in nodes:
            file = {}
            pos = self.stream.tell()
            self.stream.seek(self.name_table_offset + node["Filename Offset"])
            file["Name"] = get_string(self.stream, 0)
            file["Data"] = self.data[node["Data Start"]:node["Data End"]]
            self.stream.seek(pos)
            self.files.append(file)
        
        self.stream.seek(0, io.SEEK_END)
        self.size = self.stream.tell()

    # Converts SARC into directory
    def ExtractArchive(self, dirname=''):
        dirname = os.path.join(dirname, os.path.splitext(self.filename)[0])
        if not(os.path.exists(dirname)):
            os.makedirs(dirname)
        for file in self.files:
            if not(os.path.exists(os.path.join(dirname, os.path.dirname(file["Name"])))):
                os.makedirs(os.path.join(dirname, os.path.dirname(file["Name"])))
            with open(os.path.join(dirname, file["Name"]), 'wb') as outfile:
                outfile.write(file["Data"])

    # Filename hash algorithm
    def Hash(self, filename):
        hash = 0
        if type(filename) != bytes:
            filename = bytearray(filename.encode('utf-8'))
        if type(filename) != bytearray:
            filename = bytearray(filename)
        for byte in filename:
            hash = hash * self.hash_mult + byte
        return hash & 0xFFFFFFFF
    
    # Creates SARC file
    def CreateArchive(self, filename='', output_dir='', endianness="little"):
        if endianness.lower() == "little":
            bom = "<"
        else:
            bom = ">"
        if filename == '':
            filename = self.filename
        with open(os.path.join(output_dir, filename), 'wb+') as outfile:
            buffer = WriteStream(outfile)

            self.files = sorted(self.files, key=lambda d: self.Hash(d["Name"]))
            name_count = {}
            hashes = []
            for file in self.files:
                hash = self.Hash(file["Name"])
                hashes.append(hash)
                name_count[file["Name"]] = hashes.count(hash)
            name_offsets = {}
            buffer.seek(self.header_size + self.sfat_header_size + 0x10 * len(self.files))
            buffer.write(string(self.sfnt_magic))
            buffer.write(u16(self.sfnt_header_size, bom))
            buffer.write(padding(2))
            name_table_offset = buffer.tell()
            for file in self.files:
                buffer.align_up(4)
                if file["Name"] not in list(name_offsets.keys()):
                    name_offsets[file["Name"]] = int((buffer.tell() - name_table_offset) / 4)
                    buffer.write(string(file["Name"]) + b'\x00')
            buffer.align_up(8)
            data_offset = buffer.tell()
            data_offsets = []
            for i, file in enumerate(self.files):
                start = buffer.tell() - data_offset
                buffer.write(file["Data"])
                end = buffer.tell() - data_offset
                data_offsets.append((start, end))
                if i != len(self.files) - 1:
                    buffer.align_up(8)
            filesize = buffer.tell()
            buffer.seek(0)
            buffer.write(string(self.magic))
            buffer.write(u16(self.header_size, bom))
            if bom == "<":
                buffer.write(b'\xFF\xFE')
            elif bom == ">":
                buffer.write(b'\xFE\xFF')
            buffer.write(u32(filesize, bom))
            buffer.write(u32(data_offset, bom))
            buffer.write(u16(self.version, bom))
            buffer.write(padding(2))
            buffer.write(string(self.sfat_magic))
            buffer.write(u16(self.sfat_header_size, bom))
            buffer.write(u16(len(self.files), bom))
            buffer.write(u32(self.hash_mult, bom))
            for file in self.files:
                buffer.write(u32(self.Hash(file["Name"])))
                buffer.write(u32((name_count[file["Name"]] << 24) + name_offsets[file["Name"]]))
                buffer.write(u32(data_offsets[self.files.index(file)][0]))
                buffer.write(u32(data_offsets[self.files.index(file)][1]))
            buffer.seek(0)
            data = buffer.read()
        return data
    
    # Removes specified file
    def RemoveFile(self, filepath):
        for file in self.files:
            if file["Name"] == filepath:
                self.files.remove(file)
    
    # Adds specified file/folder
    def AddFile(self, filepath):
        if os.path.isdir(filepath):
            for root_dir, dir, files in os.walk(filepath):
                for file in files:
                    file_data = {}
                    file_data["Name"] = os.path.join(root_dir, file)
                    with open(os.path.join(root_dir, file), 'rb') as f:
                        file_data["Data"] = f.read()
                    self.files.append(file_data)
        elif os.path.isfile(filepath):
            with open(filepath, 'rb') as file:
                self.files.append({"Name" : filepath, "Data" : file.read()})
    
    # Replaces specified file with new file
    def ReplaceFile(self, old_file, new_file):
        dir_path = os.path.dirname(old_file)
        self.RemoveFile(old_file)
        self.AddFile(os.path.join(dir_path, new_file))

    # Returns a list of all files in archive
    def ListFiles(self):
        files = []
        for file in self.files:
            files.append(file["Name"])
        return files

    # For RESTBL
    def ListFileInfo(self):
        files = {}
        for file in self.files:
            files[file["Name"]] = len(file["Data"])
        return files
    
    # Removes all files in archive
    def ClearArchive(self):
        self.files = []

    # Renames specified file
    def RenameFile(self, old_filename, new_filename):
        self.files[new_filename] = self.files.pop(old_filename)

    # Returns a string list of all files in archive
    def __repr__(self):
        files = [file["Name"] for file in self.files]
        output = ''
        for i in range(len(files)):
            output += files[i]
            if i < len(files) - 1:
                output += ', '
        return output