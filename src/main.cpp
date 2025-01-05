#include "KeyValueServer.h"

int main() {
    try {
        spdlog::set_level(spdlog::level::info);
        spdlog::info("Starting Key-Value Store Server...");

        kvs::KeyValueServer server(54321); // Use port 54321
        server.run();
    } catch (std::exception &e) {
        spdlog::error("Exception: {}", e.what());
    }

    return 0;
}
