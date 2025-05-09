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

def test_create_empty_file(server):
    # Connect to the log server
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Create an empty regular file in the root directory
    l.creat(0, glfs_client.LFS_REGULAR_FILE, "empty.txt")

    # Make sure we can look it up.
    fnum = l.lookup(0, "empty.txt")
    assert fnum > 0
 
    # release the log object 
    l = None

def test_stat_empty_file(server):
    # Connect to the log server
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Look it the still existing empty file
    fnum = l.lookup(0, "empty.txt")
    assert fnum > 0
 
    # Stat the file and see if its type and size are right
    type, size = l.stat(fnum)
    assert type == glfs_client.LFS_REGULAR_FILE
    assert size == 0

    # release the log object 
    l = None

def test_create_directory(server):
    # Connect to the log server
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Create an empty directory in the root directory
    l.creat(0, glfs_client.LFS_DIRECTORY, "testdir")
    
    # Look up the empty directory
    fnum = l.lookup(0, "testdir")
    assert fnum > 0

    # Check the inodes in the empty directory
    fnum1 = l.lookup(fnum, ".")
    assert fnum1 == fnum

    # Check the inodes in the empty directory
    fnum2 = l.lookup(fnum, "..")
    assert fnum2 == 0

    # Stat the root directory
    type, size = l.stat(fnum)

    # It should be a directory
    assert type == glfs_client.LFS_DIRECTORY

    # Still with one block of entries
    assert size == 4096

def test_create_long_name(server):
    # Connect to the log server
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Create a file with a long name
    try: 
        l.creat(0, glfs_client.LFS_REGULAR_FILE, "thisnameistoolongforcreatetosucceedwithitshouldfail.txt")
    except:
        pass
    else:
        raise AssertionError("LFS_Creat did not fail with a name that was too long.");

def test_create_duplicate_name(server):
    # Connect to the log server
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Try to create a duplicate ".". THIS SHOULD SUCCEED but not actually 
    # make a duplicate
    l.creat(0, glfs_client.LFS_DIRECTORY, ".")

    # Now read the directory contents directly
    bytes = l.read(0, 0)

    # The returned root directory should have only one '.' in it.
    numdot = 0
    for i in range(0,128):
        str = bytes[i*32:i*32+28].split(b'\x00')[0].decode('utf-8')
        if str == ".":
            numdot = numdot + 1
    assert numdot == 1
