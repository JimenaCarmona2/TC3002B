#pragma once

#include <vector>

template <typename T>
class Stack {
private:
    std::vector<T> data;

public:
    void push(const T& value) {
        data.push_back(value);
    }

    void pop() {
        if (empty()) {
            throw "Vacío";
        }
        data.pop_back();
    }

    T& top() {
        if (empty()) {
            throw "Vacío";
        }
        return data.back();
    }

    const T& top() const {
        if (empty()) {
            throw "Vacío";
        }
        return data.back();
    }

    bool empty() const {
        return data.empty();
    }

    std::size_t size() const {
        return data.size();
    }

    void clear() {
        data.clear();
    }
};
