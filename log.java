        java.lang.StackTraceElement ste = Thread.currentThread().getStackTrace()[1];
        System.out.println(ste.getFileName()+":"+ste.getLineNumber()+" "+
                ste.getClassName()+"."+ste.getMethodName()+" 20150211kkang zk");
