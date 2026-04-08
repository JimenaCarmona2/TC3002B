#include <exception>
#include <functional>
#include <iostream>
#include <string>
#include <vector>

#include "dictionary.h"
#include "queue.h"
#include "stack.h"

int g_total = 0;
int g_failed = 0;

void expectTrue(bool condition, const std::string& name) {
    ++g_total;
    if (!condition) {
        ++g_failed;
        std::cout << "[FAIL] " << name << '\n';
    } else {
        std::cout << "[PASS] " << name << '\n';
    }
}

void expectThrowsMessage(const std::function<void()>& fn, const std::string& name) {
    ++g_total;
    try {
        fn();
        ++g_failed;
        std::cout << "[FAIL] " << name << " (no lanzo excepcion)\n";
    } catch (const char*) {
        std::cout << "[PASS] " << name << '\n';
    } catch (...) {
        ++g_failed;
        std::cout << "[FAIL] " << name << " (tipo de excepcion incorrecto)\n";
    }
}

void testStack() {
    Stack<int> s;
    expectTrue(s.empty(), "Stack inicia vacio");

    s.push(1);
    s.push(2);
    s.push(3);
    expectTrue(s.size() == 3, "Stack size tras push");
    expectTrue(s.top() == 3, "Stack top respeta LIFO");

    s.pop();
    expectTrue(s.top() == 2, "Stack pop elimina ultimo");

    s.clear();
    expectTrue(s.empty(), "Stack clear vacia la estructura");

    expectThrowsMessage([&]() { s.pop(); }, "Stack pop en vacio lanza excepcion");
    expectThrowsMessage([&]() { (void)s.top(); }, "Stack top en vacio lanza excepcion");
}

void testQueue() {
    Queue<std::string> q;
    expectTrue(q.empty(), "Queue inicia vacia");

    q.enqueue("A");
    q.enqueue("B");
    q.enqueue("C");

    expectTrue(q.size() == 3, "Queue size tras enqueue");
    expectTrue(q.front() == "A", "Queue front es el primero en entrar");
    expectTrue(q.back() == "C", "Queue back es el ultimo en entrar");

    q.dequeue();
    expectTrue(q.front() == "B", "Queue dequeue elimina el primero");

    q.clear();
    expectTrue(q.empty(), "Queue clear vacia la estructura");

    expectThrowsMessage([&]() { q.dequeue(); }, "Queue dequeue en vacio lanza excepcion");
    expectThrowsMessage([&]() { (void)q.front(); }, "Queue front en vacio lanza excepcion");
    expectThrowsMessage([&]() { (void)q.back(); }, "Queue back en vacio lanza excepcion");
}

void testDictionary() {
    Dictionary<std::string, int> d;
    expectTrue(d.empty(), "Dictionary inicia vacio");

    expectTrue(d.insert("uno", 1), "Dictionary insert nuevo retorna true");
    expectTrue(d.insert("dos", 2), "Dictionary insert segundo retorna true");
    expectTrue(!d.insert("uno", 100), "Dictionary insert duplicado retorna false");

    expectTrue(d.size() == 2, "Dictionary size correcto");
    expectTrue(d.contains("uno"), "Dictionary contains encuentra llave existente");
    expectTrue(!d.contains("tres"), "Dictionary contains false para inexistente");
    expectTrue(d.at("uno") == 1, "Dictionary at obtiene valor correcto");

    d.upsert("uno", 10);
    d.upsert("tres", 3);
    expectTrue(d.at("uno") == 10, "Dictionary upsert actualiza existente");
    expectTrue(d.at("tres") == 3, "Dictionary upsert inserta nuevo");

    std::vector<std::string> expectedKeys = {"uno", "dos", "tres"};
    expectTrue(d.keys() == expectedKeys, "Dictionary mantiene orden de insercion");

    expectTrue(d.remove("dos"), "Dictionary remove existente retorna true");
    expectTrue(!d.remove("nope"), "Dictionary remove inexistente retorna false");
    expectThrowsMessage([&]() { (void)d.at("dos"); }, "Dictionary at en llave eliminada lanza excepcion");

    d.clear();
    expectTrue(d.empty(), "Dictionary clear vacia la estructura");
}

int main() {
    testStack();
    testQueue();
    testDictionary();

    std::cout << "\nResumen: " << (g_total - g_failed) << "/" << g_total << " pruebas pasaron.\n";
    if (g_failed > 0) {
        return 1;
    }
    return 0;
}
