gen:
	python3 main.py

build:
	nasm -felf64 out.asm && nasm -felf64 runtime.asm && ld out.o runtime.o -o out

run: gen build
	./out

clean:
	rm runtime.o out out.asm out.o