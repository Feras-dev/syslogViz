/**
 * @file syslog_tracer.cpp
 * @author your name (you@domain.com)
 * @brief build with `g++ -o syslog_tracer -c syslog_tracer.cpp`
 * @version 0.1
 * @date 2022-05-23
 *
 * @copyright Copyright (c) 2022
 *
 */

#include <string>
#include <time.h>

#include "syslog_tracer.h"

static double getTimestampInNanoseconds() {
    time_t          s;  // Epoch time in Seconds
    long            ns; // Epoch time in nanoseconds
    double          epoch_timestamp;
    struct timespec ts;
    std::string     str;

    clock_gettime(CLOCK_REALTIME, &ts);

    s  = ts.tv_sec;
    ns = ts.tv_nsec;

    str = std::to_string(s) + "." + std::to_string(ns);

    epoch_timestamp = stod(str);

    return epoch_timestamp;
}

void init_syslog(const char *task_name) {
    openlog(task_name, LOG_CONS | LOG_PID, LOG_USER);
}

void log_frame_timestamp() {
    static int frame_number = 0;
    double     timestamp    = getTimestampInNanoseconds();
    syslog(LOG_INFO, "got frame #%i @ %f", frame_number + 1, timestamp);
    ++frame_number;
}

void log_custom_message(const char *msg) {
    double timestamp = getTimestampInNanoseconds();
    syslog(LOG_INFO, "%s @ %f", msg, timestamp);
}

void close_syslog(void) {
    // close log files
    closelog();
}