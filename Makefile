.SILENT:
.PHONY: %.zpl
%.zpl:
	make PROGRAM=$(@) compile
	$(MAKE) run clean

compile:
	python main.py $(PROGRAM)

run: out.asm runtime.asm
	nasm -felf64 out.asm
	nasm -felf64 runtime.asm
	ld out.o runtime.o -o out
	./out

test:
	python tester.py

clean:
	rm -f *out* *.o

setup:
	sudo apt update
	sudo apt install -y nasm
