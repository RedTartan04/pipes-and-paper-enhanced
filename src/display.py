"""Capture screenshot of the reMarkable."""

import math
from PIL import Image
from src.connection import run_ssh_cmd


class Display:
    """reMarkable 2"""

    screenwidth = 1872
    screenheight = 1404

    # frame buffer size
    fb_size = screenwidth * screenheight
    fb_pagesize = 4096

    capture_fb_cmd = ""

    def __init__(self, ssh_hostname: str) -> None:
        self.ssh_hostname = ssh_hostname


    def get_fb_location(self):
        """Determine framebuffer memory location and create capture command.
           Location changes after restart."""

        # Get rM software's process id.
        pid = run_ssh_cmd(self.ssh_hostname, "pidof", "xochitl")
        if (pid):
            pid = pid.strip()
        else:
            print(('* problem getting pid of xochitl'))
            return
        #'4210'
        print(f"{pid=}")

        # In-memory framebuffer location is just after the noise from /dev/fb0.

        #grep -C1 '/dev/fb0' /proc/4210/maps | tail -n1 | sed 's/-.*$//'
        cmd_params = f"-C1 '/dev/fb0' /proc/{pid}/maps | tail -n1 | sed 's/-.*$//'"
        fb_addr = run_ssh_cmd(self.ssh_hostname, "grep", cmd_params)
        if (fb_addr):
            skip_bytes = int(fb_addr.strip(), 16) + 8
        else:
            print(('* problem getting address of RM2 framebuffer'))
            return
        #73a06000
        print(f"{fb_addr=}")
        #1939890184
        print(f"{skip_bytes=}")

        self.fb_offset = skip_bytes % self.fb_pagesize
        #8
        print(f"{self.fb_offset=}")

        fb_start = int(skip_bytes / self.fb_pagesize)
        fb_length = math.ceil(self.fb_size / self.fb_pagesize)

        #473606
        print(f"{fb_start=}")
        #642
        print(f"{fb_length=}")

        #dd if=/proc/4210/mem bs=4096 skip=473606 count=642 2>/dev/null
        self.capture_fb_cmd = f"if=/proc/{pid}/mem bs={self.fb_pagesize} skip={fb_start} count={fb_length} 2>/dev/null"
        print(f"{self.capture_fb_cmd=}")


    def get_fb(self):
        """Get current framebuffer content."""

        # First get framebuffer location, if not already done.
        if (self.capture_fb_cmd == ""):
            self.get_fb_location()

        # Capture framebuffer content.
        raw_fb = run_ssh_cmd(self.ssh_hostname, "dd", self.capture_fb_cmd, raw=True)
        if (raw_fb):
            # Because this captured excess data (it was aligned to the page size) 
            # we need to trim some off.
            raw_fb = raw_fb[self.fb_offset:][:self.fb_size]        
        else:
            print(('* problem getting framebuffer'))
            return
 
        return raw_fb


    def get_image(self, orientation='landscape'):
        """Returns PNG data."""

        raw_fb = self.get_fb()

        print(f"raw_fb len={len(raw_fb)}")

        # rM pixel format: 8 bit grayscale
        # = PLI mode 'L'
        # default decoder = 'raw'
        image= Image.frombytes(mode = 'L', size = (self.screenwidth, self.screenheight), data = raw_fb)
        print("PIL ", image)

        ## TODO rotate for portrait

        ## TODO return PNG for further use
        image.save("rM_snapshot.png")



