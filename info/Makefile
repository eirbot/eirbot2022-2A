CXX=g++
CXXFLAGS=-Wall -g 

Table: Table.o Robot.o Sample.o Node.o
	$(CXX) $(CXXFLAGS) $^ -o $@

Astar: main.cpp Astar.o Table.o Robot.o Sample.o Node.o 
	$(CXX) $(CXXFLAGS) $^ -o $@

%.o : %.cpp %.hpp

clean:
	rm Astar Table.o Robot.o Sample.o Node.o Astar.o