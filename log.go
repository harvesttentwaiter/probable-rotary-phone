package main
import (
    //"fmt"
    "os"
    "runtime"
    "strconv"
    "strings"
    "time"
)
func main() {
    loggy("direct")
    go spawned()
    time.Sleep(time.Second)
}
func spawned() {
    loggy("inGoR")
}

/* import (
    "os"
    "runtime"
    "strconv"
    "strings"
    "time"
) // */
func loggy(msg string) {
    fh, err := os.OpenFile("binky.log", os.O_CREATE | os.O_RDWR | os.O_APPEND, 0666)
    if err == nil {
        now := time.Now()
        tstr := now.Format("20060102-150405.") + strconv.FormatInt(int64(now.Nanosecond()/1000),10)
        fh.WriteString(tstr + " start@"+srcFileNameLine(-1)+" "+srcFileNameLine(2) + ":"+ msg +"\n")
        fh.Close()
    }
}
func srcFileNameLine(skip int) string {
    if skip < 0 {
        var last int
        for i:=0; i<111222; i++ {
            _, _, _, ok := runtime.Caller(i)
            if !ok { break }
            last = i
        }
        skip = last + skip
    }
    _, fn, line, _ := runtime.Caller(skip)
    pathnames := strings.Split(fn, "/")

    return pathnames[len(pathnames)-1] + ":" + strconv.FormatInt(int64(line),10)
}

/* import (
    "fmt"
    "os"
    "runtime"
    "strconv"
    "strings"
    "time"
) // */
func loggy(fname string, msg string) {
    fh, err := os.OpenFile(fname, os.O_CREATE | os.O_RDWR | os.O_APPEND, 0666)
    if err == nil {
        now := time.Now()
        tstr := now.Format("20060102-150405.") + strconv.FormatInt(int64(now.Nanosecond()/1000),10)
        fh.WriteString(tstr + " start@"+srcFileNameLine(-1)+" "+srcFileNameLine(2) + ":"+ msg +"\n")
        fh.Close()
    }
}
func srcFileNameLine(skip int) string {
    if skip < 0 {
        var last int
        for i:=0; i<111222; i++ {
            _, f, l, ok := runtime.Caller(i)
            if !ok { break }
            if false {
                fmt.Print("fs"+f+":"+strconv.FormatInt(int64(l),10)+"\n")
            }
            last = i
        }
        skip = last + skip
    }
    _, fn, line, _ := runtime.Caller(skip)
    pathnames := strings.Split(fn, "/")
    return pathnames[len(pathnames)-1] + ":" + strconv.FormatInt(int64(line),10)
}
