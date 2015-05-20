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


#include <gtest/gtest.h>

#include <vad_base/test/test.h>
//#include <vad_base/common/log.h>

using std::cout;
using std::endl;

class shareddistEnvironment : public testing::Environment {
  public:
    virtual void SetUp () {

    }
    virtual void TearDown () {

    }
};

int main (int argc, char **argv) {

  //cout << "Log4cpp conf file: " << DOTEST_LOGGER_CONF << endl;
  //LOG_CONFIG(DOTEST_LOGGER_CONF);

  testing::AddGlobalTestEnvironment (new shareddistEnvironment);
  testing::InitGoogleTest (&argc, argv);

  // Runs all tests using Google Test.
  int ret = RUN_ALL_TESTS();

  //LOG_SHUTDOWN();

  return ret;
}
