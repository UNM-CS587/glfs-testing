# We actually implemenet all test in Python, and so use pytest 

# Relies on the pytest-cmake package being installed in python
# typically via `pip install pytest-cmake --user`

# Use the Pytest Cmake package to handle discocering and running python tests
find_package(Pytest)

if (ENABLE_LFS_C_LIBRARY)
    pytest_discover_tests(
        LFSTest
        LIBRARY_PATH_PREPEND
            $<TARGET_FILE_DIR:lfs>
        PYTHON_PATH_PREPEND
            $<TARGET_FILE_DIR:lfs>
        TRIM_FROM_NAME "^test_"
        DEPENDS lfs
    )
else (ENABLE_LFS_C_LIBRARY)
    pytest_discover_tests(
        LFSTest
        PYTHON_PATH_PREPEND
            ${CMAKE_CURRENT_BINARY_DIR}/../src
        TRIM_FROM_NAME "^test_"
    )
endif (ENABLE_LFS_C_LIBRARY)
