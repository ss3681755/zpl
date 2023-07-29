.SILENT:
.PHONY: sample
sample: gen run
	make clean

gen:
	python main.py

run: out.asm runtime.asm
	nasm -felf64 out.asm && nasm -felf64 runtime.asm && ld out.o runtime.o -o out && ./out

test:
	python tester.py
	make clean

clean:
	rm runtime.o out out.asm out.o test.out

setup:
	sudo apt update
	sudo apt install -y nasm
