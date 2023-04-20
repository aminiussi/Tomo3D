#!/bin/bash -f

export CXX=g++
export CC=gcc
#export CXX="g++ -std=c++11"
#export CC=gcc
#export CXX=icpc
#export CC=icc

cmake_engine="cmake" # YOU NEED CMAKE
prof_options=""
#intel_flags="-fp-model precise" # THIS IS FOR INTEL COMPILERS, JUST REMOVE IT IF YOU  ARE USING GNU COMPILERS

impi_compile_flags=$(mpicc -showme:compile)

impi_link_flags=$(mpicc -showme:link)

flavor="Release"
boost_root="/home/csic/bcf/cjt/boost_1_62_0"
src="/home/csic/bcf/cjt/0CODES/TOMO3D"

cmd="$cmake_engine -DMPI_COMPILE_FLAGS=\"$impi_compile_flags\" -DMPI_LINK_FLAGS=\"$impi_link_flags\" -DMPIEXEC=mpiexec -DMPIEXEC_NUMPROC_FLAG="-np" -DCMAKE_BUILD_TYPE=$flavor -DBOOST_ROOT=$boost_root $src"
#echo $cmd
eval $cmd
