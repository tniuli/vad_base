// copyright:
//            (C) SINA Inc.
//
//      file: define.h
//      desc:
//    author:
//     email:
//      date:
//
//    change:


#ifndef VAD_BASE_COMMON_DEFINE_H_
#define VAD_BASE_COMMON_DEFINE_H_

#define BEGIN_NAMESPACE_VAD_BASE namespace vad_base {
#define END_NAMESPACE_VAD_BASE  }
#define USING_NAMESPACE_VAD_BASE using namespace vad_base;

#define DELETE_AND_SET_NULL(x)        \
  do {                                \
    if(x){                            \
      delete x;                       \
      x = NULL;                       \
    }                                 \
  } while (0)

// Macro defined to avoid copy constructor and operator =
#define DISALLOW_COPY_AND_ASSIGN(TypeName) \
  TypeName(const TypeName &);              \
  void operator = (const TypeName &);      \
   
#endif  // VAD_BASE_COMMON_DEFINE_H_
