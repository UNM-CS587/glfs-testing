import pytest

import glfs_server
import glfs_client

import os

@pytest.fixture(scope="module")
def server():
    try:
        os.remove("glfsserver.log")
    except:
        pass
    print("Starting test server thread")
    _server = glfs_server.create_server("glfsserver.log", 12345)
    _server.start()
    yield _server  # provide the fixture value
    print("Tearing down test server thread")
    _server.stop(None)

def test_root_directory_contents(server):
    # Use GLFS_Log to connect to a server
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Lookup '.' in the root inode and make sure it is inode 0
    assert l.lookup(0, ".") == 0

    # Lookup '..' in the root inode and make sure it is inode 0
    assert l.lookup(0, "..") == 0

    # Release the connection
    l = None

def test_root_directory_stat(server):
    # Use GLFS_Log to connect to a server
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Stat the root directory
    type, size = l.stat(0)

    # It should be a directory
    assert type == glfs_client.LFS_DIRECTORY

    # Still with one block of data
    assert size == 4096

    # Release the connection
    l = None
