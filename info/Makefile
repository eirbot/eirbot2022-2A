CXX=g++
CXXFLAGS=-Wall -g -O3

Astar: main.cpp Astar.o Table.o Robot.o Sample.o Node.o Movement.o
	$(CXX) $(CXXFLAGS) $^ -o $@

%.o : %.cpp %.hpp

clean:
	rm Astar *.o map.ppm