/*
** Copyright (c) 2005-2006, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <unistd.h>
#include <time.h>
#include <sys/stat.h>

#include "cfg.h"
#include "log.h"
#include "process.h"

//! Add timestamp to log
static void
timestamp(FILE *f)
{
	static char buf[128];
	time_t t;
	struct tm *bt;

	time(&t);
	bt = gmtime(&t);
	strftime(buf, 127, "%F %T ", bt);
	fputs(buf, f);
}

//! Add comar version info and process id to log
static void
pidstamp(FILE *f)
{
	if (strlen(my_proc.desc) <= 5)
		fprintf(f, "(%s-%d) ", my_proc.desc, getpid());
	else
		fprintf(f, "(%s-%d) ", my_proc.desc + 5, getpid());
}

//! Print log
static void
log_print(const char *fmt, va_list ap, int error)
{
    /*!
    Writes log to file (cfg_log_file_name) or stdout according to cfg_log_* options
    comar version, process id, timestamp and errors(if any) are written
    \sa cfg.c
    */

	if (cfg_log_console) {
		pidstamp(stdout);
		vprintf(fmt, ap);
	}

	if (cfg_log_file) {
		FILE *f;

		f = fopen(cfg_log_file_name, "a");
		if (f) {
			timestamp(f);
			pidstamp(f);
			if (error) fprintf(f, "Error: ");
			vfprintf(f, fmt, ap);
			fclose(f);
		}
	}

	// FIXME: syslog?
}

//! Log starter. Permissions of log file are set here
void
log_start(void)
{
	log_info("COMAR v"VERSION"\n");
	if (cfg_log_file) {
		// make sure log is not readable by ordinary users
		chmod(cfg_log_file_name, S_IRUSR | S_IWUSR);
	}
}

//! Error logging
void
log_error(const char *fmt, ...)
{
    /*!
    Same as log_info, if this function is called instead, writes
    information as an 'error' to log file
    */

	va_list ap;

	va_start(ap, fmt);
	log_print(fmt, ap, 1);
	va_end(ap);
}

//! Print log info
void
log_info(const char *fmt, ...)
{
    /*!
    Prints log info of variable arguments with log_print function.
    Console or file usage depends on cfg_log_* options
    \sa log_print cfg.c
    */

	va_list ap;

	va_start(ap, fmt);
	log_print(fmt, ap, 0);
	va_end(ap);
}

//! Log messages from sub processes for debugging
void
log_debug(int subsys, const char *fmt, ...)
{
	va_list ap;

	if ((cfg_log_flags & subsys) == 0)
		return;

	va_start(ap, fmt);
	log_print(fmt, ap, 0);
	va_end(ap);
}
