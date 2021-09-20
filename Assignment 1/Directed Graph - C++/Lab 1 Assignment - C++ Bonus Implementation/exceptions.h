//
// Created by VladB on 20-Mar-21.
//

#ifndef LAB_1_ASSIGNMENT___C___BONUS_IMPLEMENTATION_EXCEPTIONS_H
#define LAB_1_ASSIGNMENT___C___BONUS_IMPLEMENTATION_EXCEPTIONS_H

#include <exception>
#include <string>

class GraphException: public std::exception {
private:
    const std::string exception_msg;
public:
    explicit GraphException(std::string msg);
    virtual const char* what();
};

#endif //LAB_1_ASSIGNMENT___C___BONUS_IMPLEMENTATION_EXCEPTIONS_H
