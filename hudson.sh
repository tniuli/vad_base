#!/bin/bash
if [ $# -ne 1 ]; then                                                                  
  echo "Usage: $0 <release/debug>" 
  exit                                                                                                 
fi 
build_mode=$1                                                                     

project_name=vad_base

# Generate code lines
line=`find $project_name -type f|grep -v ".svn" |grep -E ".c[cp]*|.h[hp]*$" \
      |xargs wc -l|grep total|awk '{print $0;}'`
echo "##########################################################################"
echo "Source code: " $line " lines"
echo "##########################################################################"

# Run hudson.pre first
bash ./hudson.pre

# Compile and run unittest, memory check(plz install tcmalloc first)
if [ "$build_mode" = "release" ]; then
  echo "Release building...................................................."

  rm -rf ./build/release64/                                                                       
                                                                                                  
  scons -D ./ mode=release coverage=false heapcheck=tcmalloc                                      
  if [ $? != 0 ] ; then                                                                           
    echo "Compile or unittest fails!"                                                             
    exit 1;                                                                                     
  fi                                                                                              
  echo "Compile and unittest succeed!!!"

  # Package                                                                                        
  echo "Begin packaging... "                                                                           
  cd rpm                                                                                          
  sh package-release.sh
  if [ $? != 0 ] ; then                                                                           
    echo "Packaging fails!"
    exit 1;                                                                                     
  fi                                                                                              
  echo "Packaging succeed!!!"
  cd ..                                                                                           
else
  echo "Debug building...................................................."
  rm -rf ./build/debug64/
  rm -rf ./gtest-output/
  scons -D ./ mode=debug coverage=true heapcheck=tcmalloc
  if [ $? != 0 ] ; then
    echo "Compile or unittest fails!"                                                             
    exit 1;
  fi
  echo "Compile and unittest succeed!!!"

  # Package
  echo "Begin packaging... "                                                                           
  cd rpm
  sh package-debug.sh
  if [ $? != 0 ] ; then
    echo "Packaging fails!"
    exit 1;
  fi
  echo "Packaging succeed!!!"
  cd ..

  rm -rf ./result
  mkdir ./result

  # Generate ut coverage
  for subdir in $(ls $project_name); do
    file_path=$project_name"/"$subdir
    if [ -d $file_path ]; then
      echo "gather "$file_path
      gcov "build/debug64/"${file_path}"/*.cpp" -o "build/debug64/"${file_path}"/"
      lcov -b ./ -d "build/debug64/"${file_path} -c >> ./result/main.info
    fi
  done

  genhtml -o ./result ./result/main.info
fi

# run hudson.post then
bash ./hudson.post
