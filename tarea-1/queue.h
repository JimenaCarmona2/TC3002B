#pragma once

#include <list>

template <typename T>
class Queue {
private:
    std::list<T> data;

public:
    void enqueue(const T& value) {
        data.push_back(value);
    }

    void dequeue() {
        if (empty()) {
            throw "Vacío";
        }
        data.pop_front();
    }

    T& front() {
        if (empty()) {
            throw "Vacío";
        }
        return data.front();
    }

    const T& front() const {
        if (empty()) {
            throw "Vacío";
        }
        return data.front();
    }

    T& back() {
        if (empty()) {
            throw "Vacío";
        }
        return data.back();
    }

    const T& back() const {
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
