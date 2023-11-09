#!/usr/bin/env python3

import atexit
from bs4 import BeautifulSoup
import sys
import os
import fnmatch
from pygments import highlight
from pygments.lexers.c_cpp import *
from pygments.formatters import HtmlFormatter
from string import *
import multiprocessing
from tempfile import mkdtemp
import socket
import struct
import tempfile
import time
import shutil
import json
from contextlib import closing, contextmanager
from pathlib import Path
from subprocess import PIPE, Popen, TimeoutExpired


@contextmanager
def socket_timeout(sock, timeout):
    """Set the timeout on a socket for a context and restore it afterwards"""

    original = sock.gettimeout()
    try:
        sock.settimeout(timeout)

        yield
    finally:
        sock.settimeout(original)


SRC_DIR = Path(__file__).parent
SCRIPT_PATH = str(SRC_DIR / "katex-server.js")

ONE_MILLISECOND = 0.001

TIMEOUT_EXPIRED_TEMPLATE = (
    "Rendering {} is taking too long. Try increasing RENDER_TIMEOUT"
)

STARTUP_TIMEOUT_EXPIRED = (
    "KaTeX server did not came up after {} seconds. "
    "Try increasing STARTUP_TIMEOUT."
)

KATEX_DEFAULT_OPTIONS = {
    # Prefer KaTeX's debug coloring by default. This will not raise exceptions.
    "throwOnError": False
}

KATEX_PATH = None

# How long to wait for the render server to start in seconds
STARTUP_TIMEOUT = 5.0

# Timeout per rendering request in seconds
RENDER_TIMEOUT = 5.0

# nodejs binary to run javascript
NODEJS_BINARY = "node"

files_list = []


def findReplace(directory, find, replace, filePattern):
    global files_list
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            # print filepath
            files_list.append(filepath)


def setup(files, find, replace):
    jobs = []
    for i in range(len(files)):
        p = multiprocessing.Process(target=process, args=(files[i], find, replace))
        jobs.append(p)

        p.start()


def process(filepath, find, replace):
    # print "in process"
    print(filepath)
    with open(filepath, 'rb') as f:
        # print "opened " + filepath
        l = filepath.split('/')
        name = ''
        if(l[len(l) - 2]) == 'build':
            name = l[len(l) - 1]
        s = f.read()
        s = s.replace(find, replace)
        s = s.replace(b"index.html", b"")
        s = s.replace(b"<html>", b"<!DOCTYPE html lang=\"en\">")
        s = s.replace(
            b'<meta', b"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><meta")
        soup = BeautifulSoup(s, "lxml")

        for i in soup.find_all("table", attrs={"summary": "Navigation header"}):
            i.contents[0].contents[0].clear()
            if name == "index.html":
                link = BeautifulSoup("<a href=\"ix01.html\">Index</a>", "lxml")
            elif name == "ix01.html":
                link = BeautifulSoup("", "lxml")
            else:
                link = BeautifulSoup(
                    "<a href=\"../ix01.html\">Index</a>", "lxml")
                i.contents[0].contents[0].insert(0, link)
            if name == "index.html":
                link = BeautifulSoup("", "lxml")
            elif name == "ix01.html":
                link = BeautifulSoup(
                    "<a href=\"index.html\">Table of Contents</a>", "lxml")
            else:
                link = BeautifulSoup(
                    "<a href=\"../\">Table of Contents</a>", "lxml")
                i.contents[1].contents[1].insert(0, link)
        soup = BeautifulSoup(soup.renderContents(), "lxml")
        for j in soup.findAll("table", attrs={"summary": "Navigation footer"}):
            if name == "index.html":
                link = BeautifulSoup("<a href=\"ix01.html\">Index</a>", "lxml")
            elif name == "ix01.html":
                link = BeautifulSoup("", "lxml")
            else:
                link = BeautifulSoup(
                    "<a href=\"../ix01.html\">Index</a>", "lxml")
            j.contents[0].contents[1].insert(0, link)
            if name == "ix01.html":
                link = BeautifulSoup(
                    "<a href=\"index.html\">Table of Contents</a>", "lxml")
            if name == "index.html":
                link = BeautifulSoup("", "lxml")
            elif name == "ix01.html":
                link = BeautifulSoup(
                    "<a href=\"index.html\">Table of Contents</a>", "lxml")
            else:
                link = BeautifulSoup(
                    "<a href=\"../\">Table of Contents</a>", "lxml")
            #j.contents[0].contents[1].insert(0, link)
            j.contents[1].contents[1].clear()
            j.contents[1].contents[1].insert(0, link)
            # Now mathjax removed
        # p = BeautifulSoup("<h3><a href='/'>Site Home</a></h3><p class='alert alert-danger'>Please see <a href=\"http://caniuse.com/#feat=mathml\">http://caniuse.com/#feat=mathml</a> if your browser supports MathML because certain sections of this book rely on MathML. If your browser does not support MathML please install Firefox from <a href=\"https://www.mozilla.org\">Mozilla</a> because AFAIK Firefox supports MathML. On other browsers Mathjax will take its sweet time to render page.</p>", "lxml")
        #soup.body.insert(0, p)
        soup = BeautifulSoup(soup.renderContents(), "lxml")
        for i in soup.find_all("pre", attrs={"class": "CLexer"}):
            code = BeautifulSoup(
                highlight(i.string, CLexer(), HtmlFormatter()), "lxml")

            i.string.replace_with(code)
        for i in soup.find_all("span", attrs={"class": "mathphrase"}):
            math = BeautifulSoup(render_latex(i.string), "lxml")
            i.string.replace_with(math)
        with open(filepath, "w") as f:
            f.write(soup.decode(formatter='html'))


