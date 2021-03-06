#!/usr/bin/python3

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum
import sys
from tabulate import tabulate

class Uimage(KaitaiStruct):

    class UimageOs(Enum):
        invalid = 0
        openbsd = 1
        netbsd = 2
        freebsd = 3
        bsd4_4 = 4
        linux = 5
        svr4 = 6
        esix = 7
        solaris = 8
        irix = 9
        sco = 10
        dell = 11
        ncr = 12
        lynxos = 13
        vxworks = 14
        psos = 15
        qnx = 16
        u_boot = 17
        rtems = 18
        artos = 19
        unity = 20
        integrity = 21

    class UimageArch(Enum):
        invalid = 0
        alpha = 1
        arm = 2
        i386 = 3
        ia64 = 4
        mips = 5
        mips64 = 6
        ppc = 7
        s390 = 8
        sh = 9
        sparc = 10
        sparc64 = 11
        m68k = 12
        nios = 13
        microblaze = 14
        nios2 = 15
        blackfin = 16
        avr32 = 17
        st200 = 18

    class UimageComp(Enum):
        none = 0
        gzip = 1
        bzip2 = 2
        lzma = 3
        lzo = 4

    class UimageType(Enum):
        invalid = 0
        standalone = 1
        kernel = 2
        ramdisk = 3
        multi = 4
        firmware = 5
        script = 6
        filesystem = 7
        flatdt = 8
        kwbimage = 9
        imximage = 10
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Uimage.Uheader(self._io, self, self._root)
        self.data = self._io.read_bytes(self.header.len_image)

    class Uheader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x27\x05\x19\x56":
                raise kaitaistruct.ValidationNotEqualError(b"\x27\x05\x19\x56", self.magic, self._io, u"/types/uheader/seq/0")
            self.header_crc = self._io.read_u4be()
            self.timestamp = self._io.read_u4be()
            self.len_image = self._io.read_u4be()
            self.load_address = self._io.read_u4be()
            self.entry_address = self._io.read_u4be()
            self.data_crc = self._io.read_u4be()
            self.os_type = KaitaiStream.resolve_enum(Uimage.UimageOs, self._io.read_u1())
            self.architecture = KaitaiStream.resolve_enum(Uimage.UimageArch, self._io.read_u1())
            self.image_type = KaitaiStream.resolve_enum(Uimage.UimageType, self._io.read_u1())
            self.compression_type = KaitaiStream.resolve_enum(Uimage.UimageComp, self._io.read_u1())
            self.name = (KaitaiStream.bytes_terminate(self._io.read_bytes(32), 0, False)).decode(u"UTF-8")



def main():

    uImage_magic = b"\x27\x05\x19\x56"


    if len(sys.argv) <=1:
        print("Usage: find_uimage.py <file>")
        exit()

    f = open(sys.argv[1], "rb")
    input_file_raw = bytearray(f.read())
    f.close()

    file_index = 0
    header_count = 0
    print("Scanning file...")

    while file_index < len(input_file_raw):
        if input_file_raw[file_index:file_index+4] == uImage_magic:
            bytes_from_index = input_file_raw[file_index:]


            valid_header = False

            try:
                uImage_header = Uimage.Uheader.from_bytes(bytes_from_index)
                valid_header = True
            except:
                pass

            if valid_header:
                header_count += 1
                header_dict_raw = uImage_header.__dict__
                header_dict = {}

                for key, value in header_dict_raw.items():
                    if key[0] != "_":
                        header_dict[key] = value



                print(f"uImage header {header_count}")
                print(f"Address: {file_index} ({hex(file_index)})")
                print(tabulate(header_dict.items()))
                print("")
                print("")


        file_index += 1

if __name__ == "__main__":
    main()



