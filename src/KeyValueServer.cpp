#include "KeyValueServer.h"
#include <sstream>
#include <boost/asio.hpp>

namespace kvs {

KeyValueServer::KeyValueServer(unsigned short port)
    : io_context_(),
      acceptor_(io_context_, boost::asio::ip::tcp::endpoint(boost::asio::ip::tcp::v6(), port)) {
    spdlog::info("Server initialized on port {}", port);
}

void KeyValueServer::run() {
    spdlog::info("Server listening...");
    while (true) {
        boost::asio::ip::tcp::socket socket(io_context_);
        acceptor_.accept(socket);
        handle_client(std::move(socket));
    }
}

void KeyValueServer::handle_client(boost::asio::ip::tcp::socket socket) {
    spdlog::info("Client connected");

    try {
        boost::asio::streambuf buffer;
        std::string welcome_message = "Key-Value Store Server\nCommands: SET, GET, DELETE, EXIT\n\n";
        boost::asio::write(socket, boost::asio::buffer(welcome_message));

        while (true) {
            boost::asio::read_until(socket, buffer, '\n');
            std::istream streambuf(&buffer);
            std::string command;
            std::getline(streambuf, command);

            std::istringstream iss(command);
            std::vector<std::string> tokens;
            std::string token;

            while (iss >> token) {
                tokens.push_back(token);
            }

            std::string response;
            if (tokens.empty()) {
                continue;
            }

            if (tokens[0] == "SET" && tokens.size() == 3) {
                store_[tokens[1]] = tokens[2];
                response = "OK\n";
                spdlog::info("SET {} {}", tokens[1], tokens[2]);
            } else if (tokens[0] == "GET" && tokens.size() == 2) {
                if (store_.find(tokens[1]) != store_.end()) {
                    response = store_[tokens[1]] + "\n";
                } else {
                    response = "Key not found\n";
                }
            } else if (tokens[0] == "DELETE" && tokens.size() == 2) {
                if (store_.erase(tokens[1]) > 0) {
                    response = "Deleted\n";
                } else {
                    response = "Key not found\n";
                }
            } else if (tokens[0] == "EXIT") {
                response = "Goodbye!\n";
                spdlog::info("Client disconnected.");
                boost::asio::write(socket, boost::asio::buffer(response));
                break;
            } else {
                response = "Invalid command\n";
            }

            boost::asio::write(socket, boost::asio::buffer(response));
        }
    } catch (std::exception &e) {
        spdlog::error("Error handling client: {}", e.what());
    }
}

} // namespace kvs

