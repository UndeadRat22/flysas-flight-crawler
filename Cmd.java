package org.deadrat22;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Cmd {
    public Cmd(){

    }
    public void run() throws Exception {
        ProcessBuilder builder = new ProcessBuilder(
                "cmd.exe", "/c", "cd \"D:\\_root\\programming\\Python\\infare\\flysas\\\" && python .\\flysas_crawler.py");
        builder.redirectErrorStream(true);
        Process p = builder.start();
        BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));
        String line;
        while (true) {
            line = r.readLine();
            if (line == null) { break; }
            System.out.println(line);
        }
    }
}
