#ifndef _SYSLOG_TRACER_H_
#define _SYSLOG_TRACER_H_

#include <syslog.h>

/**
 * @brief returns current timestamp in nanoseconds.
 * 
 * @return double current time stamp in nanoseconds in epoch format (e.g., 1645396588.006066).
 */
static double get_timestamp();

/**
call once before any logging takes place
*/
void init_syslog(const char *task_name);


/**
use overtime you want to log a time stamp of a frame captured
**/
void log_frame_timestamp();

/**
use to log a custom message with time stamp
**/
void log_custom_message(const char* msg);

/**
clean up
*/
void close_syslog(void);

#endif /* _SYSLOG_TRACER_H_ */
