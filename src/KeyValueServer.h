#ifndef KEY_VALUE_SERVER_H
#define KEY_VALUE_SERVER_H

#include <boost/asio.hpp>
#include <spdlog/spdlog.h>
#include <unordered_map>
#include <string>
#include <vector>

namespace kvs {

class KeyValueServer {
public:
    KeyValueServer(unsigned short port);
    void run();

private:
    void handle_client(boost::asio::ip::tcp::socket socket);

    boost::asio::io_context io_context_;
    boost::asio::ip::tcp::acceptor acceptor_;
    std::unordered_map<std::string, std::string> store_;
};

} // namespace kvs

#endif // KEY_VALUE_SERVER_H
