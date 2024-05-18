##
## EPITECH PROJECT, 2024
## Makefile
## File description:
## make
##

CC = python

NAME = house_burn

SRC_DIR = src

SRC = 	main.py

all: $(NAME)

$(NAME): 
	cp $(SRC_DIR)/$(SRC) .
	mv $(SRC) $(NAME)
	chmod +x $(NAME)

clean:
	rm -rf $(SRC_DIR)/__pycache__
	rm -rf sys

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean
