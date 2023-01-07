"""Capture screenshot of the reMarkable."""

import math
from src.connection import run_ssh_cmd


class Display:
    """reMarkable 2"""

    screenwidth = 1872
    screenheight = 1404

    # frame buffer size
    fb_size = screenwidth * screenheight
    fb_pagesize = 4096

    def __init__(self, ssh_hostname: str) -> None:
        self.ssh_hostname = ssh_hostname

    def get_fb_location(self):
        """Determine framebuffer memory location and create capture command.
           Location changes after restart."""

        # get rM software's process id
        pid = run_ssh_cmd(self.ssh_hostname, "pidof", "xochitl")
        if (pid):
            pid = pid.strip()
        else:
            print(('* problem getting pid of xochitl'))
            return
        #'4210'
        print(f"{pid=}")

        # in-memory framebuffer location is just after the noise from /dev/fb0.

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


 
