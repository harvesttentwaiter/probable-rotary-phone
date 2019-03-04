#include<time.h>
#include<stdarg.h>
#include<stdio.h>
#include<sys/time.h>
#define log(...) _log(__PRETTY_FUNCTION__, __LINE__, __VA_ARGS__)
static char *log_prefix = "[CLog]";
static FILE *log_file = NULL;
/*
    log_file = fopen("/tmp/debug.log","a");
    log("log mess %s", __FUNCTION__);
    fclose(log_file);
    log_file = stderr;
*/
static void _log(const char *funcname, int line, char *msg, ...) {
    va_list argptr;
    va_start(argptr, msg);

    if (log_file == NULL) {
        log_file = stderr;
    }

    struct timeval now;
    gettimeofday(&now, NULL);

    char buf[16];
    time_t t = now.tv_sec;
    struct tm *tmp;
    tmp = localtime(&t);
    strftime(buf, sizeof(buf), "%Y%m%d-%H%M%S", tmp);

    fprintf(log_file,"%s %li.%06i %i %s %i %s ", buf, (long)now.tv_sec, (int)now.tv_usec, (int)getpid(), funcname, line, log_prefix);
    vfprintf(log_file, msg, argptr);
    fprintf(log_file,"\n");
    va_end(argptr);
}
void hexDump (void *addr, int len) {
    int i;
    unsigned char buff[17];
    unsigned char *pc = (unsigned char*)addr;
    for (i = 0; i < len; i++) {
        if ((i % 16) == 0) {
            if (i != 0)
                printf ("  %s\n", buff);
            printf ("  %04x ", i);
        }
        printf (" %02x", pc[i]);
        if ((pc[i] < 0x20) || (pc[i] > 0x7e))
            buff[i % 16] = '.';
        else
            buff[i % 16] = pc[i];
        buff[(i % 16) + 1] = '\0';
    }
    while ((i % 16) != 0) {
        printf ("   ");
        i++;
    }
    printf ("  %s\n", buff);
}

#include<execinfo.h>
static void printHexStack()
{
    void *fns[32];
    FILE *fptr = log_file;
    long i, depth;
    depth = backtrace(fns, sizeof(fns));
    for (i = 0; i < depth; i++) {
        fprintf(fptr, "%p ", fns[i]);
    }
    fprintf(fptr, "\n");
}
