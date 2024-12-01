CXX = g++
CXXFLAGS = -std=c++17 -O2 -fopenmp
LDFLAGS = -lm
SRC_DIR = .
LIB_DIR = ./lib
OBJ_DIR = ./obj
BIN_DIR = .

SRCS = $(wildcard $(SRC_DIR)/*.cpp) $(wildcard $(LIB_DIR)/*.cpp)
OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(wildcard $(SRC_DIR)/*.cpp)) \
	$(patsubst $(LIB_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(wildcard $(LIB_DIR)/*.cpp))
TARGET = $(BIN_DIR)/nbody_simulation

all: $(TARGET)

$(TARGET): $(OBJS)
	@mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c -o $@ $<

$(OBJ_DIR)/%.o: $(LIB_DIR)/%.cpp
	@mkdir -p $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)

.PHONY: all clean