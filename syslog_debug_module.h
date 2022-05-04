#ifndef _SYSLOG_DEBUG_MODULE_H_
#define _SYSLOG_DEBUG_MODULE_H_

#include <syslog.h>


/**
get timestamp accurate to the usec
**/
const char* get_timestamp();

/**
call once
*/
void init_syslog(void);
// {
//   setlogmask(LOG_UPTO (LOG_NOTICE));
//   openlog("exampleprog", LOG_CONS | LOG_PID | LOG_NDELAY, LOG_LOCAL1);
// }

/**
use everytime you want to log someething
**/
void send_syslog(const char * log_msg);
// {
//   syslog(LOG_NOTICE, log_msg);
//   syslog(LOG_INFO, log_msg);
// }


/**
clean up
*/
void close_syslog(void);
// {
//   closelog ();
// }

#endif /* _SYSLOG_DEBUG_MODULE_H_ */
