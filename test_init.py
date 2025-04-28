import glfs_client
import os

def test_server_connection():
    # Use GLFS_Log to connect to a server
    l = GLFS_Log("localhost", 12345)
    # Close that connection 
    l = None;

def test_root_directory_contents():
    # Use GLFS_Log to connect to a server
    l = GLFS_Log("localhost", 12345)

    # Lookup '.' in the root inode and make sure it is inode 0
    assert l.lookup(0, ".") == 0

    # Lookup '..' in the root inode and make sure it is inode 0
    assert l.lookup(0, "..") == 0

    # Release the connection
    l = None

def test_root_directory_stat():
    # Use GLFS_Log to connect to a server
    l = GLFS_Log("localhost", 12345)

    # Stat the root directory
    type, size = l.stat(0)

    # It should be a directory
    assert type == LFS_DIRECTORY

    # Still with one block of data
    assert size == 4096

    # Release the connection
    l = None
