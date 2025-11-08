from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMake

class gaz(ConanFile):
    name = "gaz"
    version = "0.0.1"
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'CMakeToolchain', 'CMakeDeps'

    def configure(self):
        self.options["arrow"].parquet = False
        self.options["arrow"].with_boost = False
        self.options["arrow"].with_thrift = False

    def requirements(self):
        self.requires("arrow/19.0.1")
        self.requires("nlohmann_json/3.11.3")
        self.requires("pybind11/3.0.1")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self)
