#!/bin/env python

import os
import sys
import time 

def generate_file_comments(file_name, author):
    contents = """// copyright:
//    (C) Sina Weibo Inc.
//
//      file: ${file_name}
//      desc:
//    author: ${author}
//     email: ${email_author}@staff.sina.com.cn
//      date: ${date}
//
//    change:

"""
    contents = contents.replace("${file_name}", file_name)
    date = time.strftime("20%y-%m-%d")
    contents = contents.replace("${date}", date)
    contents = contents.replace("${author}", author)
    contents = contents.replace("${email_author}", author.lower())

    return contents


def generate_class_comments():
    pass
def generate_function_comments():
    pass


def generate_file_name_prefix(class_name):
    file_name = ""
    for ch in class_name:
        if ch.isupper():
            if len(file_name) != 0:
                file_name += "_"
        file_name += ch.lower()
            
    return file_name


def write_info_file(file_name, contents):
    out_file = open(file_name, 'a+')
    out_file.write(contents)
    out_file.close()


def generate_file_name(class_name, header_file_suffix, source_file_suffix):
    file_name_prefix = generate_file_name_prefix(class_name) 

    header_file = "%s.%s" % (file_name_prefix, header_file_suffix)
    source_file = "%s.%s" % (file_name_prefix, source_file_suffix)

    return (header_file, source_file) 


def generate_file_macro(project_name, directory_name, file_name):
    if len(directory_name) > 0:
        macro = "%s_%s_%s_" % (project_name, directory_name, file_name)
    else:
        macro = "%s_%s_" % (project_name, file_name)

    macro = macro.replace('.', '_')
    macro = macro.upper()
    
    begin_contents = ""
    begin_contents += "#ifndef " + macro + "\n"
    begin_contents += "#define " + macro + "\n"
    begin_contents += "\n"

    end_contents = ""
    end_contents += "#endif  // " + macro + "\n"

    return (begin_contents, end_contents)


def generate_class_declare(class_name):
    contents = """#include <vad_base/common/define.h>

BEGIN_NAMESPACE_VAD_BASE


class ${class_name} {
  public:
    ${class_name}();
    ~${class_name}();

    int Init();
    int Release();

  private:
    
    // no assign and no copy
    DISALLOW_COPY_AND_ASSIGN(${class_name});
};


END_NAMESPACE_VAD_BASE

"""
    contents = contents.replace('${class_name}', class_name)
    return contents    

 
def generate_class_definition(class_name, directory_name, header_file):
    contents = """#include <vad_base/${directory_name}/${header_file}>

BEGIN_NAMESPACE_VAD_BASE


${class_name}::${class_name}() {

}

${class_name}::~${class_name}() {

}

${class_name}::Init() {

}

${class_name}::Release() {

}


END_NAMESPACE_VAD_BASE"""
    contents = contents.replace('${class_name}', class_name)
    contents = contents.replace('${header_file}', header_file)
    if len(directory_name) == 0:
        contents = contents.replace('${directory_name}/', '')
    else:
        contents = contents.replace('${directory_name}', directory_name)

    return contents
    


if __name__ == '__main__':
    project_name = "vad_base"
    header_file_suffix = "h"
    source_file_suffix = "cc"
    
    directory_name = ""
    class_name = "GoodJob" 
    author = ""

    if len(sys.argv) < 4:
        print "Usage: %s <class_name> <relative_directory_name> <author>" % sys.argv[0]
        sys.exit(1)
    directory_name = sys.argv[2]
    class_name = sys.argv[1]
    author = sys.argv[3]
    print "##########################################################################"
    print "                           class: %s" % class_name
    print "                          author: %s" % author
    print "relative(project HOME) directory: %s" % directory_name 
    print "##########################################################################"



    (header_file, source_file) = generate_file_name(class_name,
                                                    header_file_suffix,
                                                    source_file_suffix)

    if os.path.exists(header_file):
        print "Header file %s already exist!!" % header_file
        sys.exit(1)
    if os.path.exists(source_file):
        print "Source file %s already exist!!" % source_file
        sys.exit(1)

    # write file comments
    print "Create header file: %s." % header_file
    print "Create source file: %s." % source_file

    write_info_file(header_file, generate_file_comments(header_file, author)) 
    write_info_file(source_file, generate_file_comments(source_file, author))
    print "Written file comments into files." 

    #file compile macro
    (begin_macro, end_macro) = generate_file_macro(project_name, directory_name, header_file);
    write_info_file(header_file, begin_macro) 
    print "Written file access macro into files." 


    write_info_file(header_file, generate_class_declare(class_name))
    write_info_file(source_file, generate_class_definition(class_name, directory_name, header_file))
    print "Create class done." 

    print "Written file end access macro into files." 
    write_info_file(header_file, end_macro) 
    print "Done." 



    
