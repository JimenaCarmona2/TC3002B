#pragma once

#include <utility>
#include <vector>

template <typename K, typename V>
class Dictionary {
private:
    using Entry = std::pair<K, V>;

    std::vector<Entry> entries;

    int findIndex(const K& key) const {
        for (std::size_t i = 0; i < entries.size(); ++i) {
            if (entries[i].first == key) {
                return static_cast<int>(i);
            }
        }
        return -1;
    }

public:
    bool insert(const K& key, const V& value) {
        if (findIndex(key) != -1) {
            return false;
        }
        entries.emplace_back(key, value);
        return true;
    }

    void upsert(const K& key, const V& value) {
        int idx = findIndex(key);
        if (idx == -1) {
            entries.emplace_back(key, value);
        } else {
            entries[static_cast<std::size_t>(idx)].second = value;
        }
    }

    bool remove(const K& key) {
        int idx = findIndex(key);
        if (idx == -1) {
            return false;
        }
        entries.erase(entries.begin() + idx);
        return true;
    }

    bool contains(const K& key) const {
        return findIndex(key) != -1;
    }

    V& at(const K& key) {
        int idx = findIndex(key);
        if (idx == -1) {
            throw "Llave no encontrada en Dictionary";
        }
        return entries[static_cast<std::size_t>(idx)].second;
    }

    const V& at(const K& key) const {
        int idx = findIndex(key);
        if (idx == -1) {
            throw "Llave no encontrada en Dictionary";
        }
        return entries[static_cast<std::size_t>(idx)].second;
    }

    std::size_t size() const {
        return entries.size();
    }

    bool empty() const {
        return entries.empty();
    }

    void clear() {
        entries.clear();
    }

    std::vector<K> keys() const {
        std::vector<K> result;
        result.reserve(size());
        for (const auto& entry : entries) {
            result.push_back(entry.first);
        }
        return result;
    }

    std::vector<V> values() const {
        std::vector<V> result;
        result.reserve(size());
        for (const auto& entry : entries) {
            result.push_back(entry.second);
        }
        return result;
    }
};
