#include <iostream>
#include <string>

#include "dictionary.h"
#include "queue.h"
#include "stack.h"

int main() {
	try {
		std::cout << "--- Stack ---\n";
		Stack<int> stack;
		stack.push(10);
		stack.push(20);
		stack.push(30);
		std::cout << "Top: " << stack.top() << "\n";
		stack.pop();
		std::cout << "Top después de pop: " << stack.top() << "\n";
		std::cout << "Tamaño de stack: " << stack.size() << "\n\n";

		std::cout << "--- Queue ---\n";
		Queue<std::string> queue;
		queue.enqueue("Jimena");
		queue.enqueue("Angela");
		queue.enqueue("Mariana");
		std::cout << "Front: " << queue.front() << "\n";
		std::cout << "Back: " << queue.back() << "\n";
		queue.dequeue();
		std::cout << "Front despues de dequeue: " << queue.front() << "\n";
		std::cout << "Tamano queue: " << queue.size() << "\n\n";

		std::cout << "--- Dictionary ---\n";
		Dictionary<std::string, int> dic;
		dic.insert("Jimena", 21);
		dic.insert("Angela", 23);
		dic.upsert("Mariana", 20);

		std::cout << "Contenido en orden de insercion:\n";
		for (const auto& key : dic.keys()) {
			std::cout << key << " => " << dic.at(key) << "\n";
		}

		std::cout << "Edad de Jimena: " << dic.at("Jimena") << "\n";
		std::cout << "Está Mariana? " << (dic.contains("Mariana") ? "si" : "no") << "\n";

		dic.remove("Jimena");
		std::cout << "Tras eliminar el nombre Jimena:\n";
		for (const auto& key : dic.keys()) {
			std::cout << key << " => " << dic.at(key) << "\n";
		}
	} catch (const std::exception& ex) {
		std::cerr << "Error: " << ex.what() << '\n';
		return 1;
	} catch (const char* msg) {
		std::cerr << "Error: " << msg << '\n';
		return 1;
	}

	return 0;
}
