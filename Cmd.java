package org.deadrat22;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Cmd {
    private String pythonExecCmd;
    public Cmd(){
        this("D:\\_root\\programming\\Python\\infare\\flysas\\");
    }
    public Cmd(String pythonCodePath){
        this.pythonExecCmd = "cd \"" + pythonCodePath + "\" && python .\\flysas_crawler.py";
    }
    public void run() throws Exception {
        ProcessBuilder builder = new ProcessBuilder(
                "cmd.exe", "/c", pythonExecCmd);
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
