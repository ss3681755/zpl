.SILENT:
.PHONY: %.zpl
%.zpl:
	$(MAKE) compile

compile: out
asm: out.asm

run: out
	./out

verify:
	make -B $(PROGRAM)
	./out > test.out
	diff -u test.out $(OUTPUT)

test: tester.py
	python tester.py

clean:
	rm -rf *out* *.o

setup:
	sudo apt update
	sudo apt install -y nasm

out: out.o runtime.o
	ld out.o runtime.o -o out
	chmod +x out

out.o: out.asm
	nasm -felf64 out.asm

runtime.o: runtime.asm
	nasm -felf64 runtime.asm

out.asm: main.py
	python main.py $(PROGRAM)