def random_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        # reuse sockets
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # choose port=0 for random port
        sock.bind(("127.0.0.1", 0))

        # return port
        _, p = sock.getsockname()
        return p


class KaTeXError(Exception):
    pass


class KaTeXServer:
    """Manages and communicates with an instance of the render server"""

    # Message length is 32-bit little-endian integer
    LENGTH_STRUCT = struct.Struct("<i")

    # global instance
    KATEX_SERVER = None

    # wait for the server to stop in seconds
    STOP_TIMEOUT = 0.1

    @staticmethod
    def timeout_error(self, timeout):
        message = STARTUP_TIMEOUT_EXPIRED.format(timeout)
        return KaTeXError(message)

    @staticmethod
    def build_command(socket=None, port=None):
        cmd = [NODEJS_BINARY, SCRIPT_PATH]

        if socket is not None:
            cmd.extend(["--socket", str(socket)])

        if port is not None:
            cmd.extend(["--port", str(port)])

        if KATEX_PATH:
            cmd.extend(["--katex", str(KATEX_PATH)])

        return cmd

    @classmethod
    def start_server_process(cls, rundir, timeout):
        socket_path = rundir / "katex.sock"

        # Start the server process
        cmd = cls.build_command(socket=socket_path)
        process = Popen(cmd, stdin=PIPE, stdout=PIPE, cwd=rundir)

        # Wait for the server to come up and create the socket.
        startup_start = time.monotonic()
        while not socket_path.is_socket():
            time.sleep(ONE_MILLISECOND)
            if time.monotonic() - startup_start > timeout:
                raise cls.timeout_error(timeout)

        # Connect to the server through a unix socket
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            remaining = startup_start + timeout - time.monotonic()
            with socket_timeout(sock, remaining):
                sock.connect(str(socket_path))
        except socket.timeout:
            raise cls.timeout_error(timeout)

        return process, sock

    @classmethod
    def start_network_socket(cls, rundir, timeout):
        # Start the server on a random free port and connect to it.
        # The port may become unavailable in between the check and usage.
        host = "127.0.0.1"
        port = random_free_port()

        # Start the server process
        cmd = cls.build_command(port=port)
        process = Popen(cmd, stdin=PIPE, stdout=PIPE, cwd=rundir)

        # Connect to the server through a network socket. We need to wait for
        # the server to create the server socket. A nicer solution which would
        # also side-step the race condition would be for the server to select
        # the random port and then print it to stdout. Then python could
        # select() on stdout to wait for the port/socket path without resorting
        # to polling. However, select() is not supported for pipes on Windows.
        startup_start = time.monotonic()
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remaining = startup_start + timeout - time.monotonic()
                if remaining <= 0.0:
                    raise cls.timeout_error(timeout)

                with socket_timeout(sock, remaining):
                    sock.connect((host, port))

                break
            except ConnectionRefusedError:
                # The server is not up yet. Try again.
                time.sleep(ONE_MILLISECOND)
            except socket.timeout:
                raise cls.timeout_error(timeout)

        return process, sock

    @classmethod
    def start(cls):
        rundir = Path(tempfile.mkdtemp(prefix="pelican_katex"))

        if os.name == "posix":
            process, sock = cls.start_server_process(rundir, STARTUP_TIMEOUT)
        else:
            # Non-unix systems (i.e. Windows) do not support unix
            # domain sockets for IPC, so we use network sockets.
            process, sock = cls.start_network_socket(rundir, STARTUP_TIMEOUT)

        server = KaTeXServer(rundir, process, sock)

        # Clean up after ourselves when skphinx is done. I don't want to register
        # signal handlers here.
        atexit.register(KaTeXServer.terminate, server)

        return server

    @classmethod
    def get(cls):
        """Get the current render server or start one"""
        if cls.KATEX_SERVER is None:
            cls.KATEX_SERVER = KaTeXServer.start()

        return cls.KATEX_SERVER

    def __init__(self, rundir, process, sock):
        self.rundir = rundir
        self.process = process
        self.sock = sock

        # 100KB should be large enough even for big equations
        self.buffer = bytearray(100 * 1024)

    def terminate(self):
        """Terminate the render server and clean up"""
        self.sock.close()
        try:
            self.process.terminate()
            self.process.wait(timeout=self.STOP_TIMEOUT)
        except TimeoutExpired:
            self.process.kill()
        shutil.rmtree(self.rundir)

    def render(self, request, timeout=None):
        # Configure timeouts
        if timeout is not None:
            start_time = time.monotonic()
            self.sock.settimeout(timeout)
        else:
            self.sock.settimeout(None)

        # Send the request
        request_bytes = json.dumps(request).encode("utf-8")
        length = len(request_bytes)
        self.sock.sendall(self.LENGTH_STRUCT.pack(length))
        self.sock.sendall(request_bytes)

        # Read the amount of bytes we are about to receive
        length = self.LENGTH_STRUCT.unpack(
            self.sock.recv(self.LENGTH_STRUCT.size))[0]

        # Ensure that the buffer is large enough
        if len(self.buffer) < length:
            self.buffer = bytearray(length)

        with memoryview(self.buffer) as view:
            # Keep reading from the socket until we have received all bytes
            received = 0
            remaining = length
            while remaining > 0:
                # Abort if we are not done yet but the timeout has expired
                if timeout is not None:
                    elapsed = time.monotonic() - start_time
                    if elapsed >= timeout:
                        raise socket.timeout()
                    else:
                        # Subsequent recvs only get the remaining time instead
                        # of the whole timeout again
                        self.sock.settimeout(timeout - elapsed)

                n_received = self.sock.recv_into(
                    view[received:length], remaining)
                received += n_received
                remaining -= n_received

            # Decode the response
            serialized = view[:length].tobytes().decode("utf-8")
            return json.loads(serialized)


def render_latex(latex, options=None):
    """Ask the KaTeX server to render some LaTeX.

    Parameters
    ----------
    latex : str
        LaTeX to render
    options : optional dict
        KaTeX options such as displayMode
    """

    # Combine caller-defined options with the default options
    katex_options = KATEX_DEFAULT_OPTIONS
    if options is not None:
        katex_options = katex_options.copy()
        katex_options.update(options)

    server = KaTeXServer.get()
    request = {"latex": latex, "katex_options": katex_options}

    try:
        response = server.render(request, RENDER_TIMEOUT)

        if "html" in response:
            return response["html"]
        elif "error" in response:
            raise KaTeXError(response["error"])
        else:
            raise KaTeXError("Unknown response from KaTeX renderer")
    except socket.timeout:
        raise KaTeXError(TIMEOUT_EXPIRED_TEMPLATE.format(latex))


findReplace("build/", "mml:", "", "index.html")
findReplace("build/", "mml:", "", "ix01.html")
# print files_list
setup(files_list, b"mml:", b"")
