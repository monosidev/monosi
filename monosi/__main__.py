import sys
from monosi.cli import CliParser

def main():
	parser = CliParser()
	parser.parse(sys.argv)

if __name__ == "__main__":
	main()
