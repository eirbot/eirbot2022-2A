CXX=g++
CXXFLAGS=-Wall -g 

Table: Table.o Robot.o Sample.o Node.o
	$(CXX) $(CXXFLAGS) $^ -o $@

%.o : %.cpp %.hpp

clean:
	rm Table Table.o Robot.o Sample.o Node.o