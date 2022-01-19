#include <vector>
#include <fstream>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <random>

namespace fs = std::filesystem;

using std::vector;

#define IMAGE_HEIGHT 100
#define IMAGE_WIDTH 100
#define NPIXELS (IMAGE_HEIGHT * IMAGE_WIDTH)


vector<vector<signed char>> read_in(const std::string source) {
  // read in data from a txt file into a 2d vector
  vector<vector<signed char>> data;
  std::ifstream source_file(source);

  std::string line;
  while(getline(source_file, line))
  {
    vector<signed char> line_entries;
    std::stringstream line_stream(line);

    int value;
    while(line_stream >> value)
    {
      line_entries.push_back(value);
    }
    data.push_back(line_entries);
  }
  return data;
}


void dump(const vector<vector<signed char>> image, const std::string target) {
  // save 2d array to a file
  std::ofstream target_file(target);

  for (const vector<signed char> & row : image) {
    for (const signed char & value : row) {
      target_file << (int) value << " ";
    }
    target_file << std::endl;
  }
}


vector<vector<vector<signed char>>> read_into_memory(const std::string file_directory) {
  // reads in images stored in txt files into a 3d array
  vector<vector<vector<signed char>>> memory;
  for (const auto & entry : fs::directory_iterator(file_directory)) {
    memory.push_back(read_in(entry.path()));
  }
  return memory;
}


vector<vector<int>> calculate_weights() {
  vector<vector<vector<signed char>>> memory = read_into_memory("memory");
  vector<vector<int>> weights;
  for (int pixel_i = 0; pixel_i < NPIXELS; pixel_i++) {
    vector<int> columns;
    for (int pixel_j = 0; pixel_j < NPIXELS; pixel_j++) {
      int weight = 0;
      for (vector<vector<signed char>> & image : memory) {
        weight += image[pixel_i / IMAGE_WIDTH][pixel_i % IMAGE_WIDTH] * image[pixel_j / IMAGE_WIDTH][pixel_j % IMAGE_WIDTH];
      }
      columns.push_back(weight);
    }
    weights.push_back(columns);
  }
  return weights;
}


int main(int argc, char** argv) {
  vector<vector<int>> weights = calculate_weights();
  vector<vector<signed char>> sample = read_in(argv[1]);
  dump(sample, "input_start.dat");

  std::random_device rd;
  std::mt19937 gen(rd());
  std::uniform_int_distribution<> get_random_pixel(0, NPIXELS - 1);

  for (int n = 0; n < 10 * NPIXELS; n++) {
    int pixel_i = get_random_pixel(gen);
    int tmp = 0;
    for (int pixel_j = 0; pixel_j < NPIXELS; pixel_j++)
      tmp += weights[pixel_i][pixel_j] * sample[pixel_j / IMAGE_WIDTH][pixel_j % IMAGE_WIDTH];

    sample[pixel_i / IMAGE_WIDTH][pixel_i % IMAGE_WIDTH] = (tmp < 0 ? -1 : 1);

    if (n % 10000 == 0) {
      std::stringstream filename;
      filename << "progress/step_" << n << ".dat";
      dump(sample, filename.str());
    }
  }
  dump(sample, "input_end.dat");
}
