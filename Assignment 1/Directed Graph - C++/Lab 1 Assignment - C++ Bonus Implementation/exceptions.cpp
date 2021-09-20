//
// Created by VladB on 20-Mar-21.
//

#include "exceptions.h"

GraphException::GraphException(std::string msg): exception_msg(std::move(msg)) {}

const char *GraphException::what() {
    return this->exception_msg.c_str();
}
