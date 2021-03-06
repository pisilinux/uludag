/*
** Copyright (c) 2006, TUBITAK/UEKAE
**
** This program is free software; you can redistribute it and/or modify it
** under the terms of the GNU General Public License as published by the
** Free Software Foundation; either version 2 of the License, or (at your
** option) any later version. Please read the COPYING file.
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "common.h"

int
list_has(struct list *listptr, const char *data)
{
	struct list *tmp;

	// Our lists arent big, so simple iteration isnt slow
	for (tmp = listptr; tmp; tmp = tmp->next) {
		if (0 == strcmp(tmp->data, data))
			return 1;
	}
	return 0;
}

struct list *
list_add(struct list *listptr, const char *data)
{
	struct list *tmp;

	// We dont want duplicate module names in our lists
	if (list_has(listptr, data))
		return listptr;

	tmp = zalloc(sizeof(struct list));
	tmp->next = listptr;
	tmp->data = strdup(data);
	return tmp;
}

void *
zalloc(size_t size)
{
	void *ptr = 0;
	// For small allocations we shouldn't really fail
	while (ptr == 0) {
		// we usually need zeroed buffers
		ptr = calloc(1, size);
	}
	return ptr;
}

char *
concat(const char *str, const char *append)
{
	char *buf;
	size_t str_len = strlen(str);
	size_t append_len = strlen(append);

	buf = zalloc(str_len + 1 + append_len);
	memcpy(buf, str, str_len);
	memcpy(buf + str_len, append, append_len);
	buf[str_len + append_len] = '\0';
	return buf;
}

char *
my_readlink(const char *path)
{
	char *pathdir;
	char *tmp;
	char buf[512];
	size_t size;

	size = readlink(path, buf, 510);
	if (size == -1) {
		buf[0] = '\0';
		return strdup(buf);
	}
	buf[size] = '\0';
	pathdir = strdup(path);
	tmp = pathdir + strlen(path) - 1;
	while (*tmp != '/') --tmp;
	++tmp;
	*tmp = '\0';
	return concat(pathdir, buf);
}

char *
sys_value(const char *path, const char *value)
{
	static char valbuf[128];
	static char *buf = NULL;
	static size_t buf_size = 0;
	FILE *f;
	size_t size;
	size_t path_len = strlen(path);
	size_t value_len = strlen(value);

	size = path_len + value_len + 2;
	if (buf_size < size) {
		free(buf);
		buf = zalloc(size * 2);
		buf_size = size * 2;
	}
	memcpy(buf, path, path_len);
	buf[path_len] = '/';
	memcpy(buf + path_len + 1, value, value_len);
	buf[path_len + 1 + value_len] = '\0';

	f = fopen(buf, "rb");
	if (!f) return NULL;
	size = fread(valbuf, 1, 126, f);
	if (size < 1) {
		fclose(f);
		return NULL;
	}
	fclose(f);
	valbuf[size] = '\0';
	if (valbuf[size-1] == '\n')
		valbuf[size-1] = '\0';
	return valbuf;
}
