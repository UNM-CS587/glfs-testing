import pytest

import glfs_server
import glfs_client

import os

@pytest.fixture(scope="session")
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

def test_single_write(server):
    # Connect to the log server
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Create an empty file in the root directory and look it up
    l.creat(0, glfs_client.LFS_REGULAR_FILE, "testfile.bin")
    fnum = l.lookup(0, "testfile.bin")
    assert fnum > 0

    # Stat the file and check its length
    type, size = l.stat(fnum)
    assert type == glfs_client.LFS_REGULAR_FILE
    assert size == 0

    # Create a 4k byte array to write to the file
    b = bytearray(4096)
    for i in range(4096):
        b[i] = (4096 - i) & 0xff

    # Write it to the file
    l.write(fnum, bytes(b), 0)

    # Stat the file and check its length
    type, size = l.stat(fnum)
    assert type == glfs_client.LFS_REGULAR_FILE
    assert size == 4096

    # Close the log
    l = None

def test_invalid_write(server):
    # Connect to the log server
    l = glfs_client.GLFS_Log("localhost", 12345)

    fnum = l.lookup(0, "testfile.bin")
    assert fnum > 0
    
    # Create a 4k byte array to write to the file
    b = bytearray(4096)
    for i in range(4096):
        b[i] = (4096 - i) & 0xff

    # Write to invalid inode number
    try:
        l.write(514, bytes(b), 0)
    except:
        pass
    else:
        raise AssertionError("Write to invalid inode number did not throw an exception")

    # Write to invalid block number
    try:
        l.write(fnum, b, 15)
    except:
        pass
    else:
        raise AssertionError("Write to invalid inode number did not throw an exception")

def test_single_read(server):
    # Connect to the log server
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Read back the written block
    fnum = l.lookup(0, "testfile.bin")
    assert fnum > 0
    b = l.read(fnum, 0)

    # Check its length and contents
    assert len(b) == 4096
    for i in range(4096):
        assert b[i] == (4096 - i) & 0xff

    # Close the log 
    l = None;

def test_second_write(server):
    # Connect to the log server
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Write a second block to the file
    fnum = l.lookup(0, "testfile.bin")
    assert fnum > 0
    
    # Create a 4k byte array to write to the file
    b = bytearray(4096)

    for i in range(4096):
        b[i] = (4096 - i) & 0xff
    # Write it to the file
    l.write(fnum, bytes(b), 1)

    # Stat the file and check its length
    type, size = l.stat(fnum)
    assert type == glfs_client.LFS_REGULAR_FILE
    assert size == 8192

    # Close the log 
    l = None;
