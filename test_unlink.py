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

def test_unlink_empty_file(server):
    # Use LFS_Log to create a new journal
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Create an empty regular file in the root directory
    l.creat(0, glfs_client.LFS_REGULAR_FILE, "empty.txt")

    # Make sure we can look it up
    fnum = l.lookup(0, "empty.txt")
    assert fnum > 0
 
    # Now unlink the file in the root dirctory
    l.unlink(0, "empty.txt")

    # Make sure we can look it up
    try:
        fnum = l.lookup(0, "empty.txt")
    except: 
        pass
    else:
        raise AssertionError("Was able to lookup unlinked file.")

    # release the log object 
    l = None

def test_unlink_empty_directory(server):
    # Use LFS_Log to create a new journal
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Create an empty directory in the root directory
    l.creat(0, glfs_client.LFS_DIRECTORY, "emptydir")

    # Make sure we can look it up
    fnum = l.lookup(0, "emptydir")
    assert fnum > 0
 
    # Now unlink the directory in the root dirctory
    l.unlink(0, "emptydir")

    # Make sure we cannot look it up
    try:
        fnum = l.lookup(0, "emptydir")
    except: 
        pass
    else:
        raise AssertionError("Was able to lookup unlinked directory.")

    # release the log object 
    l = None

def test_unlink_nonempty_directory(server):
    # Use LFS_Log to create a new journal
    l = glfs_client.GLFS_Log("localhost", 12345)

    # Create an empty directory in the root directory
    l.creat(0, glfs_client.LFS_DIRECTORY, "emptydir")

    # Make sure we can look it up
    fnum = l.lookup(0, "emptydir")
    assert fnum > 0
 
    # Now make a file in the empty directory
    l.creat(fnum, glfs_client.LFS_REGULAR_FILE, "empty.txt")

    # Now try to unlink the directory in the root dirctory
    try:
        l.unlink(0, "emptydir")
    except: 
        pass
    else:
        raise AssertionError("Was able to unlink non-empty directory.")

def test_unlink_nonexistent_file(server):
    # Use LFS_Log to create a new journal
    l = glfs_client.GLFS_Log("localhost", 12345)

    l.creat(0, glfs_client.LFS_REGULAR_FILE, "empty.txt")
    l.unlink(0, "empty.txt")
    l.unlink(0, "empty.txt") # This should succeed to ensure idempotency
