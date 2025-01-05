cmake_minimum_required(VERSION 3.10)

project(KeyValueServer VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(${CMAKE_SOURCE_DIR})

set(SOURCES
    KeyValueServer.cpp
    main.cpp
)

if (CMAKE_COMPILER_IS_GNUCXX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")
endif()

find_package(Boost REQUIRED COMPONENTS system)
find_package(spdlog REQUIRED)

add_executable(key-value-server ${SOURCES})

target_link_libraries(key-value-server PRIVATE Boost::system spdlog::spdlog)
